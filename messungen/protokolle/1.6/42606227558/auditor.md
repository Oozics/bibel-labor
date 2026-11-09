**Tabelle 1: Kennzahlen (Teil 3 §7)**

| Kennzahl | Wert | Beleg |
| --- | --- | --- |
| Sitzungen | 3 (Koordinator, PO Plan, PO Block 1) | lauf.jsonl Z. 1, Z. 2–5, Z. 6–21 (`total_cost_usd` steigt innerhalb jeder Sitzung weiter) |
| Schritte (`num_turns`) | 59 (6 + 18 + 35) | lauf.jsonl Z. 1–21 |
| Kostenschätzung | ca. 3,63 USD (0,21 + 1,37 + 2,05) | letzter Wert je Sitzung, Z. 1, 5, 21 |
| Aktive Laufzeit | ca. 19 Min. (11:07:42 bis 11:26:36) | lauf.jsonl `zeit` |
| Aufgaben | 5 (T001–T004, REL), nur T001 bearbeitet und nicht gemergt | docs/backlog.md |
| Erstdurchlauf | 100 % (1 von 1) | docs/tasks/T001.md „PASS (no findings)“ |
| QA-Runden | 1 | Commit f5f8b8e |
| Echte Befunde | 0 (nur 4 Hinweise) | docs/tasks/T001.md, Abschnitt „Hints“ |
| Rückfragen Plan | 5 (Widerspruch und 4 Fragen mit Vorschlag) | antworten/003.json |
| Abgelehnte Berechtigungen | 0 | `permission_denials: []` in allen 21 Zeilen |
| Tests | 35, nur lokal grün | docs/status.md Z. 11/15 |
| CI grün | nein, nicht bestätigt (Token bekommt HTTP 403) | docs/status.md Z. 4–5 |

**Tabelle 2: Regeltreue R1–R25**

| Nr. | Ergebnis | Beleg |
| --- | --- | --- |
| R1 | erfüllt | Start-Commit dde40f6 ändert laut Übergabe nur CLAUDE.md, design.md und status.md; settings.json setzt `model`, `autoMemoryEnabled:false` und den Test-Hook (Diff selbst nicht geprüft, Bash war gesperrt) |
| R2 | erfüllt | Keine zusätzliche Rolle; eine Freigabe vor dem Code (gate-plan.md); keine QA am Architekturvorschlag |
| R3 | erfüllt | antworten/003.json: „Runde 1, Widerspruch zuerst“ |
| R4 | erfüllt | 003.json: Widerspruch und 4× „Vorschlag:“, also 5 Rückfragen |
| R5 | nicht erfüllt | gate-plan.md nennt Bereitstellung und Prüfperson, aber weder Klasse S noch „personenbezogene Daten: nein“ |
| R6 | erfüllt | architecture.md Z. 52 „Gate-relevant decisions“, Z. 253 „Removing a feature“ |
| R7 | erfüllt | T001.md: „QA level: B“ und „QA check criteria“ |
| R8 | erfüllt | backlog.md: letzte Zeile ist `REL` |
| R9 | erfüllt | Neue PO-Sitzung für Plan und für Block 1 (lauf.jsonl Z. 2 und Z. 6); SP und QA als Subagenten |
| R10 | erfüllt | status.md hat 44 Zeilen und 4 Übergaben; das Archiv war noch nicht nötig |
| R11 | erfüllt | main: dde40f6 (Setup) und e8158cd (PLAN, Squash), beide mit ID |
| R12 | nicht erfüllt | architecture.md Z. 154: F02 „no (removable via registry)“, kein Ein/Aus-Schalter in der Konfiguration |
| R13 | nicht prüfbar | Ä1 wurde nie gesendet, F02 nie gebaut |
| R14 | nicht prüfbar | Ä1 wurde nie gesendet |
| R15 | nicht prüfbar | Kein Speicherwechsel |
| R16 | nicht prüfbar | Nur Tests für gesetzte, fehlende und leere Variable (T001.md); kein Test für ungültigen Pfad |
| R17 | nicht prüfbar | Benchmark gehört zu T003, nicht gebaut |
| R18 | nicht prüfbar | Keine QA-Befunde |
| R19 | erfüllt | Stufe B: „full suite not rerun (level B)“ (T001.md) |
| R20 | nicht erfüllt | ci.yml: `push: branches ["**"]` ohne `paths-ignore` |
| R21 | nicht erfüllt | lauf.jsonl Z. 8–21: wiederholte CI-Abfragen („fünfmal versucht“ Z. 13, „noch einmal geprüft“ Z. 12/18) |
| R22 | erfüllt | origin/PLAN und origin/T001 vorhanden; jede Übergabe nennt einen gepushten Branch |
| R23 | nicht prüfbar | REL nicht erreicht, docs/manual-test.md fehlt |
| R24 | erfüllt | PLAN erst nach „Freigeben“ gemergt (0b976f9 → e8158cd); T001 ohne grüne CI nicht gemergt |
| R25 | erfüllt | Actions per SHA eingebunden (ci.yml Z. 16–17); requirements-dev.txt mit 3 Versionen per `==`; Negativtest für unbekannten Befehl |

**Die drei größten Kostentreiber**

- **CI-Blockade in Block 1:** Das Token hat keine Leserechte für Actions (HTTP 403). Daraus wurden 14 Wechsel zwischen PO und Entscheider ohne Fortschritt (Z. 8–21, ca. +0,33 USD). Der Entscheider antwortete jedes Mal „Bitte prüf das selbst“. Danach brach der Lauf nach T001 ab.
- **SP und QA für T001:** Z. 7 hat 12 Schritte und kostete ca. +1,54 USD. Darin stecken unter anderem 8 Mutationsproben bei Stufe B (T001.md).
- **Plan-Phase mit Architekturentwurf:** Z. 4 hat 10 Schritte und kostete ca. +1,04 USD für Spezifikation, Architektur, Stack-Profil und Backlog-Entwurf.

{"regeln_erfuellt": 14, "regeln_gesamt": 25, "aufgaben": 5, "erstdurchlauf_prozent": 100, "qa_runden": 1, "echte_befunde": 0, "tests": 35, "ci_gruen": false}