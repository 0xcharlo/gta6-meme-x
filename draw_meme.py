#!/usr/bin/env python3
"""Draw the GTA 6 meme for make.fun's gta6-meme-x-01 bounty.

Joke: GTA 6 isn't a game, it's a Florida documentary — the make.fun ghost
as a Florida Man on a Vice City beach at sunset, holding its magenta star
coin. The ghost is drawn by hand in the logo's own style (white body, thick
black outline, black four-point sparkle eyes, round hand, magenta coin with
a white star) so it is worked into the scene, not pasted on as a sticker.

Output: meme.png, 1024x1024. Caption text is big enough to read at 480x480.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

random.seed(7)


def font(size):
    return ImageFont.truetype(BOLD, size)


def vgrad(draw, x0, y0, x1, y1, top, bottom):
    """Vertical gradient by drawing one horizontal line per row."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def star4(cx, cy, r):
    """Four-point sparkle (diamond star) as a polygon."""
    k = 0.26
    return [
        (cx, cy - r), (cx + r * k, cy - r * k),
        (cx + r, cy), (cx + r * k, cy + r * k),
        (cx, cy + r), (cx - r * k, cy + r * k),
        (cx - r, cy), (cx - r * k, cy - r * k),
    ]


def star5(cx, cy, r_out, r_in):
    """Five-point star as a polygon."""
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def dilate(mask, px):
    """Grow a mask by px pixels (for outlines)."""
    return mask.filter(ImageFilter.MaxFilter(2 * px + 1))


