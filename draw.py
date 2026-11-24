#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Monday 23 November 2026 (31 stories), numbers-led.
1024x1024 front page. All facts from the verified 23 Nov brief.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (13, 27, 46)
NAVY2 = (24, 48, 80)
GOLD = (201, 162, 39)
GOLD_LT = (232, 197, 92)
RED = (185, 28, 28)
RED_DK = (140, 20, 20)
TEAL = (15, 118, 110)
GREY = (90, 90, 90)
LINE = (200, 192, 175)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def F(path, size):
    return ImageFont.truetype(path, size)


def sans_b(s):
    return F(f"{FD}/DejaVuSans-Bold.ttf", s)


def sans(s):
    return F(f"{FD}/DejaVuSans.ttf", s)


def serif_b(s):
    return F(f"{FD}/DejaVuSerif-Bold.ttf", s)


def ital(s):
    return F(f"{FL}/LiberationSans-Italic.ttf", s)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def tw(text, font):
    return d.textlength(text, font=font)


def fit(text, font, max_w, min_size=8):
    """Shrink font until text fits max_w; returns (font, text)."""
    size = font.size
    f = font
    while tw(text, f) > max_w and size > min_size:
        size -= 1
        f = F(font.path, size)
    return f


def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def trunc(text, font, max_w, ell="..."):
    if tw(text, font) <= max_w:
        return text
    while text and tw(text + ell, font) > max_w:
        text = text[:-1]
    return text + ell


def chip(x, y, label, kind):
    """REPORTED (navy) / CLAIM (red) chip; returns width used."""
    f = sans_b(8)
    w_ = int(tw(label, f)) + 10
    col = NAVY if kind == "REPORTED" else RED
    d.rounded_rectangle([x, y, x + w_, y + 13], radius=3, fill=col)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w_


