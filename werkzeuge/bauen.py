"""Builds the two PDFs of the Bible (Parts 1+2, Part 3) from quelle/ into ausgabe/."""
import json
import re
from pathlib import Path

import markdown
from weasyprint import HTML

from teil3 import assemble as assemble_teil3

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "quelle"
OUT = ROOT / "ausgabe"
META = json.loads((SRC / "version.json").read_text(encoding="utf-8"))
V, DATE = META["version"], META["datum"]
OUT_RULES = OUT / f"KI-Projekt-Bibel_v{V}.pdf"
OUT_REF = OUT / f"KI-Projekt-Bibel_v{V}_Teil3_Referenzprojekt.pdf"
OUT_TEIL3_MD = OUT / "teil3.md"


ACCENT = "#1d4f91"
ACCENT_TINT = "#e6eef8"
INK = "#1a1d23"
QUIET = "#5b6270"
EDGE = "#9aa1ad"


def flow_svg() -> str:
    W, H = 128, 52
    rowA, rowB = 110, 250
    c1, c2, g1, c3, g2 = 88, 248, 380, 520, 672
    gq, cm, g3 = 400, 536, 680

    def box(cx, cy, name, sub):
        return (
            f'<rect x="{cx - W / 2}" y="{cy - H / 2}" width="{W}" height="{H}" rx="8" '
            f'fill="none" stroke="{EDGE}" stroke-width="1.25"/>'
            f'<text x="{cx}" y="{cy - 3}" text-anchor="middle" font-weight="600" fill="{INK}">{name}</text>'
            f'<text x="{cx}" y="{cy + 15}" text-anchor="middle" font-size="11.5" fill="{QUIET}">{sub}</text>'
        )

    def diamond(cx, cy, label, gate):
        fill = ACCENT_TINT if gate else "none"
        stroke = ACCENT if gate else EDGE
        sw = 2 if gate else 1.25
        return (
            f'<polygon points="{cx - 48},{cy} {cx},{cy - 40} {cx + 48},{cy} {cx},{cy + 40}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="12" font-weight="600" fill="{INK}">{label}</text>'
        )

    paths = [
        f"M{c1 + W / 2} {rowA}H{c2 - W / 2}",
        f"M{c2 + W / 2} {rowA}H{g1 - 48}",
        f"M{g1 + 48} {rowA}H{c3 - W / 2}",
        f"M{c3 + W / 2} {rowA}H{g2 - 48}",
        f"M{g2} {rowA + 40}V190H{c1}V{rowB - H / 2}",
        f"M{c1 + W / 2} {rowB}H{c2 - W / 2}",
        f"M{c2 + W / 2} {rowB}H{gq - 48}",
        f"M{gq + 48} {rowB}H{cm - W / 2}",
        f"M{cm + W / 2} {rowB}H{g3 - 48}",
        f"M{gq} {rowB + 40}V320H{c2}V{rowB + H / 2}",
        f"M{cm} {rowB + H / 2}V360H{c1}V{rowB + H / 2}",
    ]
    arrows = "".join(
        f'<path d="{d}" fill="none" stroke="{EDGE}" stroke-width="1.25" marker-end="url(#arrow)"/>'
        for d in paths
    )
    return f"""
<svg class="flow" viewBox="0 0 760 392" xmlns="http://www.w3.org/2000/svg" font-family="Inter" font-size="13">
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M0 0L10 5L0 10z" fill="{EDGE}"/></marker></defs>
  <text x="24" y="34" font-size="15" font-weight="600" fill="{INK}">Menschliche Freigaben steuern jedes Projekt</text>
  {arrows}
  {box(c1, rowA, "Start", "Koordinator")}
  {box(c2, rowA, "Design", "Mensch + PO")}
  {diamond(g1, rowA, "Freigabe 1", True)}
  {box(c3, rowA, "Architektur", "SP, Prüfung QA")}
  {diamond(g2, rowA, "Freigabe 2", True)}
  {box(c1, rowB, "Backlog", "PO")}
  {box(c2, rowB, "Umsetzen", "SP + Tests")}
  {diamond(gq, rowB, "QA prüft", False)}
  {box(cm, rowB, "Squash-Merge", "PO, CI grün")}
  {diamond(g3, rowB, "Freigabe 3", True)}
  <text x="{g2 - 8}" y="{rowA + 56}" text-anchor="end" font-size="11.5" fill="{QUIET}">entfällt in Klasse S</text>
  <text x="{g3}" y="{rowB + 58}" text-anchor="middle" font-size="11.5" fill="{QUIET}">vor Release</text>
  <text x="462" y="{rowB - 12}" text-anchor="middle" font-size="11.5" fill="{QUIET}">ja</text>
  <text x="324" y="312" text-anchor="middle" font-size="11.5" fill="{QUIET}">Befund</text>
  <text x="312" y="378" text-anchor="middle" font-size="11.5" fill="{QUIET}">nächste Aufgabe</text>
</svg>"""


