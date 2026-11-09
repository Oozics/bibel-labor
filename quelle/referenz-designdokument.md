# Designdokument: Kassenbuch

Version: 1.0 · Status: Entwurf · Grundformel-Version: 1.6
Projektklasse: S

## 1. Zweck und Problem
Wer Einnahmen und Ausgaben im Blick behalten will, braucht dafür oft keine
große Software. Das Kassenbuch ist ein kleines Programm für die
Kommandozeile, mit dem eine Person ihre Buchungen erfasst und anzeigt und
bei Bedarf als Datei für Excel ausgibt. Es soll ohne Installation und ohne
Internet funktionieren.

## 2. Zielnutzer und Nutzungssituation
Eine Person am eigenen Windows-Rechner, ohne Programmierkenntnisse. Ein
Durchgang dauert wenige Minuten.

## 3. Funktionen
| ID | Nutzergeschichte | Priorität | MVP | Änderbar |
| --- | --- | --- | --- | --- |
| F01 | Als Nutzer möchte ich Einträge mit Datum, Betrag, Kategorie und Text erfassen und mir alle Einträge mit dem Saldo anzeigen lassen, damit ich meinen Stand kenne. | Muss | ja | nein |
| F02 | Als Nutzer möchte ich meine Einträge als CSV-Datei exportieren, damit ich sie in Excel öffnen kann. | Soll | ja | ja |

## 4. Nicht-Ziele
- N1: Keine grafische Oberfläche.
- N2: Kein Mehrbenutzerbetrieb, keine Bankanbindung, nur Euro.
- N3: Das Programm schreibt keine Dateien außer seiner Datendatei.
- N4: Kein Bearbeiten oder Löschen von Einträgen, kein Import, keine
  Filter oder Auswertungen.

## 5. Erfolgskriterien
- Jedes Akzeptanzkriterium ist automatisch getestet.
- Die Anzeige von 100.000 Einträgen mit Saldo dauert unter 1 Sekunde.
- Die Prüfperson besteht die manuelle Prüfung in unter 10 Minuten ohne Hilfe.
- F02 lässt sich entfernen, ohne Code außerhalb seines Moduls und der
  Registrierung zu ändern.

## 6. Daten
Nur Einträge, die die Person selbst eingibt.
Personenbezogene Daten: nein (Entscheidung des Auftraggebers). Testdaten
sind erfunden. Gespeichert lokal in einer Datei, aufbewahrt, bis die
Person die Datei löscht.

## 7. Externe Systeme und Schnittstellen
Keine. Dateisystem und Systemuhr (für das Standarddatum „heute“) gelten
als Außenwelt.

## 8. Plattform, Bereitstellung und Betrieb
Kommandozeilenprogramm. Bereitstellung: Die Person lädt das Repository
auf GitHub als ZIP-Datei herunter, entpackt es und startet das Programm in
PowerShell im entpackten Ordner mit `python -m kassenbuch`. Kein
Installer, kein Hosting.
Zielgerät: Windows 11 mit Python 3.12. Andere Systeme werden nicht
unterstützt.
Manuelle Prüfung: der Auftraggeber, Windows 11, Systemsprache Deutsch,
PowerShell, keine Entwicklerkenntnisse.
Betrieb: niemand, rein lokal.

## 9. Qualitätsanforderungen
Anzeige von 100.000 Einträgen mit Saldo unter 1 Sekunde auf einem
üblichen Laptop. Keine Verfügbarkeitsanforderung, offline.

## 10. Sicherheit und Datenschutz
Keine Anmeldung. Daten nur lokal. Der Pfad der Datendatei ist über die
Umgebungsvariable KASSENBUCH_DATA einstellbar; Standard ist
`kassenbuch.json` im aktuellen Ordner. Ungültige Eingaben werden mit einer
verständlichen deutschen Meldung abgelehnt.

## 11. Rahmenbedingungen
Feste Vorgaben: Python 3.12, zur Laufzeit nur die Standardbibliothek; zur
Entwicklung pytest, ruff und mypy (strict); GitHub Actions als CI; privates
GitHub-Repository.
Zeitrahmen: etwa eine Stunde.

## 12. Glossar
| Deutsch | Englisch | Bedeutung |
| --- | --- | --- |
| Kassenbuch | cash book | Das Programm und seine Daten |
| Eintrag | entry | Eine Einnahme oder Ausgabe |
| Betrag | amount | Euro mit Cent; negativ = Ausgabe |
| Kategorie | category | Freier Begriff, z. B. „Lebensmittel“ |
| Saldo | balance | Summe der Beträge |
| Export | export | Ausgabe als CSV-Datei |

## 13. Offene Fragen
Keine.

## Anhang A: Details
- Befehle: `add` (Eintrag erfassen), `list` (alle Einträge, darunter der
  Saldo), `export` (CSV-Datei).
- Eingabe Datum: TT.MM.JJJJ; ohne Angabe gilt heute.
- Eingabe Betrag: deutsches Format mit genau zwei Nachkommastellen, z. B.
  `-12,50` oder `1.200,00`. Gespeichert in Cent als ganze Zahl, keine
  Rundung. In Anleitungen stehen Beträge immer in Anführungszeichen,
  z. B. `"-12,50"`, weil PowerShell Zahlen sonst umdeutet.
- Kategorie: frei, 1 bis 30 Zeichen. Text: 0 bis 100 Zeichen.
- Ausgabe Beträge: deutsches Format mit Euro, z. B. `-1.234,56 €`.
- CSV: Trennzeichen Semikolon, Kodierung UTF-8 mit BOM (für Excel),
  Spalten Datum;Betrag;Kategorie;Text.

## Änderungsprotokoll
| Version | Datum | Änderung |
| --- | --- | --- |
| 1.0 | – | Erstfassung |
