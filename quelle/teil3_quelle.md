# Teil 3: Referenzprojekt

Das Referenzprojekt misst, ob eine neue Version der Bibel Kosten senkt, ohne Qualität oder Regeltreue zu verlieren. Es ist ein kleines Kassenbuch für die Kommandozeile mit zwei Funktionen und einem Änderungswunsch, Projektklasse S, und so gebaut, dass jede Regel der Bibel mindestens einmal greifen muss. Ziel: ein Lauf in etwa einer Stunde, unter 10 USD API-Gegenwert und innerhalb eines Nutzungsfensters des Abos. Der Lauf ist vollständig automatisiert: Ein Steuerungsskript im privaten Repository `bibel-labor` startet auf Knopfdruck in GitHub Actions alle Rollen, spielt mit kurzen Claude-Aufrufen den Auftraggeber (den **Entscheider**) nach festen Regeln, misst exakt und erstellt am Ende einen Prüfbericht als PDF. Du drückst den Knopf und liest den Bericht.

## 1. Aufbau des Messlaufs

Der Lauf läuft auf einem Windows-Rechner von GitHub Actions. Das Python-Skript `werkzeuge/referenzlauf.py` steuert ihn und startet alle Claude-Sitzungen im nicht-interaktiven Modus von Claude Code. Für Koordinator und PO sieht der Entscheider aus wie ein Mensch.

| Wer | Kennt Teil 3? | Aufgabe |
| --- | --- | --- |
| **Du** | ja | Einmalige Einrichtung (Abschnitt 6), Start per Knopfdruck, Prüfbericht lesen, optional 10-Minuten-Stichprobe |
| **Steuerungsskript** | ja | Legt das Projekt an, startet jede Rolle, protokolliert jeden Aufruf, rechnet Kosten und Zeiten exakt aus, setzt die Kostenbremse durch, erstellt Bericht und Ergebnisgeschichte |
| **Entscheider** | ja | Ein kurzer, eigener Claude-Aufruf pro Antwort: sieht nur die Regeln aus Abschnitt 5, die aktuelle Lage und die letzte Nachricht der Rolle und antwortet als Auftraggeber |
| **Manueller Prüfer** | ja | Eigene Sitzung in einer Kopie des Projekts; führt `docs/manual-test.md` aus wie ein Nicht-Entwickler (Abschnitt 5) |
| **Koordinator, PO** | nein | Arbeiten nach Teil 1 und 2 (über das Vorlagen-Repository) und sprechen mit dem Entscheider, als wäre er ein Mensch |
| **SP, QA** | nein | Werden vom PO als Subagenten gestartet, wie in jedem Projekt |
| **Auditor** | ja | Frische, unabhängige Sitzung am Ende, nur mit Leserechten; prüft das Repository gegen R1 bis R25 |

**Ablage:** Alles, was zur Messung gehört, liegt im privaten Repository `bibel-labor`: die Quelltexte der Bibel (`quelle/`), die Werkzeuge (`werkzeuge/`) sowie Ergebnisgeschichte, Protokolle und Prüfberichte (`messungen/`). Das Projekt jedes Laufs ist ein eigenes privates Repository, z. B. `kassenbuch-1-7-<Laufnummer>`. Die Projekt-Sitzungen arbeiten nur in ihrem Projektordner und sehen `bibel-labor` nie. Die Hilfsaufrufe (Entscheider, manueller Prüfer, Auditor, Berichtstext) zählen nicht zur Kostenschätzung des Projekts; ihre Kosten stehen getrennt im Bericht.

## 2. Regeln für vergleichbare Läufe

Ein Lauf ist nur vergleichbar, wenn sich zwischen zwei Läufen nur die Bibel ändert.