def slug(text: str, prefix: str) -> str:
    s = re.sub(r"<[^>]+>", "", text).lower()
    s = re.sub(r"[^a-z0-9äöüß]+", "-", s).strip("-")
    return f"{prefix}-{s}"


def render(src: str, prefix: str):
    html = markdown.markdown(src, extensions=["tables", "fenced_code", "sane_lists"])
    html = html.replace("<p>[[DIAGRAMM]]</p>", f'<figure class="diagram">{flow_svg()}</figure>')
    html = re.sub(r"<p>(<strong>[^<]*(?:<code>[^<]*</code>[^<]*)*</strong>)</p>", r'<p class="label">\1</p>', html)
    toc = []

    def add_id(m):
        level, inner = m.group(1), m.group(2)
        anchor = slug(inner, prefix)
        toc.append((level, re.sub(r"<[^>]+>", "", inner), anchor))
        return f'<h{level} id="{anchor}">{inner}</h{level}>'

    html = re.sub(r"<h([12])>(.*?)</h\1>", add_id, html)
    return html, toc


OUT.mkdir(exist_ok=True)
teil3 = assemble_teil3()
OUT_TEIL3_MD.write_text(teil3, encoding="utf-8")
part1, toc1 = render((SRC / "teil1.md").read_text(encoding="utf-8"), "t1")
part2, toc2 = render((SRC / "teil2.md").read_text(encoding="utf-8"), "t2")
part3, toc3 = render(teil3, "t3")

css = f"""
@page {{
  size: A4; margin: 22mm 20mm 22mm 20mm;
  @bottom-left {{ content: "KI-Projekt-Bibel · Version {V}"; font: 8pt Inter; color: {QUIET}; }}
  @bottom-right {{ content: counter(page); font: 8pt Inter; color: {QUIET}; }}
}}
@page cover {{ margin: 0; @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
html {{ font-family: Inter, sans-serif; font-size: 9.6pt; line-height: 1.5; color: {INK}; }}
.cover {{ page: cover; height: 297mm; padding: 0; position: relative; break-after: page; }}
.cover .band {{ background: {ACCENT}; height: 118mm; padding: 40mm 22mm 0 22mm; color: white; }}
.cover .kicker {{ font-size: 10pt; letter-spacing: 0.14em; text-transform: uppercase; opacity: 0.8; }}
.cover h1.title {{ font-size: 36pt; line-height: 1.1; margin: 8mm 0 6mm; font-weight: 700; color: white; border: none; }}
.cover .sub {{ font-size: 13pt; max-width: 140mm; opacity: 0.92; }}
.cover .meta {{ padding: 18mm 22mm; font-size: 10.5pt; color: {QUIET}; }}
.cover .meta b {{ color: {INK}; }}
.cover .parts {{ padding: 0 22mm; display: flex; gap: 8mm; }}
.cover .part {{ border-top: 2pt solid {ACCENT}; padding-top: 4mm; width: 52mm; }}
.cover .part h3 {{ margin: 0 0 2mm; font-size: 12pt; }}
.cover .part p {{ margin: 0; color: {QUIET}; }}
nav.toc {{ break-after: page; }}
nav.toc h2 {{ font-size: 18pt; margin: 0 0 6mm; border: none; }}
nav.toc ul {{ list-style: none; padding: 0; margin: 0; }}
nav.toc li a {{ color: {INK}; text-decoration: none; }}
nav.toc li a::after {{ content: leader(".") target-counter(attr(href), page); color: {QUIET}; }}
nav.toc .toc-part {{ font-weight: 700; font-size: 11pt; margin: 6mm 0 2mm; color: {ACCENT}; }}
nav.toc .toc-part a {{ color: {ACCENT}; }}
nav.toc .toc-sec {{ margin: 1.2mm 0 1.2mm 4mm; }}
section.part {{ break-before: page; }}
h1 {{ font-size: 24pt; color: {ACCENT}; margin: 0 0 6mm; padding-bottom: 3mm; border-bottom: 1.5pt solid {ACCENT}; }}
h2 {{ font-size: 13.5pt; margin: 9mm 0 2.5mm; color: {INK}; break-after: avoid; }}
h2 + p {{ break-before: avoid; }}
p {{ margin: 0 0 2.6mm; }}
p.label {{ margin-top: 4mm; break-after: avoid; }}
ul, ol {{ margin: 0 0 3mm; padding-left: 5.5mm; }}
li {{ margin: 0.8mm 0; }}
strong {{ font-weight: 650; }}
code {{ font-family: "DejaVu Sans Mono", monospace; font-size: 8pt; background: #f1f3f6; padding: 0.2mm 1mm; border-radius: 2px; }}
pre {{ background: #f5f7fa; border: 0.6pt solid #dde1e7; border-left: 2.5pt solid {ACCENT}; border-radius: 3px;
       padding: 3mm 3.5mm; margin: 2mm 0 4mm; white-space: pre-wrap; overflow-wrap: anywhere; }}
pre code {{ background: none; padding: 0; font-size: 7.6pt; line-height: 1.42; }}
table {{ border-collapse: collapse; width: 100%; margin: 2mm 0 4mm; font-size: 8.4pt; }}
thead {{ display: table-header-group; }}
th {{ text-align: left; background: {ACCENT_TINT}; color: {INK}; font-weight: 650; }}
th, td {{ border-bottom: 0.6pt solid #dde1e7; padding: 1.6mm 2mm; vertical-align: top; }}
tr {{ break-inside: avoid; }}
table + p {{ break-before: avoid; }}
tr:last-child {{ break-after: avoid; }}
figure.diagram {{ margin: 3mm 0 3mm; break-inside: avoid; }}
svg.flow {{ width: 100%; height: auto; }}
"""


