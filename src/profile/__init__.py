from __future__ import annotations

import argparse
import io
import json, os
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageDraw, ImageFont

root = os.path.dirname(__file__).rstrip(os.sep)

_FONT_BOLD = root + os.sep + "Liberation Sans Bold.ttf"


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(_FONT_BOLD, size)


C_BORDER  = (213, 125, 248)
C_BG      = (247, 246, 251)
C_PILL_BG = (238, 230, 227)
C_BROWN   = (113, 63, 25)
C_BAR     = (213, 125, 248)
C_WHITE   = (255, 255, 255)
C_DIAMOND = (228, 223, 240)

CARD_W = 2000
CARD_H = 1142
BORDER = 20
RADIUS = 32

PHOTO_R   = 945
CONTENT_X = 1004

EMOJI_X      = CONTENT_X
EMOJI_Y      = 70
EMOJI_H      = 240
NAME_X       = 1204
NAME_FONT_SZ = 90

PILL_W  = 351
PILL_H  = 65
PILL_R  = 20
PILL_YS = [352, 437, 522, 607, 692]

LABEL_FONT_SZ = 46
VALUE_X       = 1375
VALUE_FONT_SZ = 52

BAR_Y       = 795
BAR_H       = 60
BAR_X       = CONTENT_X
BAR_W       = 951
BAR_R       = 12
BAR_FONT_SZ = 44

CMT_X       = CONTENT_X + 6
CMT_Y       = 878
CMT_FONT_SZ = 46

DIA_START_X = 1620
DIA_STEP_X  = 130
DIA_STEP_Y  = 118
DIA_HALF    = 55

LOGO_SIZE   = 500
LOGO_Y_OFF  = 143

SLASH_LEAN  = 36
SLASH_W     = 28
SLASH_GAP   = 52
SLASH_RIGHT = BAR_X + BAR_W - 18


def _fetch(url: str) -> Image.Image:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGBA")


