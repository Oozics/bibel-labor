# Prüfbericht Bibel 1.7

Automatischer Referenzlauf 42627010074 · Repository kassenbuch-1-7-42627010074 · 2026-11-09

**Teilbericht:** Der Lauf wurde abgebrochen (Kostenbremse: Projekt-Sitzungen über 10.0 USD).

## 1. Ergebnis

Dies ist der erste gültige Lauf, ein Vergleich mit einer Vorversion in Prozent ist daher nicht möglich; der Lauf kostete 10,32 USD und wurde durch die Kostenbremse (Grenze 10 USD) beim Plan-Gate 2 beendet. Von 25 Regeln wurden 18 erfüllt, 3 nicht erfüllt (R9, R12, R14) und 4 waren nicht prüfbar, weil der Lauf vorher endete. Die Qualität der umgesetzten Teile ist gut: Von 4 umgesetzten der 9 Aufgaben bestanden 75 % im ersten Durchlauf, es gab 1 echten Befund (eine versehentlich eingecheckte Datei), 231 Tests laufen und die CI ist grün.

## 2. Kennzahlen

| Kennzahl | Vorversion | Bibel 1.7 |
| --- | --- | --- |
| Datum | – | 2026-11-09 |
| Claude-Code-Version | – | 2.1.319 (Claude Code) |
| Tokens gesamt | – | 8.913.950 |
| Kostenschätzung (USD) | – | 10,32 |
| davon Koordinator | – | 0,23 |
| davon PO-Sitzungen (inkl. SP und QA) | – | 10,09 |
| Schritte | – | 78 |
| Aktive Laufzeit | – | 45 Min. |
| Limit erreicht | – | ja, 240 Min. gewartet |
| Sitzungen | – | 6 |
| Aufgaben | – | 9 |
| Erstdurchlauf | – | 75 % |
| QA-Runden | – | 5 |
| Echte Befunde | – | 1 |
| Rückfragen (davon unvorhergesehen) | – | 10 (7) |
| Abgelehnte Berechtigungen | – | 0 |
| Regeltreue | – | 18 / 25 |
| Manuelle Prüfung (Minuten) | – | – |
| Tests, CI grün | – | 231, ja |
| Bemerkung | – | Abgebrochen: Kostenbremse: Projekt-Sitzungen über 10.0 USD |

Hilfsaufrufe (Entscheider, manuelle Prüfung, Auditor, Bericht) zusätzlich: 1,06 USD, nicht in der Kostenschätzung enthalten.

## 3. Regeltreue und Auswertung

| Kennzahl | Wert | Beleg |
| --- | --- | --- |
| Sitzungen | 6 (1 Koordinator, 5 PO) | lauf.jsonl, `session_id` Zeilen 1–15 |
| Schritte (`num_turns`) | 78 | Summe der Zeilen 1–15 |
| Kosten (letzter Wert je Sitzung) | ≈ 10,32 USD, also über der Kostenbremse von 10 USD; der Lauf endete beim Plan-Gate 2 | 0,23 + 1,45 + 1,42 + 1,55 + 1,53 + 4,14 |
| Laufzeit | 13:38 bis 18:21 Uhr, mit einer Lücke von etwa 4 h zwischen 14:12 und 18:21 (Ratenlimit) | Zeilen 14/15; status.md „interrupted once by a rate limit“ |
| Aufgaben | 9 (T001–T007, H001 abgebrochen, REL); umgesetzt wurden 4 | docs/backlog.md |
| Erstdurchlauf | 75 % (3 von 4: T001, T002 und T004 im ersten Durchlauf PASS, T003 erst FAIL) | docs/tasks/T001–T004.md |
| QA-Runden | 5 | T003 FAIL → PASS (Commits b14d73a, 3273b43) |
| Echte Befunde | 1 (versehentlich eingecheckte Binärdatei `prof`) | docs/tasks/T003.md:47 |
| Rückfragen Plan | 1 Fragenrunde mit 5 Rückfragen, 4 davon unvorhergesehen, plus 5 Rückfragen nach Ä1 | Zeilen 3/4 und 14 |
| Abgelehnte Berechtigungen | 0 | `permission_denials: []` in allen Zeilen |
| Tests | 231 (209 ohne Export plus 22 Export) | docs/tasks/T004.md:73, 76 |
| CI | grün (letzter Code-Stand, Lauf 42631804074) | status.md:46 |

