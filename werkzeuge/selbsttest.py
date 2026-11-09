"""Self-test of the KI-Projekt-Bibel: consistency checks that cost no tokens.

Run: python werkzeuge/selbsttest.py [--pdf]
Exit code 0 = all checks passed, 1 = at least one check failed.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "quelle"
TOOLS = ROOT / "werkzeuge"
META = json.loads((SRC / "version.json").read_text(encoding="utf-8"))
V = META["version"]

# Words that would tell a project role that it is being measured.
FORBIDDEN_IN_TEMPLATE = ["Referenzprojekt", "Referenzlauf", "Teil 3", "Part 3", "Entscheider",
                         "Decider", "Messlauf", "Prüfbericht", "Kassenbuch", "bibel-messungen"]

failures: list[str] = []


def check(ok: bool, message: str) -> None:
    print(("  ok    " if ok else "  FEHLER ") + message)
    if not ok:
        failures.append(message)


def headings(md: str) -> set[int]:
    """Numbers of '## N.' headings outside code fences."""
    nums, fence = set(), False
    for line in md.splitlines():
        if line.startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"## (\d+)\. ", line)
        if m:
            nums.add(int(m.group(1)))
    return nums


def prose(md: str) -> str:
    """Text outside code fences."""
    return re.sub(r"```.*?```", "", md, flags=re.S)


def main() -> None:
    t1 = (SRC / "teil1.md").read_text(encoding="utf-8")
    t2 = (SRC / "teil2.md").read_text(encoding="utf-8")
    t3 = (SRC / "teil3_quelle.md").read_text(encoding="utf-8")
    design = (SRC / "referenz-designdokument.md").read_text(encoding="utf-8")
    h1, h2, h3 = headings(t1), headings(t2), headings(t3)

    print(f"Version {V}")
    print("1. Versionsangaben")
    check(f"- **{V}** (" in t1, f"Teil 1: Versionsgeschichte beginnt mit {V}")
    newest = re.search(r"- \*\*([0-9.]+)\*\* \(", t1)
    check(bool(newest) and newest.group(1) == V, "Teil 1: neuester Eintrag der Versionsgeschichte ist die aktuelle Version")
    check(f"Version {V}, gehört zur Grundformel {V}." in t2, "Teil 2: Einleitung nennt die aktuelle Version")
    role_versions = set(re.findall(r"Grundformel version: ([0-9.]+)", t2))
    check(role_versions == {V}, f"Teil 2: alle Rollendateien nennen {V} (gefunden: {sorted(role_versions)})")
    check(f"Grundformel-Version: {V}" in design, "Referenz-Designdokument nennt die aktuelle Version")

    print("2. Querverweise")
    for name, text, own in [("Teil 1", t1, h1), ("Teil 2", t2, h2), ("Teil 3", t3, h3)]:
        body = prose(text)
        for n in re.findall(r"Teil 2,? §(\d+)", body):
            check(int(n) in h2, f"{name}: Verweis auf Teil 2, §{n} existiert")
        for n in re.findall(r"Grundformel,? §(\d+)", body):
            check(int(n) in h1, f"{name}: Verweis auf Grundformel §{n} existiert")
        if name == "Teil 2":
            for n in set(re.findall(r"\(§(\d+)\)", body)):
                check(int(n) in h2, f"Teil 2: interner Verweis §{n} existiert")
    for n in set(re.findall(r"Part 3 §(\d+)", t3)):
        check(int(n) in h3, f"Teil 3: Verweis Part 3 §{n} existiert")
    for n in set(re.findall(r"Abschnitt (\d+)", prose(t3))):
        check(int(n) in h3, f"Teil 3: Verweis auf Abschnitt {n} existiert")

    print("3. Prüfliste in Teil 3")
    rules = re.findall(r"^\| R(\d+) \|", t3, flags=re.M)
    n_rules = len(rules)
    check([int(r) for r in rules] == list(range(1, n_rules + 1)), f"R1 bis R{n_rules} lückenlos nummeriert")
    stated = set(re.findall(r"R1 (?:bis|to) R(\d+)", t3))
    check(stated == {str(n_rules)}, f"Teil 3 nennt überall R1 bis R{n_rules} (gefunden: {sorted(stated)})")
    ergebnisse = (ROOT / "messungen" / "ergebnisse.md").read_text(encoding="utf-8")
    check(f"/ {n_rules}" in ergebnisse or f"von {n_rules}" in ergebnisse,
          f"ergebnisse.md rechnet mit {n_rules} Regeln")

    print("4. Vorlagen-Repository")
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run([sys.executable, str(TOOLS / "vorlage.py"), tmp], capture_output=True, text=True)
        check(result.returncode == 0, "Vorlage lässt sich erzeugen" + ("" if result.returncode == 0 else ": " + result.stderr[-300:]))
        if result.returncode == 0:
            repo = Path(tmp)
            for rel in ["CLAUDE.md", ".claude/settings.json", ".claude/agents/sp.md", ".claude/agents/qa.md",
                        ".claude/hooks/quiet_tests.py", ".claude/hooks/test_filter.py", "docs/grundformel.md",
                        "docs/roles/po.md", "docs/status.md", ".gitignore", ".env.example"]:
                check((repo / rel).exists(), f"Vorlage enthält {rel}")
            settings = json.loads((repo / ".claude/settings.json").read_text(encoding="utf-8"))
            check(settings.get("model") == "opus", "settings.json setzt das Modell")
            check(settings.get("autoMemoryEnabled") is False, "settings.json schaltet die Gedächtnisfunktion ab")
            check("PreToolUse" in settings.get("hooks", {}), "settings.json registriert den Test-Hook")
            check(any("force" in d for d in settings.get("permissions", {}).get("deny", [])), "settings.json sperrt Force-Push")
            check(f"Grundformel version: {V}" in (repo / "CLAUDE.md").read_text(encoding="utf-8"), "CLAUDE.md nennt die Version")
            leaks = []
            for f in repo.rglob("*"):
                if f.is_file():
                    text = f.read_text(encoding="utf-8", errors="ignore")
                    leaks += [f"{f.relative_to(repo)}: {w}" for w in FORBIDDEN_IN_TEMPLATE if w in text]
            check(not leaks, "kein Hinweis auf die Messung in der Vorlage" + ("" if not leaks else f" ({leaks[:5]})"))
            check(test_hooks(repo / ".claude" / "hooks"), "Hook-Skripte verhalten sich wie erwartet")

    print("5. Teil 3 ist vollständig")
    check("{{DESIGN}}" in t3, "Teil 3 enthält den Platzhalter für das Designdokument")
    check("```" not in design, "Designdokument enthält keine Codeblöcke")
    check("Projektklasse: S" in design, "Designdokument nennt Projektklasse S")

    if "--pdf" in sys.argv:
        print("6. PDFs")
        result = subprocess.run([sys.executable, str(TOOLS / "bauen.py")], capture_output=True, text=True)
        check(result.returncode == 0, "PDFs lassen sich bauen" + ("" if result.returncode == 0 else ": " + result.stderr[-300:]))

    print()
    if failures:
        print(f"{len(failures)} Prüfung(en) fehlgeschlagen.")
        sys.exit(1)
    print("Alle Prüfungen bestanden.")


def test_hooks(hooks: Path) -> bool:
    """The test hook wraps test runners, leaves other commands alone and keeps the exit code."""
    def run_hook(command: str) -> dict:
        out = subprocess.run([sys.executable, str(hooks / "quiet_tests.py")],
                             input=json.dumps({"tool_input": {"command": command}}),
                             capture_output=True, text=True, check=True).stdout
        return json.loads(out)

    if run_hook("ls -la") != {}:
        return False
    wrapped = run_hook("pytest -q").get("hookSpecificOutput", {}).get("updatedInput", {}).get("command", "")
    if "test_filter.py" not in wrapped or "pipefail" not in wrapped:
        return False
    sample = "\n".join([f"test_{i} PASSED" for i in range(200)] + ["test_x FAILED", "E   assert 1 == 2", "1 failed, 200 passed"])
    filtered = subprocess.run([sys.executable, str(hooks / "test_filter.py")], input=sample,
                              capture_output=True, text=True, check=True).stdout
    if "FAILED" not in filtered or "1 failed" not in filtered or len(filtered.splitlines()) > 40:
        return False
    if sys.platform != "win32":
        code = subprocess.run(["bash", "-c", f'set -o pipefail; ( exit 3 ) 2>&1 | "{sys.executable}" "{hooks / "test_filter.py"}"'],
                              capture_output=True).returncode
        if code != 3:
            return False
    return True


if __name__ == "__main__":
    main()
