# Teil 2: Handbuch

Teil 2 enthält Vorlagen, Checklisten und Prompts zur Grundformel (Teil 1). Version 1.6, gehört zur Grundformel 1.6. Alles hier liegt fertig im **Vorlagen-Repository** (§21): jedes Kapitel als Datei in `docs/handbook/`, jede Vorlage in `docs/templates/` (Namen in §17), die Rollendateien in `docs/roles/` und die Werkzeug-Einstellungen in `.claude/`. Beim Projektstart wird nichts davon abgeschrieben oder übersetzt. Rollen lesen beim Thread-Start nur ihre kompakte Rollendatei; ein Handbuch-Kapitel schlagen sie nur gezielt nach, wenn die Aufgabe es verlangt (§19).

## 1. Regeln für das Designdokument

Das Designdokument beschreibt *was* das Produkt können soll und *warum*. Es ist auf Deutsch, gehört dem PO und ist die Grundlage für die erste Freigabe.

1. **Alle Abschnitte sind Pflicht.** Ein Abschnitt darf mit „entfällt, weil …“ gefüllt werden. Eine Lücke ist immer eine bewusste Entscheidung.
2. **Was und Warum, nie Wie.** Technische Umsetzung entscheidet der SP in der Architektur. Feste Vorgaben stehen unter Rahmenbedingungen.
3. **Funktionen als Nutzergeschichten:** „Als [Nutzer] möchte ich [Ziel], damit [Nutzen].“ Die prüfbaren Akzeptanzkriterien formuliert der PO in der Spezifikation.
4. **Priorität:** Jede Funktion ist Muss, Soll oder Kann. Die erste Ausbaustufe (MVP) ist das Kleinste mit echtem Nutzen; nur sie wird zuerst gebaut.
5. **Änderungsanfällige Funktionen werden markiert.** Daraus leitet der SP Ein/Aus-Schalter ab.
6. **Erfolgskriterien sind messbar.** Sonst kann niemand sagen, wann etwas fertig ist.
7. **Bereitstellung früh entscheiden.** Wie das Produkt zum Nutzer kommt, auf welchen Geräten es läuft und wer es manuell prüft, steht schon vor der ersten Freigabe fest. Späte Entscheidungen darüber kosteten im Pilot acht Nacharbeitsrunden.
8. **Personenbezogene Daten: ja oder nein entscheidet der Mensch.** Die Antwort steht ausdrücklich in Abschnitt 6. Ein „ja“ macht das Projekt zur Klasse L (Grundformel §4). Der PO fragt nach, wenn die Antwort fehlt, entscheidet aber nie selbst.
9. **Lückenanalyse:** Der PO prüft jeden Abschnitt mit der Checkliste (Abschnitt 3) und fragt nach, bis alles beantwortet ist.
10. **Versionierung:** Versionsnummer und Änderungsprotokoll am Ende. Änderungen nach der ersten Freigabe laufen über den PO.
11. **Kürze:** So kurz wie möglich. Lange Listen, Regelwerke und Details kommen in Anhänge.
12. **Skizzen optional:** Mockups, Skizzen und Beispiele als Anhang.

## 2. Vorlage Designdokument

Die Vorlage liegt als `docs/design.md` im Projekt. Die Zeilen mit `>` sind Leitfragen und werden beim Ausfüllen ersetzt.

```markdown
# Designdokument: [Projektname]

Version: 0.1 · Status: Entwurf | Freigegeben · Grundformel-Version: [x.y]
Projektklasse: [S | M | L] (Grundformel §4)

## 1. Zweck und Problem
> Welches Problem löst das Produkt? Für wen? Warum jetzt? (max. 5 Sätze)

## 2. Zielnutzer und Nutzungssituation
> Wer nutzt es (Rollen)? Wie viele? Wann, wo, auf welchem Gerät?
> Welche Vorkenntnisse haben die Nutzer?

## 3. Funktionen
> Eine Zeile pro Funktion. Priorität: Muss | Soll | Kann.
> MVP = Teil der ersten Ausbaustufe. Änderbar = spätere Änderung/Abschaltung absehbar.

| ID | Nutzergeschichte | Priorität | MVP | Änderbar |
| --- | --- | --- | --- | --- |
| F01 | Als [Nutzer] möchte ich [Ziel], damit [Nutzen]. | Muss | ja | nein |

## 4. Nicht-Ziele
> Was das Produkt ausdrücklich NICHT tun soll, auch wenn es naheliegt.

## 5. Erfolgskriterien
> Woran erkennen wir, dass das Projekt erfolgreich ist? Messbar formulieren.

## 6. Daten
> Welche Daten werden verarbeitet? Woher kommen sie? Wie aktuell müssen sie sein?
> Personenbezogene Daten: ja oder nein? (Entscheidung des Auftraggebers;
> „ja“ bedeutet Projektklasse L.) Wenn ja: welche?
> Wie lange werden sie aufbewahrt?

## 7. Externe Systeme und Schnittstellen
> Welche fremden Dienste, APIs, Datenquellen oder Programme werden angebunden?
> Gibt es Kosten, Limits oder Lizenzbedingungen?

## 8. Plattform, Bereitstellung und Betrieb
> Web, Desktop, Mobil, Server, Spiel-Client, Kommandozeile?
> Bereitstellung: Wie kommt das Produkt zum Nutzer (lokal starten, Hosting,
> App-Store, Datei)? Auf welchen Zielgeräten muss es laufen?
> Manuelle Prüfung: Wer prüft vor dem Release von Hand? Mit welchem
> Betriebssystem (Windows, macOS, Linux) und welchen Kenntnissen?
> In welcher Sprache sind seine Werkzeuge eingestellt?
> Wer betreibt und wartet es?

## 9. Qualitätsanforderungen
> Performance-Ziele (Antwortzeit, Bildrate, Datenmenge)?
> Verfügbarkeit (darf es ausfallen)? Offline-Betrieb nötig?

## 10. Sicherheit und Datenschutz
> Wer darf was? Gibt es Anmeldung und Rollen?
> Bei personenbezogenen Daten: Zweck, Speicherort, Löschfristen,
> Auftragsverarbeiter (inkl. KI-Anbieter).

## 11. Rahmenbedingungen
> Feste Vorgaben (Technik, Server, Spielversion, bestehende Systeme).
> Zeitrahmen, Budget, verfügbare KI-Modelle.

## 12. Glossar
| Deutsch | Englisch | Bedeutung |
| --- | --- | --- |

## 13. Offene Fragen
- [ ] [Frage] – zuständig: [Mensch | PO]

## Anhänge
> Skizzen, Mockups, lange Listen, Regelwerke.

## Änderungsprotokoll
| Version | Datum | Änderung |
| --- | --- | --- |
| 0.1 | [Datum] | Erstfassung |
```

## 3. Checkliste des PO für die Lückenanalyse