- **Gleiches Designdokument:** immer das aus Abschnitt 4, unverändert. Nur die Zeile „Grundformel-Version“ wird angepasst.
- **Gleiche Vorlage:** das Vorlagen-Repository im Stand der gemessenen Version (z. B. Tag `v1.7`); der Bericht nennt die Commit-Kennung der Vorlage.
- **Kein Wissen über den Test:** Koordinator, PO, SP und QA sehen nie Teil 3, den Messordner oder ein Wort über Messung. Der Entscheider antwortet wie ein Auftraggeber, nie mit Regelnummern, Drehbuch oder Kennzahlen.
- **Gleiche Entscheidungen:** Der Entscheider antwortet wörtlich nach Abschnitt 5, zum vorgesehenen Zeitpunkt. Jede seiner Entscheidungen steht im Protokoll (`entscheidungen.jsonl`).
- **Gleiche Umgebung:** Windows-Rechner von GitHub Actions, derselbe Workflow, gleiche Claude-Code-Version wenn möglich (steht im Bericht), Modell aus den Projekteinstellungen, gleiche Berechtigungseinstellung. Abweichungen stehen im Bericht.
- **Frisches Repository:** für jeden Lauf ein neues privates Repository `kassenbuch-<Version>-<Laufnummer>` aus dem Vorlagen-Repository.
- **Schwankung:** KI-Läufe streuen. Unterschiede unter etwa zehn Prozent gelten nicht als Wirkung. Im Zweifel den Lauf wiederholen und den Mittelwert nehmen.

## 3. Was das Projekt prüft

Jede Regel der Bibel hat im Referenzprojekt einen Auslöser. Diese Tabelle ist zugleich die Prüfliste für die Auswertung (Abschnitt 8).

| Nr. | Regel der Bibel | Auslöser im Referenzprojekt | Woran man es erkennt |
| --- | --- | --- | --- |
| R1 | Projektstart aus dem Vorlagen-Repository | Start mit Designdokument | Gegenüber der Vorlage ändert der Start-Commit nur `CLAUDE.md` (Name, Zweck, Klasse S, Version), `docs/design.md` und `docs/status.md`; `.claude/settings.json` setzt das Modell, schaltet die Gedächtnisfunktion ab und aktiviert den Test-Hook |
| R2 | Ablauf passend zur Klasse S | Klasse S im Designdokument | Keine zusätzliche Rolle, keine QA-Prüfung des Architekturvorschlags, genau eine Freigabe vor dem ersten Code |
| R3 | Lückenanalyse, Widersprüche zuerst | Eingebauter Widerspruch: Nicht-Ziel N3 gegen Funktion F02 | PO meldet den Widerspruch als ersten Punkt |
| R4 | Höchstens fünf Rückfragen pro Durchgang | Designdokument ist sonst vollständig | Zahl der Rückfragen je Durchgang ≤ 5 |
| R5 | Erste Freigabe vollständig | Abschnitte 6 und 8 des Designdokuments | Zusammenfassung nennt Klasse, Bereitstellung, Prüfperson, „personenbezogene Daten: nein“ und die Architektur in Alltagssprache |
| R6 | Architektur mit freigaberelevanten Entscheidungen und Entfernungsanleitung | Erste Freigabe | Beide Abschnitte in `architecture.md` ausgefüllt |
| R7 | Vollständige Aufgaben-Briefs | Alle Aufgaben | Jeder Brief hat QA-Stufe und konkrete QA-Prüfkriterien |
| R8 | Release-Aufgabe zuletzt | Backlog | Letzte Zeile ist `REL` |
| R9 | Kurzlebige Threads | Ganzer Lauf | PO-Sitzung pro Phase bzw. Block neu; SP und QA als Subagenten pro Aufgabe |
| R10 | `status.md` unter 100 Zeilen, Archiv | Mehr als fünf Übergaben im Lauf | `status.md` ≤ 100 Zeilen; bei mehr als fünf Übergaben `status-archive.md` gefüllt |
| R11 | Ein Commit pro Aufgabe, nichts direkt auf `main` | Ganzer Lauf | `git log main`: Start-Commit plus ein Commit pro Aufgabe oder Phase, alle mit ID |
| R12 | Feature-Schalter für Änderbares | F02 ist als änderbar markiert | F02 hat einen Ein/Aus-Schalter in der Konfiguration |
| R13 | Feature sauber entfernbar | Änderungswunsch Ä1, Teil a: F02 entfernen | Diff berührt nur Modul, Registrierung, Tests und Doku; alle Tests grün |
| R14 | Regel „berührt Freigabe“ | Ä1, Teil b: Speicher von JSON auf SQLite | SP markiert „touches gate“; QA prüft die Architekturänderung; der PO holt eine erneute Freigabe ein |
| R15 | Adapter für Außenwelt | Ä1, Teil b | Diff des Speicherwechsels liegt fast nur im Speicher-Adapter und der Datenübernahme |
| R16 | Konfiguration geprüft beim Start | `KASSENBUCH_DATA` | Ungültiger Pfad führt zu klarer Fehlermeldung, Test vorhanden |
| R17 | Performance messen | Erfolgskriterium 100.000 Einträge | Benchmark-Test vorhanden und grün |
| R18 | Fehlerbehebung beginnt mit rotem Test | Jeder QA-Befund | Im Branch-Verlauf erst roter Test, dann Fix |
| R19 | QA-Stufen | Gemischte Aufgaben | Stufe A/B/C im Brief, QA wiederholt die volle Suite nur bei C |
| R20 | Keine CI für reine Doku | Phasen-Branches `PLAN`, `REL` | CI-Workflow mit `paths-ignore`; keine CI-Läufe für Doku-Commits |
| R21 | Kein Abfragen der CI in Schleifen | Ganzer Lauf | Keine wiederholten CI-Abfragen in den Protokollen; Wartezeilen in `status.md` |
| R22 | Push vor jeder Übergabe | Ganzer Lauf | Jede Übergabe nennt einen gepushten Branch; am Ende liegt kein Branch nur lokal |
| R23 | Anleitung für die manuelle Prüfung | Aufgabe `REL` | `docs/manual-test.md` auf Deutsch, für Windows, ohne Entwicklerwissen ausführbar |
| R24 | Freigaben nur ausdrücklich | Freigaben 1, 1b (nach Ä1), 3 | Kein Merge einer Phase ohne ausdrückliche Antwort des Entscheiders |
| R25 | Sicherheitsregeln für Abhängigkeiten und CI | CI-Workflow, Entwicklungswerkzeuge (pytest, ruff, mypy), Eingabeprüfung | Actions per Commit-SHA eingebunden; Abhängigkeiten mit fixierter Version; Negativtests für ungültige Eingaben |