# ---------------------------------------------------------------- number grid
NUMBERS = [
    ("-3.3%", "KOSPI FALLS"),
    ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T WON", "SEOUL RESCUE FUND"),
    ("2%", "BILLIONAIRE TAX"),
    ("$450M", "SKUBAL DEAL"),
    ("165", "RUSSIAN MISSILES / WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"),
    ("264 KG", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
GRID_Y, GRID_H, ROW_H = 6, 96, 48
CELL_W = (W - 12) / 5
d.rectangle([0, 0, W, GRID_Y + GRID_H], fill=NAVY)
for i, (val, lab) in enumerate(NUMBERS):
    row, col = divmod(i, 5)
    cx = 6 + col * CELL_W
    cy = GRID_Y + row * ROW_H
    vf = fit(val, sans_b(24), CELL_W - 10)
    d.text((cx + 8, cy + 2), val, font=vf, fill=GOLD_LT)
    lf = fit(lab, sans_b(9), CELL_W - 12)
    d.text((cx + 8, cy + 30), lab, font=lf, fill=(255, 255, 255))

# ---------------------------------------------------------------- masthead
MH_Y = 108
d.text((8, MH_Y), "THE WORLD TODAY", font=serif_b(34), fill=INK)
df = sans_b(11)
d.text((W - 8 - tw("MONDAY 23 NOVEMBER 2026", df), MH_Y + 12),
       "MONDAY 23 NOVEMBER 2026", font=df, fill=INK)
d.rectangle([8, MH_Y + 42, W - 8, MH_Y + 45], fill=GOLD)
d.text((8, MH_Y + 50), "One day of world news — 31 stories, six regions, verified against the wires.",
       font=ital(12), fill=GREY)

# ---------------------------------------------------------------- region bar
RB_Y = 172
d.rectangle([8, RB_Y, W - 8, RB_Y + 20], fill=INK)
regions = [("ASIA-PACIFIC", 7), ("AMERICAS", 8), ("MIDDLE EAST", 6),
           ("EUROPE", 5), ("AFRICA", 3), ("WORLD", 2)]
rf = sans_b(10)
x = 16
for name, n in regions:
    t = f"{name} {n}"
    d.text((x, RB_Y + 5), t, font=rf, fill=(255, 255, 255))
    x += tw(t, rf) + 26
d.text((W - 8 - tw("31 STORIES", rf), RB_Y + 5), "31 STORIES", font=rf, fill=GOLD_LT)

# ---------------------------------------------------------------- hero scenes
HERO_Y = 198
COL_W = 326
GAP = 8
SCENE_H = 118


def scene_kospi(x0, y0, w):
    d.rectangle([x0, y0, x0 + w, y0 + SCENE_H], fill=(10, 22, 40))
    # lit buildings
    import random
    rnd = random.Random(7)
    bx = x0 + 8
    while bx < x0 + w - 26:
        bw = rnd.randint(18, 30)
        bh = rnd.randint(30, 48)
        d.rectangle([bx, y0 + SCENE_H - 26 - bh, bx + bw, y0 + SCENE_H - 26],
                    fill=(30, 52, 88))
        for wy in range(y0 + SCENE_H - 22 - bh, y0 + SCENE_H - 30, 9):
            for wx in range(int(bx) + 3, int(bx) + bw - 3, 7):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 110))
        bx += bw + 5
    # descending orange chart line, kept in upper zone
    pts = [(x0 + 12, y0 + 14), (x0 + 70, y0 + 26), (x0 + 130, y0 + 22),
           (x0 + 190, y0 + 40), (x0 + 250, y0 + 34), (x0 + w - 12, y0 + 52)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 140, 40))
    d.text((x0 + 12, y0 + 62), "-3.3%", font=sans_b(30), fill=(255, 255, 255))
    # solid navy band for caption
    d.rectangle([x0, y0 + SCENE_H - 20, x0 + w, y0 + SCENE_H], fill=NAVY2)
    cap = "KOSPI 4,708.54 \u00b7 -161 PTS \u00b7 SAMSUNG -3.1%"
    cf = fit(cap, sans_b(10), w - 12)
    d.text((x0 + 6, y0 + SCENE_H - 16), cap, font=cf, fill=GOLD_LT)


def scene_guterres(x0, y0, w):
    d.rectangle([x0, y0, x0 + w, y0 + SCENE_H], fill=(8, 42, 44))
    # globe, masked circle layer
    layer = Image.new("RGBA", (w, SCENE_H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    cx, cy, r = w - 62, 52, 44
    ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 96, 110))
    for k in range(-2, 3):
        ld.arc([cx - r + abs(k) * 12, cy - r, cx + r - abs(k) * 12, cy + r],
               90, 270, fill=(140, 220, 220))
    ld.line([cx - r, cy, cx + r, cy], fill=(140, 220, 220))
    ld.line([cx, cy - r, cx, cy + r], fill=(140, 220, 220))
    img.paste(layer, (x0, y0), layer)
    d.text((x0 + 10, y0 + 10), "150", font=sans_b(34), fill=GOLD_LT)
    d.text((x0 + 10, y0 + 48), "DELEGATES BACK", font=sans_b(15), fill=(255, 255, 255))
    d.text((x0 + 10, y0 + 68), "A RISK FRAMEWORK", font=sans_b(15), fill=(255, 255, 255))
    d.text((x0 + 10, y0 + 92), "BRIDGETOWN SUMMIT", font=sans_b(11), fill=GOLD_LT)
    # small flags row
    fx = x0 + 10
    for col in [(0, 90, 180), (255, 215, 0), (200, 40, 40), (40, 140, 60)]:
        d.rectangle([fx, y0 + SCENE_H - 14, fx + 16, y0 + SCENE_H - 6], fill=col)
        fx += 21