def draw_ghost():
    """The make.fun ghost, drawn in the logo's style, on its own RGBA layer."""
    LW, LH = 560, 600
    layer = Image.new("RGBA", (LW, LH), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # --- body silhouette mask: dome top, straight sides, wavy hem ---
    mask = Image.new("L", (LW, LH), 0)
    md = ImageDraw.Draw(mask)
    cx, dome_cy, r = 260, 170, 150
    pts = []
    for a in range(180, 361, 4):  # dome, left to right over the top
        t = math.radians(a)
        pts.append((cx + r * math.cos(t), dome_cy + r * math.sin(t)))
    # right side down, then wavy hem leftwards (3 bumps)
    pts.append((cx + r, 360))
    for i in range(41):
        t = i / 40
        x = (cx + r) - t * (2 * r)
        y = 348 + 18 * math.sin(3 * math.pi * t)
        pts.append((x, y))
    md.polygon(pts, fill=255)
    # outline = dilated mask, body = mask
    out = dilate(mask, 13)
    body = Image.new("RGBA", (LW, LH), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.bitmap((0, 0), out, fill=(26, 22, 32, 255))   # near-black outline
    bd.bitmap((0, 0), mask, fill=(255, 255, 255, 255))  # white body
    layer.alpha_composite(body)

    # --- magenta star coin, right side (drawn before the hand) ---
    coin = Image.new("RGBA", (LW, LH), (0, 0, 0, 0))
    cmask = Image.new("L", (LW, LH), 0)
    cd = ImageDraw.Draw(cmask)
    cd.ellipse([410 - 54, 280 - 54, 410 + 54, 280 + 54], fill=255)
    cout = dilate(cmask, 10)
    cod = ImageDraw.Draw(coin)
    cod.bitmap((0, 0), cout, fill=(26, 22, 32, 255))
    cod.bitmap((0, 0), cmask, fill=(230, 0, 126, 255))  # magenta coin
    cod.polygon(star5(410, 280, 32, 13), fill=(255, 255, 255, 255))
    layer.alpha_composite(coin)

    # --- round hand holding the coin from below-left ---
    hand = Image.new("RGBA", (LW, LH), (0, 0, 0, 0))
    hmask = Image.new("L", (LW, LH), 0)
    hd = ImageDraw.Draw(hmask)
    hd.ellipse([355 - 30, 335 - 30, 355 + 30, 335 + 30], fill=255)
    hout = dilate(hmask, 9)
    hod = ImageDraw.Draw(hand)
    hod.bitmap((0, 0), hout, fill=(26, 22, 32, 255))
    hod.bitmap((0, 0), hmask, fill=(255, 255, 255, 255))
    layer.alpha_composite(hand)

    # --- sparkle eyes ---
    d.polygon(star4(205, 195, 30), fill=(26, 22, 32, 255))
    d.polygon(star4(315, 195, 30), fill=(26, 22, 32, 255))
    return layer.rotate(-4, resample=Image.BICUBIC, expand=False)


def quad(p0, p1, p2, n=24):
    """Points along a quadratic Bezier curve."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


def palm(draw, base, crown, ctrl, fronds):
    """A palm silhouette: one smooth curved trunk + drooping frond blades."""
    ink = (24, 10, 46)
    draw.line(quad(base, ctrl, crown), fill=ink, width=20, joint="curve")
    for tip, lift in fronds:
        mid = ((crown[0] + tip[0]) / 2, min(crown[1], tip[1]) - lift)
        draw.line(quad(crown, mid, tip), fill=ink, width=10,
                  joint="curve")


def main():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img, "RGBA")

    # --- sky: purple -> pink -> orange sunset ---
    vgrad(d, 0, 0, W, 560, (43, 16, 85), (255, 46, 136))
    vgrad(d, 0, 300, W, 560, (255, 46, 136), (255, 154, 61))
    # sun with glow
    d.ellipse([700 - 150, 300 - 150, 700 + 150, 300 + 150],
              fill=(255, 214, 106, 60))
    d.ellipse([700 - 88, 300 - 88, 700 + 88, 300 + 88],
              fill=(255, 224, 138, 255))

    # --- Vice City skyline silhouette + lit windows ---
    for x in range(0, W, 4):
        pass
    bx = -10
    while bx < W:
        bw = random.randint(46, 96)
        bh = random.randint(60, 185)
        d.rectangle([bx, 560 - bh, bx + bw, 560], fill=(28, 11, 51))
        for _ in range(bw * bh // 260):
            wx = random.randint(bx + 6, bx + bw - 10)
            wy = random.randint(560 - bh + 8, 550)
            d.rectangle([wx, wy, wx + 5, wy + 7],
                        fill=random.choice([(255, 214, 106), (0, 229, 255),
                                            (255, 214, 106)]))
        bx += bw + random.randint(2, 14)

    # --- ocean ---
    vgrad(d, 0, 560, W, 685, (0, 179, 200), (0, 119, 163))
    for y, wdt in [(585, 5), (615, 4), (650, 5)]:
        for x in range(0, W, 90):
            d.arc([x, y - 14, x + 70, y + 14], start=200, end=340,
                  fill=(255, 255, 255, 170), width=wdt)

    # --- beach ---
    vgrad(d, 0, 685, W, H, (242, 201, 138), (224, 168, 102))
    for _ in range(500):
        x, y = random.randint(0, W - 1), random.randint(690, H - 1)
        d.point((x, y), fill=(190, 140, 80))

    # --- palms framing the scene ---
    palm(d, (70, H), (170, 480), (55, 760),
         [((30, 500), 55), ((55, 425), 75), ((130, 395), 80),
          ((215, 400), 80), ((280, 440), 70), ((310, 510), 55)])
    palm(d, (954, H), (860, 490), (965, 760),
         [((995, 510), 55), ((970, 435), 75), ((895, 405), 80),
          ((810, 410), 80), ((745, 450), 70), ((715, 520), 55)])

    # --- ghost shadow + ghost ---
    d.ellipse([430, 892, 780, 926], fill=(0, 0, 0, 70))
    ghost = draw_ghost()
    img.paste(ghost, (340, 520), ghost)

    # --- beach sign, bottom-left: VICE CITY / make.fun ---
    sign = Image.new("RGBA", (320, 132), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sign)
    sd.rounded_rectangle([10, 12, 310, 120], radius=14,
                         fill=(245, 222, 179, 255), outline=(120, 82, 40),
                         width=6)
    sd.text((160, 44), "VICE CITY", font=font(32), fill=(60, 30, 10),
            anchor="mm")
    sd.text((160, 92), "make.fun", font=font(34), fill=(230, 0, 126),
            anchor="mm")
    sign = sign.rotate(-5, resample=Image.BICUBIC, expand=True)
    img.paste(sign, (30, 792), sign)

    # --- top caption ---
    d.text((W // 2, 44), "GTA 6 ISN'T A GAME", font=font(74),
           fill=(255, 255, 255), anchor="ma",
           stroke_width=8, stroke_fill=(20, 8, 40))
    d.text((W // 2, 128), "IT'S A FLORIDA DOCUMENTARY", font=font(54),
           fill=(255, 255, 255), anchor="ma",
           stroke_width=7, stroke_fill=(20, 8, 40))

    # --- bottom news bar: the punchline ---
    d.rectangle([0, 940, W, H], fill=(12, 6, 24))
    d.text((W // 2, 982), "FLORIDA MAN: “FINALLY, A REALISTIC GAME”",
           font=font(38), fill=(255, 255, 255), anchor="mm")

    img.save("meme.png")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