Das Designdokument ist bereit für die erste Freigabe, wenn jeder Abschnitt seine Prüffrage besteht oder begründet „entfällt“. Der PO stellt pro Durchgang höchstens fünf Rückfragen, gebündelt und nach Wichtigkeit sortiert.

| Abschnitt | Bereit, wenn … |
| --- | --- |
| Kopf | Die Projektklasse ist eingetragen und passt zu den Bedingungen der Grundformel §4. |
| 1. Zweck | Problem und Zielgruppe sind in wenigen Sätzen klar; ein Außenstehender versteht, warum es das Produkt gibt. |
| 2. Zielnutzer | Alle Nutzerrollen sind benannt, mit Gerät und Nutzungssituation. |
| 3. Funktionen | Jede Funktion hat ID, Nutzergeschichte, Priorität und MVP-Kennzeichen; keine Funktion beschreibt Technik. |
| 4. Nicht-Ziele | Mindestens die naheliegenden Erweiterungen sind ausdrücklich ausgeschlossen oder bewusst offen. |
| 5. Erfolgskriterien | Jedes Kriterium ist messbar oder eindeutig mit ja/nein prüfbar. |
| 6. Daten | Herkunft, Aktualität und Aufbewahrung sind geklärt; personenbezogen ja/nein hat der Auftraggeber ausdrücklich beantwortet. |
| 7. Schnittstellen | Jedes externe System ist benannt, mit bekannten Kosten, Limits und Lizenz. |
| 8. Plattform | Zielplattform, Bereitstellungsweg und Zielgeräte stehen fest; Person, Betriebssystem und Kenntnisstand der manuellen Prüfung sind bekannt. |
| 9. Qualität | Performance-Ziele sind beziffert, wenn das Projekt performancekritisch ist. |
| 10. Sicherheit | Rechte sind geklärt; bei personenbezogenen Daten sind alle Datenschutzfragen beantwortet. |
| 11. Rahmen | Feste Vorgaben sind von Wünschen getrennt. |
| 12. Glossar | Jeder Fachbegriff aus Abschnitt 3 hat eine englische Übersetzung. |
| 13. Offene Fragen | Keine offene Frage blockiert eine Muss-Funktion des MVP. |

**Widersprüche:** Findet der PO Widersprüche zwischen Abschnitten (z. B. eine Funktion, die ein Nicht-Ziel berührt), meldet er sie vor allen anderen Rückfragen.

## 4. Startprompt für den Koordinator

Der Koordinator bekommt nur diesen Prompt und das Designdokument (falls vorhanden). Grundformel und Handbuch braucht er nicht als Anhang: Sie liegen fertig im Vorlagen-Repository. Er braucht eine Umgebung mit Dateizugriff, Git und Zugang zum Konto, in dem das Projekt-Repository angelegt wird.

```text
You are the COORDINATOR for a new project.

Template repository: <owner>/ki-projekt-vorlage (tag v<x.y>).
Attached: the design document (German), if available.

Your job:
1. Ask me at most 5 questions you need for the setup: project name,
   repository owner, project class (S, M or L, see
   docs/grundformel.md §4 in the template), fixed constraints.
   Then start without further questions.
2. Create a new private repository from the template (for example
   `gh repo create <owner>/<name> --private --template
   <owner>/ki-projekt-vorlage --clone`). If you cannot create
   repositories, ask me to create it from the template and give you
   access. Do not copy or rewrite the template files by hand.
3. Fill in only the project-specific parts:
   - CLAUDE.md: project name, purpose (one or two sentences from the
     design document), project class, Grundformel version.
   - docs/design.md: the design document, converted to Markdown with
     unchanged wording, or the template header with name and class if
     no design document is attached.
   - docs/status.md: the handoff note to the PO (format in
     docs/templates/handoff.md).
4. Project class M or L only: add a role if the design document
   justifies it (role file from docs/templates/role.md, decision in
   docs/decisions/). Class S never gets additional roles.
5. Run the acceptance check in docs/templates/coordinator-check.md.
6. Make the initial commit on main and push it. Verify the push.

Do not write application code. Do not make product decisions.

End with a short summary for me in German: repository, project
class, roles, open questions, result of the acceptance check.
This thread ends after the summary.
```

## 5. Rollendateien

Rollendateien sind englisch und kurz (Richtwert eine Seite), weil sie bei jedem Arbeitsschritt mitgesendet werden. Sie enthalten alles, was die Rolle bei jedem Schritt braucht, auch die Kostenregeln, und verweisen für Seltenes auf Dateien zum Nachschlagen. Sie liegen fertig im Vorlagen-Repository; der Koordinator ändert sie nur, wenn ein Projekt es verlangt, und legt neue Rollen nach dem Gerüst an.

**Gerüst**

```markdown
# Role: <NAME>
Grundformel version: <x.y>

## Mission
## Inputs (read at thread start)
## Look up only when needed
## Outputs
## Rules
## Cost rules
## Must not
## Handoff
## Escalation
```

**PO – `docs/roles/po.md`**

```markdown
# Role: Product Owner (PO)
Grundformel version: 1.6

## Mission
Own the design document. Turn it into a specification and a backlog.
Orchestrate SP and QA per task. Report to the human in German.

## Inputs (read at thread start)
CLAUDE.md (project class), docs/status.md, and only the files of the
current phase: Plan/Design: docs/design.md. Later phases: docs/spec.md,
docs/backlog.md. Never the full design document in later phases.

## Look up only when needed
docs/templates/: gap-checklist.md, spec.md, backlog.md, task.md,
gate-summary.md, handoff.md, status.md. docs/handbook/ only if a
template leaves a question open.

## Phases by project class
S: Plan (design + spec + architecture, one gate) -> blocks of at most
   5 tasks -> Release (gate 3). The SP writes the architecture as a
   subagent in the Plan thread; no QA review of the architecture.
M, L: Design (gate 1) -> Architecture (SP proposes, QA reviews,
   gate 2) -> blocks -> Release (gate 3).

## Outputs
docs/spec.md, docs/backlog.md, docs/status.md, task briefs in
docs/tasks/, German gate summaries.

## Rules
- Talk to the human in German. All files except design.md in English.
- Gap analysis: max 5 bundled questions per round, contradictions
  first. Deployment, target devices, manual tester and "personal data
  yes/no" are decided by the human before the first gate. Never
  decide whether data is personal.
- Each task brief: goal, acceptance criteria, affected files, out of
  scope, dependencies, QA level (A/B/C) and concrete QA check
  criteria. Must fit one SP thread.
- The last backlog task is always REL (release preparation).
- Collect QA hints without findings; plan them as one hardening task
  from 5 hints or before REL.
- Start SP and QA as fresh subagents with only the task brief.
- Stop and ask the human at every gate, on escalations and when the
  SP marks a change "touches gate". Only an explicit approval counts.
- Before merging: update backlog and status on the task branch, check
  CI once (no polling; no CI needed for doc-only branches), note it in
  the handoff. Then squash-merge: one commit per task on main.
- Phase work lives on branch PLAN, DESIGN, ARCH or REL and is merged
  after the gate. Never commit directly to main.

## Cost rules
- One PO thread per phase or block. Then push, hand off and end.
- Context budget about a quarter of the context window.
- Keep docs/status.md under 100 lines; move handoffs older than the
  last five to docs/status-archive.md.
- Never poll CI. Write the expected end time into status.md and stop.

## Must not
Write code. Approve gates. Change scope without updating design.md.
Add roles (that is the Coordinator's job, and never in class S).

## Handoff
docs/templates/handoff.md format, short, with references to files.

## Escalation
After 2 failed SP/QA cycles on one task: analyse, re-scope or ask
the human.
```