## 4. Designdokument

Dieses Dokument wird unverändert an den Koordinator übergeben (Datei `Referenzprojekt-Designdokument.md`). Es enthält mit Absicht genau einen Widerspruch (N3 gegen F02), um die Lückenanalyse zu prüfen, und ist bewusst neutral geschrieben: Nichts darin verrät, dass es sich um einen Messlauf handelt. Alle Fragen, die im ersten Lauf unvorhergesehen waren (personenbezogene Daten, Bereitstellung, macOS, Beträge in PowerShell), sind darin bereits beantwortet.

{{DESIGN}}

## 5. Entscheidungsregeln des Entscheiders

Der Entscheider spielt den Auftraggeber: Er antwortet auf Deutsch, knapp und freundlich, wie ein Mensch ohne Entwicklerwissen. Er nennt nie Regelnummern, Kennzahlen, Teil 3 oder die Messung. Er antwortet wörtlich nach diesen Regeln.

**Für alles, was hier nicht steht:**

- Würde die Antwort eine zusätzliche Rolle, eine andere Projektklasse oder personenbezogene Daten bedeuten: **„Nein. Bleib bei Klasse S ohne zusätzliche Rollen.“**
- Sonst: **„Entscheide nach bestem Ermessen und vermerke es im Designdokument.“**

Beides zählt als unvorhergesehene Frage.

**Koordinator**

Direkt nach dem Startprompt aus Teil 2 §4 sendet der Entscheider in derselben Nachricht diese Zusatzangaben:

```text
Repository: <konto>/kassenbuch-<Version>. It is already created from
the template and is the current folder; do not create another one.
The design document is in _handover/Referenzprojekt-Designdokument.md.
Delete the _handover folder after you have taken it over.
```

