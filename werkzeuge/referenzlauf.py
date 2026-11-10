"""Automated reference run of the KI-Projekt-Bibel (Part 3).

The script replaces the Decider thread: it starts every role with `claude -p`,
asks a small, stateless Claude call for each answer of the "client" (rules from
Part 3 §5), measures exactly, enforces the cost brake and writes the report.

Run (normally from .github/workflows/referenzlauf.yml):
    python werkzeuge/referenzlauf.py --owner <github-account> [--version 1.6]
Test without GitHub and without tokens:
    python werkzeuge/referenzlauf.py --owner test --dry-run   (with CLAUDE_BIN=<stub>)
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "quelle"
META = json.loads((SRC / "version.json").read_text(encoding="utf-8"))

CALL_TIMEOUT_S = 45 * 60          # Part 3 §6: safety net per session call
LIMIT_SLEEP_S = 15 * 60           # wait between retries when the usage limit is reached
MAX_ROUNDS_PER_PHASE = 15
MAX_PHASES = 10
STUCK_REPEATS = 3                 # identical client answers in a row = the role is stuck
HELPER_MODEL = "sonnet"
MESSAUFBAU = "M1"  # frozen measurement setup, Part 3 §2; change only with a new baseline           # Decider answers, manual tester and report text (not part of the measurement)
ENV_DROP = ["CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_REMOTE_SESSION_ID", "CLAUDE_CODE_CHILD_SESSION"]


# --------------------------------------------------------------------------- helpers

def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def say(text: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {text}", flush=True)


def code_blocks(text: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"```[a-z]*\n(.*?)\n```", text, flags=re.S)]


def section(text: str, number: int) -> str:
    """Body of '## N.' in a markdown file, ignoring headings inside code fences."""
    out, current, fence = [], None, False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"## (\d+)\. ", line)
        if m:
            current = int(m.group(1))
            continue
        if current == number:
            out.append(line)
    return "\n".join(out).strip()


def first_json(text: str) -> dict:
    """The last top-level JSON object in a model answer."""
    candidates = re.findall(r"\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}", text, flags=re.S)
    for raw in reversed(candidates):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            continue
    raise ValueError("no JSON object in answer")


def run(cmd: list[str], cwd: Path, check: bool = True) -> str:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and result.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed: {result.stderr.strip()[-500:]}")
    return result.stdout


# --------------------------------------------------------------------------- run state

class Lauf:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.version = args.version
        self.vdash = self.version.replace(".", "-")
        self.run_id = args.run_id or dt.datetime.now().strftime("%Y%m%d-%H%M")
        self.repo = f"kassenbuch-{self.vdash}-{self.run_id}"
        self.work = Path(args.workdir).resolve()
        self.work.mkdir(parents=True, exist_ok=True)
        self.project = self.work / self.repo
        self.out = ROOT / "messungen" / "protokolle" / self.version / self.run_id
        self.answers_dir = self.out / "antworten"
        self.log_path = self.out / "lauf.jsonl"
        self.claude = shutil.which(os.environ.get("CLAUDE_BIN", "claude")) or os.environ.get("CLAUDE_BIN", "claude")
        self.env = {k: v for k, v in os.environ.items() if k not in ENV_DROP}
        sys.path.insert(0, str(ROOT / "werkzeuge"))
        import teil3 as teil3_module
        teil3 = teil3_module.write(self.work / "teil3" / "teil3.md")
        self.teil3_path = teil3
        self.teil3 = teil3.read_text(encoding="utf-8")
        self.rules = section(self.teil3, 5)
        self.call_no = 0
        self.sessions: dict[str, dict] = {}     # project sessions: latest cumulative values
        self.helper_cost = 0.0
        self.turns = 0
        self.denials: dict[str, set] = {}
        self.limit_wait_s = 0.0
        self.started = time.time()
        self.stopped_reason = ""
        self.ae1_sent = False
        self.manual: dict | None = None
        self.questions = 0
        self.unforeseen = 0
        self.decisions: list[dict] = []
        self.budget_resumed: set[str] = set()

    # ------------------------------------------------------------------ claude calls

    def claude_call(self, prompt: str, cwd: Path, *, session: str | None = None, resume: bool = False,
                    helper: bool = False, extra: list[str] | None = None, budget: float | None = None) -> dict:
        def command() -> list[str]:
            cmd = [self.claude, "-p", "--output-format", "json"]
            if helper:
                cmd += ["--model", HELPER_MODEL, "--no-session-persistence"]
            elif not any(a == "--permission-mode" for a in extra or []):
                cmd += ["--permission-mode", self.args.permission_mode]
            if session:
                cmd += ["--resume", session] if resume else ["--session-id", session]
            if budget:
                cmd += ["--max-budget-usd", str(budget)]
            return cmd + (extra or [])

        waited = 0.0
        while True:
            cmd = command()
            t0 = time.time()
            try:
                proc = subprocess.run(cmd, input=prompt, cwd=cwd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace", env=self.env, timeout=CALL_TIMEOUT_S)
                raw = proc.stdout.strip()
                data = json.loads(raw[raw.find("{"):]) if "{" in raw else {"is_error": True, "result": proc.stderr[-2000:]}
            except subprocess.TimeoutExpired:
                data = {"is_error": True, "result": "timeout after 45 minutes", "subtype": "timeout"}
            except json.JSONDecodeError:
                data = {"is_error": True, "result": (proc.stdout + proc.stderr)[-2000:], "subtype": "no_json"}
            data["_wall_s"] = round(time.time() - t0, 1)
            text = str(data.get("result", "")).lower()
            if data.get("is_error") and "limit" in text and ("reset" in text or "usage" in text):
                if waited + LIMIT_SLEEP_S > self.args.max_limit_wait_min * 60:
                    data["_limit_abort"] = True
                    return data
                say(f"Nutzungslimit erreicht, warte {LIMIT_SLEEP_S // 60} Minuten.")
                time.sleep(LIMIT_SLEEP_S)
                waited += LIMIT_SLEEP_S
                self.limit_wait_s += LIMIT_SLEEP_S
                if session and not resume and data.get("session_id") == session:
                    resume = True   # the session exists now; continue it instead of creating it again
                continue
            return data

    def role(self, role: str, phase: str, prompt: str, session: str, resume: bool) -> str:
        """One call of a project role. Returns the role's answer text."""
        data = self.claude_call(prompt, self.project, session=session, resume=resume, budget=self.args.budget_call)
        result = str(data.get("result", ""))
        if data.get("is_error") and "budget" in (result + str(data.get("subtype", ""))).lower() \
                and session not in self.budget_resumed:
            self.budget_resumed.add(session)
            self.log(role, phase, session, prompt, data)
            say(f"{role}: Kostenbremse pro Aufruf erreicht, setze einmal fort.")
            return self.role(role, phase, "Bitte mach weiter.", session, True)
        self.log(role, phase, session, prompt, data)
        if data.get("_limit_abort"):
            self.stopped_reason = "Nutzungslimit, maximale Wartezeit überschritten"
        return result

    def log(self, role: str, phase: str, session: str, sent: str, data: dict) -> None:
        self.call_no += 1
        (self.answers_dir / f"{self.call_no:03d}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        if not data.get("is_error") or "total_cost_usd" in data:
            # total_cost_usd, modelUsage and permission_denials accumulate over a resumed session: keep the latest
            self.sessions[session] = {"role": role, "phase": phase,
                                      "cost": float(data.get("total_cost_usd") or self.sessions.get(session, {}).get("cost", 0)),
                                      "usage": data.get("modelUsage") or self.sessions.get(session, {}).get("usage", {})}
        self.turns += int(data.get("num_turns") or 0)
        for d in data.get("permission_denials") or []:
            self.denials.setdefault(session, set()).add(json.dumps(d, sort_keys=True)[:300])
        entry = {"nr": self.call_no, "zeit": now(), "rolle": role, "phase": phase, "session_id": session,
                 "gesendet": sent[:500], "antwort": str(data.get("result", ""))[:1000],
                 "num_turns": data.get("num_turns"), "total_cost_usd": data.get("total_cost_usd"),
                 "modelUsage": data.get("modelUsage"), "permission_denials": data.get("permission_denials"),
                 "is_error": data.get("is_error"), "subtype": data.get("subtype"), "wall_s": data.get("_wall_s")}
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        say(f"#{self.call_no} {role} · {phase} · {self.project_cost():.2f} USD bisher")

    def project_cost(self) -> float:
        return sum(s["cost"] for s in self.sessions.values())

    def over_budget(self) -> bool:
        if self.project_cost() > self.args.budget_total and not self.stopped_reason:
            self.stopped_reason = f"Kostenbremse: Projekt-Sitzungen über {self.args.budget_total} USD"
        return bool(self.stopped_reason)

    def helper(self, prompt: str, cwd: Path, name: str, tools: str = "", budget: float = 2.0) -> str:
        extra = ["--tools", tools] if tools is not None else []
        if tools:
            extra += ["--permission-mode", self.args.permission_mode]
        data = self.claude_call(prompt, cwd, helper=True, extra=extra, budget=budget)
        self.helper_cost += float(data.get("total_cost_usd") or 0)
        (self.out / f"hilfe-{name}-{self.call_no:03d}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        return str(data.get("result", ""))

    # ------------------------------------------------------------------ setup

    def setup(self) -> None:
        self.out.mkdir(parents=True, exist_ok=True)
        self.answers_dir.mkdir(exist_ok=True)
        self.work.mkdir(parents=True, exist_ok=True)
        owner = self.args.owner
        if self.args.dry_run:
            # Local stand-in for GitHub: template generated from the sources, bare repo as "remote"
            remote = self.work / f"{self.repo}.git"
            run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], self.work)
            subprocess.run([sys.executable, str(ROOT / "werkzeuge" / "vorlage.py"), str(self.project)], check=True)
            run(["git", "init", "-q", "-b", "main"], self.project)
            self.git_identity()
            run(["git", "add", "-A"], self.project)
            run(["git", "commit", "-q", "-m", "Initial commit from template"], self.project)
            run(["git", "remote", "add", "origin", str(remote)], self.project)
            run(["git", "push", "-q", "-u", "origin", "main"], self.project)
        else:
            run(["gh", "repo", "create", f"{owner}/{self.repo}", "--private",
                 "--template", f"{owner}/ki-projekt-vorlage"], self.work)
            for attempt in range(6):
                result = subprocess.run(["gh", "repo", "clone", f"{owner}/{self.repo}", str(self.project)],
                                        cwd=self.work, capture_output=True, text=True)
                if result.returncode == 0 and (self.project / "CLAUDE.md").exists():
                    break
                shutil.rmtree(self.project, ignore_errors=True)
                time.sleep(10)
            else:
                raise RuntimeError("template clone failed: " + result.stderr[-300:])
            self.git_identity()
        handover = self.project / "_handover"
        handover.mkdir(exist_ok=True)
        design = (SRC / "referenz-designdokument.md").read_text(encoding="utf-8")
        design = re.sub(r"Grundformel-Version: [0-9.]+", f"Grundformel-Version: {self.version}", design)
        (handover / "Referenzprojekt-Designdokument.md").write_text(design, encoding="utf-8")
        self.template_sha = run(["git", "rev-parse", "HEAD"], self.project).strip()
        say(f"Projekt {self.repo} eingerichtet ({self.template_sha[:8]}).")

    def git_identity(self) -> None:
        run(["git", "config", "user.name", "Referenzlauf"], self.project)
        run(["git", "config", "user.email", "referenzlauf@users.noreply.github.com"], self.project)

    # ------------------------------------------------------------------ the client

    def situation(self, role: str, phase: str, rounds: int) -> str:
        log = run(["git", "log", "main", "--oneline", "-15"], self.project, check=False).strip() or "(leer)"
        gate, removal = self.architecture_ready()
        manual = json.dumps(self.manual, ensure_ascii=False) if self.manual else "noch nicht durchgeführt"
        return (f"- Rolle, die spricht: {role}\n- Phase: {phase}\n- Bisherige Antworten von dir in dieser Phase: {rounds}\n"
                f"- Änderungswunsch Ä1 schon gesendet: {'ja' if self.ae1_sent else 'nein'}\n"
                f"- architecture.md: freigaberelevante Entscheidungen ausgefüllt: {'ja' if gate else 'nein'}; "
                f"Entfernungsanleitung ausgefüllt: {'ja' if removal else 'nein'}\n"
                f"- Ergebnis der manuellen Prüfung: {manual}\n- Git-Hauptzweig main (neueste zuerst):\n{log}")

    def architecture_ready(self) -> tuple[bool, bool]:
        refs = ["HEAD"] + run(["git", "for-each-ref", "--format=%(refname:short)", "refs/heads"], self.project, check=False).split()
        best = (False, False)
        for ref in refs:
            text = subprocess.run(["git", "show", f"{ref}:docs/architecture.md"], cwd=self.project,
                                  capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
            gate = self._filled(text, "## Gate-relevant decisions")
            removal = self._filled(text, "## Removing a feature")
            best = (best[0] or gate, best[1] or removal)
        return best

    @staticmethod
    def _filled(text: str, heading: str) -> bool:
        if heading not in text:
            return False
        body = text.split(heading, 1)[1].split("\n## ", 1)[0]
        return "<...>" not in body and "<file>" not in body and len(body.strip()) > 40

    def decide(self, role: str, phase: str, message: str, rounds: int) -> dict:
        prompt = f"""Du bist der Entscheider in einem Referenzlauf. Du spielst den Auftraggeber eines kleinen
Softwareprojekts: ein Mensch ohne Entwicklerwissen, der knapp, freundlich und auf Deutsch antwortet.
Du nennst nie Regelnummern, Kennzahlen, Teil 3 oder die Messung.

Deine verbindlichen Antwortregeln:
<<<REGELN
{self.rules}
REGELN>>>

Lage:
{self.situation(role, phase, rounds)}

Nachricht der Rolle:
<<<NACHRICHT
{message[-12000:]}
NACHRICHT>>>

Entscheide streng nach den Regeln und antworte NUR mit einem JSON-Objekt:
{{"aktion": "antworten" | "phase_fertig" | "manuelle_pruefung",
  "antwort": "Text an die Rolle; leer bei phase_fertig und manuelle_pruefung",
  "naechste_phase": "Plan" | "Block 1" | "Block 2" | "Block 3" | "Change" | "Release" | "Ende" | null,
  "anzahl_fragen": Zahl der Fragen, die die Rolle in dieser Nachricht an dich stellt,
  "unvorhergesehen": true, wenn du eine Standardantwort für etwas geben musstest, das nicht in den Regeln steht,
  "freigabe": "keine" | "erteilt" | "abgelehnt",
  "notiz": "ein Satz für das Protokoll"}}

Hinweise:
- "phase_fertig": Die Rolle hat ihre Phase oder ihren Auftrag abgeschlossen, übergeben und braucht nichts mehr
  von dir. Nenne die nächste Phase: nach dem Koordinator "Plan"; nach "Plan" "Block 1"; nach einem Block der
  nächste Block oder "Release", wenn alle Aufgaben außer REL erledigt sind; nach "Release" "Ende".
  Nach "Change" der nächste Block oder "Release", wie oben.
- "manuelle_pruefung": Die Rolle bittet in der Release-Phase um die manuelle Prüfung oder um Freigabe 3, und es
  liegt noch kein Ergebnis der manuellen Prüfung vor.
- Den Änderungswunsch Ä1 sendest du nie selbst; er kommt als erste Nachricht der Phase "Change".
- Steht die Antwort in den Regeln, gib sie wörtlich. Sonst die passende Standardantwort aus den Regeln."""
        try:
            decision = first_json(self.helper(prompt, self.work, "entscheider"))
        except ValueError:
            decision = {"aktion": "antworten", "antwort": "Entscheide nach bestem Ermessen und vermerke es im Designdokument.",
                        "unvorhergesehen": True, "notiz": "Entscheider-Antwort war kein JSON, Standardantwort gesendet."}
        decision["_rolle"], decision["_phase"] = role, phase
        self.decisions.append(decision)
        self.questions += int(decision.get("anzahl_fragen") or 0)
        self.unforeseen += 1 if decision.get("unvorhergesehen") else 0
        with (self.out / "entscheidungen.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(decision, ensure_ascii=False) + "\n")
        return decision

    def manual_test(self) -> dict:
        # A fresh folder per test: on Windows, rmtree often fails on read-only git files.
        target = self.work / f"manuell-{int(time.time())}"
        run(["git", "clone", "-q", str(self.project), str(target)], self.work)
        t0 = time.time()
        prompt = """Du bist eine Person ohne Entwicklerkenntnisse und prüfst ein Programm nach einer Anleitung.
Lies docs/manual-test.md und tu genau das, was dort steht, Schritt für Schritt, nicht mehr. Befehle für
PowerShell führst du so aus, damit Umlaute und das Euro-Zeichen so ankommen wie in einem normalen Fenster:
`powershell -NoProfile -Command "[Console]::OutputEncoding=[Text.Encoding]::UTF8; $env:PYTHONIOENCODING='utf-8'; <Befehl>"`.
Der Ordner, in dem du bist, ist schon das heruntergeladene und entpackte Projekt. Schritte zum Herunterladen,
Entpacken und Öffnen des Fensters gelten als erledigt; prüfe bei ihnen nur, ob sie verständlich beschrieben sind. Wenn ein Schritt nicht wie beschrieben
funktioniert oder Wissen voraussetzt, das in der Anleitung fehlt, notiere ihn und mach mit dem nächsten weiter.
Antworte am Ende NUR mit JSON:
{"schritte_gesamt": n, "problematische_schritte": [{"nr": n, "grund": "..."}],
 "geschaetzte_minuten_fuer_einen_menschen": n, "bestanden": true|false}"""
        if not (target / "docs" / "manual-test.md").exists():
            result = {"bestanden": False, "problematische_schritte": [{"nr": 0, "grund": "docs/manual-test.md fehlt auf main"}]}
        else:
            try:
                result = first_json(self.helper(prompt, target, "manuell", tools="Bash,Read,Glob,Grep", budget=3.0))
            except ValueError:
                result = {"bestanden": False, "problematische_schritte": [{"nr": 0, "grund": "Prüfer lieferte kein Ergebnis"}]}
        result["wandzeit_minuten"] = round((time.time() - t0) / 60, 1)
        self.manual = result
        (self.out / "manuelle-pruefung.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
        say(f"Manuelle Prüfung: {'bestanden' if result.get('bestanden') else 'nicht bestanden'}.")
        return result

    # ------------------------------------------------------------------ phases

    def prompt_coordinator(self) -> str:
        start = code_blocks((self.project / "docs/handbook/04-coordinator-start.md").read_text(encoding="utf-8"))[0]
        start = start.replace("<owner>", self.args.owner).replace("<x.y>", self.version)
        extra = next(b for b in code_blocks(self.rules) if "already created from" in b)
        extra = extra.replace("<konto>/kassenbuch-<Version>", f"{self.args.owner}/{self.repo}")
        return start + "\n\n" + extra

    def prompt_po(self, phase: str) -> str:
        block = code_blocks((self.project / "docs/templates/thread-start.md").read_text(encoding="utf-8"))[0]
        if "<Plan | Design | Architecture | Block n | Change | Release>" not in block:
            raise RuntimeError("PO-Startprompt der Vorlage hat ein unerwartetes Format")
        return (block.replace("<owner>/<name>", f"{self.args.owner}/{self.repo}").replace("<name>", "Kassenbuch")
                .replace("<Plan | Design | Architecture | Block n | Change | Release>", phase))

    def change_request(self) -> str:
        match = re.search(r"\*\*Ä1:\*\* „(.+?)“\s*$", self.rules, flags=re.M)
        if not match:
            raise RuntimeError("Änderungswunsch Ä1 nicht in Teil 3, Abschnitt 5 gefunden")
        return match.group(1)

    def conversation(self, role: str, phase: str, first_prompt: str) -> str | None:
        """One thread: start, answer until the phase is done. Returns the next phase."""
        session = str(uuid.uuid4())
        message = self.role(role, phase, first_prompt, session, resume=False)
        recent: list[str] = []
        for rounds in range(MAX_ROUNDS_PER_PHASE):
            if self.over_budget():
                return None
            decision = self.decide(role, phase, message, rounds)
            action = decision.get("aktion")
            if action == "phase_fertig":
                return decision.get("naechste_phase") or "Ende"
            if action == "manuelle_pruefung" and role == "PO" and not self.ae1_sent:
                return "Change"  # the client brings the change request before the release
            if action == "manuelle_pruefung":
                self.manual_test()
                decision = self.decide(role, phase, message, rounds)
                if decision.get("aktion") == "phase_fertig":
                    return decision.get("naechste_phase") or "Ende"
            answer = decision.get("antwort") or "Bitte mach weiter."
            recent.append(" ".join(answer.lower().split()))
            if len(recent) >= STUCK_REPEATS and len(set(recent[-STUCK_REPEATS:])) == 1:
                self.stopped_reason = (f"{role} {phase}: steckt fest, der Entscheider gab {STUCK_REPEATS}-mal "
                                       f"dieselbe Antwort („{answer[:80]}“)")
                return None
            message = self.role(role, phase, answer, session, resume=True)
        self.stopped_reason = self.stopped_reason or f"{role} {phase}: keine Einigung nach {MAX_ROUNDS_PER_PHASE} Runden"
        return None

    def execute(self) -> None:
        self.setup()
        phase = self.conversation("Koordinator", "Koordinator", self.prompt_coordinator())
        for _ in range(MAX_PHASES):
            if not phase or phase == "Ende" or self.over_budget():
                break
            if phase in ("Release", "Ende") and not self.ae1_sent:
                phase = "Change"  # the change request always comes before the release
            if phase == "Change" and self.ae1_sent:
                phase = "Release"
            say(f"PO-Phase {phase} startet.")
            first = self.prompt_po(phase)
            if phase == "Change":
                first += "\n\n" + self.change_request()
                self.ae1_sent = True
            phase = self.conversation("PO", phase, first)
        else:
            self.stopped_reason = self.stopped_reason or f"mehr als {MAX_PHASES} Phasen"

    # ------------------------------------------------------------------ audit and report

    def audit(self) -> tuple[str, dict]:
        prompt = code_blocks(section(self.teil3, 8))[0]
        prompt = prompt.replace("Part 3 is\nat <path>", f"Part 3 is\nat {self.teil3_path.as_posix()}", 1)
        prompt = prompt.replace("<path>", self.teil3_path.as_posix()).replace("<path to lauf.jsonl>", self.log_path.as_posix())
        data = self.claude_call(prompt, self.project, helper=False, budget=3.0,
                                extra=["--permission-mode", "dontAsk", "--add-dir", str(self.out),
                                       "--add-dir", str(self.teil3_path.parent), "--allowedTools",
                                       "Read", "Grep", "Glob", "Bash(git log:*)", "Bash(git diff:*)", "Bash(git show:*)",
                                       "Bash(git branch:*)", "Bash(git ls-remote:*)", "Bash(git rev-parse:*)"])
        self.helper_cost += float(data.get("total_cost_usd") or 0)
        text = str(data.get("result", ""))
        (self.out / "auditor.md").write_text(text, encoding="utf-8")
        try:
            summary = first_json(text)
        except ValueError:
            summary = {}
        return text, summary

    def metrics(self, audit: dict) -> dict:
        def tokens(usage: dict) -> int:
            return sum(int(u.get(k) or 0) for u in usage.values()
                       for k in ("inputTokens", "outputTokens", "cacheReadInputTokens", "cacheCreationInputTokens"))
        by_role: dict[str, float] = {}
        for s in self.sessions.values():
            by_role[s["role"]] = by_role.get(s["role"], 0) + s["cost"]
        active_min = (time.time() - self.started - self.limit_wait_s) / 60
        version = subprocess.run([self.claude, "--version"], capture_output=True, text=True).stdout.strip()
        return {
            "version": self.version, "lauf": self.run_id, "repository": self.repo, "datum": dt.date.today().isoformat(),
            "claude_code": version, "vorlage_commit": getattr(self, "template_sha", ""),
            "tokens": sum(tokens(s["usage"]) for s in self.sessions.values()),
            "kosten_usd": round(self.project_cost(), 2), "kosten_rollen": {k: round(v, 2) for k, v in by_role.items()},
            "hilfskosten_usd": round(self.helper_cost, 2), "schritte": self.turns, "sitzungen": len(self.sessions),
            "aktive_minuten": round(active_min), "limit_wartezeit_min": round(self.limit_wait_s / 60),
            "rueckfragen": self.questions, "unvorhergesehen": self.unforeseen,
            "abgelehnte_berechtigungen": sum(len(v) for v in self.denials.values()),
            "aenderungswunsch_gesendet": self.ae1_sent, "manuelle_pruefung": self.manual,
            "abbruch": self.stopped_reason, "audit": audit,
        }

    def report(self, metrics: dict, audit_text: str) -> None:
        previous = previous_column(ROOT / "messungen" / "ergebnisse.md")
        prompt = f"""Du schreibst Teile eines Prüfberichts auf Deutsch für einen Leser ohne Entwicklerwissen.
Kennzahlen dieses Laufs (exakt): {json.dumps(metrics, ensure_ascii=False)}
Vergleichswerte der Vorversion (Spalte aus ergebnisse.md, kann leer sein): {json.dumps(previous, ensure_ascii=False)}
Auswertung des Auditors:
<<<
{audit_text[-15000:]}
>>>
Antworte NUR mit JSON mit vier Markdown-Texten:
{{"ergebnis": "Ergebnis in drei Sätzen: Verbrauch gegenüber der Vorversion in Prozent (oder 'erster gültiger Lauf'), Regeltreue, Qualität",
  "kostentreiber": "die drei größten Kostentreiber als Liste, mit Beleg",
  "auffaelligkeiten": "abgelehnte Berechtigungen, Abbrüche, Limit, unvorhergesehene Fragen, als kurze Liste",
  "empfehlungen": "höchstens fünf Empfehlungen für die nächste Bibel-Version, jede mit dem Befund, auf dem sie beruht"}}
Verwende nur Zahlen aus den Kennzahlen und der Auswertung, erfinde keine."""
        try:
            parts = first_json(self.helper(prompt, self.work, "bericht"))
        except ValueError:
            parts = {}
        write_report(self.out, metrics, audit_text, parts, previous)
        update_results(ROOT / "messungen" / "ergebnisse.md", metrics)


# --------------------------------------------------------------------------- results table

ROWS = ["Datum", "Claude-Code-Version", "Tokens gesamt", "Kostenschätzung (USD)", "davon Koordinator",
        "davon PO-Sitzungen (inkl. SP und QA)", "Schritte", "Aktive Laufzeit", "Limit erreicht", "Sitzungen",
        "Aufgaben", "Erstdurchlauf", "QA-Runden", "Echte Befunde", "Rückfragen (davon unvorhergesehen)",
        "Abgelehnte Berechtigungen", "Regeltreue", "Manuelle Prüfung (Minuten)", "Tests, CI grün", "Bemerkung"]


def column_values(m: dict) -> dict:
    a, manual = m.get("audit") or {}, m.get("manuelle_pruefung") or {}
    n_rules = a.get("regeln_gesamt") or ""
    return {
        "Datum": m["datum"], "Claude-Code-Version": m["claude_code"], "Tokens gesamt": f"{m['tokens']:,}".replace(",", "."),
        "Kostenschätzung (USD)": f"{m['kosten_usd']:.2f}".replace(".", ","),
        "davon Koordinator": f"{m['kosten_rollen'].get('Koordinator', 0):.2f}".replace(".", ","),
        "davon PO-Sitzungen (inkl. SP und QA)": f"{m['kosten_rollen'].get('PO', 0):.2f}".replace(".", ","),
        "Schritte": str(m["schritte"]), "Aktive Laufzeit": f"{m['aktive_minuten']} Min.",
        "Limit erreicht": f"ja, {m['limit_wartezeit_min']} Min. gewartet" if m["limit_wartezeit_min"] else "nein",
        "Sitzungen": str(m["sitzungen"]), "Aufgaben": str(a.get("aufgaben", "–")),
        "Erstdurchlauf": f"{a['erstdurchlauf_prozent']} %" if "erstdurchlauf_prozent" in a else "–",
        "QA-Runden": str(a.get("qa_runden", "–")), "Echte Befunde": str(a.get("echte_befunde", "–")),
        "Rückfragen (davon unvorhergesehen)": f"{m['rueckfragen']} ({m['unvorhergesehen']})",
        "Abgelehnte Berechtigungen": str(m["abgelehnte_berechtigungen"]),
        "Regeltreue": f"{a.get('regeln_erfuellt', '–')} / {n_rules}",
        "Manuelle Prüfung (Minuten)": str(manual.get("geschaetzte_minuten_fuer_einen_menschen", "–")),
        "Tests, CI grün": f"{a.get('tests', '–')}, {'ja' if a.get('ci_gruen') else 'nein'}",
        "Bemerkung": (f"Messaufbau {MESSAUFBAU} · " + (("Abgebrochen: " + m["abbruch"]) if m["abbruch"] else f"Automatischer Lauf {m['lauf']}")),
    }


def read_table(path: Path) -> tuple[list[str], list[str], list[list[str]], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("| Kennzahl"))
    end = start
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines[start:end]]
    return lines[:start], rows[0], [r for r in rows[2:]], lines[end:]


def previous_column(path: Path) -> dict:
    _, header, rows, _ = read_table(path)
    for col in range(len(header) - 1, 0, -1):
        values = {r[0]: r[col] if col < len(r) else "" for r in rows}
        if (values.get("Kostenschätzung (USD)") and "abgebrochen" not in header[col]
                and f"Messaufbau {MESSAUFBAU}" in values.get("Bemerkung", "")):
            return {"spalte": header[col], **values}
    return {}


def update_results(path: Path, m: dict) -> None:
    before, header, rows, after = read_table(path)
    title = f"Bibel {m['version']}"
    col = header.index(title) if title in header else -1
    filled = any(r[0] == "Kostenschätzung (USD)" and len(r) > col and r[col] for r in rows)
    if col == -1 or filled:
        header.append(title if col == -1 else f"{title} (Lauf {m['lauf']})")
        col = len(header) - 1
    if m.get("abbruch") and "abgebrochen" not in header[col]:
        header[col] += " (abgebrochen)"
    values = column_values(m)
    for r in rows:
        while len(r) < len(header):
            r.append("")
        r[col] = values.get(r[0], r[col])
    table = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    table += ["| " + " | ".join(r) + " |" for r in rows]
    path.write_text("\n".join(before + table + after) + "\n", encoding="utf-8", newline="\n")


def write_report(out: Path, m: dict, audit_text: str, parts: dict, previous: dict) -> None:
    values = column_values(m)
    lines = [f"# Prüfbericht Bibel {m['version']}", "",
             f"Automatischer Referenzlauf {m['lauf']} · Repository {m['repository']} · {m['datum']}", ""]
    if m["abbruch"]:
        lines += [f"**Teilbericht:** Der Lauf wurde abgebrochen ({m['abbruch']}).", ""]
    lines += ["## 1. Ergebnis", "", parts.get("ergebnis", "–"), "", "## 2. Kennzahlen", "",
              f"| Kennzahl | {previous.get('spalte', 'Vorversion')} | Bibel {m['version']} |", "| --- | --- | --- |"]
    lines += [f"| {r} | {previous.get(r, '–') or '–'} | {values.get(r, '')} |" for r in ROWS]
    lines += ["", f"Hilfsaufrufe (Entscheider, manuelle Prüfung, Auditor, Bericht) zusätzlich: {str(m['hilfskosten_usd']).replace('.', ',')} USD, "
              "nicht in der Kostenschätzung enthalten.", "",
              "## 3. Regeltreue und Auswertung", "", re.sub(r"\n?\{[^{}]*\}\s*$", "", audit_text.strip()), "",
              "## 4. Größte Kostentreiber", "", parts.get("kostentreiber", "–"), "",
              "## 5. Auffälligkeiten", "", parts.get("auffaelligkeiten", "–"), "", "## 6. Manuelle Prüfung", ""]
    manual = m.get("manuelle_pruefung") or {}
    if manual:
        lines += [f"Bestanden: {'ja' if manual.get('bestanden') else 'nein'} · geschätzte Dauer für einen Menschen: "
                  f"{manual.get('geschaetzte_minuten_fuer_einen_menschen', '–')} Minuten · Schritte: {manual.get('schritte_gesamt', '–')}", ""]
        lines += [f"- Schritt {p.get('nr')}: {p.get('grund')}" for p in manual.get("problematische_schritte", [])]
    else:
        lines += ["Nicht durchgeführt."]
    lines += ["", "Die Prüfung lief automatisch. Ein Mensch sollte die Verständlichkeit der Anleitung mit einer "
              "10-Minuten-Stichprobe bestätigen.", "", "## 7. Empfehlungen für die nächste Bibel-Version", "",
              parts.get("empfehlungen", "–"), ""]
    (out / "bericht.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    (out / "kennzahlen.json").write_text(json.dumps(m, ensure_ascii=False, indent=1, default=list), encoding="utf-8")


# --------------------------------------------------------------------------- main

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--owner", required=True)
    p.add_argument("--version", default=META["version"])
    p.add_argument("--run-id", default="")
    p.add_argument("--workdir", default=str(ROOT.parent / "lauf"))
    p.add_argument("--budget-call", type=float, default=8.0)
    p.add_argument("--budget-total", type=float, default=30.0)
    p.add_argument("--permission-mode", default="auto")
    p.add_argument("--max-limit-wait-min", type=int, default=240)
    p.add_argument("--dry-run", action="store_true")
    lauf = Lauf(p.parse_args())
    try:
        lauf.execute()
    except Exception as exc:  # the report must still be written
        lauf.stopped_reason = lauf.stopped_reason or f"Fehler: {exc}"
        say(f"Abbruch: {exc}")
    audit_text, audit = lauf.audit() if lauf.project.exists() else ("Kein Projekt vorhanden.", {})
    metrics = lauf.metrics(audit)
    lauf.report(metrics, audit_text)
    say(f"Fertig. Projektkosten {metrics['kosten_usd']} USD, Bericht in {lauf.out.relative_to(ROOT)}.")
    Path(os.environ.get("GITHUB_OUTPUT", os.devnull)).open("a").write(f"protokoll={lauf.out.relative_to(ROOT).as_posix()}\n")


if __name__ == "__main__":
    main()