**SP – `docs/roles/sp.md`**

```markdown
# Role: Senior Programmer (SP)
Grundformel version: 1.6

## Mission
Propose the architecture, fill the stack profile, then implement
exactly one task per thread with tests.

## Inputs (read at thread start)
CLAUDE.md, the task brief (docs/tasks/T<NNN>.md) or the architecture
request, docs/architecture.md, docs/stack-profile.md, and only the
files the task affects.

## Look up only when needed
docs/templates/: architecture.md, stack-profile.md, decision.md,
changelog.md, manual-test.md (task REL), handoff.md.

## Outputs
Code and tests on a task branch, commits, updated architecture,
decision log, changelog and CLAUDE.md where affected, handoff note.

## Rules
- Plan before coding, then implement in one go.
- One feature = one module. Small core. Features talk only through
  defined interfaces. Central feature registration.
- Everything external behind an adapter (files, clock, network, DB).
  Domain logic has no infrastructure dependencies.
- Config outside code, validated at startup. Validate all input at
  system boundaries, including AI output. Never swallow errors.
  Structured logging, no secrets or personal data in logs.
- Timeouts, bounded retries and defined failure behaviour for
  external calls.
- Hot paths (see architecture): direct code allowed, measure first.
- Every bug fix starts with a failing test.
- Before adding a library: check that it exists, is widely used and
  maintained. Install only via the official package manager, pinned.
  Pin CI actions to a commit SHA.
- Security-relevant code gets negative tests. Never pass input to
  eval, exec or a shell.
- Branch per task; task ID in every commit message and PR title.
- Architecture details: change freely, note in architecture.md. A
  change to an approved decision: mark "touches gate" in the handoff.
- The architecture always contains "Gate-relevant decisions" and
  "Removing a feature", in every project class.

## Cost rules
- One thread = one task. Context budget about a quarter of the
  context window; when reached, push, hand off and end.
- Batch related commands into one tool call (format + lint + test).
- Quiet output only: tests in quiet mode, logs shortened, search
  files instead of opening them whole.
- Staged tests: affected area while working, full suite once before
  the handoff. Then CI is the proof.
- Never poll CI. After 2 failed attempts on one problem, stop.

## Must not
Expand scope. Change tested code outside the task. Merge to main.
Commit secrets. Use real personal data. Run irreversible actions.

## Handoff
Push the branch, then a handoff note (docs/templates/handoff.md)
addressed to QA.

## Escalation
After 2 failed attempts on one problem: stop, write a root-cause
analysis and hand it to the PO.
```

**QA – `docs/roles/qa.md`**

```markdown
# Role: Quality Assurance (QA)
Grundformel version: 1.6

## Mission
Verify one task per thread independently. You never see the SP's
session. In class M and L, also review the architecture proposal
before gate 2; in every class, review a change marked "touches gate"
as part of that task.

## Inputs (read at thread start)
CLAUDE.md, the task brief with acceptance criteria, QA level and
check criteria, the diff, docs/stack-profile.md, the related tests.

## Look up only when needed
docs/spec.md (only the referenced criteria), docs/architecture.md,
docs/templates/task.md.

## Outputs
PASS, or a findings list: severity, location, expected vs. actual,
affected criterion. Hints without findings go to a separate list.
Write the result into the "Result" section of the task brief.

## Rules
- Check at the level the brief sets:
  A: CI green, read the diff.
  B (default): targeted probes - edge cases, mutations, actually
     remove the feature, rulebook compliance, security.
  C: as B, plus a fresh clone, full suite and end-to-end tests.
- Do not rerun the full suite at levels A and B; CI is the proof.
- Red CI means no PASS.

## Cost rules
- One thread = one task. Quiet output only. Never poll CI.

## Must not
Fix code. Weaken acceptance criteria. Pass with failing checks.

## Handoff
Push the result, then a handoff note addressed to the PO.

## Escalation
If acceptance criteria are unclear or contradictory: report to PO,
do not interpret.
```

**Koordinator – `docs/roles/coordinator.md`**

Für spätere Einsätze als Schnittstelle nach außen. Der Koordinator ist die einzige Rolle, die Zugänge anfordert (Ordner, Repositories, Konnektoren, Rechte) und neue Rollen anlegt.

```markdown
# Role: Coordinator
Grundformel version: 1.6

## Mission
Set up projects from the template repository and act as the external
interface: request access, add roles (class M and L only), connect
external systems, propose changes to the Grundformel.

## Inputs (read at thread start)
CLAUDE.md, docs/status.md, the request.

## Look up only when needed
docs/grundformel.md, docs/templates/role.md, decision.md,
coordinator-check.md, docs/handbook/08-adapter.md.

## Outputs
New or changed role files, decision log entries, change proposals
for the Grundformel (German, for the human).

## Cost rules
- One thread = one request. Push, hand off and end.

## Must not
Write application code. Make product decisions. Change the
Grundformel without human approval. Grant rights without human
approval.

## Handoff / Escalation
Handoff note to the PO in docs/status.md. Anything outside the
Grundformel goes to the human.
```

## 6. Übergabeformat zwischen Rollen

Jede Übergabe wird oben in `docs/status.md` eingetragen, neueste zuerst. So kann die nächste Rolle kalt starten. Übergaben sind kurz und verweisen auf Dateien, statt Inhalte zu wiederholen. Es bleiben nur die letzten fünf in `status.md`; ältere verschiebt der PO nach `docs/status-archive.md`. Geschrieben wird die Übergabe erst, wenn die Arbeit gepusht ist.

```markdown
### 2026-11-01 · T042 · Export as CSV
From: SP → To: QA
Done: CSV export, feature flag `export_csv`. Details: docs/tasks/T042.md
Branch: feature/T042-export (pushed)
Changed files: src/features/export/*, tests/features/export/*
Touches gate: no
Open issues: none
Next step: QA level B, criteria F03-AC1 to F03-AC3
```

## 7. Vorlage Stack-Profil

Die Datei liegt leer im Vorlagen-Repository; der SP füllt sie mit der Architektur. Jeder Eintrag ist eine konkrete Festlegung, keine Absicht.

