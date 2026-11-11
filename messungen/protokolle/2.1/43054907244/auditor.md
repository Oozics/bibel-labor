## Kennzahlen (Teil 3 §7)

| Kennzahl | Wert | Beleg |
| --- | --- | --- |
| Sitzungen | 7 (1 Koordinator, 6 PO) | `lauf.jsonl`: 7 verschiedene `session_id` |
| Schritte (`num_turns`) | 139 | Summe der Zeilen 1–25 |
| Kosten (USD) | ca. 18,64 (Koordinator 0,23; Plan 1,32; Block 1 4,10; Block 2 2,87; Change 4,40; Block 3a 5,19; Block 3b 0,54) | Letzter `total_cost_usd` je Sitzung (der Wert steigt innerhalb einer Sitzung immer weiter) |
| Aktive Laufzeit | 16:07–20:48 UTC; davon ca. 3,5 h ohne Aufruf zwischen Block 2 und Change | `zeit` in Zeile 1, 8 und 25 |
| Aufgaben | 6 (T001–T005, REL); REL nicht begonnen, T004 und T005 nicht gemergt | `docs/backlog.md` auf `main`, Branch `feature/T005-sqlite` |
| Erstdurchlauf | 3 von 5 = 60 % (T001, T004, T005 PASS; T002 und T003 nicht) | `docs/tasks/T00x.md` „Result“, Commits 6e414c2, 081dfd7 |
| QA-Runden | 9 (7 für Aufgaben: T001 1, T002 2, T003 2, T004 1, T005 1; dazu 2 für das CHANGE-Review) | Commits 3fcb232, 6e414c2/8339eaa, 081dfd7/155d35f, 68dfba8, ec89d61, 538e91f/427e044 |
| Echte Befunde | 1 Code-Fehler (T003: `--Date` wird nicht mehr abgelehnt). Dazu ein Fehler im Brief von T002 und 7 Doku-Befunde im CHANGE-Review | 081dfd7, 627214f, `status.md` Zeile 16 |
| Abgelehnte Berechtigungen | 3 | `permission_denials` in Zeile 8, 12 und 21 |
| Rückfragen Plan | 5 (1 Widerspruch, 4 Lücken) | Zeile 2 |
| Tests | 303, laut Protokoll lokal grün (Stand T005-Branch) | Zeile 12 |
| CI grün | nein: die Läufe 43096225532 und 43097322251 für T004 und T005 blieben „queued“ | Zeile 19, Commit 28449d4 |

## Regelprüfung R1–R25