def toc_for(tocs):
    out = ""
    for level, text, anchor in tocs:
        cls = "toc-part" if level == "1" else "toc-sec"
        out += f'<li class="{cls}"><a href="#{anchor}">{text}</a></li>'
    return out


def page(title, sub, cards, tocs, sections, footer):
    c = css.replace(f"KI-Projekt-Bibel · Version {V}", footer)
    cards_html = "".join(f'<div class="part"><h3>{h}</h3><p>{t}</p></div>' for h, t in cards)
    body = "".join(f'<section class="part">{x}</section>' for x in sections)
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>{title}</title><style>{c}</style></head><body>
<div class="cover">
  <div class="band">
    <div class="kicker">Leitfaden für KI-Projekte</div>
    <h1 class="title">{title}</h1>
    <div class="sub">{sub}</div>
  </div>
  <div class="meta"><b>Version {V}</b> · {DATE}</div>
  <div class="parts">{cards_html}</div>
</div>
<nav class="toc"><h2>Inhalt</h2><ul>{toc_for(tocs)}</ul></nav>
{body}
</body></html>"""


rules = page(
    "KI-Projekt-Bibel",
    "Grundformel und Handbuch für effiziente, robuste, sichere und jederzeit änderbare KI-Projekte",
    [("Teil 1: Grundformel", "Das verbindliche Regelwerk. Liegt als docs/grundformel.md fertig im Vorlagen-Repository."),
     ("Teil 2: Handbuch", "Startprompts, Rollendateien und Vorlagen. Liegen fertig im Vorlagen-Repository und werden nur gezielt nachgeschlagen.")],
    toc1 + toc2, [part1, part2], f"KI-Projekt-Bibel · Version {V}")
ref = page(
    "Referenzprojekt",
    "Teil 3 der KI-Projekt-Bibel: Messlauf für jede neue Version. Nur für den Menschen, nie an Koordinator oder Rollen übergeben.",
    [("Nur für dich", "Enthält Drehbuch, eingebaute Stolpersteine und Prüfliste. Würde eine KI das lesen, wäre der Messlauf verfälscht.")],
    toc3, [part3], f"KI-Projekt-Bibel · Teil 3 · Version {V} · nicht an KI übergeben")
HTML(string=rules, base_url=str(ROOT)).write_pdf(OUT_RULES)
HTML(string=ref, base_url=str(ROOT)).write_pdf(OUT_REF)
print("written", OUT_RULES, OUT_REF)