```markdown
# Stack Profile

## Basics
- Language and version:
- Framework(s):
- Package manager, lockfile:

## Commands
- Install:
- Run:
- Test (quiet mode, affected area):
- Test (full suite):
- Lint / format / type check (one command):
- Build:

## Code style
- Formatter and config file:
- Linter and rule set:
- Type checking mode:
- Naming conventions:

## Structure
- Folder layout (core, features, adapters, tests):
- How a feature module is registered:
- How feature flags are read:

## Patterns
- Error handling and error types:
- Logging library and format:
- Config loading and validation:

## Testing
- Test framework:
- Unit / integration / end-to-end locations:
- How external services are faked:

## Dependencies
- Approved libraries:
- Rule for adding a new library:

## Tooling
- Test filter hook: interpreter command, test runners it covers:

## Performance (if critical)
- Hot paths:
- Targets:
- Benchmark and profiling tools:
```

## 8. Adapter: Claude Code und Claude-App

Die Bibel läuft in zwei Oberflächen derselben Technik: **Claude Code** (Terminal oder Bereich „Code“ der Desktop-App, mit einem Ordner auf deinem Rechner) und den **Threads in Projekten der Claude-App** (Arbeitsumgebung in der Cloud, Zugriff auf das Repository über GitHub). Beide lesen `CLAUDE.md`, die Subagenten in `.claude/agents/` und die Einstellungen in `.claude/settings.json`. Syntax und Optionen vor dem ersten Einsatz mit der aktuellen Dokumentation abgleichen, da sich Details ändern.

**Gemeinsam für beide**

In jeder Oberfläche ist die Hauptsitzung des Threads der PO; SP und QA laufen als Subagenten mit eigenem, frischem Kontext. Zum PO kommt nur ihre Abschlussmeldung zurück, nicht ihr Arbeitsverlauf. Die Rollendateien bleiben die einzige Quelle in `docs/roles/`; die Subagenten-Dateien verweisen nur darauf.

| Grundformel | Umsetzung |
| --- | --- |
| Kontextdatei | `CLAUDE.md` im Projektwurzelverzeichnis, wird automatisch geladen |
| Kurzlebiger PO-Thread | Pro Phase bzw. Block eine neue Sitzung (neuer Thread) |
| SP, QA pro Aufgabe | Jeder Subagent-Aufruf ist ein eigener, frischer Thread; pro Aufgabe ein neuer Aufruf |
| Stärkstes Modell, fest | `"model": "opus"` in `.claude/settings.json`, `model: opus` in jedem Subagenten |
| Kontext-Budget | Kontextanzeige der Sitzung beachten; bei etwa einem Viertel übergeben |
| Plan vor Umsetzung | Plan-Modus |
| Verbotene Aktionen technisch absichern | Berechtigungsregeln in `.claude/settings.json` |
| Keine CI für reine Doku | `paths-ignore` im CI-Workflow |
| Kein Gedächtnis neben den Projektdateien | `"autoMemoryEnabled": false` in `.claude/settings.json` |
| Kleine Testausgaben, technisch abgesichert | Hook `.claude/hooks/quiet_tests.py` vor jedem Shell-Befehl |

**Claude Code (Terminal oder Bereich „Code“ der Desktop-App)**

- Neue Sitzung pro Phase: im Terminal `claude` im Projektordner, in der Desktop-App **+ New** und den Projektordner wählen.
- Das Projekt liegt in einem Ordner auf deinem Rechner. Ein Push nach jeder Übergabe ist trotzdem Pflicht (Grundformel §3 und §11).
- Berechtigungsmodus: „Auto“ bzw. „Accept edits“; nie „Bypass permissions“.

**Threads in Projekten der Claude-App**

- **Ein App-Projekt pro Bibel-Projekt.** Die Projektanweisungen enthalten nur: Name des Repositorys, „Read CLAUDE.md first“ und den Hinweis auf die Startprompts. Keine Regeln, keine Bibel-Texte.
- **Der Koordinator ist das Fenster nach außen.** Er fordert Zugänge an (Repository, Ordner auf deinem Rechner, Konnektoren). Diese Freigaben gelten aber nur für den Thread, in dem sie erteilt werden.
- **Deshalb holt sich jeder Thread den Zugriff auf das Repository selbst.** Die erste Zeile jedes Startprompts nennt das Repository (§18); der Thread verbindet es, bevor er etwas anderes tut.
- **Die Arbeitsumgebung eines Threads ist vorübergehend.** Was nicht gepusht ist, geht mit dem Thread verloren. Die Hauptquelle ist das Repository auf GitHub, nicht ein lokaler Ordner.
- **Modell:** Die Modellauswahl des Threads auf das stärkste Modell stellen. Die Subagenten nehmen ihr Modell aus `.claude/agents/`.
- **Verbrauch:** Die App zeigt keinen Verbrauch pro Thread. Gemessen wird von außen (Grundformel §13).

**Ersetzt den Abschnitt „Roles“ der Vorlage in `CLAUDE.md`** (im Vorlagen-Repository bereits so eingetragen)

```markdown
## Roles
The main session of a thread acts as PO: read and follow
docs/roles/po.md. SP and QA are subagents (.claude/agents/sp.md,
.claude/agents/qa.md). Delegate each task to a fresh subagent call
with the task brief. Never do SP or QA work in the main session.
```

**Subagent `.claude/agents/sp.md`**

```markdown
---
name: sp
description: Senior Programmer. Use for an architecture proposal or for
  implementing exactly one backlog task with tests.
model: opus
---
Read and follow docs/roles/sp.md. Read CLAUDE.md, docs/stack-profile.md
and the task brief you received; nothing else unless the task needs
it. Push your branch before you finish. End with a handoff note and a
summary of at most 10 lines; do not repeat file contents.
```

**Subagent `.claude/agents/qa.md`**

```markdown
---
name: qa
description: Quality Assurance. Use to verify exactly one backlog task
  against its acceptance criteria, or to review an architecture
  proposal or a change marked "touches gate".
model: opus
---
Read and follow docs/roles/qa.md. Read CLAUDE.md, docs/stack-profile.md
and the task brief you received; nothing else unless the check needs
it. You never see the SP's session. Push the result before you finish.
End with PASS or a findings list of at most 15 lines.
```

**Technische Absicherung (`.claude/settings.json`)**

Das Modell steht fest in den Einstellungen, damit es nicht von einer Voreinstellung des Werkzeugs abhängt. Die automatische Gedächtnisfunktion ist abgeschaltet (Grundformel §5). Regeln wie „kein Force-Push“ oder „keine Secrets lesen“ werden zusätzlich technisch gesperrt. `.env.example` bleibt lesbar, weil sie keine Werte enthält; Sperrregeln haben Vorrang vor Erlaubnisregeln, deshalb werden die echten Dateien einzeln gesperrt.

```json
{
  "model": "opus",
  "autoMemoryEnabled": false,
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/quiet_tests.py"]
          }
        ]
      }
    ]
  },
  "permissions": {
    "deny": [
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Read(./.env)",
      "Read(./.env.local)",
      "Read(./.env.*.local)",
      "Read(./.env.production)",
      "Read(./secrets/**)"
    ]
  }
}
```

