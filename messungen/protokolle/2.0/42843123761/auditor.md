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

{"regeln_erfuellt": 22, "regeln_gesamt": 25, "aufgaben": 7, "erstdurchlauf_prozent": 57, "qa_runden": 11, "echte_befunde": 5, "tests": 358, "ci_gruen": true}