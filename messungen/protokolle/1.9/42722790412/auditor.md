**Tabelle 1: Kennzahlen (Teil 3 §7)**

| Kennzahl | Wert | Beleg |
| --- | --- | --- |
| Sitzungen | 7 (Koordinator 1, PO 6: Plan, Block 1, Change, Block 2 ×2, Release) | `lauf.jsonl`, 7 verschiedene `session_id` |
| Schritte (`num_turns`) | 118 (8+3+9+2+23+4+23+3+8+13+18+4) | `lauf.jsonl`, Zeilen 1–12 |
| Kostenschätzung | ≈ 19,49 USD (letzter Wert je Sitzung: 0,27 / 1,06 / 4,96 / 3,34 / 5,82 / 1,36 / 2,68) | `lauf.jsonl`, `total_cost_usd` |
| Aufgaben | 7 (T001–T006, REL; davon 2 Härtungsaufgaben) | `docs/backlog.md` |
| Erstdurchlauf | 5 von 7 = 71 % (T006 und REL mit Befund in Runde 1) | `docs/tasks/T006.md:68`, `docs/tasks/REL.md:134` |
| QA-Runden | 9 Runden zu Aufgaben, dazu 2 Architektur-Reviews in der Phase CHANGE | `.git/logs/HEAD` 43, 48, 79–81, 93–95 |
| Echte Befunde | 2 (T006: CHANGELOG-Eintrag zerteilt; REL F1: Testlücke beim schreibgeschützten Altbestand) | `T006.md:71`, `REL.md:164` |
| Abgelehnte Berechtigungen | 6, alle Bash (1 im Block 1, 5 im Release wegen powershell.exe) | `lauf.jsonl`, Zeilen 5 und 11 |
| Tests | 333 bestanden | `REL.md:120` |
| CI | grün (Lauf 42759208668 auf d92b28a, danach nur Doku-Commits) | `docs/status.md:14`, `:31` |

**Tabelle 2: Regelprüfung R1–R25**

| Regel | Ergebnis | Beleg |
| --- | --- | --- |
| R1 | erfüllt | Start-Commit 5f81359 ändert nur CLAUDE.md, design.md und status.md (`status-archive.md:112`; den Diff selbst konnte ich nicht ausführen, weil Bash gesperrt war); `settings.json`: model, `autoMemoryEnabled:false`, Test-Hook |
| R2 | erfüllt | Kein QA-Review der Architektur in der Planphase, eine Freigabe vor T001 (`status-archive.md:91–104`) |
| R3 | erfüllt | Erste Rückfrage des PO: „1. Widerspruch: N3 und F02“ (`lauf.jsonl`, Zeile 2) |
| R4 | erfüllt | Plan: 5 Rückfragen, Change: 4 (`lauf.jsonl`, Zeilen 2 und 6) |
| R5 | erfüllt | `docs/gates/freigabe-1.md:12–26` nennt Klasse, Bereitstellung, Prüfperson, „Personenbezogene Daten: nein“ und die Architektur in Alltagssprache |
| R6 | erfüllt | `architecture.md:34` „Gate-relevant decisions“, `:260` „Removing a feature“ |
| R7 | erfüllt | Alle 7 Briefs haben „QA level“ und „QA check criteria“ (`docs/tasks/*.md`, Zeile 2) |
| R8 | erfüllt | Letzte Backlog-Zeile ist REL (`backlog.md:12`) |
| R9 | erfüllt | Eigene PO-Sitzung je Phase bzw. Block; SP und QA als Subagenten |
| R10 | erfüllt | `status.md` hat 95 Zeilen, `status-archive.md` hat 8 Übergaben |
| R11 | erfüllt | `main` = Setup plus Squash-Merges PLAN, T001…T006, CHANGE, REL, alle mit ID (`.git/logs/HEAD` 12–100) |
| R12 | erfüllt | T002: „F02 CSV export behind flag `export_csv`“ (`backlog.md:7`) |
| R13 | nicht erfüllt | Der T004-Diff berührt auch `core/errors.py` und `core/domain.py` (`status.md:88–89`) |
| R14 | erfüllt | T005 ist „Touches gate: yes“, QA-Review plus Re-Review (415f772, 227cb5e), erneute Freigabe in `docs/gates/freigabe-change.md` |
| R15 | erfüllt (knapp) | Kern des Diffs: `adapters/store.py` und `legacy_json.py`; zusätzlich `core/*` für die Pfadregel (`status.md:70–71`) |
| R16 | erfüllt | `tests/features/entries/test_storage.py:316` (Endungsregel), `tests/adapters/test_store.py:266` (fehlender Ordner) |
| R17 | erfüllt | `tests/perf/test_list_perf.py`, auf CI grün (0,35 s, `status.md:65`) |
| R18 | nicht prüfbar | Beide Befunde (Doku, Testlücke) waren keine Codefehler; im Branch-Verlauf gibt es keinen eigenen roten Test-Commit (d92b28a) |
| R19 | nicht erfüllt | QA auf Stufe B hat in T006 trotzdem die volle Suite ausgeführt: „full suite incl. perf 330 passed“ (`T006.md:91`) |
| R20 | erfüllt | `ci.yml:5–11` `paths-ignore` für `docs/**` und `*.md`; PLAN und CHANGE ohne CI gemergt |
| R21 | erfüllt | Kein `gh run watch` und keine Schleife im Protokoll; QA vermerkt „not polled“; Wartezeile in `status.md:4` |
| R22 | erfüllt | Für jeden Branch PLAN…REL gibt es `refs/remotes/origin/*`; jede Übergabe nennt einen Branch |
| R23 | erfüllt | `docs/manual-test.md`: Deutsch, Windows 11 und PowerShell, Hinweise für Nicht-Entwickler |
| R24 | erfüllt | Ausdrückliche Freigaben 1, Change und 3 sind vor dem Merge vermerkt (`freigabe-1.md:48`, `status.md:12`) |
| R25 | erfüllt | Actions per SHA eingebunden (`ci.yml:21–22`), `requirements-dev.txt` mit `==`, Negativtests (z. B. `test_parse_date_rejects_invalid`) |

**Drei größte Kostentreiber**

1. **PO-Sitzung Block 2 (T004+T005), 5,82 USD:** T005 brauchte 8 SP-Commits, eine Unterbrechung durch das Nutzungslimit von etwa 4 h (`.git/logs/HEAD` 61→62) und QA auf Stufe C mit 18 Mutationsproben. Der PR-Lauf von T004 war wegen des Performance-Tests rot und musste geklärt werden (`status.md:82–86`).
2. **PO-Sitzung Block 1, 4,96 USD bei 23 Schritten:** T001 wurde auf Stufe C mit 33 Mutationen geprüft. Dazu kam die zusätzliche Härtungsaufgabe T003 in derselben Sitzung, insgesamt 3 SP/QA-Zyklen (`lauf.jsonl`, Zeile 5).
3. **Change-Phase, 3,34 USD bei 23 Schritten:** 11 Doku-Commits mit zwei QA-Architektur-Reviews und Nacharbeit (`.git/logs/HEAD` 40–50). Dazu kommen die Release-Schleifen mit 2 QA-Runden und 5 abgelehnten PowerShell-Aufrufen (`lauf.jsonl`, Zeile 11).

{"regeln_erfuellt": 22, "regeln_gesamt": 25, "aufgaben": 7, "erstdurchlauf_prozent": 71, "qa_runden": 9, "echte_befunde": 2, "tests": 333, "ci_gruen": true}