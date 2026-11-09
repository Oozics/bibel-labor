"""Assembles Part 3 (with the embedded reference design document) without any PDF dependencies."""
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "quelle"


def assemble() -> str:
    """Part 3 embeds the reference design document; its version line is neutralised."""
    design = (SRC / "referenz-designdokument.md").read_text(encoding="utf-8").strip()
    design = re.sub(r"Grundformel-Version: [0-9.]+", "Grundformel-Version: [aktuelle Version]", design)
    if "```" in design:
        raise SystemExit("design document must not contain code fences")
    return (SRC / "teil3_quelle.md").read_text(encoding="utf-8").replace("{{DESIGN}}", "```markdown\n" + design + "\n```")


def write(target: Path) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(assemble(), encoding="utf-8")
    return target
