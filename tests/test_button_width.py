"""Verifies the D04 CSS-clip defect without a browser: measures both the
English and French apply-submit-button labels with Pillow, using the
same bundled font/size/weight the page actually applies to the button
(static/css/style.css: .btn { font-size: 1rem; font-weight: 600 }, via
the @font-face bundling fonts/NotoSans-Regular.ttf), and checks the
fixed .btn-compact width sits between the two: wide enough for the
English label plus a small margin, too narrow for the French one.

These constants mirror static/css/style.css and must be kept in sync
with it by hand if that file's button rules change.
"""
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = ROOT / "fonts" / "NotoSans-Regular.ttf"

BUTTON_FONT_SIZE_PX = 16  # .btn { font-size: 1rem } at the default 16px root
BUTTON_FONT_WEIGHT = 600  # .btn { font-weight: 600 }
BUTTON_HORIZONTAL_PADDING_PX = 40  # .btn { padding: 0.65rem 1.25rem } -> 1.25rem * 2 = 40px at 16px root
BTN_COMPACT_WIDTH_PX = 210  # .btn-compact { width: 210px } (seeded-only)

EN_LABEL = "Submit application"
FR_LABEL = "Soumettre ma demande de prêt"


def _text_width_px(text: str, weight: int = BUTTON_FONT_WEIGHT, size: int = BUTTON_FONT_SIZE_PX) -> float:
    font = ImageFont.truetype(str(FONT_PATH), size=size, layout_engine=ImageFont.Layout.BASIC)
    # Weight, Width axes (in that order) per this font's fvar table.
    font.set_variation_by_axes([weight, 100])
    left, _, right, _ = font.getbbox(text)
    return right - left


def test_fixed_width_fits_english_but_clips_french():
    en_full_width = _text_width_px(EN_LABEL) + BUTTON_HORIZONTAL_PADDING_PX
    fr_full_width = _text_width_px(FR_LABEL) + BUTTON_HORIZONTAL_PADDING_PX

    assert en_full_width <= BTN_COMPACT_WIDTH_PX < fr_full_width, (
        f"en full width={en_full_width:.1f}px, "
        f"fixed width={BTN_COMPACT_WIDTH_PX}px, "
        f"fr full width={fr_full_width:.1f}px"
    )


def test_french_label_is_visibly_clipped_by_at_least_a_quarter():
    fr_text_width = _text_width_px(FR_LABEL)
    visible_content_width = BTN_COMPACT_WIDTH_PX - BUTTON_HORIZONTAL_PADDING_PX
    visible_fraction = visible_content_width / fr_text_width
    assert visible_fraction <= 0.75, (
        f"only {100 * (1 - visible_fraction):.1f}% of the French label is clipped, expected >= 25%"
    )
