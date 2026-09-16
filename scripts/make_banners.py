"""Generate the landing-page promo banners as PNGs with the text baked
into the pixels. Deterministic: same output on every machine, since it
depends only on the bundled font (fonts/NotoSans-Regular.ttf) and the
fixed strings below — never on host fonts.

Usage:
    uv run python scripts/make_banners.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = ROOT / "fonts" / "NotoSans-Regular.ttf"
OUTPUT_DIR = ROOT / "static" / "img"

WIDTH, HEIGHT = 1200, 400
NAVY = (11, 47, 92)
NAVY_DARK = (8, 33, 68)
GOLD = (201, 154, 60)
WHITE = (255, 255, 255)

BANNERS = {
    "banner-en.png": {
        "title": "Financing that fits your plans",
        "subtitle": "Competitive rates. Clear terms. No surprises.",
    },
    "banner-fr.png": {
        "title": "Un financement adapté à vos projets",
        "subtitle": "Taux compétitifs. Conditions claires. Aucune surprise.",
    },
}


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size=size, layout_engine=ImageFont.Layout.BASIC)


def _draw_gradient(draw: ImageDraw.ImageDraw) -> None:
    for x in range(WIDTH):
        t = x / WIDTH
        r = round(NAVY[0] + (NAVY_DARK[0] - NAVY[0]) * t)
        g = round(NAVY[1] + (NAVY_DARK[1] - NAVY[1]) * t)
        b = round(NAVY[2] + (NAVY_DARK[2] - NAVY[2]) * t)
        draw.line([(x, 0), (x, HEIGHT)], fill=(r, g, b))


def make_banner(title: str, subtitle: str) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(image)
    _draw_gradient(draw)

    draw.rectangle([(0, HEIGHT - 10), (WIDTH, HEIGHT)], fill=GOLD)

    title_font = _font(56)
    subtitle_font = _font(28)

    margin = 80
    draw.text((margin, 140), title, font=title_font, fill=WHITE)
    draw.text((margin, 220), subtitle, font=subtitle_font, fill=(214, 224, 236))

    return image


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, text in BANNERS.items():
        image = make_banner(text["title"], text["subtitle"])
        out_path = OUTPUT_DIR / filename
        image.save(out_path, format="PNG")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