| Frage | Antwort |
| --- | --- |
| Projektname | Kassenbuch |
| Repository | „Ist schon angelegt, es ist der aktuelle Ordner.“ |
| Projektklasse | S |
| Feste Vorgaben | „Stehen im Designdokument, Abschnitt 11. Sonst keine.“ |
| Vorhandenes Material | „Nein.“ |

**PO, Phase Plan**

| Frage oder Ereignis | Antwort |
| --- | --- |
| Widerspruch N3 gegen F02 | „F02 hat Vorrang. N3 lautet neu: Das Programm schreibt keine Dateien außer seiner Datendatei und der vom Nutzer verlangten Exportdatei.“ |
| Personenbezogene Daten | „Nein, wie im Designdokument.“ |
| Andere Systeme als Windows | „Nein, nur Windows.“ |
| Merge einer Doku-Phase ohne CI | „Ja, das ist in Ordnung.“ |
| Erste Freigabe | „Freigeben“, wenn Bereitstellung und Prüfperson genannt sind und `architecture.md` die freigaberelevanten Entscheidungen und die Entfernungsanleitung enthält (der Entscheider liest die Datei); sonst „Zurück an PO, weil … fehlt“. |

**PO, Umsetzung**

Der Entscheider gibt nichts vor, außer einem Änderungswunsch. Sind F01 und F02 auf `main` und hat die laufende PO-Sitzung geendet, startet das Skript eine neue PO-Sitzung für die Phase „Change“; deren erste Nachricht ist:

> **Ä1:** „Zwei Änderungen: Den CSV-Export brauchen wir nicht mehr, bitte F02 vollständig entfernen. Außerdem sollen die Daten künftig in einer SQLite-Datei statt in JSON gespeichert werden; vorhandene JSON-Daten müssen beim ersten Start automatisch übernommen werden.“

| Ereignis | Antwort |
| --- | --- |
| Erneute Freigabe nach Ä1 (Speicherwechsel) | „Freigeben“. Kommt keine Freigabe-Anfrage, gilt R14 als nicht erfüllt. |
| Eskalation nach zwei Fehlrunden | „Teile die Aufgabe und mach weiter.“ |
| Bitte, die CI oder einen Merge zu prüfen | „Bitte prüf das selbst.“ |

**PO, Release**

1. Der Entscheider führt `docs/manual-test.md` aus, als wäre er der darin genannte Nicht-Entwickler: Er tut genau, was dort steht, nicht mehr, misst die Zeit und notiert jeden Schritt, der Entwicklerwissen voraussetzt oder nicht wie beschrieben funktioniert. Er arbeitet dazu in einer Kopie des Projekts in einem Wegwerf-Ordner, nie im Projektordner.
2. Freigabe 3: „Freigeben“, wenn alle Schritte ohne eigenes Zusatzwissen funktionieren und die Prüfung unter 10 Minuten dauert; sonst „Zurück an PO“ mit der Nummer des Schritts, der gehakt hat.

## 6. Technischer Ablauf

**Einmalige Einrichtung (etwa 15 Minuten)**

1. **Abo-Schlüssel:** Auf deinem Rechner `claude setup-token` ausführen und den angezeigten Schlüssel in `bibel-labor` unter *Settings → Secrets and variables → Actions* als Secret `CLAUDE_CODE_OAUTH_TOKEN` speichern. Damit laufen alle Aufrufe über dein Abo.
2. **GitHub-Schlüssel:** Unter *GitHub → Settings → Developer settings → Fine-grained tokens* einen Token anlegen: Eigentümer dein Konto, Zugriff auf alle Repositories, Rechte *Administration*, *Contents* und *Workflows* jeweils mit Lesen und Schreiben, dazu *Actions* und *Commit statuses* nur Lesen (ohne sie sieht der PO nicht, ob die CI grün ist). Als Secret `BIBEL_GH_TOKEN` speichern. Damit legt der Lauf das Projekt-Repository an, und die Rollen können pushen.
3. **Vorlage:** Das Vorlagen-Repository ist als „Template repository“ markiert. Die zu messende Version bringt der Workflow *Vorlage veröffentlichen* auf `main`, samt Release `v<Version>`; mit der Option „Danach den Referenzlauf starten“ folgt der Lauf automatisch.

