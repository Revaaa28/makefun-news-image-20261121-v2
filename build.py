#!/usr/bin/env python3
"""Build entry.png for make.fun competition news-image-20261121 (v2).

Draws a dense one-page broadsheet summing up the world news of
Saturday 21 November 2026: masthead, stat strip, region bar, a
DATE CHECK box, 3 illustrated hero stories, 6 illustrated briefs
and a 27-item index -- 36 stories in all, every one dated that day.

Pure Pillow, no network, deterministic output.
Run:  python3 build.py   ->  writes entry.png next to this file.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN            # content width: 976

PAPER = (246, 241, 230)
INK = (24, 26, 32)
NAVY = (18, 38, 74)
RED = (178, 34, 30)
GREY = (105, 102, 96)
HAIR = (178, 170, 156)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def F(kind, size):
    paths = {
        "serif_b": FL + "LiberationSerif-Bold.ttf",
        "serif_i": FL + "LiberationSerif-Italic.ttf",
        "sans_b": FD + "DejaVuSans-Bold.ttf",
        "sans": FD + "DejaVuSans.ttf",
    }
    return ImageFont.truetype(paths[kind], size)


# ---------------------------------------------------------------- text utils

def wrap(draw, text, font, max_w):
    """Split text into lines that fit max_w, on word boundaries."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block_h(draw, text, font, max_w, lh):
    return len(wrap(draw, text, font, max_w)) * lh


def draw_block(draw, x, y, text, font, fill, max_w, lh, align="left"):
    lines = wrap(draw, text, font, max_w)
    for ln in lines:
        if align == "center":
            tw = draw.textlength(ln, font=font)
            draw.text((x + (max_w - tw) / 2, y), ln, font=font, fill=fill)
        else:
            draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def centered(draw, cx, y, text, font, fill):
    tw = draw.textlength(text, font=font)
    draw.text((cx - tw / 2, y), text, font=font, fill=fill)


# ---------------------------------------------------------------- art: heroes
# Each painter draws inside the box (x, y, w, h) on the main draw context.

def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -90 + i * 36
        rr = r if i % 2 == 0 else r * 0.45
        import math
        pts.append((cx + rr * math.cos(math.radians(ang)),
                    cy + rr * math.sin(math.radians(ang))))
    draw.polygon(pts, fill=fill)


def art_cop(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(198, 228, 205))
    # globe
    gx, gy, gr = x + 92, y + h // 2, 33
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(52, 110, 178))
    draw.ellipse([gx - 24, gy - 18, gx - 2, gy - 2], fill=(66, 148, 84))
    draw.ellipse([gx + 4, gy + 6, gx + 26, gy + 24], fill=(66, 148, 84))
    draw.ellipse([gx - 8, gy + 16, gx + 6, gy + 28], fill=(66, 148, 84))
    # thermometer
    tx = x + w - 66
    draw.rounded_rectangle([tx, y + 8, tx + 20, y + h - 18], radius=9,
                           fill=(250, 250, 248), outline=INK, width=2)
    draw.rectangle([tx + 6, y + h // 2, tx + 14, y + h - 20], fill=RED)
    draw.ellipse([tx - 4, y + h - 26, tx + 24, y + h - 2], fill=RED)
    for i in range(4):
        ly = y + 14 + i * 12
        draw.line([tx - 8, ly, tx - 2, ly], fill=INK, width=2)
    # sun
    draw.ellipse([x + w - 130, y + 10, x + w - 104, y + 36], fill=(240, 178, 60))


def art_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(13, 22, 48))
    rng = random.Random(7)
    for _ in range(26):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(3, h - 34)
        draw.point((sx, sy), fill=(220, 224, 235))
    # missile trails
    draw.arc([x + 30, y - 26, x + 190, y + 62], start=18, end=88,
             fill=(206, 210, 218), width=3)
    draw.arc([x + 150, y - 34, x + 300, y + 54], start=24, end=92,
             fill=(206, 210, 218), width=3)
    star(draw, x + 176, y + 52, 13, (244, 164, 52))
    star(draw, x + 282, y + 44, 10, (244, 164, 52))
    # skyline
    base = y + h
    for bx, bh in [(0, 20), (38, 30), (84, 24), (128, 34), (178, 22),
                   (222, 30), (268, 25)]:
        draw.rectangle([x + bx, base - bh, x + bx + 40, base], fill=(6, 9, 18))
        for wy in range(base - bh + 5, base - 6, 9):
            draw.rectangle([x + bx + 8, wy, x + bx + 13, wy + 4],
                           fill=(246, 205, 96))
            draw.rectangle([x + bx + 24, wy, x + bx + 29, wy + 4],
                           fill=(246, 205, 96))


def art_riyadh(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(16, 20, 44))
    draw.ellipse([x + w - 52, y + 7, x + w - 30, y + 29], fill=(232, 228, 205))
    draw.ellipse([x + w - 59, y + 5, x + w - 37, y + 27], fill=(16, 20, 44))
    base = y + h
    for bx, bw, bh in [(0, 44, 34), (50, 34, 46), (90, 52, 28), (148, 36, 52),
                       (190, 46, 32), (242, 34, 44), (282, 35, 30)]:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 10, 22))
        for wy in range(base - bh + 6, base - 7, 10):
            for wx in range(x + bx + 6, x + bx + bw - 8, 12):
                draw.rectangle([wx, wy, wx + 5, wy + 4], fill=(246, 205, 96))
    # intercept arcs
    draw.arc([x + 18, y + 8, x + 168, y + 96], start=195, end=305,
             fill=(238, 128, 60), width=3)
    draw.arc([x + 110, y + 2, x + 268, y + 92], start=200, end=300,
             fill=(238, 128, 60), width=3)
    draw.arc([x + 190, y + 10, x + 330, y + 88], start=205, end=295,
             fill=(238, 128, 60), width=3)
    star(draw, x + 160, y + 26, 9, (250, 190, 80))
    star(draw, x + 252, y + 18, 8, (250, 190, 80))


