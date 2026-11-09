# Prüfbericht Bibel 1.8

Automatischer Referenzlauf 42686492874 · Repository kassenbuch-1-8-42686492874 · 2026-11-09

**Teilbericht:** Der Lauf wurde abgebrochen (Fehler: git clone -q D:\a\bibel-labor\lauf\kassenbuch-1-8-42686492874 D:\a\bibel-labor\lauf\manuell failed: fatal: destination path 'D:\a\bibel-labor\lauf\manuell' already exists and is not an empty directory.).

## 1. Ergebnis

Dies ist der erste gültige Lauf, ein Vergleich mit einer Vorversion in Prozent ist deshalb nicht möglich (Verbrauch: 7,32 Mio. Tokens, 7,91 USD). Von 25 Regeln wurden 20 erfüllt, 4 waren nicht prüfbar, und 1 wurde nicht erfüllt: Die Prüfanleitung wurde nach der ersten Fassung nicht erneut von Menschen geprüft. Die Qualität der Software ist gut (alle 3 Aufgaben im Erstdurchlauf bestanden, 0 echte Befunde, 205 Tests, CI grün), aber die manuelle Prüfung ist nicht bestanden, weil 11 von 12 Schritten als problematisch eingestuft wurden.

## 2. Kennzahlen

| Kennzahl | Vorversion | Bibel 1.8 |
| --- | --- | --- |
| Datum | – | 2026-11-09 |
| Claude-Code-Version | – | 2.1.321 (Claude Code) |
| Tokens gesamt | – | 7.320.645 |
| Kostenschätzung (USD) | – | 7,91 |
| davon Koordinator | – | 0,31 |
| davon PO-Sitzungen (inkl. SP und QA) | – | 7,60 |
| Schritte | – | 56 |
| Aktive Laufzeit | – | 39 Min. |
| Limit erreicht | – | ja, 180 Min. gewartet |
| Sitzungen | – | 3 |
| Aufgaben | – | 3 |
| Erstdurchlauf | – | 100 % |
| QA-Runden | – | 5 |
| Echte Befunde | – | 0 |
| Rückfragen (davon unvorhergesehen) | – | 3 (1) |
| Abgelehnte Berechtigungen | – | 4 |
| Regeltreue | – | 20 / 25 |
| Manuelle Prüfung (Minuten) | – | 10 |
| Tests, CI grün | – | 205, ja |
| Bemerkung | – | Abgebrochen: Fehler: git clone -q D:\a\bibel-labor\lauf\kassenbuch-1-8-42686492874 D:\a\bibel-labor\lauf\manuell failed: fatal: destination path 'D:\a\bibel-labor\lauf\manuell' already exists and is not an empty directory. |

Hilfsaufrufe (Entscheider, manuelle Prüfung, Auditor, Bericht) zusätzlich: 0,97 USD, nicht in der Kostenschätzung enthalten.

## 3. Regeltreue und Auswertung

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


## 4. Größte Kostentreiber

- **Eine lange PO-Sitzung für Block 1 mit allen Unterstützern und Prüfern:** 6,34 von 7,91 USD (80 %), 5,48 Mio. Tokens aus dem Zwischenspeicher gelesen, Laufzeit 1328 s plus 375 s (lauf.jsonl, Zeilen 5–6).
- **Nacharbeit nach der Rückgabe von Freigabe 3:** zusätzlich 1,47 USD (Zeile 6 minus Zeile 5) und zwei zusätzliche QA-Runden auf Stufe C, obwohl nur Dokumentation geändert wurde (REL.md:73 und 105). Auslöser war eine Prüfanleitung, die ohne Entwicklerwissen nicht ausführbar war (manuelle-pruefung.json).
- **Aufwendige QA auf Stufe C:** 23 bzw. 18 Mutationsproben, wörtliches Nachspielen der Anleitung in PowerShell und Versuche zur Zeichenkodierung (T001.md, status.md:20).

## 5. Auffälligkeiten

- **Abgelehnte Berechtigungen:** 4, alle für Bash (3 in Zeile 5, 1 in Zeile 6 von lauf.jsonl).
- **Abbruch:** Die manuelle Prüfung brach mit einem Fehler ab: Das Zielverzeichnis für `git clone` existierte schon und war nicht leer. Die Prüfung lief danach im vorhandenen Ordner, daher konnten die Anleitungsschritte 1 bis 3 (ZIP entpacken, Terminal öffnen) nicht ausgeführt werden.
- **Limit:** Die Wartezeit durch das Limit betrug 180 Minuten, die aktive Laufzeit 39 Minuten.
- **Rückfragen und Unvorhergesehenes:** 3 Rückfragen in der Planphase (eine davon ein Widerspruch zwischen Nicht-Ziel N3 und F02); 1 unvorhergesehene Frage.
- **Anzeigeprobleme:** In fast allen Prüfschritten erschienen Umlaute und das Euro-Zeichen als „�“, vermutlich wegen der umgeleiteten Ausgabe; ob sie in einem echten Terminal stimmen, blieb ungeprüft.
- **Nicht prüfbar:** Excel stand nicht zur Verfügung, das Öffnen der CSV-Datei wurde nicht getestet. Der Änderungswunsch wurde nicht gesendet, daher waren R13, R14, R15 und R18 nicht prüfbar.