**Start:** Am besten direkt nach dem Zurücksetzen des Nutzungslimits, damit der Lauf in ein Nutzungsfenster passt. In `bibel-labor` unter *Actions → Referenzlauf → Run workflow*. Eingaben: Version (leer = aktuelle Version), Kostenbremse für den ganzen Lauf (Standard 20 USD), Berechtigungsmodus (Standard `auto`; `bypassPermissions` nur, wenn `auto` nicht verfügbar ist, denn der Rechner von GitHub wird nach dem Lauf gelöscht).

**Ablauf des Skripts**

1. **Einrichtung:** Projekt-Repository aus der Vorlage anlegen und klonen, Designdokument nach `_handover/` legen.
2. **Koordinator:** neue Sitzung mit dem Startprompt aus dem Handbuch des Projekts (`docs/handbook/04-coordinator-start.md`) und den Zusatzangaben aus Abschnitt 5. Der Entscheider beantwortet jede Nachricht, bis der Koordinator fertig ist.
3. **PO pro Phase:** für jede Phase bzw. jeden Block eine neue Sitzung mit dem PO-Startprompt (`docs/templates/thread-start.md`). Der Entscheider beantwortet jede Nachricht und meldet, wann eine Phase fertig ist und welche folgt.
4. **Änderung:** Sind F01 und F02 auf `main`, startet das Skript eine neue PO-Sitzung für die Phase „Change“ und sendet Ä1 als erste Nachricht.
5. **Release:** Bittet der PO um die manuelle Prüfung oder Freigabe 3, startet das Skript den manuellen Prüfer in einer Kopie von `main`. Danach entscheidet der Entscheider über Freigabe 3.
6. **Auswertung:** Auditor-Sitzung mit dem Prompt aus Abschnitt 8, nur mit Leserechten.
7. **Bericht:** Kennzahlen exakt aus dem Protokoll, Regeltreue vom Auditor, die Texte für Ergebnis, Kostentreiber, Auffälligkeiten und Empfehlungen von einem kurzen Claude-Aufruf. Das Skript schreibt `bericht.md` und trägt den Lauf in `ergebnisse.md` ein. Nach dem Lauf erzeugt der Workflow *Bericht* die PDF und speichert alles in `bibel-labor`; er lässt sich für einen Lauf auch von Hand starten (Eingabe: Lauf-Nummer).

**Messung:** Jeder Aufruf steht als Zeile in `messungen/protokolle/<Version>/<Lauf>/lauf.jsonl`: Zeit, Rolle, Phase, Sitzung, gekürzte Nachricht und Antwort, `num_turns`, `total_cost_usd`, `modelUsage` und abgelehnte Berechtigungen. Die vollständigen Antworten liegen daneben in `antworten/`. `total_cost_usd` und `modelUsage` zählen über eine fortgesetzte Sitzung weiter; das Skript nimmt deshalb pro Sitzung den letzten Wert, statt die Aufrufe zu addieren. `num_turns` gilt pro Aufruf und wird addiert.

**Kostenbremse:** Jeder Aufruf bekommt `--max-budget-usd 8`; die Grenze liegt bewusst weit über dem Bedarf einer Aufgabe, damit keine Rolle wegen ihr früher aufhört. Bricht ein Aufruf daran ab, setzt das Skript dieselbe Sitzung einmal mit „Bitte mach weiter.“ fort. Übersteigen die Projekt-Sitzungen zusammen die Kostenbremse des Laufs, endet der Lauf; Auditor und Bericht laufen trotzdem, als Teilbericht.

**Limit:** Erreicht ein Aufruf das Nutzungslimit, wartet das Skript jeweils 15 Minuten und versucht es erneut, insgesamt höchstens 4 Stunden. Die Wartezeit zählt nicht zur Laufzeit; das Erreichen des Limits steht im Bericht.