# ---------------------------------------------------------------- art: tiles
# Painted on a 300x119 canvas, shrunk to 86x34 with LANCZOS.

def tile_canvas():
    img = Image.new("RGB", (300, 119), PAPER)
    return img, ImageDraw.Draw(img)


def art_warsaw():
    img, d = tile_canvas()
    d.rectangle([0, 0, 300, 119], fill=(206, 220, 234))
    star(d, 150, 30, 17, NAVY)
    for bx, bw in [(18, 76), (112, 76), (206, 76)]:
        d.rectangle([bx, 78, bx + bw, 119], fill=(150, 92, 70))
        d.polygon([(bx - 5, 78), (bx + bw / 2, 52), (bx + bw + 5, 78)],
                  fill=(104, 52, 42))
        d.rectangle([bx + 28, 94, bx + 48, 119], fill=(70, 44, 34))
    return img


def art_mercury():
    img, d = tile_canvas()
    d.rectangle([0, 0, 300, 119], fill=(8, 8, 14))
    rng = random.Random(3)
    for _ in range(30):
        d.point((rng.randint(2, 298), rng.randint(2, 117)),
                fill=(210, 210, 220))
    d.ellipse([28, 22, 128, 112], fill=(158, 150, 142))
    d.ellipse([48, 42, 68, 60], outline=(128, 120, 112), width=3)
    d.ellipse([84, 66, 108, 88], outline=(128, 120, 112), width=3)
    d.ellipse([58, 82, 74, 96], outline=(128, 120, 112), width=2)
    # spacecraft
    d.rectangle([196, 48, 226, 66], fill=(216, 216, 220), outline=INK, width=2)
    d.polygon([(168, 40), (196, 50), (196, 64), (168, 74)], fill=(52, 92, 168))
    d.polygon([(226, 50), (254, 40), (254, 74), (226, 64)], fill=(52, 92, 168))
    d.line([211, 48, 211, 30], fill=(216, 216, 220), width=3)
    d.ellipse([207, 24, 215, 32], fill=(240, 190, 80))
    return img


def art_chip():
    img, d = tile_canvas()
    d.rectangle([0, 0, 300, 119], fill=(18, 44, 38))
    cx, cy, s = 128, 22, 76
    d.rounded_rectangle([cx, cy, cx + s, cy + s], radius=8,
                        fill=(38, 158, 116), outline=(214, 246, 230), width=3)
    d.rectangle([cx + 20, cy + 20, cx + s - 20, cy + s - 20],
                outline=(214, 246, 230), width=3)
    for i in range(5):
        px = cx + 8 + i * 15
        d.line([px, cy - 10, px, cy], fill=(214, 246, 230), width=3)
        d.line([px, cy + s, px, cy + s + 10], fill=(214, 246, 230), width=3)
        py = cy + 8 + i * 15
        d.line([cx - 10, py, cx, py], fill=(214, 246, 230), width=3)
        d.line([cx + s, py, cx + s + 10, py], fill=(214, 246, 230), width=3)
    return img


