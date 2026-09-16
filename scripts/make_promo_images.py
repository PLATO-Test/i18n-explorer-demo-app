"""Generate the calculator page's small promo images as PNGs with the
text baked into the pixels, same approach as make_banners.py (bundled
font, deterministic). File names are locale/build-neutral on purpose -
see A07 in ground_truth/defects.yaml.

Usage:
    uv run python scripts/make_promo_images.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from webapp.formatting import percent

ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = ROOT / "fonts" / "NotoSans-Regular.ttf"
OUTPUT_DIR = ROOT / "static" / "img"

WIDTH, HEIGHT = 480, 140
NAVY = (11, 47, 92)
GOLD = (201, 154, 60)
WHITE = (255, 255, 255)

PROMOS = {
    "promo-a.png": "Variable rate: " + percent(0.052, "en"),
    "promo-b.png": "Taux variable : " + percent(0.052, "fr"),
    "promo-c.png": "Taux fixe : " + percent(0.049, "fr"),
}


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size=size, layout_engine=ImageFont.Layout.BASIC)


def make_promo(text: str) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    draw.rectangle([(0, 0), (10, HEIGHT)], fill=GOLD)

    font = _font(30)
    draw.text((36, HEIGHT // 2 - 18), text, font=font, fill=WHITE)

    return image


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, text in PROMOS.items():
        image = make_promo(text)
        out_path = OUTPUT_DIR / filename
        image.save(out_path, format="PNG")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