| Regel | Ergebnis | Beleg |
| --- | --- | --- |
| R1 | erfüllt | 633842c ändert nur `CLAUDE.md`, `docs/design.md` und `docs/status.md`; `.claude/settings.json` setzt Modell, `autoMemoryEnabled:false` und Test-Hook |
| R2 | erfüllt | `docs/tasks/ARCH.md:2` „class S: no QA review of the architecture“; eine Freigabe vor T001 (c318741) |
| R3 | erfüllt | Zeile 2: „1. Widerspruch: Nicht-Ziel N3 und Funktion F02“ steht an erster Stelle |
| R4 | erfüllt | Zeile 2: 1 Widerspruch und 4 Lücken = 5 Fragen |
| R5 | nicht erfüllt | Zeile 4: Entscheider schickt zurück, weil Bereitstellung und Prüfperson fehlten |
| R6 | erfüllt | `architecture.md:36` „Gate-relevant decisions“, `:274` „Removing a feature“ |
| R7 | erfüllt | Alle Briefs T001–T005 haben „QA level“ und „QA check criteria“ (der REL-Brief wurde nie geschrieben) |
| R8 | erfüllt | `backlog.md:11` letzte Zeile ist `REL` |
| R9 | erfüllt | Neue PO-Sitzung je Phase (6 Sitzungen); SP und QA liefen als Subagenten |
| R10 | erfüllt | `status.md` hat 99 Zeilen; `status-archive.md` ist gefüllt (c394671) |
| R11 | erfüllt | `main`: 511f432/633842c, dann je ein Squash-Commit mit ID (c318741 … b1e86a9) |
| R12 | erfüllt | 99b175c: Schalter `export_csv` in `config.toml` |
| R13 | nicht erfüllt | Diff b1e86a9..d54bcdc ändert `src/core/errors.py` und `src/core/ports.py`, d. h. Teile von F02 lagen im Kern |
| R14 | erfüllt | QA-Review CHANGE (538e91f, 427e044), erneute Freigabe 1 (0ed0b08, Zeile 11) |
| R15 | erfüllt | d54bcdc..e9a6e98: der Code-Diff liegt überwiegend in `sqlite_store.py` und `legacy_json_migration.py` (kleinere Änderungen in core/config, ports, entries) |
| R16 | nicht erfüllt | Auf `main` gibt es in `tests/core/test_config.py` keinen Test für einen ungültigen `KASSENBUCH_DATA`-Pfad; die Prüfung kam erst in T005, das nicht gemergt ist (Zeile 12) |
| R17 | erfüllt | Perf-Test `tests/perf/test_list_perf.py`: 0,7 s gegen die CI-Grenze von 3,0 s, CI war grün bei T001 (Zeile 6) |
| R18 | nicht erfüllt | 7d200a7: Fix und Tests in einem Commit, ohne vorherigen roten Test |
| R19 | erfüllt | Stufen A/B/C stehen in den Briefs; genau eine Härtungsaufgabe (T003) |
| R20 | erfüllt | `ci.yml` hat `paths-ignore` für `docs/**` und `**/*.md`; Zeile 20: der Doku-Commit hat keinen Lauf ausgelöst |
| R21 | nicht erfüllt | Zeilen 13–24: die CI wurde wiederholt abgefragt (z. B. Zeile 16: „Eben habe ich die CI noch einmal geprüft“) |
| R22 | erfüllt | `git branch -a`: zu jedem lokalen Branch gibt es `origin/…` |
| R23 | nicht erfüllt | `docs/manual-test.md` fehlt, weil REL nicht stattgefunden hat |
| R24 | erfüllt | „Freigeben“ in Zeile 5 und 11; ohne grüne CI wurde nichts gemergt; Freigabe 3 wurde nicht erreicht |
| R25 | erfüllt | Actions per SHA eingebunden (`ci.yml:24-25`); `requirements-dev.txt` mit `==`; Erlaubnisliste in `settings.json`; Negativtest `test_invalid_config_rejected` |

## Kostentreiber

- **Block 3, Sitzung 01cf5612 (5,19 USD):** Allein der erste Aufruf brauchte 14 Schritte und 7,27 Mio. Cache-Read-Tokens (Zeile 12). Danach kamen fünf weitere Aufrufe, in denen die CI wiederholt geprüft wurde (Zeilen 13–18). Die Folgesitzung 5d9d143d kostete für dasselbe Thema weitere 0,54 USD.
- **Change, Sitzung 5aba3b38 (4,40 USD):** 25 Schritte, ein QA-Review mit 7 Doku-Befunden, zwei Überarbeitungen der Architektur und eine Nachprüfung (Zeile 10, Commits 681512c–427e044).
- **Block 1, Sitzung fe0be079 (4,10 USD):** 203.164 Tokens 5-Minuten-Cache-Erstellung und 4,6 Mio. Cache-Read. Der T002-Durchgang lief zweimal durch QA, weil der Brief einen Fehler hatte (Zeile 6, 627214f).

{"regeln_erfuellt": 19, "regeln_gesamt": 25, "aufgaben": 6, "erstdurchlauf_prozent": 60, "qa_runden": 9, "echte_befunde": 1, "tests": 303, "ci_gruen": false}