def scene_power(x0, y0, w):
    d.rectangle([x0, y0, x0 + w, y0 + SCENE_H], fill=(245, 240, 228))
    bars = [("US", 78.9, NAVY), ("CHINA", 73.6, (70, 90, 120)), ("INDIA", 40.5, GOLD)]
    by = y0 + 14
    for name, val, col in bars:
        d.text((x0 + 8, by), name, font=sans_b(11), fill=INK)
        bw = (w - 90) * val / 80.0
        d.rectangle([x0 + 62, by, x0 + 62 + bw, by + 16], fill=col)
        vcol = INK if col is GOLD else INK
        d.text((x0 + 66 + bw, by + 2), f"{val}", font=sans_b(11), fill=vcol)
        by += 26
    d.text((x0 + 8, by + 2), "GAP 5.3 \u2014 NARROWEST SINCE 2018",
           font=sans_b(11), fill=RED)


HEROES = [
    ("AI ROUT HITS ASIA",
     "Kospi -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%.",
     "REUTERS", "REPORTED", scene_kospi),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "Bridgetown summit: 150 delegates back a risk framework, not a treaty.",
     "AP", "REPORTED", scene_guterres),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6; India 3rd at 40.5.",
     "LOWY INSTITUTE", "REPORTED", scene_power),
]
for i, (head, body, src, kind, fn) in enumerate(HEROES):
    x0 = 8 + i * (COL_W + GAP)
    fn(x0, HERO_Y, COL_W)
    hy = HERO_Y + SCENE_H + 6
    hf = fit(head, sans_b(13), COL_W)
    lines = wrap(head, hf, COL_W)
    for ln in lines[:2]:
        d.text((x0, hy), ln, font=hf, fill=INK)
        hy += 16
    bf = sans(10)
    blines = wrap(body, bf, COL_W)
    for ln in blines[:2]:
        d.text((x0, hy), ln, font=bf, fill=(40, 40, 40))
        hy += 13
    # source + chip on their own row, below body
    sy = HERO_Y + SCENE_H + 6 + 2 * 16 + 2 * 13 + 2
    sf = sans_b(8)
    d.text((x0, sy + 2), src, font=sf, fill=GREY)
    cw = chip(x0 + tw(src, sf) + 8, sy, kind, kind)

# ---------------------------------------------------------------- more of the day
MORE_Y = 402
d.rectangle([8, MORE_Y, W - 8, MORE_Y + 20], fill=INK)
d.text((16, MORE_Y + 5), "MORE OF THE DAY", font=sans_b(11), fill=(255, 255, 255))
d.text((W - 8 - tw("10 STORIES", sans_b(11)), MORE_Y + 5), "10 STORIES",
       font=sans_b(11), fill=GOLD_LT)

# ---------------------------------------------------------------- 10 cards
CARDS = [
    ("1", "BESSENT DEMANDS NVIDIA ANSWERS", "Treasury presses chipmaker on China.",
     "BLOOMBERG", "REPORTED"),
    ("2", "FBI PROBES NCIC HACK", "Police-database breach investigated.",
     "AP", "REPORTED"),
    ("3", "IRAN STRIKES MAY RESUME", "Trump: may resume in New Year.",
     "REUTERS", "REPORTED"),
    ("4", "NASDAQ FUTURES +3%", "Holiday week lifts US futures.",
     "WSJ", "REPORTED"),
    ("5", "SKUBAL $450M TO METS", "Two-time Cy Young, nine-year deal.",
     "ESPN", "REPORTED"),
    ("6", "TOM JACKSON DIES AT 75", "NFL star turned broadcaster.",
     "AP", "REPORTED"),
    ("7", "STATES SUE SPACEX", "AI safety claims challenged in court.",
     "REUTERS", "REPORTED"),
    ("8", "ANTHROPIC IPO $107.3B", "Raised at $83/share; close $97.17.",
     "BLOOMBERG", "REPORTED"),
    ("9", "POLAND: 3 MISSILES CROSSED", "Kh-101s entered airspace, Warsaw says.",
     "AP", "CLAIM"),
    ("10", "RUSSIAN NUCLEAR SATELLITE", "Intel warns of orbital weapon test.",
     "WSJ", "CLAIM"),
]
CARD_Y, CARD_H = 428, 66
CCW = (W - 16 - 4 * GAP) / 5
for i, (num, head, body, src, kind) in enumerate(CARDS):
    row, col = divmod(i, 5)
    x0 = 8 + col * (CCW + GAP)
    y0 = CARD_Y + row * (CARD_H + 6)
    d.rectangle([x0, y0, x0 + CCW, y0 + CARD_H], outline=LINE, width=1)
    nf = sans_b(9)
    d.text((x0 + 6, y0 + 4), num, font=nf, fill=RED)
    hf = fit(head, sans_b(10), CCW - 12)
    d.text((x0 + 6, y0 + 16), trunc(head, hf, CCW - 12), font=hf, fill=INK)
    bf = sans(9)
    d.text((x0 + 6, y0 + 30), trunc(body, bf, CCW - 12), font=bf, fill=(40, 40, 40))
    sf = sans_b(8)
    d.text((x0 + 6, y0 + 47), src, font=sf, fill=GREY)
    chip(x0 + 6 + tw(src, sf) + 6, y0 + 45, kind, kind)

