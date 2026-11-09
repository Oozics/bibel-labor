## Kennzahlen (Teil 3 §7)

| Kennzahl | Wert | Beleg |
| --- | --- | --- |
| Sitzungen | 3 Sitzungen mit 6 Aufrufen: Koordinator, PO Plan, PO Block 1 | lauf.jsonl, 3 verschiedene `session_id` (Zeilen 2–4 und 5–6 sind fortgesetzte Sitzungen) |
| Schritte (`num_turns`) | 56 (8+3+16+3+18+8) | lauf.jsonl, Zeilen 1–6 |
| Tokens gesamt | ca. 7,32 Mio. (Koordinator 0,27 · Plan 1,02 · Block 1 6,04 Mio.) | `modelUsage` im jeweils letzten Eintrag pro Sitzung; die Werte zählen innerhalb einer Sitzung weiter |
| Kosten (USD) | ca. 7,91 (0,31 + 1,26 + 6,34) | `total_cost_usd`, Zeilen 1, 4, 6 |
| Aktive Laufzeit | ca. 34 min (2051 s `wall_s`) | lauf.jsonl |
| Aufgaben | 3 (T001, T002, REL; keine eigene Härtungsaufgabe) | docs/backlog.md |
| Erstdurchlauf | 100 % (3 von 3 mit PASS in der ersten QA-Runde) | docs/tasks/T001.md:44, T002.md:35, REL.md:39 |
| QA-Runden | 5 (T001: 1, T002: 1, REL: 3) | docs/tasks/REL.md:39, 73, 105 |
| Echte Befunde | 0 (nur Hinweise H1–H8 und zwei Hinweise zu REL) | docs/backlog.md:14–24 |
| Rückfragen Planphase | 3 (davon 1 Widerspruch N3/F02) | lauf.jsonl, Zeile 2, `antwort` |
| Abgelehnte Berechtigungen | 4 (3 in Zeile 5, 1 in Zeile 6, alle Bash) | `permission_denials` |
| Manuelle Prüfung | 12 Schritte, davon 11 problematisch, nicht bestanden; geschätzt 10 min | manuelle-pruefung.json |
| Tests | 205 | docs/tasks/REL.md:92 |
| CI | grün (Lauf 42690243491 auf main f7ed6e6) | docs/status.md:6 |

## Regelprüfung R1–R25

| Regel | Ergebnis | Beleg |
| --- | --- | --- |
| R1 | erfüllt | Start-Commit 5c10bdd ändert nur CLAUDE.md, docs/design.md, docs/status.md (status-archive.md:8). `.claude/settings.json` setzt `model`, `autoMemoryEnabled: false` und den Test-Hook. Einen eigenen Diff gegen die Vorlage konnte ich nicht erzeugen, weil die Shell gesperrt war. |
| R2 | erfüllt | Architektur vom SP ohne QA-Prüfung, keine zusätzliche Rolle, nur Freigabe 1 vor T001 (status-archive.md:15, HEAD-Log Zeilen 8–12) |
| R3 | erfüllt | lauf.jsonl Zeile 2: „1. Widerspruch: Nicht-Ziel N3 und F02 …“ steht an erster Stelle |
| R4 | erfüllt | lauf.jsonl Zeile 2: drei Rückfragen |
| R5 | erfüllt | docs/gate-1.md:10 nennt Klasse S, Bereitstellung, Prüfperson und „Personenbezogene Daten: nein“; Architektur in Alltagssprache in Zeile 13 |
| R6 | erfüllt | architecture.md:31 „Gate-relevant decisions“, architecture.md:140 „Removing a feature“ |
| R7 | erfüllt | Alle drei Briefs haben „QA level“ (Zeile 2) und „## QA check criteria“ |
| R8 | erfüllt | backlog.md:9, letzte Zeile ist `REL` |
| R9 | erfüllt | Neue PO-Sitzung für Plan und für Block 1 (verschiedene `session_id`); SP und QA laufen als Subagenten pro Aufgabe (status.md:20, 29, 38) |
| R10 | erfüllt | status.md hat 52 Zeilen; 7 Übergaben, status-archive.md enthält 2 davon |
| R11 | erfüllt | logs/refs/heads/main: Setup, Plan, T001, T002, je ein Squash-Commit mit ID |
| R12 | erfüllt | kassenbuch/app.py:30 `cfg.flag("export_csv", True)` |
| R13 | nicht prüfbar | Änderungswunsch Ä1 wurde im Lauf nicht gestellt (lauf.jsonl endet mit Freigabe 3) |
| R14 | nicht prüfbar | Ä1 Teil b (SQLite) kam nicht vor |
| R15 | nicht prüfbar | Kein Speicherwechsel im Lauf |
| R16 | erfüllt | tests/core/test_config.py; ein leeres `KASSENBUCH_DATA` endet mit Exit 2 (status.md:38) |
| R17 | erfüllt | tests/perf/test_list_perf.py mit 100.000 Einträgen ist grün (T001.md:48) |
| R18 | nicht prüfbar | 0 echte Befunde, also keine Fehlerbehebung |
| R19 | erfüllt | Stufen C/B/C in den Briefs; T002 auf Stufe B prüft nur die Prüfkriterien (T002.md:44) |
| R20 | erfüllt | ci.yml:5–11 `paths-ignore` für docs und md; kein CI-Lauf auf REL (status.md:20) |
| R21 | erfüllt | status.md:29, 38 „CI green once checked“; Wartezeile in status.md:4 |
| R22 | erfüllt | origin/REL = 9013718 = lokal, origin/main = f7ed6e6; alle Branches liegen auf dem Remote |
| R23 | nicht erfüllt | Erste Fassung fiel durch (manuelle-pruefung.json: `"bestanden": false`, Schritte 1, 7, 9 unklar); die überarbeitete Fassung wurde nicht erneut von Menschen geprüft |
| R24 | erfüllt | PLAN erst nach „Freigeben“ gemergt (lauf.jsonl Zeile 4); REL nach „Zurück an PO“ nicht gemergt (status.md:12) |
| R25 | erfüllt | ci.yml:24–25 Actions per SHA; requirements-dev.txt mit `==`; Negativtests für beschädigte Dateien und ungültige Eingaben (T001.md:50) |

## Größte Kostentreiber

1. **Eine lange PO-Sitzung für Block 1 mit allen SP- und QA-Subagenten.** Sie kostete 6,34 von 7,91 USD (80 %), las 5,48 Mio. Tokens aus dem Cache und lief 1328 s plus 375 s (lauf.jsonl, Zeilen 5–6).
2. **Die Nacharbeit nach der Rückgabe von Freigabe 3.** Sie kostete +1,47 USD (Zeile 6 minus Zeile 5) und brauchte zwei zusätzliche QA-Runden auf Stufe C, obwohl nur Doku geändert wurde (c4858b9, ac517c5; REL.md:73 und 105). Auslöser war eine Prüfanleitung, die ohne Entwicklerwissen nicht ausführbar war (manuelle-pruefung.json).
3. **Aufwendige QA auf Stufe C.** Dazu gehörten 23 bzw. 18 Mutationsproben, wörtliches Nachspielen der Anleitung in PowerShell und Versuche zur Zeichenkodierung (R2). Diese Versuche führten zu 4 abgelehnten Bash-Aufrufen (T001.md, status.md:20, `permission_denials` in den Zeilen 5–6).

{"regeln_erfuellt": 20, "regeln_gesamt": 25, "aufgaben": 3, "erstdurchlauf_prozent": 100, "qa_runden": 5, "echte_befunde": 0, "tests": 205, "ci_gruen": true}