def art_tanker():
    img, d = tile_canvas()
    d.rectangle([0, 0, 300, 62], fill=(240, 176, 96))
    d.rectangle([0, 34, 300, 62], fill=(232, 128, 70))
    d.ellipse([128, 16, 172, 60], fill=(246, 214, 130))
    d.rectangle([0, 62, 300, 119], fill=(38, 84, 118))
    # tanker silhouette
    d.polygon([(38, 62), (262, 62), (244, 82), (58, 82)], fill=(20, 22, 30))
    d.rectangle([52, 50, 236, 62], fill=(150, 52, 40))
    d.rectangle([216, 34, 240, 62], fill=(24, 26, 34))
    d.rectangle([224, 26, 232, 34], fill=(24, 26, 34))
    return img


def art_imphal():
    img, d = tile_canvas()
    d.rectangle([0, 0, 300, 119], fill=(228, 210, 182))
    d.polygon([(0, 119), (0, 66), (90, 34), (180, 78), (240, 52),
               (300, 84), (300, 119)], fill=(116, 108, 84))
    d.polygon([(0, 119), (0, 88), (110, 58), (210, 92), (300, 70),
               (300, 119)], fill=(92, 88, 66))
    # smoke plumes
    for gx, gy in [(196, 44), (222, 56), (246, 40)]:
        d.ellipse([gx - 15, gy - 26, gx + 17, gy + 4], fill=(148, 146, 140))
        d.ellipse([gx - 8, gy - 38, gx + 22, gy - 10], fill=(160, 158, 152))
    return img


def art_voyager():
    img, d = tile_canvas()
    d.rectangle([0, 0, 300, 119], fill=(10, 12, 30))
    rng = random.Random(11)
    for _ in range(34):
        d.point((rng.randint(2, 298), rng.randint(2, 117)),
                fill=(225, 228, 240))
    # dish
    d.pieslice([96, 22, 196, 108], start=300, end=118,
               fill=(224, 224, 228), outline=INK, width=2)
    d.line([146, 62, 196, 34], fill=(224, 224, 228), width=4)
    d.ellipse([192, 30, 202, 40], fill=(240, 190, 80))
    d.rectangle([138, 62, 154, 76], fill=(170, 170, 178))
    # signal arcs
    for r in (20, 34, 48):
        d.arc([196 - r, 34 - r, 196 + r, 34 + r], start=288, end=62,
              fill=(110, 186, 246), width=3)
    return img


# ---------------------------------------------------------------- content

STATS = [
    ("3", "missiles downed over Riyadh"),
    ("42", "injured in the Kryvyi Rih strike"),
    ("~900,000", "AI chips cleared for China"),
    ("$94.65", "Brent crude, up 4.6% in a day"),
    ("11", "dead in Imphal, Manipur"),
    ("1", "light-day to Voyager 1"),
]

REGIONS = [
    ("Europe", 12, (31, 78, 150)),
    ("Asia", 7, (178, 34, 30)),
    ("Americas", 7, (110, 60, 140)),
    ("Middle East", 4, (190, 140, 30)),
    ("Africa", 2, (46, 110, 60)),
    ("Oceania", 2, (20, 120, 130)),
    ("Space & Global", 2, (88, 88, 98)),
]

DATE_CHECK = (
    "Left out as earlier-day news, NOT shown as Saturday's: the Shenzhen "
    "summit declaration (Thu 19 Nov) - the World Court's Myanmar ruling "
    "(Thu 19 Nov) - Wall Street's Friday close and Anthropic's slide "
    "(Fri 20 Nov) - Kyiv's bridge strikes (Fri 20 Nov) - UK-EU summit "
    "deals (Fri 20 Nov) - GTA VI's first-day sales (Fri 20 Nov)."
)