**Keine CI für reine Doku (Beispiel GitHub Actions)**

```yaml
on:
  push:
    paths-ignore:
      - "docs/**"
      - "*.md"
  pull_request:
    paths-ignore:
      - "docs/**"
      - "*.md"
```

Fremde Actions werden immer mit Commit-SHA eingebunden, z. B. `uses: actions/checkout@<commit-sha>  # v4` (Grundformel §12).

**Hook für knappe Testausgaben (`.claude/hooks/`)**

Vor jedem Shell-Befehl prüft `quiet_tests.py`, ob ein Testlauf gestartet wird. Wenn ja, leitet es die Ausgabe durch `test_filter.py`: Übrig bleiben Fehlerzeilen mit etwas Umgebung und die Zusammenfassung am Ende, höchstens 150 Zeilen. Der Exit-Code des Tests bleibt erhalten. Der Hook braucht Python 3 und ist für Windows eingestellt (Befehl `python`). Unter macOS und Linux trägt der SP `python3` ein; fehlt Python oder nutzt das Projekt einen Testbefehl, den der Hook nicht kennt, passt der SP ihn an und vermerkt das im Stack-Profil.

```python
"""PreToolUse hook: pipe test runs through test_filter.py so only failures and the summary reach the context."""
import json
import re
import sys
from pathlib import Path

TEST_RUNNER = re.compile(
    r"^\s*(python3? -m pytest|pytest|npm (run )?test|pnpm test|yarn test|go test"
    r"|cargo test|dotnet test|mvn( -q)? test|\./gradlew test|gradle test)\b"
)


def main() -> None:
    data = json.load(sys.stdin)
    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")
    if not TEST_RUNNER.match(command) or "test_filter.py" in command:
        print("{}")
        return
    python = Path(sys.executable).as_posix()
    filter_script = (Path(__file__).parent / "test_filter.py").as_posix()
    wrapped = f'set -o pipefail; ( {command} ) 2>&1 | "{python}" "{filter_script}"'
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "updatedInput": {**tool_input, "command": wrapped},
    }}))


if __name__ == "__main__":
    main()
```

```python
"""Reduce test output to failure lines (with a little context) and the closing summary."""
import re
import sys

SIGNAL = re.compile(r"FAIL|ERROR|Error|error:|Traceback|Exception|assert|panic", re.I)
CONTEXT, TAIL, LIMIT = 3, 15, 150


def main() -> None:
    lines = sys.stdin.read().splitlines()
    keep: set[int] = set(range(max(0, len(lines) - TAIL), len(lines)))
    for i, line in enumerate(lines):
        if SIGNAL.search(line):
            keep.update(range(max(0, i - 1), min(len(lines), i + CONTEXT + 1)))
    out, last = [], -1
    for i in sorted(keep):
        if i != last + 1:
            out.append("...")
        out.append(lines[i])
        last = i
    if len(out) > LIMIT:
        out = out[: LIMIT - TAIL] + ["... (shortened)"] + out[-TAIL:]
    print("\n".join(out))


if __name__ == "__main__":
    main()
```

## 9. Vorlage CLAUDE.md

Die Kontextdatei wird in jeder Sitzung geladen und muss deshalb kurz bleiben (Richtwert unter 100 Zeilen). Sie enthält nur Projektspezifisches; alle allgemeinen Regeln stehen in der Grundformel und den Rollendateien. Felder mit `<at setup>` füllt der Koordinator, Felder mit `<after architecture>` der SP.

```markdown
# <Project name>  <at setup>
Grundformel version: <x.y> · Binding rules: docs/grundformel.md
Project class: <S | M | L>  <at setup>

## Purpose  <at setup>
<One or two sentences from design.md section 1.>

## Roles
The main session of a thread acts as PO: read and follow
docs/roles/po.md. SP and QA are subagents (.claude/agents/sp.md,
.claude/agents/qa.md). Delegate each task to a fresh subagent call
with the task brief. Never do SP or QA work in the main session.

## Start of every thread
1. Read docs/status.md (not the archive).
2. Read your role file in docs/roles/.
3. Read your task brief in docs/tasks/ (SP, QA).
4. Read only the files the task needs. docs/handbook/ and
   docs/grundformel.md only when a question is not answered by your
   role file or a template.
A thread does one unit of work, pushes, hands off and ends.

## Commands  <after architecture>
- Install:
- Run:
- Test (quiet, affected area):
- Test (full suite):
- Lint / format / type check:
- Build:

## Structure  <after architecture>
- src/core/       config, logging, errors, feature registry
- src/features/   one folder per feature
- src/adapters/   everything external
- tests/          mirrors src/
- docs/           project memory

## Project-specific rules
- <Only rules that are not in the Grundformel. Empty is fine.>

## Never
- Commit secrets or read .env files.
- Use real personal data outside production.
- Commit directly to main or force-push. Only the PO squash-merges
  a task branch into main, after QA PASS and green CI.
- Delete data, deploy or migrate production without human approval.
- Poll CI or other running jobs in a loop.
- End a thread with unpushed work.
```

## 10. Vorlage Spezifikation

Die Spezifikation übersetzt das Designdokument in prüfbare Anforderungen. Jedes Akzeptanzkriterium hat eine eindeutige ID (z. B. `F03-AC2`), die in Aufgaben, Tests und QA-Berichten wiederkehrt. So ist jede Codezeile auf eine freigegebene Anforderung rückführbar.

**Regeln für Akzeptanzkriterien**

- Immer im Muster *Given – When – Then* (Ausgangslage – Aktion – erwartetes Ergebnis).
- Ein Kriterium prüft genau eine Sache.
- Keine weichen Wörter wie „schnell“, „einfach“, „benutzerfreundlich“. Stattdessen Zahlen oder eindeutig prüfbare Ergebnisse.
- Jedes Kriterium muss als automatischer Test formulierbar sein. Geht das nicht, wird es als „manuell geprüft“ markiert und begründet.

```markdown
# Specification
Version: <x.y> · Based on design.md version <x.y>
Status: Draft | Approved (gate <n>, <date>)

## Release scope (MVP)
| Feature | Title | Priority | Feature flag |
| --- | --- | --- | --- |
| F01 | <title> | Must | no |

## Requirements

### F01 – <title>
User story: As <user> I want <goal> so that <benefit>.

Acceptance criteria:
- F01-AC1: Given <situation>, when <action>, then <result>.
- F01-AC2: Given ..., when ..., then ...

Edge cases:
- <empty input, missing data, external service down, ...>

## Non-functional requirements
- NFR-1 Performance: <measurable target, or "not critical">
- NFR-2 Availability: <...>
- NFR-3 Security / privacy: <...>

## Delivery
- Deployment: <how the product reaches the user>
- Target devices: <...>
- Manual tester: <who, operating system, knowledge level>

## Out of scope
- <copied from design.md non-goals, plus anything deferred>
```

## 11. Vorlage Backlog und Aufgaben-Brief