# ---------------------------------------------------------------- map + ALSO
MAP_Y = 574
MAP_H = 200
MAP_W = 500
d.rectangle([8, MAP_Y, 8 + MAP_W, MAP_Y + MAP_H], fill=(232, 226, 210))
d.text((16, MAP_Y + 6), "THE WORLD IN ONE MAP", font=sans_b(11), fill=INK)
# stylised continents (blobs)
d.ellipse([30, 640, 150, 700], fill=(190, 200, 170))          # N America
d.ellipse([120, 700, 185, 745], fill=(190, 200, 170))         # S America
d.ellipse([230, 640, 330, 700], fill=(200, 190, 160))         # Europe/Africa top
d.ellipse([250, 695, 320, 750], fill=(200, 190, 160))         # Africa
d.ellipse([350, 640, 480, 700], fill=(185, 195, 175))         # Asia
d.ellipse([390, 720, 450, 745], fill=(185, 195, 175))         # SE Asia / Oceania
PINS = [
    (1, 430, 668), (2, 88, 700), (3, 96, 664), (4, 398, 668),
    (5, 266, 668), (6, 246, 686), (7, 276, 690), (8, 232, 664),
    (9, 316, 702), (10, 258, 644), (11, 296, 692), (12, 314, 722),
    (13, 288, 720),
]
for n, px, py in PINS:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
    tf = sans_b(9)
    t = str(n)
    d.text((px - tw(t, tf) / 2, py - 6), t, font=tf, fill=(255, 255, 255))
d.text((16, MAP_Y + MAP_H - 34), "Pins 1-7: Seoul, Bridgetown, Washington, Beijing,", font=sans(9), fill=GREY)
d.text((16, MAP_Y + MAP_H - 22), "Paris, Manchester, London.  Pins 8-13: Kyiv, Antalya,", font=sans(9), fill=GREY)
d.text((16, MAP_Y + MAP_H - 10), "Gaza, Beirut, Khartoum, Kinshasa, Dhaka.", font=sans(9), fill=GREY)