HEROES = [
    {
        "kicker": "1  ANTALYA, TURKIYE - Reuters, UN News",
        "head": "COP31 runs into overtime with no deal",
        "brief": ("Talks blew past their scheduled close with no agreement. "
                  "A third draft lands Saturday morning, fossil-fuel "
                  "language is out of the text, and at 92,000 attendees "
                  "this is the largest COP ever held."),
        "art": art_cop,
    },
    {
        "kicker": "2  KRYVYI RIH & KYIV, UKRAINE - AP, city officials",
        "head": "Russian strikes kill 12 in a day across Ukraine",
        "brief": ("An overnight barrage hits cities across the country. In "
                  "Kryvyi Rih two are killed and 42 injured, four of them "
                  "children; Kyiv rations power and 50 Rivne settlements "
                  "are left dark."),
        "art": art_kyiv,
    },
    {
        "kicker": "3  RIYADH, SAUDI ARABIA - Reuters, AFP",
        "head": "Coalition downs three Houthi missiles over Riyadh",
        "brief": ("Air defences destroy three ballistic missiles fired at "
                  "the capital early on Saturday, the second attack in "
                  "days. Coalition jets strike Hodeidah port and six "
                  "Sana'a workshops."),
        "art": art_riyadh,
    },
]

MIDS = [
    {
        "label": "4  WARSAW - NATO - AP",
        "head": "Rutte in Warsaw as Poland seeks more cover",
        "brief": ("NATO's chief visits after Friday's Kh-101 crash near "
                  "Nowy Lipowiec; Warsaw wants more allied cover."),
        "art": art_warsaw,
    },
    {
        "label": "5  MERCURY - SPACE - ESA",
        "head": "BepiColombo reaches Mercury after eight years",
        "brief": ("The ESA-JAXA craft fires its thrusters at 19:24 CET on "
                  "Saturday to fall into Mercury's orbit."),
        "art": art_mercury,
    },
    {
        "label": "6  WASHINGTON - TECH - House panel",
        "head": "US clears some 900,000 AI chips for China",
        "brief": ("A House committee says nearly 900,000 AI chips were "
                  "approved for China in six months."),
        "art": art_chip,
    },
    {
        "label": "7  KHARG ISLAND - ENERGY - Reports",
        "head": "Iran masses tankers to test the US blockade",
        "brief": ("14+ Iranian tankers wait at Kharg Island; Brent rose "
                  "4.6% to $94.65 as US escorts worked Hormuz."),
        "art": art_tanker,
    },
    {
        "label": "8  IMPHAL, INDIA - UNREST - Officials",
        "head": "Manipur's capital counts 11 dead as violence spreads",
        "brief": ("Officials confirm 11 dead and 181 in hospital; higher "
                  "press tolls are unconfirmed."),
        "art": art_imphal,
    },
    {
        "label": "9  PASADENA - SPACE - NASA",
        "head": "Voyager 1 is now one light-day from Earth",
        "brief": ("NASA confirms the probe is a full light-day out, 25.9 "
                  "billion km; Spain picked up its signal."),
        "art": art_voyager,
    },
]

INDEX = [
    (10, "DELHI", "Modi opens an SCO dialogue forum on culture and cooperation.", "PIB"),
    (11, "LONDON", "A UK military official says Britain hit Moscow with cyberattacks.", "UK"),
    (12, "JAKARTA", "The ministry asks Google why 19,000 YouTube accounts are gone.", "Ministry"),
    (13, "SUMY", "A HIMARS strike wipes out 20 Russian commanders, reports say.", "Reports"),
    (14, "CALIFORNIA", "The attorney general subpoenas Nvidia over its ex-CEO's exit.", "AG"),
    (15, "NEW DELHI", "India launches its first home-made H5N1 vaccine, for chickens.", "PIB"),
    (16, "COPENHAGEN", "Denmark charges two over a plot to kill a Ukrainian rapper.", "Reports"),
    (17, "BRUSSELS", "The EU completes its largest-ever reform payment to Kyiv, nearly 8bn euros.", "EU"),
    (18, "HODEIDAH", "The UN warns coalition port strikes threaten Yemen's aid lifeline.", "UN, AP"),
    (19, "WELLINGTON", "India resume day three on 159/1; NZ made 368, Nicholls 175 not out.", "Scorecard"),
    (20, "TURIN", "Medvedev meets Zverev in tonight's ATP semi-final.", "ATP"),
    (21, "LAS VEGAS", "F1 qualifying runs under the lights today; race on Sunday.", "F1"),
    (22, "MELBOURNE", "Australia and England open their T20 series at the MCG tonight.", "AFP diary"),
    (23, "BERLIN", "Students march against rearmament and mandatory military service.", "Reports"),
    (24, "BAGHDAD", "Iraq's pipeline chief is arrested over oil-trading claims.", "Reports"),
    (25, "SEOUL", "South Korean exporters pass a $1 trillion year on chip demand.", "Reports"),
    (26, "NAIROBI", "Kenya's Treasury keeps fuel subsidies to hold down the import bill.", "Reports"),
    (27, "LAGOS", "A security report counts 7.8bn naira in ransoms paid in the year to July.", "Report"),
    (28, "ATLANTA", "Measles ends US elimination status; cases are the highest in 35 years.", "Reports"),
    (29, "BRASILIA", "Brazil advances an Indigenous land bill as Raoni visits.", "Reports"),
    (30, "MADRID", "A general strike halts Spain; Amnesty faults police force.", "Reports"),
    (31, "ROME", "Workers and students march against Meloni's budget.", "Reports"),
    (32, "LOS ANGELES", "A jury convicts the man who started the 2025 Palisades Fire.", "Court reports"),
    (33, "WASHINGTON", "Trump: no rush on new Iran strikes; may not decide until 2027.", "Interview"),
    (34, "KYIV", "Ukraine to send large-scale food aid to nine countries.", "Kyiv"),
    (35, "BERN", "Switzerland calls the Myanmar ruling an important step.", "Swiss govt"),
    (36, "MUMBAI", "IndusInd ends its ex-CEO Kathpalia's job and seeks to recover his pay.", "Reuters"),
]