**Sicherheitsnetz:** Ein Aufruf, der länger als 45 Minuten läuft, wird beendet. Gibt der Entscheider dreimal hintereinander dieselbe Antwort, steckt die Rolle fest; das Skript beendet den Lauf mit dieser Meldung. Ebenso eine Phase, die nach 15 Antworten nicht abgeschlossen ist, oder mehr als 10 Phasen. Abgelehnte Berechtigungen werden nicht umgangen, sondern gezählt. Außer bei der Einrichtung ändert das Skript nie Dateien im Projekt.

**Probelauf ohne Kosten:** `python werkzeuge/referenzlauf.py --owner test --dry-run` mit einer Attrappe für `claude` (Umgebungsvariable `CLAUDE_BIN`) prüft den Ablauf lokal, ohne GitHub und ohne Tokens.

## 7. Kennzahlen

| Kennzahl | Quelle |
| --- | --- |
| Tokens gesamt | Summe aus `modelUsage` aller Projekt-Sitzungen (ohne Entscheider und Auditor) |
| Kostenschätzung (USD, API-Gegenwert) | Summe `total_cost_usd` derselben Sitzungen |
| davon Koordinator / PO-Sitzungen | je Sitzung aus dem Protokoll; SP und QA laufen als Subagenten in den PO-Sitzungen und sind dort enthalten |
| Schritte | Summe `num_turns` |
| Aktive Laufzeit | erster bis letzter Aufruf, ohne Wartezeit auf Limits |
| Limit erreicht | ja/nein, Dauer |
| Sitzungen | Anzahl aller Projekt-Sitzungen |
| Aufgaben | Anzahl im Backlog, einschließlich `REL` und Härtung |
| Erstdurchlauf | Aufgaben mit „PASS“ in der ersten QA-Runde, in Prozent |
| QA-Runden | Summe aller QA-Runden |
| Echte Befunde | QA-Befunde, die einen Fehler belegen (keine Hinweise) |
| Rückfragen | Rückfragen in der Planphase; davon unvorhergesehen |
| Abgelehnte Berechtigungen | Summe `permission_denials` |
| Regeltreue | erfüllte Regeln R1 bis R25 von 25 |
| Manuelle Prüfung | Minuten, Zahl der problematischen Schritte |
| Tests | Anzahl Tests am Ende, CI grün ja/nein |

## 8. Auswertungs-Prompt

Das Skript startet am Ende eine neue, unabhängige Sitzung im Projektordner mit diesem Prompt und gibt ihr die Pfade zu Teil 3 und zum Protokoll mit, nur mit Leserechten. Die Auswertung ist die einzige Sitzung im Projektordner, die Teil 3 kennt; sie läuft erst, wenn alle Projekt-Sitzungen beendet sind.

```text
Project: Kassenbuch · Role: Auditor
You audit a finished reference run of the KI-Projekt-Bibel. Part 3 is
at <path>. Do not change any file. Read only what you need: git log of
main and of all remote branches, the diff of the first commit against
the template repository, docs/status.md, docs/status-archive.md,
docs/backlog.md, docs/tasks/*.md, docs/architecture.md, docs/roles/,
.claude/, .github/workflows/, docs/manual-test.md, and the run log at
<path to lauf.jsonl>.

1. Fill the metrics from Part 3 §7 that the repository and the log can
   show: sessions, turns, tasks, first-pass rate, QA rounds, real
   findings, permission denials, tests, CI status.
2. Check every rule R1 to R25 from Part 3 §3. For each: met / not met /
   not checkable, with one line of evidence (file, commit or log line).
3. List the three biggest cost drivers you can see, each with evidence.
4. End with exactly one line of JSON, nothing after it:
   {"regeln_erfuellt": n, "regeln_gesamt": n, "aufgaben": n,
    "erstdurchlauf_prozent": n, "qa_runden": n, "echte_befunde": n,
    "tests": n, "ci_gruen": true|false}

Answer in German, as two tables, one short list and the JSON line.
No other text.
```

