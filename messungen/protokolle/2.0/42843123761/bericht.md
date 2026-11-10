# Prüfbericht Bibel 2.0

Automatischer Referenzlauf 42843123761 · Repository kassenbuch-2-0-42843123761 · 2026-11-10

**Teilbericht:** Der Lauf wurde abgebrochen (Kostenbremse: Projekt-Sitzungen über 20.0 USD).

## 1. Ergebnis

Der Lauf verbrauchte gegenüber der Vorversion Bibel 1.9 etwa 17,7 % mehr Tokens (25.945.593 statt 22.044.086) und etwa 12,8 % mehr Kosten (21,98 statt 19,49 USD). Er wurde von der Kostenbremse (Projekt-Sitzungen über 20,0 USD) abgebrochen: REL2 ist nicht übernommen, die Freigabe 3 für 2.0.0 steht aus. Die Regeltreue ist mit 22 von 25 Regeln gleich geblieben (R13 und R19 nicht erfüllt, R18 nicht prüfbar). Bei der Qualität sind alle 358 Tests und die CI grün, aber der Erstdurchlauf sank von 71 % auf 57 %, und es gab 5 echte Befunde statt 2.

## 2. Kennzahlen

| Kennzahl | Bibel 1.9 | Bibel 2.0 |
| --- | --- | --- |
| Datum | 2026-11-10 | 2026-11-10 |
| Claude-Code-Version | 2.1.321 (Claude Code) | 2.1.322 (Claude Code) |
| Tokens gesamt | 22.044.086 | 25.945.593 |
| Kostenschätzung (USD) | 19,49 | 21,98 |
| davon Koordinator | 0,27 | 0,25 |
| davon PO-Sitzungen (inkl. SP und QA) | 19,21 | 21,73 |
| Schritte | 118 | 112 |
| Aktive Laufzeit | 79 Min. | 91 Min. |
| Limit erreicht | ja, 240 Min. gewartet | ja, 210 Min. gewartet |
| Sitzungen | 7 | 7 |
| Aufgaben | 7 | 7 |
| Erstdurchlauf | 71 % | 57 % |
| QA-Runden | 9 | 11 |
| Echte Befunde | 2 | 5 |
| Rückfragen (davon unvorhergesehen) | 6 (2) | 5 (6) |
| Abgelehnte Berechtigungen | 6 | 3 |
| Regeltreue | 22 / 25 | 22 / 25 |
| Manuelle Prüfung (Minuten) | 8 | – |
| Tests, CI grün | 333, ja | 358, ja |
| Bemerkung | Automatischer Lauf 42722790412 | Abgebrochen: Kostenbremse: Projekt-Sitzungen über 20.0 USD |

Hilfsaufrufe (Entscheider, manuelle Prüfung, Auditor, Bericht) zusätzlich: 1,21 USD, nicht in der Kostenschätzung enthalten.

## 3. Regeltreue und Auswertung

