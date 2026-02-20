#!/usr/bin/env python3
"""Generate OG cover image for Autonomous Research Press.

Matches the Warm Amber Design System. Minimal, typographic, authoritative.
Output: web/images/og-cover.png (1200x630, standard OG size)
"""

from PIL import Image, ImageDraw, ImageFont

# --- Design tokens ---
BG_DARK = (22, 21, 20)       # #161514
AMBER = (150, 118, 14)       # #96760E
AMBER_LIGHT = (212, 168, 83) # #D4A853
TEXT_PRIMARY = (238, 236, 234)  # #EEECEA
TEXT_DIM = (107, 104, 96)     # #6B6860
RULE_COLOR = (58, 58, 58)    # #3A3A3A

WIDTH, HEIGHT = 1200, 630

# --- Fonts ---
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
SANS_MEDIUM = "/usr/share/fonts/truetype/noto/NotoSans-Medium.ttf"
SANS_LIGHT = "/usr/share/fonts/truetype/noto/NotoSans-Light.ttf"


def _hex(r, g, b):
    return (r, g, b)


def _lerp_color(c1, c2, t):
    """Linearly interpolate between two RGB tuples."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def generate():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    # --- Subtle radial vignette (darker edges, slightly lighter center) ---
    # Creates depth without being obvious
    center_color = (28, 27, 25)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Distance from center-left area (where text lives)
            dx = (x - WIDTH * 0.35) / WIDTH
            dy = (y - HEIGHT * 0.45) / HEIGHT
            dist = (dx * dx + dy * dy) ** 0.5
            t = max(0, min(1, 1.0 - dist * 1.2))
            if t > 0.01:
                bg = img.getpixel((x, y))
                blended = _lerp_color(bg, center_color, t * 0.6)
                img.putpixel((x, y), blended)

    draw = ImageDraw.Draw(img)  # refresh after pixel manipulation

    # --- Amber accent: thin left edge ---
    draw.rectangle([0, 0, 3, HEIGHT], fill=AMBER)

    # --- Decorative amber rule (top area, short) ---
    draw.rectangle([80, 160, 136, 163], fill=AMBER)

    # --- Title: large serif, two lines ---
    title_font = ImageFont.truetype(SERIF_BOLD, 72)
    draw.text((80, 190), "Autonomous", fill=TEXT_PRIMARY, font=title_font)
    draw.text((80, 274), "Research Press", fill=TEXT_PRIMARY, font=title_font)

    # --- Single tagline ---
    tag_font = ImageFont.truetype(SANS_LIGHT, 21)
    draw.text(
        (84, 380),
        "Peer-reviewed research, autonomously produced",
        fill=TEXT_DIM,
        font=tag_font,
    )

    # --- Bottom rule ---
    draw.rectangle([80, HEIGHT - 80, WIDTH - 80, HEIGHT - 79], fill=RULE_COLOR)

    # --- Footer ---
    domain_font = ImageFont.truetype(SANS_MEDIUM, 16)
    draw.text((80, HEIGHT - 60), "ar-press.com", fill=AMBER_LIGHT, font=domain_font)

    # --- Right side: subtle abstract mark ---
    # Three horizontal amber lines of decreasing opacity, suggesting layers/pages
    mark_x = WIDTH - 200
    mark_y = HEIGHT // 2 - 60
    for i, alpha_mult in enumerate([1.0, 0.5, 0.25]):
        line_y = mark_y + i * 28
        line_color = _lerp_color(BG_DARK, AMBER, alpha_mult * 0.7)
        draw.rectangle([mark_x, line_y, mark_x + 100, line_y + 2], fill=line_color)

    # --- Save ---
    img.save("web/images/og-cover.png", "PNG", optimize=True)
    print(f"Generated: web/images/og-cover.png ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    generate()
