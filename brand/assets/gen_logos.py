#!/usr/bin/env python3
"""Generate MAUA ASCII-art logo PNGs in multiple sizes and variants."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ASCII = [
    "███╗   ███╗ █████╗ ██╗   ██╗ █████╗",
    "████╗ ████║██╔══██╗██║   ██║██╔══██╗",
    "██╔████╔██║███████║██║   ██║███████║",
    "██║╚██╔╝██║██╔══██║██║   ██║██╔══██║",
    "██║ ╚═╝ ██║██║  ██║╚██████╔╝██║  ██║",
    "╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝",
]

ORANGE = (217, 119, 6, 255)
BLACK = (13, 13, 13, 255)
WHITE = (244, 244, 245, 255)
TRANSPARENT = (0, 0, 0, 0)

FONT_PATH = "/System/Library/Fonts/Menlo.ttc"  # fallback if JetBrains Mono not installed

OUT = Path(__file__).parent / "logos"
OUT.mkdir(exist_ok=True)


def render(font_size: int, fg, bg, padding: int = 40) -> Image.Image:
    font = ImageFont.truetype(FONT_PATH, font_size)
    # Measure using a probe image
    probe = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(probe)
    widths = [d.textbbox((0, 0), line, font=font)[2] for line in ASCII]
    max_w = max(widths)
    line_h = int(font_size * 1.15)
    total_h = line_h * len(ASCII)

    img = Image.new("RGBA", (max_w + padding * 2, total_h + padding * 2), bg)
    draw = ImageDraw.Draw(img)
    for i, line in enumerate(ASCII):
        draw.text((padding, padding + i * line_h), line, font=font, fill=fg)
    return img


variants = [
    # (name, fg, bg, sizes)
    ("orange-on-dark", ORANGE, BLACK, [24, 48, 96]),
    ("orange-on-transparent", ORANGE, TRANSPARENT, [24, 48, 96]),
    ("black-on-light", BLACK, WHITE, [24, 48, 96]),
    ("white-on-transparent", WHITE, TRANSPARENT, [24, 48, 96]),
]

size_label = {24: "sm", 48: "md", 96: "lg"}

for name, fg, bg, sizes in variants:
    for s in sizes:
        img = render(s, fg, bg)
        out = OUT / f"maua-logo-{name}-{size_label[s]}.png"
        img.save(out)
        print(f"wrote {out} ({img.size[0]}x{img.size[1]})")

print("\ndone.")
