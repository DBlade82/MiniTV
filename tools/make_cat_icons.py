"""Generate the four cat enter/leave icons for the MiniTV display.

Draws simple cartoon cat faces (Chilli: orange tabby, Snoopy: brown/white
tabby) next to a house with a direction arrow, and writes 160x120 PNGs to
src/common/. Black (0,0,0) is the background.

Usage:
    python tools/make_cat_icons.py
"""

from pathlib import Path

from PIL import Image, ImageDraw

OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "common"
W, H = 160, 120
S = 4  # supersampling factor

CATS = {
    "chilli": {
        "fur": (240, 150, 60),
        "stripe": (185, 90, 20),
        "muzzle": (255, 225, 185),
        "ear_in": (255, 170, 160),
        "blaze": None,
    },
    "snoopy": {
        "fur": (130, 105, 85),
        "stripe": (55, 40, 30),
        "muzzle": (255, 255, 255),
        "ear_in": (230, 160, 160),
        "blaze": (255, 255, 255),
    },
}

GREEN = (40, 220, 60)
RED = (255, 60, 50)


def draw_cat(d: ImageDraw.ImageDraw, cx: int, cy: int, p: dict) -> None:
    """Draw a cat face centred at (cx, cy) in supersampled coordinates."""
    r = 28 * S
    # Ears.
    for sx in (-1, 1):
        pts = [(cx + sx * 6 * S, cy - 18 * S), (cx + sx * 27 * S, cy - 16 * S),
               (cx + sx * 24 * S, cy - 48 * S)]
        d.polygon(pts, fill=p["fur"], outline=p["stripe"])
        inner = [(cx + sx * 12 * S, cy - 22 * S), (cx + sx * 24 * S, cy - 21 * S),
                 (cx + sx * 23 * S, cy - 39 * S)]
        d.polygon(inner, fill=p["ear_in"])
    # Head.
    d.ellipse([cx - r, cy - 24 * S, cx + r, cy + 26 * S], fill=p["fur"],
              outline=p["stripe"], width=S)
    # Forehead stripes.
    for dx in (-8, 0, 8):
        d.line([(cx + dx * S, cy - 23 * S), (cx + dx * S, cy - 11 * S)],
               fill=p["stripe"], width=3 * S)
    # Cheek stripes.
    for sx in (-1, 1):
        for dy in (4, 10):
            d.line([(cx + sx * 27 * S, cy + dy * S), (cx + sx * 19 * S, cy + (dy + 1) * S)],
                   fill=p["stripe"], width=2 * S)
    # Muzzle / blaze.
    if p["blaze"]:
        d.polygon([(cx, cy - 12 * S), (cx - 6 * S, cy + 6 * S), (cx + 6 * S, cy + 6 * S)],
                  fill=p["blaze"])
    d.ellipse([cx - 14 * S, cy + 2 * S, cx + 14 * S, cy + 24 * S], fill=p["muzzle"])
    # Eyes.
    for sx in (-1, 1):
        ex = cx + sx * 12 * S
        d.ellipse([ex - 6 * S, cy - 6 * S, ex + 6 * S, cy + 5 * S], fill=(120, 230, 60),
                  outline=(0, 0, 0), width=S)
        d.ellipse([ex - 2 * S, cy - 5 * S, ex + 2 * S, cy + 4 * S], fill=(0, 0, 0))
    # Nose and mouth.
    d.polygon([(cx - 4 * S, cy + 7 * S), (cx + 4 * S, cy + 7 * S), (cx, cy + 12 * S)],
              fill=(255, 110, 140))
    d.line([(cx, cy + 12 * S), (cx, cy + 15 * S)], fill=(60, 30, 30), width=S)
    d.arc([cx - 7 * S, cy + 11 * S, cx, cy + 19 * S], 0, 180, fill=(60, 30, 30), width=S)
    d.arc([cx, cy + 11 * S, cx + 7 * S, cy + 19 * S], 0, 180, fill=(60, 30, 30), width=S)
    # Whiskers.
    for sx in (-1, 1):
        for dy in (-1, 3):
            d.line([(cx + sx * 14 * S, cy + (12 + dy) * S),
                    (cx + sx * 34 * S, cy + (9 + dy * 2) * S)], fill=(255, 255, 255), width=S)