def _square_crop(img: Image.Image) -> Image.Image:
    w, h = img.size
    if w <= h:
        return img
    s = h
    return img.crop(((w - s) // 2, 0, (w + s) // 2, h))


def _text_wh(draw: ImageDraw.ImageDraw, text: str,
             font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0], bb[3] - bb[1]


def _place_photo(card: Image.Image, profile: Image.Image) -> None:
    tw = PHOTO_R - BORDER
    th = CARD_H - BORDER * 2
    pw, ph = profile.size
    scale = max(tw / pw, th / ph)
    nw, nh = int(pw * scale), int(ph * scale)
    img = profile.resize((nw, nh), Image.LANCZOS)
    cx = (nw - tw) // 2
    cy = (nh - th) // 2
    img = img.crop((cx, cy, cx + tw, cy + th))
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [(0, 0), (tw + RADIUS, th - 1)], radius=RADIUS, fill=255
    )
    card.paste(img.convert("RGB"), (BORDER, BORDER), mask)


def _place_logo(card: Image.Image) -> None:
    logo_path = os.path.join(root, "logo.png")
    if not os.path.exists(logo_path):
        return
    logo = Image.open(logo_path).convert("RGBA")
    logo = logo.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
    card.paste(logo, (BORDER, BORDER-LOGO_Y_OFF), logo.split()[3])


def _draw_diamonds(draw: ImageDraw.ImageDraw) -> None:
    s = DIA_HALF
    for ox in range(DIA_START_X, CARD_W + DIA_STEP_X, DIA_STEP_X):
        for oy in range(BORDER + 10, BAR_Y - DIA_STEP_Y, DIA_STEP_Y):
            cx = ox
            cy = oy + DIA_STEP_Y // 2
            pts = [
                (cx,     cy - s),
                (cx + s, cy),
                (cx,     cy + s),
                (cx - s, cy),
            ]
            draw.polygon(pts, outline=C_DIAMOND, fill=None)


def _place_header(card: Image.Image, draw: ImageDraw.ImageDraw,
                  emoji: Image.Image, name: str) -> None:
    emoji  = _square_crop(emoji)
    ew, eh = emoji.size
    scale  = EMOJI_H / eh
    new_w  = int(ew * scale)
    emoji  = emoji.resize((new_w, EMOJI_H), Image.LANCZOS)
    card.paste(emoji, (EMOJI_X, EMOJI_Y), emoji.split()[3])
    font   = _font(NAME_FONT_SZ)
    _, th  = _text_wh(draw, name, font)
    text_y = EMOJI_Y + (EMOJI_H - th) // 2
    draw.text((NAME_X, text_y), name, font=font, fill=C_BROWN)


def _draw_pills(draw: ImageDraw.ImageDraw, labels: dict[str, Any]) -> None:
    f_label = _font(LABEL_FONT_SZ)
    f_value = _font(VALUE_FONT_SZ)
    for i, (key, value) in enumerate(labels.items()):
        if i >= len(PILL_YS):
            break
        py = PILL_YS[i]
        draw.rounded_rectangle(
            [(CONTENT_X, py), (CONTENT_X + PILL_W, py + PILL_H)],
            radius=PILL_R,
            fill=C_PILL_BG,
        )
        lw, lh = _text_wh(draw, str(key), f_label)
        lx = CONTENT_X + (PILL_W - lw) // 2
        ly = py + (PILL_H - lh) // 2 - 1
        draw.text((lx, ly), str(key), font=f_label, fill=C_BROWN)
        _, vh = _text_wh(draw, str(value), f_value)
        vy = py + (PILL_H - vh) // 2 - 1
        draw.text((VALUE_X, vy), str(value), font=f_value, fill=C_BROWN)


def _draw_comment_section(card: Image.Image, draw: ImageDraw.ImageDraw,
                           comment: str, bg_color: tuple) -> None:
    bx2 = BAR_X + BAR_W

    draw.rounded_rectangle(
        [(BAR_X, BAR_Y), (bx2, BAR_Y + BAR_H)],
        radius=BAR_R,
        fill=C_BAR,
    )

    for i in range(2):
        rx = SLASH_RIGHT - i * (SLASH_W + SLASH_GAP)
        lx = rx - SLASH_W
        pts = [
            (lx - SLASH_LEAN, BAR_Y),
            (rx - SLASH_LEAN, BAR_Y),
            (rx + SLASH_LEAN, BAR_Y + BAR_H),
            (lx + SLASH_LEAN, BAR_Y + BAR_H),
        ]
        draw.polygon(pts, fill=bg_color)

    f_bar = _font(BAR_FONT_SZ)
    draw.text(
        (BAR_X + 22, BAR_Y + (BAR_H - BAR_FONT_SZ) // 2 - 3),
        "Comment", font=f_bar, fill=C_WHITE,
    )

    f_cmt = _font(CMT_FONT_SZ)
    draw.text((CMT_X, CMT_Y), comment, font=f_cmt, fill=C_BROWN)


def _draw_border(draw: ImageDraw.ImageDraw) -> None:
    for t in range(BORDER):
        draw.rounded_rectangle(
            [(t, t), (CARD_W - 1 - t, CARD_H - 1 - t)],
            radius=max(RADIUS - t, 0),
            outline=C_BORDER,
            width=1,
        )


def card(
    profile_url: str,
    emoji_url: str,
    name: str,
    labels: dict[str, Any],
    comment: str,
    background_url: str | None = None,
    output_path: str | Path = "trainer_card_out.png",
) -> Path:
    profile = _fetch(profile_url)
    emoji   = _fetch(emoji_url)

    img    = Image.new("RGB", (CARD_W, CARD_H), C_BG)
    bar_bg = C_BG

    if background_url:
        _bg = _fetch(background_url) if ":" in background_url else Image.open(background_url)
        bg  = _bg.convert("RGB")
        bw, bh = bg.size
        scale = max(CARD_W / bw, CARD_H / bh)
        nw, nh = int(bw * scale), int(bh * scale)
        bg = bg.resize((nw, nh), Image.LANCZOS)
        cx = (nw - CARD_W) // 2
        cy = (nh - CARD_H) // 2
        bg = bg.crop((cx, cy, cx + CARD_W, cy + CARD_H))
        mask = Image.new("L", (CARD_W, CARD_H), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [(0, 0), (CARD_W - 1, CARD_H - 1)], radius=RADIUS, fill=255
        )
        img.paste(bg, (0, 0), mask)
        px     = bg.getpixel((CARD_W // 2, CARD_H // 2))
        bar_bg = px[:3] if len(px) == 4 else px

    _place_photo(img, profile)

    draw = ImageDraw.Draw(img)
    _draw_diamonds(draw)
    _place_header(img, draw, emoji, name)
    _draw_pills(draw, labels)
    _draw_comment_section(img, draw, comment, bar_bg)
    _place_logo(img)
    _draw_border(draw)

    out = Path(output_path)
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Generate a trainer card PNG.")
    ap.add_argument("--profile",    required=True)
    ap.add_argument("--emoji",      required=True)
    ap.add_argument("--name",       default="Trainer")
    ap.add_argument("--labels",     required=True)
    ap.add_argument("--comment",    required=True)
    ap.add_argument("--background", default=None)
    ap.add_argument("--output",     default="trainer_card_out.png")
    args = ap.parse_args()
    card(
        profile_url=args.profile,
        emoji_url=args.emoji,
        name=args.name,
        labels=json.loads(args.labels),
        comment=args.comment,
        background_url=args.background,
        output_path=args.output,
    )
