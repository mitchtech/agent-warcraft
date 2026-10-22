"""Write the nine-row web pet atlas from the active sprite sheet and record its hash. Requires requirements-dev.txt."""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def export(pet_id="peon"):
    SHEET = ROOT / "pets" / pet_id / "spritesheet.webp"
    prefix = "agent-warcraft" if pet_id == "peon" else "agent-warcraft-peasant"
    EXPORT = ROOT / "assets" / "exports" / f"{prefix}-pet-web.webp"
    REVISION = ROOT / "assets" / ("pet-revision.json" if pet_id == "peon" else "peasant-pet-revision.json")
    with Image.open(SHEET) as source:
        # The web format keeps the nine animation rows and drops the two look-direction rows.
        web = source.convert("RGBA").crop((0, 0, 1536, 1872))
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    web.save(EXPORT, lossless=True, quality=100, method=6, exact=True)
    revision = json.loads(REVISION.read_text(encoding="utf-8"))
    revision["web"] = {"file": EXPORT.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(EXPORT.read_bytes()).hexdigest()}
    REVISION.write_text(json.dumps(revision, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {EXPORT.relative_to(ROOT)} ({EXPORT.stat().st_size} bytes)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pet", choices=["peon", "peasant"])
    args = parser.parse_args()
    for pet_id in [args.pet] if args.pet else ["peon", "peasant"]:
        export(pet_id)