def draw_house(d: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    """Draw a white house with a dark door at (cx, cy)."""
    white = (255, 255, 255)
    d.polygon([(cx - 26 * S, cy - 4 * S), (cx, cy - 32 * S), (cx + 26 * S, cy - 4 * S)],
              fill=(200, 60, 50), outline=white, width=S)
    d.rectangle([cx - 20 * S, cy - 4 * S, cx + 20 * S, cy + 32 * S], fill=white)
    d.rectangle([cx - 7 * S, cy + 8 * S, cx + 7 * S, cy + 32 * S], fill=(90, 55, 30))


def draw_arrow(d: ImageDraw.ImageDraw, cx: int, cy: int, direction: int, color) -> None:
    """Draw a horizontal block arrow; direction=+1 points right, -1 left."""
    half = 14 * S
    tip = cx + direction * half
    base = cx + direction * (half - 12 * S)
    tail = cx - direction * half
    d.rectangle([min(tail, base), cy - 5 * S, max(tail, base), cy + 5 * S], fill=color)
    d.polygon([(tip, cy), (base, cy - 14 * S), (base, cy + 14 * S)], fill=color)


def make_icon(cat: str, entering: bool) -> Image.Image:
    img = Image.new("RGB", (W * S, H * S), (0, 0, 0))
    d = ImageDraw.Draw(img)
    cy = 64 * S
    if entering:  # cat -> house
        draw_cat(d, 38 * S, cy, CATS[cat])
        draw_arrow(d, 82 * S, cy, +1, GREEN)
        draw_house(d, 130 * S, cy)
    else:  # house -> cat
        draw_house(d, 30 * S, cy)
        draw_arrow(d, 78 * S, cy, +1, RED)
        draw_cat(d, 122 * S, cy, CATS[cat])
    return img.resize((W, H), Image.LANCZOS)


def make_small_icon(cat: str, at_home: bool, size: int = 40) -> Image.Image:
    """Corner status icon: cat face inside a house (home) or on a meadow (out)."""
    base = 96
    img = Image.new("RGB", (base * S, base * S), (0, 0, 0))
    d = ImageDraw.Draw(img)
    if at_home:
        white = (255, 255, 255)
        d.polygon([(2 * S, 42 * S), (48 * S, 4 * S), (94 * S, 42 * S)],
                  fill=(200, 60, 50), outline=white, width=S)
        d.rectangle([10 * S, 42 * S, 86 * S, 94 * S], fill=white)
        cat_cy = 58
    else:
        d.rectangle([0, 76 * S, base * S, base * S], fill=(40, 170, 50))
        for gx in range(4, base, 8):
            d.polygon([(gx * S, 76 * S), ((gx + 3) * S, 66 * S), ((gx + 6) * S, 76 * S)],
                      fill=(40, 170, 50))
        cat_cy = 56
    # Draw the cat on its own layer so it can be scaled down to fit.
    layer = Image.new("RGBA", (80 * S, 80 * S), (0, 0, 0, 0))
    draw_cat(ImageDraw.Draw(layer), 40 * S, 48 * S, CATS[cat])
    layer = layer.resize((int(layer.width * 0.78), int(layer.height * 0.78)), Image.LANCZOS)
    img.paste(layer, (48 * S - layer.width // 2, (cat_cy - 30) * S), layer)
    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    for cat in CATS:
        for entering in (True, False):
            name = f"cat_{cat}_{'in' if entering else 'out'}.png"
            make_icon(cat, entering).save(OUT_DIR / name)
            print("wrote", OUT_DIR / name)
        for at_home in (True, False):
            name = f"cat_{cat}_small_{'home' if at_home else 'out'}.png"
            make_small_icon(cat, at_home).save(OUT_DIR / name)
            print("wrote", OUT_DIR / name)


if __name__ == "__main__":
    main()