Das Backlog ist nur eine Übersichtstabelle. Jede Aufgabe hat zusätzlich einen eigenen Brief in `docs/tasks/T042.md`. So lädt der SP nur seine eine Aufgabe statt des ganzen Backlogs.

**`docs/backlog.md`**

```markdown
# Backlog
Status values: todo | in progress | in review | done | blocked

| ID | Title | Feature | QA | Status | Depends on |
| --- | --- | --- | --- | --- | --- |
| T001 | <title> | F01 | B | todo | – |
| REL | Release preparation | – | C | todo | all |

## Hardening queue
QA hints without findings. Plan as one task from 5 entries or before REL.
- <hint> – from T0xx
```

**`docs/tasks/T042.md`**

```markdown
# T042 – <title>
Feature: F03 · QA level: A | B | C

## Goal
<One sentence.>

## Acceptance criteria (verbatim from spec)
- F03-AC1: Given ..., when ..., then ...
- F03-AC2: Given ..., when ..., then ...

## QA check criteria
- <concrete probes, e.g. "actually remove the feature and run tests",
  "guard rejects calls without type information">

## Affected modules / files
- <path>

## Out of scope
- <what must NOT be touched or added>

## Depends on
- <task IDs, or none>

## Notes for SP
- <constraints from architecture or decisions; no ad-hoc solutions>

## Result (filled by QA)
PASS | FINDINGS – <date>
```

**Feste letzte Aufgabe `REL` (Release-Vorbereitung)**

- Versionsnummer setzen, Changelog-Eintrag schreiben.
- Rückfallplan: wie die vorherige Version wiederhergestellt wird.
- `docs/manual-test.md` nach Vorlage §20 für die in der Spezifikation genannte Person schreiben.
- QA-Stufe C.

**Regeln für den PO beim Erstellen eines Briefs**

- Akzeptanzkriterien werden wörtlich aus der Spezifikation kopiert, nie umformuliert.
- „Out of scope“ ist nie leer. Mindestens die naheliegendste Erweiterung wird ausgeschlossen.
- Die QA-Prüfkriterien sind konkret. Sie stehen schon im Brief, damit der SP sie kennt und die erste Runde besteht.
- Passt die Aufgabe nicht in einen SP-Thread, wird sie geteilt, bevor sie an den SP geht. Ist sie so klein, dass der Grundaufwand überwiegt, wird sie mit einer verwandten Aufgabe zusammengelegt.
- In Klasse S werden Themen optionaler Rollen (z. B. Sicherheit, Performance) als Prüfpunkte in die QA-Prüfkriterien geschrieben.

## 12. Vorlage Architektur

Die Architektur ist die Grundlage für die Freigabe der Architektur (in Klasse S Teil der einzigen Freigabe vor dem Bau). Pflicht ist in jeder Klasse vor allem die Entfernungsanleitung: Sie beweist schon vor dem Bau, dass jedes Feature später ohne Folgeschäden entfernt werden kann. Der Abschnitt „Gate-relevant decisions“ legt fest, welche Änderungen später als „berührt Freigabe“ gelten. In Klasse S genügen Overview, Gate-relevant decisions, Features, Adapters und Removing a feature; die übrigen Abschnitte dürfen „not needed“ sein.

```markdown
# Architecture
Version: <x.y> · Status: Draft | Approved (gate <n>, <date>)

## Overview
<Three sentences and one diagram: core, features, adapters.>

## Gate-relevant decisions
Changing any of these needs QA review and a new approval:
- Technology and frameworks: <...>
- Module boundaries and external interfaces: <...>
- Data model: <...>
- Security concept: <...>
Everything else is a detail the SP may change and note here.

## Core
- Config: <how loaded and validated at startup>
- Logging: <format, levels>
- Errors: <error types, how propagated>
- Feature registry: <where and how features are registered>

## Features
| Feature | Module | Public interface | Flag | Depends on |
| --- | --- | --- | --- | --- |
| F01 | src/features/<name> | <functions/events> | no | core |

## Adapters
| External system | Adapter | Timeout | Retries | Failure behaviour |
| --- | --- | --- | --- | --- |

## Data model and migrations
<Entities, ownership per feature, migration tool.>

## Communication between features
<Interfaces or events only; list them.>

## Hot paths and performance
<List with targets from NFRs, or "none".>

## Security
<Authentication, roles, secret handling, personal data flow.>

## Removing a feature
1. Remove its registration in <file>.
2. Delete src/features/<name> and tests/features/<name>.
3. Run migration <...> to archive or drop its data.
4. All tests green = removal complete.

## Change log of details
- <date> · <task> · <detail change>

## Open risks
- <risk, impact, mitigation>
```

## 13. Vorlage Entscheidungslog

Eine Datei pro Entscheidung, fortlaufend nummeriert (`docs/decisions/0001-<titel>.md`). Entscheidungen werden nie gelöscht oder umgeschrieben; eine neue Entscheidung ersetzt eine alte und verweist auf sie. So bleibt nachvollziehbar, warum etwas so gebaut wurde, auch nach einem Jahr.

**Pflicht für einen Eintrag:** Wahl von Technologie oder Bibliothek, Abweichung von einer SOLL-Regel, inkompatible Schnittstellenänderung, Optimierung zulasten der Lesbarkeit, zusätzliche Rolle, Änderung der Projektklasse.

```markdown
# 0007 – <Decision title>
Date: <YYYY-MM-DD> · Status: proposed | accepted | superseded by 0012
Author role: SP | PO | Coordinator

## Context
<What problem forced a decision? Constraints?>

## Decision
<What was decided, in one or two sentences.>

## Alternatives considered
- <option> – rejected because <reason>

## Consequences
<What becomes easier, what becomes harder, what to watch.>
```

## 14. Vorlagen Status, Changelog, .env.example, .gitignore

**`docs/status.md`** – höchstens 100 Zeilen: Kopf mit aktuellem Stand und die letzten fünf Übergaben (Format aus Abschnitt 6). Ältere Übergaben verschiebt der PO nach `docs/status-archive.md`, das beim Start niemand liest.

```markdown
# Status
Phase: Plan | Design | Architecture | Implementation (block n) | Release
Current task: –
Waiting for: – (e.g. "CI of T042, expected 14:20")
Blocked: –
Next step: PO starts the gap analysis of design.md with the human.

## Handoffs (newest first, max. 5; older ones in status-archive.md)
```

**`CHANGELOG.md`** – nach dem verbreiteten Format „Keep a Changelog“.

```markdown
# Changelog

## [Unreleased]
### Added
### Changed
### Removed
### Fixed
```

**`.env.example`** – jede Variable, die das Programm braucht, mit Kommentar, aber ohne echten Wert.

```text
# Copy to .env and fill in. Never commit .env.
# Every variable the app reads must be listed here.
APP_ENV=development
# EXAMPLE_API_KEY=   # where to get it, who owns it
```

**`.gitignore`** – Grundausstattung ab dem ersten Commit; der SP ergänzt Stack-Spezifisches.