## 9. Prüfbericht (PDF)

Der Bericht ist auf Deutsch, für einen Leser ohne Entwicklerwissen. Ablage: `messungen/berichte/Pruefbericht-Bibel-<Version>-<Lauf>.pdf` in `bibel-labor`; zusätzlich steht er im Workflow-Lauf zum Herunterladen bereit.

1. **Ergebnis in drei Sätzen:** Verbrauch gegenüber der Vorversion (in Prozent), Regeltreue, Qualität.
2. **Kennzahlen:** Tabelle aus Abschnitt 7, mit Spalte der Vorversion und Veränderung in Prozent.
3. **Regeltreue:** R1 bis R25 mit erfüllt / nicht erfüllt / nicht prüfbar und Beleg.
4. **Größte Kostentreiber:** die drei aus der Auswertung, mit Beleg.
5. **Auffälligkeiten:** abgelehnte Berechtigungen, abgebrochene Sitzungen, Limit, unvorhergesehene Fragen, Abweichungen von Abschnitt 2.
6. **Manuelle Prüfung:** Dauer, problematische Schritte, Hinweis, dass ein Mensch die Verständlichkeit mit einer 10-Minuten-Stichprobe bestätigen sollte.
7. **Empfehlungen für die nächste Bibel-Version:** höchstens fünf, jede mit dem Befund, auf dem sie beruht.

## 10. Ergebnisgeschichte

Die Datei `messungen/ergebnisse.md` hält alle Läufe fest: eine Spalte pro Lauf, neue Läufe rechts. Das Skript nimmt die letzte gültige Spalte als Vergleichswert und trägt den neuen Lauf ein.

| Kennzahl | Bibel 1.4 (abgebrochen) | Bibel 1.8 |
| --- | --- | --- |
| Datum | 1.–2. Nov. 2026 | |
| Claude-Code-Version | 2.1.302 | |
| Tokens gesamt | 7.187.320 (bis Abbruch) | |
| Kostenschätzung (USD) | 12,03 (bis Abbruch) | |
| davon Koordinator | 3,86 | |
| davon PO-Sitzungen (inkl. SP und QA) | 8,17 | |
| Schritte | 184 | |
| Aktive Laufzeit | 50 Min. | |
| Limit erreicht | ja, nach 50 Min. | |
| Sitzungen | 4 | |
| Aufgaben | – | |
| Erstdurchlauf | – | |
| QA-Runden | – | |
| Echte Befunde | – | |
| Rückfragen (davon unvorhergesehen) | 6 (5) | |
| Abgelehnte Berechtigungen | 2 | |
| Regeltreue | nicht bewertet | / 25 |
| Manuelle Prüfung (Minuten) | – | |
| Tests, CI grün | 0, keine CI | |
| Bemerkung | Größeres Projekt (fünf Funktionen, zwei Änderungswünsche), abgebrochen in der Architekturphase; nicht vergleichbar, nur Anhaltspunkt | Erster gültiger Lauf mit dem verkleinerten Projekt |

Der Solitaire-Pilot (Bibel 1.0, 341 Mio. Tokens, 15,5 Stunden) ist ein anderes Projekt und deshalb kein Vergleichswert.

## 11. Ausweichweg: Lauf auf deinem Rechner

Ist GitHub Actions nicht verfügbar, läuft derselbe Ablauf auf deinem Rechner:

1. `bibel-labor` klonen, `gh auth login` und `gh auth refresh -s workflow` ausführen, Claude Code angemeldet.
2. Im Ordner `bibel-labor`: `python werkzeuge/referenzlauf.py --owner <konto>`. Das Fenster bleibt bis zum Ende offen.
3. Danach `python werkzeuge/bericht.py <Protokollordner>` (braucht `pip install -r werkzeuge/requirements.txt`) und die Ergebnisse committen und pushen.

Die Projekt-Sitzungen laufen dann unter deinem Betriebssystem; das steht im Bericht als Abweichung von Abschnitt 2.
