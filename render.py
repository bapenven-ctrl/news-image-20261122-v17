#!/usr/bin/env python3
"""Paint "THE DAY IN NUMBERS" — one image of Sunday 22 November 2026.

Everything on the page is drawn here with Pillow primitives: no image
assets, no network, no clock, no randomness, so two runs write the same
bytes. The story data below is the page's single source of truth: the
breadth line in the masthead and the per-region counts are computed
from it, never typed by hand, so the printed numbers cannot drift
from the stories actually shown.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 16
CONTENT_W = W - 2 * MARGIN
GAP = 12

PAPER = (246, 241, 229)
INK = (23, 34, 44)
NAVY = (30, 58, 92)
RED = (179, 53, 43)
ORANGE = (224, 123, 36)
WHITE = (255, 255, 255)
SEA = (178, 205, 224)
SKY = (214, 228, 240)

REGION_COLORS = {
    "EUROPE": (47, 93, 138),
    "AFRICA": (128, 79, 20),
    "AMERICAS": (47, 107, 60),
    "MIDEAST": (140, 54, 39),
    "ASIA-PACIFIC": (94, 67, 150),
    "OCEANIA": (27, 99, 110),
    "WORLD": (66, 61, 54),
}
REGION_SHORT = {
    "EUROPE": "EUR", "AFRICA": "AFR", "AMERICAS": "AME", "MIDEAST": "MID",
    "ASIA-PACIFIC": "ASI", "OCEANIA": "OCE", "WORLD": "WOR",
}
CARD_TINTS = [
    (255, 255, 255), (253, 246, 227), (238, 244, 228), (251, 239, 230),
    (233, 239, 247), (242, 234, 249), (231, 242, 242), (251, 243, 217),
]

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_BOLD = f"{FONT_DIR}/LiberationSerif-Bold.ttf"
SANS = f"{FONT_DIR}/LiberationSans-Regular.ttf"
SANS_BOLD = f"{FONT_DIR}/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, line_h, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += line_h
    return y


# ---------------------------------------------------------------- data
# key, region, field, baked number, headline, one-line fact, archetype
FEATURED = [
    ("cop31", "EUROPE", "CLIMATE", "130+",
     "COP31 ENDS WITH NO DEAL ON FOSSIL FUELS",
     "The final 'Antalya Pact' draft dropped the words 'fossil fuels'. "
     "The EU and some 130 parties said no, and the longest UN climate "
     "summit on record closed with nothing signed.",
     "globe"),
    ("house", "AMERICAS", "POLITICS", "258",
     "DEMOCRATS TAKE THE HOUSE",
     "A North Carolina recount flipped the last big race: Hubbard beat "
     "Foxx. It is the biggest House majority since 1992; Republicans "
     "hold 173 seats.",
     "capitol"),
    ("benghazi", "AFRICA", "CONFLICT", "2",
     "RUSSIAN WARSHIP HIT AT BENGHAZI",
     "Merkury was struck by a suspected Ukrainian sea drone; "
     "a Malta-flag ship was targeted too.",
     "warship"),
    ("dymer", "EUROPE", "CONFLICT", "186",
     "186 DRONES IN ONE NIGHT OVER UKRAINE",
     "161 were downed or jammed; one tore into a five-storey block in "
     "Dymer, killing 4.",
     "drones"),
    ("markets", "WORLD", "MARKETS", "-3.7%",
     "AI SELL-OFF SLASHES WORLD MARKETS",
     "The Nikkei fell 5.06% too, as Nvidia faced an SEC accounting "
     "inquiry and its CEO stepped down.",
     "chart"),
    ("sparta", "EUROPE", "CONFLICT", "16",
     "RUSSIAN CARGO SHIP ABLAZE OFF FINLAND",
     "Still burning in the Gulf of Finland; all 16 crew evacuated.",
     "cargo"),
    ("bahrain", "MIDEAST", "CONFLICT", "2",
     "BAHRAIN: 2 HURT, RADAR CLAIM DISPUTED",
     "Tehran claimed two US radars; Manama says a civilian site was hit.",
     "radar"),
    ("icj", "ASIA-PACIFIC", "LAW", "2017",
     "ICJ: MYANMAR RESPONSIBLE FOR GENOCIDE",
     "The Hague backed Gambia's case over the 2017 Rohingya exodus.",
     "scales"),
    ("india", "ASIA-PACIFIC", "SPORT", "720",
     "INDIA DECLARE ON 720/9",
     "Rahul made 136 in the biggest Test total ever scored in "
     "New Zealand.",
     "stumps"),
]

# number, region, field, one-line brief
BRIEFS = [
    ("EUROPE", "DIPLOMACY", "Denmark expels Russian defence attaché; 3 held"),
    ("EUROPE", "TRANSPORT", "Belgium air controllers strike Mon; all flights off"),
    ("EUROPE", "SOCIETY", "France cost-of-living protests go on; 144 held"),
    ("EUROPE", "POLITICS", "Istanbul rallies vs opposition media takeover"),
    ("EUROPE", "SPORT", "Alcaraz beats Zverev 6-2 7-6, first ATP Finals title"),
    ("EUROPE", "SPORT", "England beat New Zealand at Twickenham"),
    ("AFRICA", "CONFLICT", "Sudan: drone hits home + UN site in Khartoum"),
    ("AFRICA", "DISASTER", "Nigeria mourning boat capsizes: 24 dead, 24 safe"),
    ("AMERICAS", "CYBER", "FBI probes NCIC database hack, 2nd in 2 months"),
    ("AMERICAS", "POLITICS", "Trump: contractors must report Congress requests"),
    ("AMERICAS", "LAW", "ICE arrests 2 at Seattle-Tacoma airport"),
    ("AMERICAS", "SPORT", "Skubal agrees $450M Mets deal, richest for a pitcher"),
    ("AMERICAS", "SPORT", "Wembanyama 50 pts, 19 reb as Spurs beat Pelicans"),
    ("AMERICAS", "SPORT", "Harden scores 51, passes Kobe with 26th 50-pt game"),
    ("AMERICAS", "SPORT", "KC Current win first NWSL title, beat Spirit 2-1"),
    ("AMERICAS", "LAW", "Jury: Rinderknecht guilty of Palisades fire, 12 died"),
    ("AMERICAS", "DIPLOMACY", "Haiti-El Salvador agree to build 3 prisons"),
    ("MIDEAST", "CONFLICT", "Gaza: Israeli strikes kill 3 near food-aid van"),
    ("MIDEAST", "CONFLICT", "Houthis claim Rabigh refinery hit; Saudis intercept"),
    ("MIDEAST", "ENERGY", "Iran starts power rationing, timed blackouts"),
    ("MIDEAST", "DISASTER", "Basra plant fire kills 4, about 30 hurt"),
    ("ASIA-PACIFIC", "POLITICS", "Hong Kong committee vote: ~99% turnout, a record"),
    ("ASIA-PACIFIC", "EDUCATION", "S. Korea education minister quits in AI-cheat scandal"),
    ("ASIA-PACIFIC", "HEALTH", "One CRISPR shot cuts bad cholesterol 52%"),
    ("ASIA-PACIFIC", "DISASTER", "Cikande candy-factory fire: 3 dead, 36 missing"),
    ("OCEANIA", "WEATHER", "Cyclone Xavier weakens near Cook Is.; Nassau safe"),
    ("WORLD", "SCIENCE", "Anthropic team claims AI-aided Riemann proof"),
    ("WORLD", "DIPLOMACY", "EU-Rwanda: deportation hub + 3% digital tax deal"),
]

DATE_CHECK_LINE = ("DATE CHECK — LEFT OUT AS EARLIER NEWS: 'El Chapo Isidro' held Sat 21 Nov · "
                   "Peru M6.7 quake Fri 20 Nov · BepiColombo orbit Sat 21 Nov · "
                   "400-drone barrage 19-20 Nov")


# ------------------------------------------------------------- pictograms
def pic_globe(d, x, y, w, h):
    r = min(w, h) // 2 - 4
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(198, 222, 205), outline=NAVY, width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=NAVY, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY, width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=NAVY, width=2)
    d.polygon([(cx - r + 14, cy - r + 22), (cx - 6, cy - r + 12), (cx + 2, cy - r + 30),
               (cx - 14, cy - r + 38)], fill=(94, 141, 96))
    d.polygon([(cx + 8, cy + 16), (cx + 30, cy + 8), (cx + 34, cy + 30),
               (cx + 14, cy + 38)], fill=(94, 141, 96))


def pic_capitol(d, x, y, w, h):
    cx = x + w // 2
    base = y + h - 8
    d.polygon([(cx, y + 6), (cx - 30, base - 34), (cx + 30, base - 34)], fill=NAVY)
    d.rectangle([cx - 3, y + 2, cx + 3, y + 12], fill=NAVY)
    d.rectangle([x + 8, base - 34, x + w - 8, base - 28], fill=NAVY)
    for i in range(5):
        col_x = x + 14 + i * (w - 28) // 4 - 3
        d.rectangle([col_x, base - 28, col_x + 6, base - 6], fill=NAVY)
    d.rectangle([x + 6, base - 6, x + w - 6, base], fill=NAVY)


def _sea(d, x, y, w, h):
    d.rectangle([x, y + h - 16, x + w, y + h], fill=SEA)
    for i in range(3):
        yy = y + h - 12 + i * 5
        d.line([x + 4 + i * 9, yy, x + w - 14 - i * 5, yy], fill=(120, 160, 195), width=2)


def _explosion(d, cx, cy, r):
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r // 2
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    d.polygon(pts, fill=ORANGE, outline=RED)
    d.ellipse([cx - r // 4, cy - r // 4, cx + r // 4, cy + r // 4], fill=RED)


def _smoke(d, cx, cy):
    for dx, dy, r in [(0, 0, 10), (12, -8, 8), (-11, -7, 7), (4, -16, 6)]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(105, 105, 105))


def pic_warship(d, x, y, w, h):
    hull_y = y + h - 22
    d.polygon([(x + 8, hull_y), (x + w - 4, hull_y), (x + w - 18, hull_y + 10),
               (x + 20, hull_y + 10)], fill=INK)
    d.rectangle([x + 30, hull_y - 14, x + 58, hull_y], fill=INK)
    d.rectangle([x + 40, hull_y - 22, x + 48, hull_y - 14], fill=INK)
    _explosion(d, x + w - 16, hull_y - 2, 15)
    _smoke(d, x + w - 20, hull_y - 22)
    _sea(d, x, y, w, h)


def pic_cargo(d, x, y, w, h):
    hull_y = y + h - 22
    d.polygon([(x + 4, hull_y), (x + w - 8, hull_y), (x + w - 20, hull_y + 10),
               (x + 16, hull_y + 10)], fill=(120, 62, 40))
    cols = [(176, 92, 46), (47, 93, 138), (47, 107, 60), (140, 54, 39)]
    for i, c in enumerate(cols):
        bx = x + 14 + i * 20
        d.rectangle([bx, hull_y - 12, bx + 17, hull_y], fill=c)
        if i % 2 == 0:
            d.rectangle([bx, hull_y - 23, bx + 17, hull_y - 13], fill=c)
    for fx in (x + 30, x + 52):
        d.polygon([(fx, hull_y - 24), (fx + 7, hull_y - 40), (fx + 14, hull_y - 24)], fill=ORANGE)
        d.polygon([(fx + 4, hull_y - 24), (fx + 7, hull_y - 33), (fx + 10, hull_y - 24)], fill=RED)
    _smoke(d, x + 44, hull_y - 46)
    _sea(d, x, y, w, h)


def pic_drones(d, x, y, w, h):
    bx, by, bw, bh = x + 6, y + h - 52, 44, 44
    d.rectangle([bx, by, bx + bw, by + bh], fill=(90, 98, 110))
    for r in range(3):
        for c in range(3):
            wx, wy = bx + 6 + c * 13, by + 6 + r * 13
            lit = (r + c) % 3 != 0
            d.rectangle([wx, wy, wx + 8, wy + 8], fill=(255, 209, 102) if lit else (60, 66, 76))
    for dx, dy in [(x + w - 34, y + 8), (x + w - 58, y + 20), (x + w - 22, y + 26)]:
        d.line([dx - 7, dy, dx + 7, dy], fill=INK, width=3)
        d.line([dx, dy - 5, dx, dy + 5], fill=INK, width=3)
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)


def pic_chart(d, x, y, w, h):
    d.line([x + 6, y + 6, x + 6, y + h - 8], fill=INK, width=2)
    d.line([x + 6, y + h - 8, x + w - 4, y + h - 8], fill=INK, width=2)
    pts = [(x + 10, y + 14), (x + w // 3, y + 20), (x + w // 2, y + h // 2),
           (x + w - 16, y + h - 14)]
    d.line(pts, fill=RED, width=4)
    px, py = pts[-1]
    d.polygon([(px, py), (px - 12, py - 2), (px - 4, py - 11)], fill=RED)


def pic_radar(d, x, y, w, h):
    cx, base = x + w // 3, y + h - 6
    d.polygon([(cx - 4, base), (cx + 10, y + 16), (cx + 18, y + 22), (cx + 2, base)], fill=NAVY)
    d.line([cx + 12, y + 18, cx + 30, y + 8], fill=NAVY, width=3)
    for r in (12, 20, 28):
        d.arc([cx + 22 - r // 2, y + 4 - r // 2, cx + 22 + r, y + 4 + r], -60, 60, fill=ORANGE, width=3)


def pic_scales(d, x, y, w, h):
    cx = x + w // 2
    top, base = y + 8, y + h - 8
    d.line([cx, top, cx, base], fill=INK, width=4)
    d.line([cx - w // 3, top + 8, cx + w // 3, top + 8], fill=INK, width=4)
    d.ellipse([cx - 5, top - 4, cx + 5, top + 6], fill=INK)
    for sx in (cx - w // 3, cx + w // 3):
        d.line([sx, top + 8, sx - 12, top + 30], fill=INK, width=2)
        d.line([sx, top + 8, sx + 12, top + 30], fill=INK, width=2)
        d.arc([sx - 14, top + 18, sx + 14, top + 42], 0, 180, fill=INK, width=3)
    d.rectangle([cx - 16, base, cx + 16, base + 5], fill=INK)


def pic_stumps(d, x, y, w, h):
    base = y + h - 10
    d.rectangle([x + 4, base, x + w - 4, base + 6], fill=(94, 141, 96))
    for i in range(3):
        sx = x + w // 2 - 16 + i * 14
        d.rectangle([sx, y + 16, sx + 5, base], fill=(176, 132, 52))
    d.rectangle([x + w // 2 - 18, y + 10, x + w // 2 + 20, y + 15], fill=(140, 100, 36))
    d.ellipse([x + w - 28, base - 15, x + w - 13, base], fill=RED)


PICS = {"globe": pic_globe, "capitol": pic_capitol, "warship": pic_warship,
        "drones": pic_drones, "chart": pic_chart, "cargo": pic_cargo,
        "radar": pic_radar, "scales": pic_scales, "stumps": pic_stumps}


def stamp_no_deal(d, cx, cy):
    layer = Image.new("RGBA", (150, 54), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([3, 3, 146, 50], outline=RED + (255,), width=4)
    ld.text((75, 27), "NO DEAL", font=font(SANS_BOLD, 27), fill=RED + (255,), anchor="mm")
    layer = layer.rotate(11, resample=Image.BICUBIC, expand=True)
    return layer, cx, cy


def card_header(d, x, y, w, region, field):
    col = REGION_COLORS[region]
    f_chip = font(SANS_BOLD, 13)
    label = region
    tw = d.textlength(label, font=f_chip)
    d.rectangle([x + 10, y + 8, x + 18 + tw, y + 29], fill=col)
    d.text((x + 14, y + 11), label, font=f_chip, fill=WHITE)
    f_field = font(SANS_BOLD, 12)
    fw = d.textlength(field, font=f_field)
    d.text((x + w - 10 - fw, y + 12), field, font=f_field, fill=col)


def draw_pic(img, fn, x, y, w, h):
    """Draw a pictogram on its own layer at a standard size, then scale
    it into the slot so it can never spill over neighbouring text."""
    layer = Image.new("RGBA", (120, 90), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    fn(ld, 0, 0, 120, 90)
    layer = layer.resize((w, h), Image.LANCZOS)
    img.paste(layer, (x, y), layer)


def draw_card(img, box, item, tint, big=False):
    d = ImageDraw.Draw(img)
    x, y, w, h = box
    key, region, field, number, headline, fact, arche = item
    d.rectangle([x, y, x + w, y + h], fill=tint, outline=(178, 168, 148), width=2)
    card_header(d, x, y, w, region, field)
    pic_fn = PICS[arche]
    if big and w > 500:
        draw_pic(img, pic_fn, x + 12, y + 40, 176, 104)
        d.text((x + 12, y + 148), number, font=font(SANS_BOLD, 47), fill=NAVY)
        tx = x + 208
        yy = text_block(d, (tx, y + 42), headline, font(SANS_BOLD, 33), INK, w - 220, 38, 2)
        text_block(d, (tx, yy + 8), fact, font(SANS, 15), INK, w - 220, 20, 4)
    elif big:  # second lead card, narrower
        draw_pic(img, pic_fn, x + 10, y + 38, 104, 76)
        d.text((x + 10, y + 120), number, font=font(SANS_BOLD, 38), fill=NAVY)
        tx = x + 128
        yy = text_block(d, (tx, y + 40), headline, font(SANS_BOLD, 24), INK, w - 140, 28, 3)
        text_block(d, (tx, yy + 7), fact, font(SANS, 14), INK, w - 140, 19, 5)
    elif w > 280:  # row-2 card: left rail
        draw_pic(img, pic_fn, x + 10, y + 38, 78, 62)
        d.text((x + 10, y + 104), number, font=font(SANS_BOLD, 27), fill=NAVY)
        tx = x + 100
        yy = text_block(d, (tx, y + 40), headline, font(SANS_BOLD, 19), INK, w - 110, 22, 3)
        text_block(d, (tx, yy + 5), fact, font(SANS, 13), INK, w - 110, 16, 3)
    else:  # row-3 card: pic + number on one row, text below
        draw_pic(img, pic_fn, x + 10, y + 34, 52, 34)
        nw = d.textlength(number, font=font(SANS_BOLD, 26))
        d.text((x + w - 10 - nw, y + 36), number, font=font(SANS_BOLD, 26), fill=NAVY)
        yy = text_block(d, (x + 10, y + 72), headline, font(SANS_BOLD, 17), INK, w - 20, 19, 2)
        text_block(d, (x + 10, yy + 2), fact, font(SANS, 12), INK, w - 20, 14, 2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- counts, computed from the data itself
    stories = [(it[1], it[2]) for it in FEATURED] + [(r, f) for r, f, _ in BRIEFS]
    total = len(stories)
    regions = {}
    fields = set()
    for r, f in stories:
        regions[r] = regions.get(r, 0) + 1
        fields.add(f)
    region_order = ["EUROPE", "AMERICAS", "ASIA-PACIFIC", "MIDEAST", "AFRICA", "WORLD", "OCEANIA"]
    breadth = (f"{total} STORIES · {len(regions)} REGIONS · {len(fields)} FIELDS — "
               + " · ".join(f"{r} {regions[r]}" for r in region_order))
    assert total == 37, total

    # ---- masthead
    d.text((MARGIN, 14), "THE DAY IN NUMBERS — ONE IMAGE, ONE DAY, THE WHOLE WORLD",
           font=font(SANS_BOLD, 15), fill=INK)
    d.text((MARGIN, 34), "SUNDAY 22 NOVEMBER 2026", font=font(SERIF_BOLD, 61), fill=RED)
    d.rectangle([MARGIN, 106, MARGIN + CONTENT_W, 130], fill=NAVY)
    bsize = 16
    while d.textlength(breadth, font=font(SANS_BOLD, bsize)) > CONTENT_W - 20 and bsize > 10:
        bsize -= 1
    bw = d.textlength(breadth, font=font(SANS_BOLD, bsize))
    d.text((MARGIN + (CONTENT_W - bw) / 2, 110), breadth, font=font(SANS_BOLD, bsize), fill=WHITE)

    # ---- featured cards
    lead_y, lead_h = 142, 212
    draw_card(img, (MARGIN, lead_y, 604, lead_h), FEATURED[0], CARD_TINTS[0], big=True)
    draw_card(img, (MARGIN + 616, lead_y, 376, lead_h), FEATURED[1], CARD_TINTS[4], big=True)
    # NO DEAL stamp across the globe of the lead card
    stamp, sx, sy = stamp_no_deal(d, 0, 0)
    img.paste(stamp, (MARGIN + 18, lead_y + 52), stamp)
    d = ImageDraw.Draw(img)

    row2_y, row_h = 366, 144
    for i, item in enumerate(FEATURED[2:5]):
        draw_card(img, (MARGIN + i * (322 + GAP), row2_y, 322, row_h), item, CARD_TINTS[(i + 1) % len(CARD_TINTS)])
    row3_y = 522
    for i, item in enumerate(FEATURED[5:9]):
        draw_card(img, (MARGIN + i * (239 + GAP), row3_y, 239, row_h), item, CARD_TINTS[(i + 3) % len(CARD_TINTS)])

    # ---- briefs
    bh_y = 682
    d.text((MARGIN, bh_y), "THE REST OF THE DAY — 28 MORE STORIES, NUMBERED AND DATED",
           font=font(SANS_BOLD, 19), fill=INK)
    d.line([MARGIN, bh_y + 28, MARGIN + CONTENT_W, bh_y + 28], fill=NAVY, width=3)
    col_w = (CONTENT_W - GAP) // 2
    f_brief = font(SANS, 14)
    f_num = font(SANS_BOLD, 14)
    top = bh_y + 36
    for idx, (region, field, brief) in enumerate(BRIEFS):
        col = 0 if idx < 14 else 1
        row = idx if idx < 14 else idx - 14
        x = MARGIN + col * (col_w + GAP)
        y = top + row * 18
        num = f"{idx + 10:02d}"
        d.text((x, y), num, font=f_num, fill=REGION_COLORS[region])
        tag = REGION_SHORT[region]
        d.text((x + 30, y), tag, font=f_num, fill=REGION_COLORS[region])
        line = f"{brief} [{field}]"
        d.text((x + 66, y), line, font=f_brief, fill=INK)

    # ---- footer: date check
    fy = 984
    d.line([MARGIN, fy - 6, MARGIN + CONTENT_W, fy - 6], fill=NAVY, width=2)
    fw = d.textlength(DATE_CHECK_LINE, font=font(SANS_BOLD, 12))
    d.text((MARGIN + (CONTENT_W - fw) / 2, fy), DATE_CHECK_LINE, font=font(SANS_BOLD, 12), fill=RED)
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build().save(out, optimize=True)
    print(f"saved {out}")