| Kennzahl | Wert | Beleg |
| --- | --- | --- |
| Sitzungen | 7 (1 Koordinator, 6 PO) | lauf.jsonl, 7 verschiedene `session_id` |
| Schritte (num_turns) | 112 | Summe der Zeilen 1–14 |
| Kosten (je Sitzung der letzte Wert) | ca. 21,98 USD | 0,25 + 1,33 + 3,69 + 1,21 + 6,52 + 2,57 + 6,41 |
| Aufgaben | 7 (T001, T002, H001, REL, T003, T004, REL2) | docs/backlog.md |
| Erstdurchlauf | 4 von 7 = 57 % (T002, H001, T003, T004) | docs/tasks/*.md, Abschnitt „Result“ |
| QA-Runden | 11 für Aufgaben (T001 3, REL 2, REL2 2, die übrigen je 1); dazu 1 QA-Prüfung der Änderung 1.1 | docs/tasks/T001.md:72/110/147, REL.md:61/112, REL2.md:58/68 |
| Echte Befunde | 5 (T001: 2, REL: 2, REL2: 1); dazu 6 Befunde aus der Prüfung der Änderung 1.1 | T001.md:75/116, REL.md:63, status.md:51 |
| Abgelehnte Berechtigungen | 3 (alle Bash mit Python-Heredoc) | lauf.jsonl Zeilen 3, 13, 14 |
| Tests | 358 (357 bestanden, 1 übersprungen) | status.md:44 |
| CI | grün: Lauf 42893214103 (aeba598) ohne Fehler, Mutationstest eingeschlossen | status.md:11 |
| Wartezeit durch Nutzungslimit | Lücke von etwa 3,8 Stunden zwischen den Aufrufen 8 und 9 (15:48 bis 19:35) | lauf.jsonl Zeilen 8–9 |
| Offen am Ende | REL2 ist nicht in `main` übernommen, Freigabe 3 für 2.0.0 steht aus | status.md:3–4; `origin/main` = b943049 |

| Regel | Ergebnis | Beleg |
| --- | --- | --- |
| R1 | erfüllt | Setup-Commit 9104b41 ändert nur CLAUDE.md, design.md und status.md (status-archive.md:443ff); settings.json: `"model"`, `autoMemoryEnabled:false`, Test-Hook. Den Diff selbst konnte ich nicht ansehen, weil kein Bash-Zugriff bestand. |
| R2 | erfüllt | gate-plan.md:5 „Klasse S, eine gemeinsame Freigabe“; Architekturvorschlag ohne QA-Prüfung (status-archive.md:459) |
| R3 | erfüllt | lauf.jsonl Zeile 2: „1. Widerspruch: Export gegen Nicht-Ziel N3“ |
| R4 | erfüllt | lauf.jsonl Zeile 3: Antwort nennt „Punkte 2 bis 5“, also 5 Rückfragen |
| R5 | erfüllt | gate-plan.md:12–32 nennt Klasse, Bereitstellung, Prüfperson, „Personenbezogene Daten: nein“ und die Architektur in einfachen Worten |
| R6 | erfüllt | architecture.md:66 „Gate-relevant decisions“, :272 „Removing a feature“ |
| R7 | erfüllt | Alle 7 Briefs haben in Zeile 2 eine QA-Stufe und einen Abschnitt „QA check criteria“ |
| R8 | erfüllt | backlog.md:12: letzte Zeile ist REL2 |
| R9 | erfüllt | Neue PO-Sitzung je Phase bzw. Block (Plan, Block 1 ×3, Change, Block 2); SP und QA laufen als Subagenten |
| R10 | erfüllt | status.md hat 67 Zeilen; status-archive.md ist mit über 40 Übergaben gefüllt |
| R11 | erfüllt | main-Reflog: Setup, Plan, T001/T002/H001 (Fast-Forward), CHANGE (REL steckt darin), T003, T004. Kein direkter Commit auf `main`. |
| R12 | erfüllt | Schalter `export_csv` in config.toml (status-archive.md:257, :111) |
| R13 | nicht erfüllt | Der Diff von T003 berührt zusätzlich core/config.py, `__init__.py`, ci.yml und .gitignore (status-archive.md:119–123) |
| R14 | erfüllt | „Touches gate: yes“ mit QA-Prüfung der Änderung (status-archive.md:150–156); Entscheider antwortet „Freigeben“ (lauf.jsonl Zeile 12) |
| R15 | erfüllt | Kern von T004 liegt in den Adaptern sqlite_store, takeover und entry_rows; dazu kleinere Änderungen in config, context, messages und service (status-archive.md:62–64) |
| R16 | erfüllt | tests/core/test_config.py:43 `test_empty_env_var_is_error`; Sonden „directory as data file, missing folder“ (status-archive.md:207) |
| R17 | erfüllt | tests/perf/test_list_perf.py: lokal 0,91 s, Grenze in der CI 3 s, Ziel 1 s (gate-plan.md:49) |
| R18 | nicht prüfbar | Die Reihenfolge der Commits auf den Aufgaben-Branches war ohne `git log` nicht sichtbar. Der Fix für T001 meldet nur „failed before, passes now“ (status-archive.md:369). |
| R19 | nicht erfüllt | Stufen A/B/C und mutmut als CI-Job sind vorhanden, nur eine Härtungsaufgabe (H001). Aber QA hat bei Stufe B die volle Suite laufen lassen (T002: „259 passed“, H001: „258 passed“, status-archive.md:241/209). |
| R20 | erfüllt | ci.yml:5 `paths-ignore`; PLAN und CHANGE ohne CI-Lauf (status-archive.md:138, :423) |
| R21 | erfüllt | Übergaben vermerken „checked once“ bzw. „not polled“; status.md:4 enthält eine „Waiting for“-Zeile |
| R22 | erfüllt | Alle lokalen Branches zeigen auf denselben Commit wie `origin` (packed-refs, refs/heads = refs/remotes) |
| R23 | erfüllt | manual-test.md: deutsch, Windows 11 und PowerShell, Schritte für Nicht-Entwickler. Die Prüfung durch den Entscheider steht nicht im Protokoll. |
| R24 | erfüllt | Freigabe 1 (lauf.jsonl Zeile 4) und Freigabe 1b (Zeile 12) sind ausdrücklich erteilt. REL und REL2 sind ohne Freigabe 3 nicht übernommen. |
| R25 | erfüllt | Actions per SHA eingebunden (ci.yml:17–18); requirements-dev.txt mit `==`; Negativtests vorhanden; Erlaubnisliste in gate-plan.md:37 |

- **Mutationstest mit mutmut in T001 und REL:** T001 brauchte 4 Zyklen aus SP und QA mit einer Eskalation an den Entscheider. Hinzu kamen 2 REL-Zyklen und jedes Mal ein Umweg über die CI. Belege: status-archive.md:285–393 und :473–503, lauf.jsonl Zeile 5 (949 s, 3,69 USD).
- **Lange PO-Sitzungen mit mehreren Aufgaben und Subagenten:** Sitzung 1acb (T002, H001, REL) kostete 6,52 USD in 600 s. Sitzung 5687 (T003, T004, REL2) kostete 6,41 USD in 31 Schritten. Belege: lauf.jsonl Zeilen 9, 13, 14.
- **Doppelte Release-Vorbereitung und Nacharbeit an der Doku:** REL für 1.0.0 wurde komplett gemacht und dann durch REL2 ersetzt. Dazu kamen drei Commits nur für den Netzwerkpfad (6bd4f86, 40505ba, f376c99) und die Planung der Änderung mit 6 QA-Befunden für 2,57 USD. Belege: backlog.md:16–18, REL2-Reflog, lauf.jsonl Zeile 12.


## 4. Größte Kostentreiber

- **Mutationstest (mutmut) in T001 und REL:** T001 brauchte 4 Zyklen aus Umsetzung und Prüfung mit einer Eskalation an den Entscheider, REL weitere 2 Zyklen, jedes Mal mit Umweg über die CI. Beleg: status-archive.md:285–393 und :473–503; lauf.jsonl Zeile 5 (949 s, 3,69 USD).
- **Lange PO-Sitzungen mit mehreren Aufgaben:** Sitzung 1acb (T002, H001, REL) kostete 6,52 USD in 600 s, Sitzung 5687 (T003, T004, REL2) 6,41 USD in 31 Schritten. Beleg: lauf.jsonl Zeilen 9, 13, 14.
- **Doppelte Release-Vorbereitung und Nacharbeit an der Doku:** REL für 1.0.0 wurde komplett erstellt und dann durch REL2 ersetzt. Dazu kamen drei Commits nur für den Netzwerkpfad (6bd4f86, 40505ba, f376c99) und die Planung der Änderung mit 6 Befunden aus der QA-Prüfung für 2,57 USD. Beleg: backlog.md:16–18; lauf.jsonl Zeile 12.

## 5. Auffälligkeiten

- **Abbruch:** Kostenbremse bei über 20,0 USD für Projekt-Sitzungen. Die Gesamtkosten liegen bei 21,98 USD, zuzüglich 1,21 USD Hilfskosten.
- **Offen am Ende:** REL2 ist nicht in `main` übernommen, Freigabe 3 für 2.0.0 steht aus.
- **Nutzungslimit:** Wartezeit von 210 Minuten (Vorversion: 240 Minuten). Die Lücke liegt zwischen den Aufrufen 8 und 9 (15:48 bis 19:35).
- **Abgelehnte Berechtigungen:** 3, alle für Bash mit Python-Heredoc (lauf.jsonl Zeilen 3, 13, 14). Die Vorversion hatte 6.
- **Rückfragen:** 5, in den Kennzahlen sind 6 als unvorhergesehen geführt (Vorversion: 6, davon 2 unvorhergesehen). Die Zählweise sollte geprüft werden.
- **Änderungswunsch:** wurde gesendet. Die Prüfung der Änderung 1.1 ergab 6 Befunde.
- **Manuelle Prüfung:** nicht erfasst (Vorversion: 8 Minuten). Die Prüfung durch den Entscheider steht nicht im Protokoll.
- **Regeln:** R13 nicht erfüllt (T003 berührt zusätzlich core/config.py, `__init__.py`, ci.yml und .gitignore). R19 nicht erfüllt (QA ließ bei Stufe B die volle Suite laufen). R18 nicht prüfbar (Commit-Reihenfolge ohne `git log` nicht sichtbar).

## 6. Manuelle Prüfung

Nicht durchgeführt.

Die Prüfung lief automatisch. Ein Mensch sollte die Verständlichkeit der Anleitung mit einer 10-Minuten-Stichprobe bestätigen.

## 7. Empfehlungen für die nächste Bibel-Version

1. **Mutationstest in weniger Zyklen abschließen:** Mutmut-Vorgaben und Erwartungen schon im Aufgabenbrief festlegen, damit nicht mehrere Zyklen mit CI-Umweg nötig sind. Befund: T001 brauchte 4 Zyklen, REL 2 (3,69 USD in Sitzung 5).
2. **Release nur einmal vorbereiten:** REL erst starten, wenn Änderungswünsche und Freigaben geklärt sind. Befund: REL wurde durch REL2 ersetzt, dazu 3 Commits nur für den Netzwerkpfad.
3. **Sitzungen früher teilen oder Kostengrenze vorab prüfen:** Befund: Zwei Sitzungen kosteten je über 6 USD, der Lauf endete mit 21,98 USD an der Kostenbremse, bevor REL2 übernommen war.
4. **Regeln R13 und R19 schärfen:** Der Umfang einer Aufgabe soll vor der Übergabe gegen die genannten Dateien geprüft werden. QA soll bei Stufe B nur die gezielten Tests laufen lassen. Befund: R13 und R19 nicht erfüllt (T003; 259 bzw. 258 Tests in T002 und H001).
5. **Nachweisbarkeit verbessern:** Die Commit-Reihenfolge (rot vor grün) und die manuelle Prüfung sollen im Protokoll festgehalten werden. Das Berechtigungsmuster Bash mit Python-Heredoc soll vorab erlaubt oder vermieden werden. Befund: R18 nicht prüfbar, manuelle Prüfung null, 3 abgelehnte Berechtigungen.
