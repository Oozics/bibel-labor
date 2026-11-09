# bibel-labor

Arbeitsrepository der KI-Projekt-Bibel. **Privat halten**: Hier liegt Teil 3 (das Drehbuch des
Referenzlaufs). Kein Projekt und keine Projekt-Sitzung darf dieses Repository sehen.

## Inhalt

| Ordner | Inhalt |
| --- | --- |
| `quelle/` | Quelltexte der Bibel: Teil 1, Teil 2, Teil 3, Referenz-Designdokument, `version.json` |
| `werkzeuge/` | `bauen.py` (PDFs), `vorlage.py` (Vorlagen-Repository), `selbsttest.py`, `referenzlauf.py`, `bericht.py` |
| `messungen/` | `ergebnisse.md`, Protokolle und Prüfberichte aller Referenzläufe |
| `.github/workflows/` | Selbsttest bei jeder Änderung, Referenzlauf per Knopfdruck |

## Eine neue Bibel-Version

1. Texte in `quelle/` ändern, Version und Datum in `quelle/version.json` anpassen, Versionsgeschichte in Teil 1 ergänzen.
2. Pushen. Der Workflow **Selbsttest** prüft Verweise, Versionen, Vorlage und Hooks und baut die PDFs (unter *Actions* zum Herunterladen).
3. *Actions → Vorlage veröffentlichen → Run workflow*. Der Workflow prüft die Bibel, erzeugt die Vorlage, bringt sie auf `main` von `ki-projekt-vorlage`, legt das Release `v<Version>` an und startet auf Wunsch gleich den Referenzlauf.
4. Den Prüfbericht lesen.

## Referenzlauf

Einmalig: die Secrets `CLAUDE_CODE_OAUTH_TOKEN` und `BIBEL_GH_TOKEN` anlegen (Teil 3, Abschnitt 6).

Start: *Actions → Referenzlauf → Run workflow*. Der Lauf dauert etwa eine Stunde. Danach liegen in
`messungen/` das Protokoll, der Prüfbericht als PDF und die ergänzte `ergebnisse.md`; der Bericht steht
zusätzlich im Workflow-Lauf unter *Artifacts* bereit.

Probelauf ohne Kosten (lokal, mit einer Attrappe für `claude`):

```bash
CLAUDE_BIN=/pfad/zur/attrappe python werkzeuge/referenzlauf.py --owner test --dry-run
```

## Lokal arbeiten

```bash
pip install -r werkzeuge/requirements.txt
python werkzeuge/selbsttest.py --pdf
```