FOOTER = (
    "Every story here happened, or was first reported, on Saturday "
    "21 November 2026 in at least one time zone. Claims are attributed; "
    "unconfirmed reports are flagged as such. Sources: Reuters, AP, AFP, "
    "BBC, The Guardian, Al Jazeera, The Hindu, UN News, ESA, NASA, PIB. "
    "Original drawings, not photographs."
)


# ---------------------------------------------------------------- layout

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # --- top strip
    y = 14
    d.text((x0, y), "THE WORLD IN ONE DAY", font=F("sans_b", 17), fill=RED)
    right = "36 STORIES - 7 REGIONS - EVERY ONE DATED"
    rf = F("sans_b", 13)
    d.text((x1 - d.textlength(right, font=rf), y + 3), right, font=rf, fill=INK)
    y += 27
    d.rectangle([x0, y, x1, y + 3], fill=INK)
    y += 9

    # --- masthead + strapline
    mf = F("serif_b", 58)
    centered(d, W / 2, y, "Saturday 21 November 2026", mf, INK)
    y += 60
    sf = F("serif_i", 17)
    centered(d, W / 2, y, "COP31 runs past its deadline - Russian strikes "
                          "kill 12 in Ukraine - Riyadh downs three missiles",
             sf, (70, 70, 76))
    y += 24
    d.line([x0, y, x1, y], fill=INK, width=1)
    y += 8

    # --- stat strip
    cell = CW / 6.0
    num_f, lab_f = F("sans_b", 24), F("sans", 10)
    lab_lh = 12
    lab_lines = [wrap(d, lab, lab_f, cell - 14) for _, lab in STATS]
    stat_h = 30 + max(len(ls) for ls in lab_lines) * lab_lh + 4
    for i, (num, _lab) in enumerate(STATS):
        cx = x0 + i * cell
        if i:
            d.line([cx, y + 3, cx, y + stat_h - 5], fill=HAIR, width=1)
        centered(d, cx + cell / 2, y, num, num_f, NAVY)
        ly = y + 31
        for ln in lab_lines[i]:
            centered(d, cx + cell / 2, ly, ln, lab_f, GREY)
            ly += lab_lh
    y += stat_h + 2
    d.line([x0, y, x1, y], fill=HAIR, width=1)
    y += 4

    # --- region bar + legend
    total = sum(n for _, n, _ in REGIONS)
    rx = float(x0)
    for _name, n, color in REGIONS:
        seg = CW * n / total
        d.rectangle([rx, y, rx + seg - 2, y + 18], fill=color)
        rx += seg
    y += 21
    legend = " - ".join(f"{name} {n}" for name, n, _ in REGIONS)
    centered(d, W / 2, y, legend, F("sans_b", 12), INK)
    y += 18

    # --- DATE CHECK box
    dc_f = F("sans", 10)
    dc_lines = wrap(d, DATE_CHECK, dc_f, CW - 20)
    box_h = 17 + len(dc_lines) * 12 + 7
    d.rectangle([x0, y, x1, y + box_h], outline=RED, width=2)
    d.text((x0 + 10, y + 4), "DATE CHECK", font=F("sans_b", 11), fill=RED)
    ly = y + 19
    for ln in dc_lines:
        d.text((x0 + 10, ly), ln, font=dc_f, fill=INK)
        ly += 12
    y += box_h + 6

    # --- heroes: 3 columns, flow height = tallest column
    col_w, gut = 317, 12.5
    kick_f, head_f, brief_f = F("sans_b", 9), F("sans_b", 19), F("sans", 11)
    head_lh, brief_lh = 22, 13
    hero_h = 0
    for hero in HEROES:
        hh = 74 + 16 + 3
        hh += block_h(d, hero["head"], head_f, col_w, head_lh) + 2
        hh += block_h(d, hero["brief"], brief_f, col_w, brief_lh)
        hero_h = max(hero_h, hh)
    for i, hero in enumerate(HEROES):
        cx = int(x0 + i * (col_w + gut))
        hero["art"](d, cx, y, col_w, 74)
        ky = y + 74
        d.rectangle([cx, ky, cx + col_w, ky + 16], fill=RED)
        d.text((cx + 6, ky + 3), hero["kicker"], font=kick_f,
               fill=(255, 255, 255))
        ty = ky + 19
        ty = draw_block(d, cx, ty, hero["head"], head_f, INK, col_w, head_lh)
        ty += 2
        draw_block(d, cx, ty, hero["brief"], brief_f, (52, 52, 58),
                   col_w, brief_lh)
    y += hero_h + 6
    d.line([x0, y, x1, y], fill=HAIR, width=1)
    y += 5

    # --- mid grid: 3 x 2, flow rows
    lab_f2, head_f2, brief_f2 = F("sans_b", 9), F("sans_b", 12), F("sans", 10)
    head_lh2, brief_lh2 = 15, 12
    tiles = {}
    for mid in MIDS:
        tile = mid["art"]().resize((86, 34), Image.LANCZOS)
        tiles[mid["label"]] = tile

    def mid_h(mid):
        hh = 34 + 3
        hh += block_h(d, mid["head"], head_f2, col_w, head_lh2) + 1
        hh += block_h(d, mid["brief"], brief_f2, col_w, brief_lh2)
        return hh

    for row in range(2):
        cells = MIDS[row * 3:(row + 1) * 3]
        rh = max(mid_h(m) for m in cells)
        for j, mid in enumerate(cells):
            cx = int(x0 + j * (col_w + gut))
            img.paste(tiles[mid["label"]], (int(cx), y))
            d.text((cx + 94, y + 2), mid["label"].split("  ", 1)[0] + "  " +
                   mid["label"].split("  ", 1)[1], font=lab_f2, fill=RED)
            ty = y + 37
            ty = draw_block(d, cx, ty, mid["head"], head_f2, INK,
                            col_w, head_lh2)
            ty += 1
            draw_block(d, cx, ty, mid["brief"], brief_f2, (52, 52, 58),
                       col_w, brief_lh2)
        y += rh + 6
    d.line([x0, y, x1, y], fill=HAIR, width=1)
    y += 5

    # --- index header bar
    d.rectangle([x0, y, x1, y + 21], fill=NAVY)
    d.text((x0 + 8, y + 4), "ALSO ON SATURDAY 21 NOVEMBER - 27 MORE STORIES",
           font=F("sans_b", 12), fill=(255, 255, 255))
    y += 25

    # --- index: 3 columns x 9 rows, flow rows
    num_f, txt_f = F("sans_b", 10), F("sans", 10)
    txt_lh = 12
    for row in range(9):
        cells = INDEX[row * 3:(row + 1) * 3]
        rh = 0
        for num, place, text, src in cells:
            full = f"{place} - {text} ({src})"
            rh = max(rh, block_h(d, full, txt_f, col_w - 30, txt_lh))
        for j, (num, place, text, src) in enumerate(cells):
            cx = int(x0 + j * (col_w + gut))
            d.text((cx, y), str(num), font=num_f, fill=RED)
            draw_block(d, cx + 30, y, f"{place} - {text} ({src})",
                       txt_f, INK, col_w - 30, txt_lh)
        y += rh + 3

    # --- footer
    y += 1
    d.line([x0, y, x1, y], fill=HAIR, width=1)
    y += 4
    y = draw_block(d, x0, y, FOOTER, F("sans", 10), GREY, CW, 12)

    print(f"final y = {y} (canvas {H})")
    img.save(OUT)
    print(f"wrote {OUT}: {os.path.getsize(OUT)} bytes")
    return OUT


if __name__ == "__main__":
    build()