```text
# Secrets
.env
.env.*
!.env.example

# Build output, logs, local data
dist/
build/
*.log
data/local/

# OS and editor files
.DS_Store
Thumbs.db
.vscode/
.idea/

# Claude Code local settings
.claude/settings.local.json
```

## 15. Vorlage Freigabe-Zusammenfassung

An jedem Freigabepunkt legt der PO dir eine Zusammenfassung auf Deutsch vor. Sie muss ohne Lesen der Projektdateien verständlich sein und endet immer mit genau drei Antwortmöglichkeiten. Eine Freigabe gilt nur, wenn du sie ausdrücklich erteilst; Schweigen ist keine Freigabe.

```markdown
# Freigabe <1 | 2 | 3>: <Projekt> – <Datum>

## Worum es geht
<Maximal drei Sätze.>

## Was du entscheidest
<Eine konkrete Frage.>

## Die wichtigsten Punkte
- <Punkt, in Alltagssprache>

## Risiken und offene Fragen
- <Risiko – was passiert, wenn es eintritt – Gegenmaßnahme>

## Was nach der Freigabe passiert
<Nächste Schritte, ab wann du wieder gefragt wirst.>

## Deine Antwort
- Freigeben
- Freigeben mit Auflagen: <welche>
- Zurück an <Rolle>, weil: <Grund>
```

**Zusätzlich bei der ersten Freigabe:** Projektklasse, Bereitstellung, Zielgeräte, die Person der manuellen Prüfung und „personenbezogene Daten ja/nein“ sind genannt. In Klasse S fasst sie zusätzlich die Architektur in Alltagssprache zusammen: Aufteilung in Module, was später leicht änderbar ist und wie ein Feature entfernt wird.

**Zusätzlich bei Freigabe 3 (Release)**

- Alle Aufgaben des Releases auf „done“, einschließlich `REL`; alle Tests grün, QA bestanden.
- Bekannte Fehler mit Auswirkung.
- Changelog-Eintrag und neue Versionsnummer.
- `docs/manual-test.md` liegt vor und ist für die genannte Person verständlich.
- Sicherung der Daten vor jeder Migration, mit Ort der Sicherung.
- Rückfallplan: wie die vorherige Version wiederhergestellt wird.

Die erteilte Freigabe trägt der PO mit Datum in die freigegebene Datei (Designdokument, Spezifikation, Architektur) bzw. ins Changelog ein.

## 16. Abnahme-Checkliste des Koordinators

Bevor der Koordinator übergibt, prüft er jeden Punkt selbst und meldet das Ergebnis in seiner Zusammenfassung. Ein nicht erfüllter Punkt wird behoben oder als offene Frage gemeldet, nie übergangen.

```markdown
## Coordinator acceptance check
- [ ] Repository created from the template repository (not copied
      by hand), private, initial commit on main, push verified
- [ ] CLAUDE.md: project name, purpose, project class and Grundformel
      version filled in; under 100 lines
- [ ] docs/design.md holds the design document with unchanged
      wording, or the template header with name and class
- [ ] Project class matches the conditions in docs/grundformel.md §4
- [ ] Class S: no additional roles. Class M/L: each additional role
      has a role file and a decision log entry
- [ ] .claude/settings.json sets the model, turns auto memory off,
      registers the test filter hook and the deny rules;
      .claude/agents/ contains sp.md and qa.md, .claude/hooks/ both
      hook scripts
- [ ] No secrets anywhere in the repository
- [ ] Handoff note to the PO in docs/status.md
- [ ] German summary for the human: repository, class, roles, open
      questions, result of this check
```

## 17. Vorlagen-Verzeichnis

Jede Vorlage liegt unter genau diesem Namen in `docs/templates/` des Vorlagen-Repositorys. Rollendateien verweisen nur auf Dateien im Projekt, nie auf Abschnitte von Teil 2.

| Datei in `docs/templates/` | Quelle in Teil 2 | Sprache | Genutzt von |
| --- | --- | --- | --- |
| `design.md` | §2 | Deutsch | PO |
| `gap-checklist.md` | §3 | Deutsch | PO |
| `role.md` | §5 Gerüst | Englisch | Koordinator |
| `handoff.md` | §6 | Englisch | Alle Rollen |
| `stack-profile.md` | §7 | Englisch | SP |
| `claude-md.md` | §9 | Englisch | Koordinator |
| `spec.md` | §10 | Englisch | PO |
| `backlog.md` | §11 | Englisch | PO |
| `task.md` | §11 | Englisch | PO, QA |
| `architecture.md` | §12 | Englisch | SP |
| `decision.md` | §13 | Englisch | SP, PO, Koordinator |
| `status.md` | §14 | Englisch | PO |
| `changelog.md` | §14 | Englisch | SP |
| `env-example.txt` | §14 | Englisch | SP |
| `gitignore.txt` | §14 | Englisch | SP |
| `gate-summary.md` | §15 | Deutsch | PO |
| `coordinator-check.md` | §16 | Englisch | Koordinator |
| `thread-start.md` | §18 | Englisch | Mensch |
| `manual-test.md` | §20 | Sprache der prüfenden Person | SP (Aufgabe `REL`) |

## 18. Startprompts für Rollen-Threads

Jeder neue Thread beginnt mit dem Startprompt seiner Rolle (Grundformel §3). Die erste Zeile nennt Repository, Projekt, Rolle und Arbeitseinheit; so holt sich der Thread in der Claude-App zuerst den Zugriff (§8), und jeder Thread erkennt sofort, wenn ein Auftrag im falschen Thread landet. Jeder Thread endet nach Push und Übergabe. Für den allerersten Projektstart gilt der Koordinator-Startprompt aus §4. SP und QA startet der PO als Subagenten; eigene Threads für sie öffnest du nur, wenn das Werkzeug keine Subagenten hat.

**Thread-Namen:** `<Projekt> · Koordinator · <Auftrag>`, `<Projekt> · PO · <Phase>`, `<Projekt> · SP · T042`, `<Projekt> · QA · T042`.

**PO** (neuer Thread pro Phase bzw. Block)

```text
Repository: <owner>/<name> · Project: <name> · Role: PO
Phase: <Plan | Design | Architecture | Block n | Release>
If the repository is not available in this thread, connect it first.
You are the Product Owner of this project. Work only in this role
and only on this phase.
Read CLAUDE.md, docs/status.md and docs/roles/po.md, nothing else
yet. Then tell me in German where the project stands and what you
need from me.
When the phase is done or your context budget is reached, push,
write a handoff in docs/status.md and end this thread.
If a request belongs to another role or another project, do not
carry it out; tell me which thread it belongs in.
```

**SP** (nur ohne Subagenten: neuer Thread pro Aufgabe)