# ALSO list (2 cols x 9)
ALSO_X = 524
ALSO = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 Russian missiles in a week",
    "COP31: day after \u2014 Antalya pact rejected",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: Iranian strike hits plant, 2 hurt",
    "Benghazi: UN demands probe [CLAIM]",
    "Sudan: air defences down drones [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits over AI exam chaos",
    "SK Telecom -7.3%",
    "China eases margin rules to 80%",
    "Seoul readies 10T-won stabilisation fund",
]
d.text((ALSO_X, MAP_Y + 6), "ALSO ON MONDAY", font=sans_b(11), fill=INK)
af = sans(10)
COL2_W = 236
for i, item in enumerate(ALSO):
    col, row = divmod(i, 9)
    ax = ALSO_X + col * (COL2_W + 8)
    ay = MAP_Y + 26 + row * 19
    red = "[CLAIM]" in item
    d.text((ax, ay), "\u2022", font=af, fill=INK)
    if red:
        item2 = item.replace(" [CLAIM]", "")
        t2 = trunc(item2, af, COL2_W - 34)
        d.text((ax + 10, ay), t2, font=af, fill=INK)
        d.text((ax + 10 + tw(t2, af) + 4, ay), "[CLAIM]", font=sans_b(9), fill=RED)
    else:
        d.text((ax + 10, ay), trunc(item, af, COL2_W - 12), font=af, fill=INK)

# ---------------------------------------------------------------- DATE CHECK
DC_Y = 786
DC_H = 132
d.rectangle([8, DC_Y, W - 8, DC_Y + DC_H], outline=RED, width=2)
d.rectangle([8, DC_Y, W - 8, DC_Y + 22], fill=RED)
d.text((16, DC_Y + 5), "DATE CHECK \u2014 LEFT OUT ON PURPOSE", font=sans_b(11), fill=(255, 255, 255))
d.text((W - 8 - tw("NOT 23 NOVEMBER", sans_b(10)), DC_Y + 6), "NOT 23 NOVEMBER",
       font=sans_b(10), fill=(255, 255, 255))
LEFT = ["Democrats reach 258  (22 Nov)", "Sparta II fire  (22 Nov)",
        "El Chapo Isidro captured  (22 Nov)", "EU\u2013Indonesia pact  (21 Nov)",
        "Nigeria boat  (21 Nov)", "ICJ Myanmar ruling  (19 Nov)"]
NOTYET = ["Dymer search continues  (14 missing)", "4 House races uncalled",
          "COP32 venue not set", "WHO evacuating trapped Ebola staff"]
df2 = sans(10)
d.text((16, DC_Y + 30), "LEFT OUT:", font=sans_b(10), fill=RED_DK)
for i, item in enumerate(LEFT):
    col, row = divmod(i, 3)
    ax = 16 + col * 250
    ay = DC_Y + 48 + row * 16
    d.text((ax, ay), "\u2022 " + item, font=df2, fill=INK)
d.text((530, DC_Y + 30), "NOT YET:", font=sans_b(10), fill=RED_DK)
for i, item in enumerate(NOTYET):
    ay = DC_Y + 48 + i * 16
    d.text((530, ay), "\u2022 " + item, font=df2, fill=INK)
d.text((16, DC_Y + DC_H - 16), "These stories are real \u2014 but they did not happen on 23 November.",
       font=ital(10), fill=GREY)

# ---------------------------------------------------------------- footer
FT_Y = 930
d.rectangle([8, FT_Y, W - 8, FT_Y + 2], fill=GOLD)
d.text((8, FT_Y + 8), "Sources: Reuters, AP, Bloomberg, WSJ, Yonhap, Lowy Institute.",
       font=sans(9), fill=GREY)
d.text((8, FT_Y + 22), "REPORTED = confirmed by wires  \u00b7  CLAIM = one side's claim, unverified",
       font=sans(9), fill=GREY)
d.text((W - 8 - tw("THE WORLD TODAY \u00b7 Monday 23 November 2026 \u00b7 31 stories \u00b7 6 regions", sans_b(9)),
           FT_Y + 8),
       "THE WORLD TODAY \u00b7 Monday 23 November 2026 \u00b7 31 stories \u00b7 6 regions",
       font=sans_b(9), fill=INK)
d.text((W - 8 - tw("Drawn by hand, checked against the wires.", ital(9)), FT_Y + 22),
       "Drawn by hand, checked against the wires.", font=ital(9), fill=GREY)
d.rectangle([8, H - 6, W - 8, H - 4], fill=GOLD)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
