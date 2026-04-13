#!/usr/bin/env python3
"""Generate MAUA 'M' logomark — ASCII M, orange on black, square icon sizes."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

M = [
    "███╗   ███╗",
    "████╗ ████║",
    "██╔████╔██║",
    "██║╚██╔╝██║",
    "██║ ╚═╝ ██║",
    "╚═╝     ╚═╝",
]

ORANGE = (217, 119, 6, 255)
BLACK = (13, 13, 13, 255)
TRANSPARENT = (0, 0, 0, 0)
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"

OUT = Path(__file__).parent / "logos"
OUT.mkdir(exist_ok=True)


def render_square(size: int, fg, bg) -> Image.Image:
    """Render M centered in a square canvas of `size`x`size`."""
    # Find the largest font size that fits comfortably (with ~12% padding per side)
    target = int(size * 0.76)
    font_size = 4
    while True:
        f = ImageFont.truetype(FONT_PATH, font_size + 1)
        probe = Image.new("RGBA", (10, 10))
        d = ImageDraw.Draw(probe)
        w = max(d.textbbox((0, 0), line, font=f)[2] for line in M)
        h = int((font_size + 1) * 1.1) * len(M)
        if max(w, h) > target:
            break
        font_size += 1

    font = ImageFont.truetype(FONT_PATH, font_size)
    probe = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(probe)
    line_widths = [d.textbbox((0, 0), line, font=font)[2] for line in M]
    block_w = max(line_widths)
    line_h = int(font_size * 1.1)
    block_h = line_h * len(M)

    img = Image.new("RGBA", (size, size), bg)
    draw = ImageDraw.Draw(img)
    x0 = (size - block_w) // 2
    y0 = (size - block_h) // 2
    for i, line in enumerate(M):
        draw.text((x0, y0 + i * line_h), line, font=font, fill=fg)
    return img


sizes = [16, 32, 64, 128, 256, 512, 1024]
# Render small sizes by downscaling from a high-res master for crispness
master = render_square(1024, ORANGE, BLACK)
master_t = render_square(1024, ORANGE, TRANSPARENT)

for s in sizes:
    if s <= 64:
        img = master.resize((s, s), Image.LANCZOS)
    else:
        img = render_square(s, ORANGE, BLACK)
    out = OUT / f"maua-mark-{s}.png"
    img.save(out)
    print(f"wrote {out}")

# Transparent versions (orange M, no background)
for s in [64, 128, 256, 512, 1024]:
    img = render_square(s, ORANGE, TRANSPARENT)
    out = OUT / f"maua-mark-transparent-{s}.png"
    img.save(out)
    print(f"wrote {out}")

# ICO favicon (multi-resolution) — build from downscaled master for crispness
ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
ico_frames = [master.resize(sz, Image.LANCZOS) for sz in ico_sizes]
ico_frames[0].save(OUT / "maua-mark.ico", format="ICO", sizes=ico_sizes, append_images=ico_frames[1:])
print(f"wrote {OUT / 'maua-mark.ico'}")

print("\ndone.")
