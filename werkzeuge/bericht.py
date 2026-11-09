"""Turns a run's bericht.md into berichte/Pruefbericht-Bibel-<version>-<run>.pdf."""
import json
import sys
from pathlib import Path

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
CSS = """
@page { size: A4; margin: 20mm 18mm; @bottom-right { content: counter(page); font: 8pt sans-serif; color: #5b6270; } }
html { font-family: Inter, "DejaVu Sans", sans-serif; font-size: 9.6pt; line-height: 1.5; color: #1a1d23; }
h1 { font-size: 22pt; color: #1d4f91; border-bottom: 1.5pt solid #1d4f91; padding-bottom: 3mm; }
h2 { font-size: 13pt; margin: 8mm 0 2mm; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 4mm; font-size: 8.4pt; }
th { text-align: left; background: #e6eef8; }
th, td { border-bottom: 0.6pt solid #dde1e7; padding: 1.4mm 2mm; vertical-align: top; }
tr { break-inside: avoid; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8pt; background: #f1f3f6; padding: 0 1mm; }
"""


def main(run_dir: str) -> None:
    folder = ROOT / run_dir
    metrics = json.loads((folder / "kennzahlen.json").read_text(encoding="utf-8"))
    body = markdown.markdown((folder / "bericht.md").read_text(encoding="utf-8"), extensions=["tables", "sane_lists"])
    target = ROOT / "messungen" / "berichte" / f"Pruefbericht-Bibel-{metrics['version']}-{metrics['lauf']}.pdf"
    target.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>').write_pdf(target)
    print(target.relative_to(ROOT))


if __name__ == "__main__":
    main(sys.argv[1])