## 6. Manuelle Prüfung

Bestanden: nein · geschätzte Dauer für einen Menschen: 10 Minuten · Schritte: 12

- Schritt 2: Die Umlaute in 'für' und 'überschrieben' erschienen als '�'. Das liegt vermutlich an meiner umgeleiteten Ausgabe (Codepage) und nicht an einem echten Terminal. Ich konnte nicht prüfen, ob sie dort richtig aussehen.
- Schritt 3: 'Keine Einträge' und das '€' erschienen als '�'. Die Ursache ist vermutlich dieselbe wie bei Schritt 2 und nicht sicher festzustellen.
- Schritt 4: Das '€', 'Brötchen' und 'Bäcker' erschienen als '�'. Der Rest der Zeile entsprach der Erwartung.
- Schritt 6: Das '€' und das 'é' erschienen als '�'. Das heutige Datum 09.11.2026 war korrekt.
- Schritt 7: Reihenfolge und Saldo 1.192,50 stimmten. Das '€' und die Umlaute erschienen als '�', also genau der Fall, vor dem die Anleitung warnt. Die Anleitung sagt nicht, was zu tun ist, wenn es so aussieht. Der Hinweis auf 'chcp' und Schritt 12 steht weit weg.
- Schritt 8: Die Fehlermeldung war inhaltlich richtig. Das 'Ü' in 'Ungültiger' erschien als '�'.
- Schritt 9: Fehlermeldung und unveränderte Liste waren richtig. Die Umlaute erschienen als '�'. Schritt 9 enthält zwei Befehle, und die Anleitung sagt nicht klar, dass beide getrennt eingegeben werden.
- Schritt 10: Die Meldung stimmte, und die CSV-Datei hat den richtigen Inhalt mit Kopfzeile und UTF-8-BOM. Excel steht nicht zur Verfügung, deshalb konnte ich das Öffnen und die Darstellung der Spalten nicht prüfen. Die Buchung 'Café' hat einen leeren Text, was die Anleitung nicht erwähnt.
- Schritt 11: Die Fehlermeldung stimmte. Das 'ä' in 'verändert' erschien als '�'. Das Änderungsdatum der Datei habe ich nicht verglichen.
- Schritt 12: Optionaler Schritt, nicht ausgeführt. Er braucht außerdem den Editor per Doppelklick, den ich nicht habe.
- Schritt 1: Funktioniert (Python 3.12.10). Die Anleitungsschritte 1 bis 3 (ZIP entpacken, Terminal über Rechtsklick öffnen) konnte ich nicht ausführen, weil ich im bereits vorhandenen Ordner gearbeitet habe. Außerdem fehlt in der Anleitung ein Hinweis, dass die Schritte 1 bis 12 in der Tabelle von den nummerierten Startschritten 1 bis 4 zu unterscheiden sind. Die Nummern doppeln sich.

Die Prüfung lief automatisch. Ein Mensch sollte die Verständlichkeit der Anleitung mit einer 10-Minuten-Stichprobe bestätigen.

## 7. Empfehlungen für die nächste Bibel-Version

1. **Prüfanleitung vor Freigabe 3 von einer Person ohne Entwicklerwissen testen lassen.** Befund: Die erste Fassung fiel durch (11 von 12 Schritten problematisch, R23 nicht erfüllt) und die Nacharbeit kostete 1,47 USD.
2. **Die Anleitung bei Zeichenkodierung ausdrücklich führen.** Sie sollte sagen, was zu tun ist, wenn Umlaute oder „€“ als „�“ erscheinen, und den Hinweis auf `chcp` an den Anfang stellen statt weit weg in Schritt 12. Befund: Schritt 7 und fast alle weiteren Schritte zeigten „�“.
3. **Anleitung klarer gliedern.** Die Nummern der Tabellenschritte 1 bis 12 sollten sich nicht mit den Startschritten 1 bis 4 doppeln, und Schritt 9 sollte zwei getrennt einzugebende Befehle klar benennen. Außerdem sollte die Anleitung erwähnen, dass die Buchung „Café“ einen leeren Text hat. Befund: manuelle-pruefung.json, Schritte 1, 9 und 10.
4. **Die manuelle Prüfung in einem frischen, leeren Verzeichnis starten.** Befund: Der Abbruch durch `git clone` in ein bereits vorhandenes Verzeichnis verhinderte die Prüfung der Schritte 1 bis 3.
5. **Die Stufe C bei reinen Dokumentationsänderungen begrenzen und Bash-Rechte für QA-Versuche vorab klären.** Befund: Zwei zusätzliche QA-Runden auf Stufe C nach einer reinen Doku-Änderung sowie 4 abgelehnte Bash-Aufrufe.