```text
Repository: <owner>/<name> · Project: <name> · Role: SP · Task: <T042>
If the repository is not available in this thread, connect it first.
You are the Senior Programmer of this project. Work only in this
role and only on task <T042>.
Read CLAUDE.md, docs/roles/sp.md, docs/stack-profile.md and
docs/tasks/<T042>.md, then only the files the task brief names.
Push your branch, write a handoff note in docs/status.md, then end
this thread.
If a request belongs to another role, task or project, do not
carry it out; say which thread it belongs in.
```

**QA** (nur ohne Subagenten: neuer Thread pro Aufgabe, nie der Thread des SP)

```text
Repository: <owner>/<name> · Project: <name> · Role: QA · Task: <T042>
If the repository is not available in this thread, connect it first.
You are QA for this project. Work only in this role and only on
task <T042>. You have not seen the SP's work session.
Read CLAUDE.md, docs/roles/qa.md, docs/stack-profile.md,
docs/tasks/<T042>.md and the diff of branch <branch>. Check at the
QA level the brief sets.
Write PASS or findings into the task brief, push, write a handoff
note to the PO in docs/status.md, then end this thread.
If a request belongs to another role, task or project, do not
carry it out; say which thread it belongs in.
```

**Koordinator** (späterer Einsatz, nicht für den Projektstart)

```text
Repository: <owner>/<name> · Project: <name> · Role: Coordinator
Request: <short title>
If the repository is not available in this thread, connect it first.
You are the Coordinator of this project: the external interface.
Read CLAUDE.md, docs/status.md and docs/roles/coordinator.md. Then
carry out my request (access, new role, external system, change
proposal for the Grundformel).
Do not write application code. Push, hand off and end this thread.
If a request belongs to another role or project, do not carry it
out; say which thread it belongs in.
```

## 19. Nachschlagen im Handbuch

Jedes Kapitel von Teil 2 liegt im Vorlagen-Repository als eigene Datei in `docs/handbook/`. Beim Thread-Start liest **keine** Rolle ein Kapitel. Was sie bei jedem Schritt braucht, steht in ihrer Rollendatei; die Vorlagen in `docs/templates/` genügen für fast alles andere. Ein Kapitel wird nur gezielt geöffnet, wenn eine Frage weder Rollendatei noch Vorlage beantwortet. Die Tabelle zeigt, wer welches Kapitel typischerweise nachschlägt.

| Kapitel | Datei in `docs/handbook/` | Schlägt nach |
| --- | --- | --- |
| §1 Regeln Designdokument | `01-design-rules.md` | PO |
| §2 Vorlage Designdokument | `02-design-template.md` | PO |
| §3 Checkliste Lückenanalyse | `03-gap-checklist.md` | PO |
| §4 Startprompt Koordinator | `04-coordinator-start.md` | Mensch |
| §5 Rollendateien | `05-role-files.md` | Koordinator |
| §6 Übergabeformat | `06-handoff.md` | alle |
| §7 Stack-Profil | `07-stack-profile.md` | SP |
| §8 Adapter | `08-adapter.md` | Koordinator, PO |
| §9 CLAUDE.md | `09-claude-md.md` | Koordinator, SP |
| §10 Spezifikation | `10-specification.md` | PO, QA |
| §11 Backlog und Aufgaben-Brief | `11-backlog-and-task.md` | PO, QA |
| §12 Architektur | `12-architecture.md` | SP, QA |
| §13 Entscheidungslog | `13-decision-log.md` | alle |
| §14 Status, Changelog, .env, .gitignore | `14-status-changelog-env.md` | PO, SP |
| §15 Freigabe-Zusammenfassung | `15-gate-summary.md` | PO |
| §16 Abnahme-Checkliste | `16-coordinator-check.md` | Koordinator |
| §17 Vorlagen-Verzeichnis | `17-template-index.md` | Koordinator |
| §18 Thread-Startprompts | `18-thread-start.md` | Mensch |
| §19 Nachschlagen | `19-lookup.md` | Koordinator |
| §20 Anleitung manuelle Prüfung | `20-manual-test.md` | SP (`REL`) |
| §21 Vorlagen-Repository | `21-template-repository.md` | Koordinator |

## 20. Vorlage Anleitung für die manuelle Prüfung

Die Anleitung schreibt der SP in der Aufgabe `REL` für die Person, die in der Spezifikation unter „Delivery“ genannt ist. Zielgruppe ist ausdrücklich ein Nicht-Entwickler: keine Fachbegriffe ohne Erklärung, keine Entwicklerwerkzeuge, jeder Schritt einzeln. Sie ist in der Sprache dieser Person geschrieben.

```markdown
# Manuelle Prüfung: <Projekt> <Version>
Für: <Person> · Dauer: ca. <n> Minuten

## Was du brauchst
- <Gerät, Betriebssystem, Browser, Zugang>

## Starten
### Windows
1. <Schritt, genau so, wie er auf dem Bildschirm aussieht>
### macOS
1. <Schritt>

## Was du siehst und was normal ist
- <Erwartete Warnungen oder Hinweise und warum sie harmlos sind>

## Prüfschritte
| Nr. | Tu das | Erwartet | Ok? |
| --- | --- | --- | --- |
| 1 | <Aktion> | <sichtbares Ergebnis> | ☐ |

## Wenn etwas nicht stimmt
<Was du notierst (Nummer des Schritts, was du gesehen hast) und an wen
du es gibst.>
```

## 21. Vorlagen-Repository

Das Vorlagen-Repository enthält alles Allgemeine eines Projekts fertig, englisch und geprüft. Ein neues Projekt entsteht daraus mit einem Klick („Use this template“ auf GitHub) oder einem Befehl (`gh repo create <owner>/<name> --private --template <owner>/ki-projekt-vorlage`).

```text
ki-projekt-vorlage/
  CLAUDE.md                  context file with <at setup> fields
  CHANGELOG.md
  .env.example
  .gitignore
  .claude/settings.json      model + deny rules
  .claude/agents/sp.md
  .claude/agents/qa.md
  .claude/hooks/             quiet_tests.py, test_filter.py
  docs/grundformel.md        Part 1, German, unchanged
  docs/design.md             design template (German)
  docs/spec.md, backlog.md, architecture.md, stack-profile.md
                             unfilled templates
  docs/status.md             empty status
  docs/status-archive.md
  docs/roles/                po.md, sp.md, qa.md, coordinator.md
  docs/templates/            all templates (names in §17)
  docs/handbook/             every Part 2 chapter as its own file (§19)
  docs/decisions/            empty
  docs/tasks/                empty
```

- **MUSS:** Eine neue Bibel-Version wird zuerst im Vorlagen-Repository umgesetzt und mit der Version getaggt (z. B. `v1.6`). Das PDF der Bibel ist die lesbare Fassung für den Menschen, das Vorlagen-Repository die Fassung für die Rollen. Beide haben immer dieselbe Version.
- **MUSS:** Im Vorlagen-Repository gibt es keinen projektspezifischen Inhalt und keine Secrets.
- **SOLL:** Das Vorlagen-Repository ist auf GitHub als „Template repository“ markiert, damit „Use this template“ verfügbar ist.
