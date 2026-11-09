"""Builds the template repository (ki-projekt-vorlage) from Part 1 and Part 2 of the Bible."""
import json
import re
import sys
from pathlib import Path

BIBLE = Path(__file__).resolve().parent.parent / "quelle"
REPO = Path(sys.argv[1])
_META = json.loads((BIBLE / "version.json").read_text(encoding="utf-8"))
VERSION, DATE = _META["version"], _META["datum"]


def sections(md: str) -> dict:
    """Split a part into {section number: (title, body)}, ignoring headings inside code fences."""
    out, current, in_fence = {}, None, False
    for line in md.splitlines(keepends=True):
        if line.startswith("```"):
            in_fence = not in_fence
        m = None if in_fence else re.match(r"## (\d+)\. (.*)", line)
        if m:
            current = int(m.group(1))
            out[current] = [m.group(2).strip(), ""]
        elif current is not None:
            out[current][1] += line
    return {k: (t, b.strip("\n")) for k, (t, b) in out.items()}


def blocks(text: str) -> list:
    return [m.group(1) for m in re.finditer(r"```[a-z]*\n(.*?)\n```", text, flags=re.S)]


def write(rel: str, content: str):
    path = REPO / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip("\n") + "\n", encoding="utf-8")


part1 = (BIBLE / "teil1.md").read_text(encoding="utf-8")
part2 = (BIBLE / "teil2.md").read_text(encoding="utf-8")
s = sections(part2)
b = {k: blocks(v[1]) for k, v in s.items()}

# --- Grundformel (German, unchanged) -------------------------------------
mermaid = """```mermaid
flowchart LR
  A[Start<br/>Koordinator] --> B[Design<br/>Mensch + PO] --> G1{Freigabe 1} --> C[Architektur<br/>SP, Prüfung QA] --> G2{Freigabe 2<br/>entfällt in Klasse S}
  G2 --> D[Backlog<br/>PO] --> E[Umsetzen<br/>SP + Tests] --> Q{QA prüft}
  Q -- Befund --> E
  Q -- ja --> M[Squash-Merge<br/>PO, CI grün] --> G3{Freigabe 3<br/>vor Release}
  M -- nächste Aufgabe --> D
```"""
gf = part1.replace("# Teil 1: Grundformel", f"# KI-Projekt-Bibel – Teil 1: Grundformel\n\nVersion {VERSION} · {DATE}", 1)
write("docs/grundformel.md", gf.replace("[[DIAGRAMM]]", mermaid))

# --- Handbook: every Part 2 chapter as its own file (Part 2 §19) -----------
names = {}
for row in re.finditer(r"^\| §(\d+) [^|]+\| `([^`]+)` \|", s[19][1], flags=re.M):
    names[int(row.group(1))] = row.group(2)
assert sorted(names) == list(range(1, 22)), names
for num, fname in names.items():
    title, body = s[num]
    write(f"docs/handbook/{fname}", f"# Teil 2, §{num}. {title}\n\nKI-Projekt-Bibel {VERSION}\n\n{body}")

# --- Templates (Part 2 §17) ------------------------------------------------
gap = "# Lückenanalyse – Checkliste des PO\n\n" + s[3][1]
thread_start = "# Thread start prompts\n\n" + "\n\n".join(f"```text\n{x}\n```" for x in b[18])
templates = {
    "design.md": b[2][0],
    "gap-checklist.md": gap,
    "role.md": b[5][0],
    "handoff.md": b[6][0],
    "stack-profile.md": b[7][0],
    "claude-md.md": b[9][0],
    "spec.md": b[10][0],
    "backlog.md": b[11][0],
    "task.md": b[11][1],
    "architecture.md": b[12][0],
    "decision.md": b[13][0],
    "status.md": b[14][0],
    "changelog.md": b[14][1],
    "env-example.txt": b[14][2],
    "gitignore.txt": b[14][3],
    "gate-summary.md": b[15][0],
    "coordinator-check.md": b[16][0],
    "thread-start.md": thread_start,
    "manual-test.md": b[20][0],
}
listed = re.findall(r"^\| `([^`]+)` \| §", s[17][1], flags=re.M)
assert sorted(listed) == sorted(templates), (listed, templates.keys())
for name, body in templates.items():
    write(f"docs/templates/{name}", body)

# --- Role files (Part 2 §5) ------------------------------------------------
for name, body in zip(["po", "sp", "qa", "coordinator"], b[5][1:5]):
    write(f"docs/roles/{name}.md", body)

# --- Project files, unfilled -----------------------------------------------
write("CLAUDE.md", templates["claude-md.md"].replace("<x.y>", VERSION))
write("docs/design.md", templates["design.md"])
write("docs/spec.md", "<!-- Filled by the PO before the first gate. -->\n\n" + templates["spec.md"])
write("docs/backlog.md", "<!-- Filled by the PO after the architecture is approved. -->\n\n" + templates["backlog.md"])
write("docs/architecture.md", "<!-- Filled by the SP before the architecture gate. -->\n\n" + templates["architecture.md"])
write("docs/stack-profile.md", "<!-- Filled by the SP with the architecture. -->\n\n" + templates["stack-profile.md"])
write("docs/status.md", templates["status.md"])
write("docs/status-archive.md", "# Status archive\nOlder handoffs, moved here by the PO. Not read at thread start.")
write("docs/tasks/.gitkeep", "")
write("docs/decisions/.gitkeep", "")
write("CHANGELOG.md", templates["changelog.md"])
write(".env.example", templates["env-example.txt"])
write(".gitignore", templates["gitignore.txt"])

# --- Tool adapter (Part 2 §8) ------------------------------------------------
write(".claude/agents/sp.md", b[8][1])
write(".claude/agents/qa.md", b[8][2])
write(".claude/settings.json", b[8][3])
write(".claude/hooks/quiet_tests.py", b[8][5])
write(".claude/hooks/test_filter.py", b[8][6])

write("README.md", f"""# ki-projekt-vorlage

Template repository of the KI-Projekt-Bibel, version {VERSION}.

Create a new project from it ("Use this template" on GitHub, or
`gh repo create <owner>/<name> --private --template <owner>/ki-projekt-vorlage`).
The Coordinator then fills in only the fields marked `<at setup>` in
CLAUDE.md, the design document and the first handoff in docs/status.md.

Do not change this repository for a single project. Changes come only
with a new Bible version and get a tag (e.g. `v{VERSION}`).
""")
print("ok", sum(1 for p in REPO.rglob("*") if p.is_file() and ".git" not in p.parts), "files")