| Regel | Ergebnis | Beleg |
| --- | --- | --- |
| R1 | erfüllt | Commit 11a721f: Koordinator meldet nur CLAUDE.md, design.md und status.md; settings.json setzt model, `autoMemoryEnabled: false` und den Test-Hook |
| R2 | erfüllt | ARCH ohne QA-Commit, eine einzige Freigabe (gate-plan.md) vor T001 |
| R3 | erfüllt | Zeile 4: „Zu 1: F02 hat Vorrang …“, der Widerspruch war Frage 1 |
| R4 | erfüllt | Zeile 3: 5 Rückfragen, Zeile 14: 5 Rückfragen |
| R5 | erfüllt | gate-plan.md:12–19: Klasse, Bereitstellung, personenbezogene Daten nein, Architektur in einfachen Worten; die Prüfperson steht in der Antwort Zeile 3 |
| R6 | erfüllt | architecture.md:35 „Gate-relevant decisions“, :237 „Removing a feature“ |
| R7 | erfüllt | Alle Briefs T001–T007, H001 und REL haben eine QA-Stufe und den Abschnitt „QA check criteria“ |
| R8 | erfüllt | Letzte Zeile in backlog.md ist `REL` |
| R9 | nicht erfüllt | Sitzung a47f133b (Zeilen 12–15) umfasst T004 und die komplette Neuplanung nach Ä1 |
| R10 | erfüllt | status.md hat 95 Zeilen, status-archive.md enthält 3 ältere Übergaben |
| R11 | erfüllt | main: 11a721f, fad09fe (PR #1), dann je ein Squash-Commit für T001–T004 |
| R12 | nicht erfüllt | Kein Ein/Aus-Schalter in der Konfiguration, nur die Registrierungszeile in features/__init__.py:10 |
| R13 | nicht prüfbar | T005 (F02 entfernen) wurde nicht ausgeführt, der Lauf endete beim Plan-Gate 2 |
| R14 | nicht erfüllt | „Touches gate“ steht in architecture.md:323 und die Freigabe wurde angefragt (Zeile 15), aber QA hat architecture 1.1 nicht geprüft (kein QA-Commit nach add9aee) |
| R15 | nicht prüfbar | T006 und T007 nicht umgesetzt |
| R16 | erfüllt | tests/core/test_config.py:28 erwartet `ConfigError` mit „KASSENBUCH_DATA“ |
| R17 | erfüllt | tests/perf/test_nfr1.py, CI grün (status.md:52) |
| R18 | nicht prüfbar | Der einzige Befund war eine eingecheckte Datei, kein Codefehler; ein roter Test war nicht anwendbar (dcf0cd9) |
| R19 | erfüllt | Stufen A/B im Backlog, REL = C; QA testet bei A/B nur den betroffenen Bereich (T003.md:91) |
| R20 | erfüllt | ci.yml:5–11 `paths-ignore` für docs/** und **/*.md |
| R21 | erfüllt | Keine wiederholten CI-Abfragen im Protokoll; CI-Zeilen in jeder Übergabe in status.md |
| R22 | erfüllt | Der Remote-Log von PLAN endet auf ad69d88 = lokaler HEAD; T001–T004 sind gepusht |
| R23 | nicht prüfbar | docs/manual-test.md fehlt, weil REL nicht erreicht wurde |
| R24 | erfüllt | Merge von PLAN erst nach „Freigeben“ (Zeile 5); PLAN 2 ohne Freigabe nicht gemergt |
| R25 | erfüllt | Actions per SHA eingebunden (ci.yml:23–24), requirements-dev.txt mit `==`, Negativtests vorhanden (test_config.py:28) |

Damit sind 18 Regeln erfüllt, 3 nicht erfüllt (R9, R12, R14) und 4 nicht prüfbar (R13, R15, R18, R23).

Die drei größten Kostentreiber:
- **Eine überlange PO-Sitzung in Block 2:** Sitzung a47f133b erledigte T004 und danach die ganze Neuplanung nach Ä1 im selben Kontext. Die Kosten stiegen von 1,68 auf 4,14 USD (Zeilen 14→15). Allein diese Sitzung hat die Kostenbremse von 10 USD überschritten und den Lauf vor T005 beendet.
- **Ein voller SP- und QA-Zyklus je Aufgabe in eigener PO-Sitzung:** Jede Sitzung kostete etwa 1,4 bis 1,55 USD (Zeilen 7, 9, 11). Dazu kamen Mutationstests und CI-Abgleich in der QA (T001.md:42, T003.md:87, T004.md:77) und bei T003 eine zweite QA-Runde nur wegen der Datei `prof`.
- **Zusatzrunden zu Beginn jeder Sitzung:** Jede PO-Sitzung begann mit einem Statusbericht und einer Frage (2 Schritte, je etwa 0,09 USD; Zeilen 2, 6, 8, 10, 12). Dreimal folgte nur die Antwort „Entscheide nach bestem Ermessen“ (Zeilen 9, 11, 13), einmal sogar die Klärung, was „Block 2“ bedeutet (Design 1.3, Commit 44db7c6).


## 4. Größte Kostentreiber

- **Eine überlange Arbeitssitzung (PO) im zweiten Block:** Sitzung a47f133b erledigte Aufgabe T004 und danach die ganze Neuplanung nach dem Änderungswunsch im selben Kontext. Die Kosten stiegen dort von 1,68 auf 4,14 USD (Zeilen 14→15); diese Sitzung überschritt die Kostenbremse und beendete den Lauf vor T005.
- **Voller Umsetzungs- und Prüfzyklus je Aufgabe in eigener Sitzung:** Jede Sitzung kostete etwa 1,4 bis 1,55 USD (Zeilen 7, 9, 11). Hinzu kamen Mutationstests und CI-Abgleich in der Qualitätsprüfung (T001.md:42, T003.md:87, T004.md:77) sowie bei T003 eine zweite Prüfrunde nur wegen der Datei `prof`.
- **Zusatzrunden zu Beginn jeder Sitzung:** Jede PO-Sitzung begann mit einem Statusbericht und einer Frage (2 Schritte, je etwa 0,09 USD; Zeilen 2, 6, 8, 10, 12). Dreimal folgte nur die Antwort „Entscheide nach bestem Ermessen“ (Zeilen 9, 11, 13), einmal wurde geklärt, was „Block 2“ bedeutet (Design 1.3, Commit 44db7c6).

## 5. Auffälligkeiten

- **Abgelehnte Berechtigungen:** keine (0).
- **Abbruch:** Kostenbremse „Projekt-Sitzungen über 10.0 USD“; der Lauf endete beim Plan-Gate 2, T005 bis T007 und REL wurden nicht umgesetzt.
- **Limit:** Ratenlimit mit etwa 4 Stunden Wartezeit (240 Minuten) zwischen 14:12 und 18:21 Uhr, bei 45 aktiven Minuten.
- **Rückfragen:** 10 insgesamt (5 im Plan, 5 nach dem Änderungswunsch), davon 7 unvorhergesehen.
- **Änderungswunsch:** wurde gesendet und führte zur Neuplanung.
- **Nicht erfüllte Regeln:** R9 (Sitzung zu lang), R12 (kein Ein/Aus-Schalter für die Funktion), R14 (Architektur 1.1 nicht von der Qualitätsprüfung geprüft).
- **Manuelle Prüfung:** nicht erfolgt, da die Freigabestufe REL nicht erreicht wurde (docs/manual-test.md fehlt).

## 6. Manuelle Prüfung

Nicht durchgeführt.

Die Prüfung lief automatisch. Ein Mensch sollte die Verständlichkeit der Anleitung mit einer 10-Minuten-Stichprobe bestätigen.

## 7. Empfehlungen für die nächste Bibel-Version

1. **Sitzungen nach Aufgabe begrenzen:** Nach einer Aufgabe eine neue Sitzung beginnen, besonders vor einer Neuplanung. Befund: R9 nicht erfüllt, Sitzung a47f133b stieg von 1,68 auf 4,14 USD und löste die Kostenbremse aus.
2. **Kostenbremse und Planung abstimmen:** Bei einem Änderungswunsch rechtzeitig prüfen, ob das Budget für die Neuplanung reicht, oder die Bremse bewusst anpassen. Befund: Der Lauf endete mit 10,32 USD beim Plan-Gate 2, 4 von 9 Aufgaben wurden umgesetzt.
3. **Startrunden sparen:** Die Rückfrage zu Sitzungsbeginn entfallen lassen, wenn Standardantwort „nach bestem Ermessen“ gilt, und Begriffe wie „Block 2“ vorab im Design definieren. Befund: dreimal nur diese Antwort (Zeilen 9, 11, 13), 7 unvorhergesehene Rückfragen.
4. **Ein/Aus-Schalter als feste Vorgabe für Funktionen:** In Architektur und Briefs verlangen, dass jede Funktion in der Konfiguration abschaltbar ist. Befund: R12 nicht erfüllt, nur Registrierungszeile in features/__init__.py:10.
5. **Architekturänderungen immer von der Qualitätsprüfung prüfen lassen:** Vor der Freigabeanfrage einen QA-Commit verlangen; zudem Binärdateien per Ignore-Regel ausschließen. Befund: R14 nicht erfüllt (kein QA-Commit nach add9aee); der einzige echte Befund war die eingecheckte Datei `prof`, die eine zweite Prüfrunde bei T003 auslöste.
