#!/usr/bin/env python3
"""Render an event cover image (default 1600x640, 2.5:1, the Discord event banner ratio)
from a JSON spec, plus a small preview that shows how the cover reads as a thumbnail.

Usage:
  make_cover.py <spec.json> <out.jpg> [--preview <preview.png>] [--font <path>]

Layouts (spec["layout"]):

  compare   two images side by side (input -> output, before -> after), a label pill on
            each half and a dark badge with an arrow in the middle.
    {
      "layout": "compare",
      "left":  {"image": "figures/real.jpg",  "label": "Real Video"},
      "right": {"image": "figures/sim.jpg",   "label": "Simulation", "crop": [0, 0, 1920, 960]},
      "center": "Agent +\\n3D Tools"
    }

  showcase  dark background: title, subtitle, a row of steps with one highlighted and
            optionally a dashed "skip" arc with a warning line, a footer line, and a
            cropped screenshot on the right with an accent border.
    {
      "layout": "showcase",
      "title": "matt-flow", "subtitle": "讓 Claude Code 照流程走",
      "steps": ["問清楚", "寫規格", "動手做", "檢查", "複盤"], "highlight": 2,
      "skip": {"from": 0, "to": 2, "label": "想跳步？擋下來"},
      "footer": "每一步做完，把下一步指令交給你",
      "image": {"path": "figures/pane.png", "crop": [792, 18, 640, 500]},
      "accent": "#e8913a"
    }

Optional keys: "size": [w, h], "font": path to a CJK-capable font (bold weight preferred).
"crop" is [x, y, w, h] in the source image's pixels; without it the image is centre-cropped
to fill its slot. Emoji are not drawn by Pillow fonts: keep them out of cover text.
Needs Pillow.
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    # Linux (Noto CJK)
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    # Windows
    "C:/Windows/Fonts/msjhbd.ttc",
    "C:/Windows/Fonts/msjh.ttc",
    # macOS
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
]
# index of the Traditional Chinese face inside Noto CJK .ttc collections
NOTO_TC_INDEX = 2


def find_font(explicit=None):
    for path in ([explicit] if explicit else []) + FONT_CANDIDATES:
        if path and os.path.exists(path):
            return path
    sys.exit("No CJK font found: pass --font <path to a .ttf/.ttc/.otf>")


class Fonts:
    def __init__(self, path):
        self.path = path
        self.cache = {}

    def get(self, size):
        if size not in self.cache:
            index = NOTO_TC_INDEX if "NotoSansCJK" in self.path else 0
            try:
                self.cache[size] = ImageFont.truetype(self.path, size, index=index)
            except OSError:
                self.cache[size] = ImageFont.truetype(self.path, size)
        return self.cache[size]


def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def load_slot(spec, base_dir, w, h):
    """Open an image, apply an optional crop, then centre-crop to fill w x h."""
    path = spec.get("image") or spec.get("path")
    img = Image.open(os.path.join(base_dir, path)).convert("RGB")
    if spec.get("crop"):
        x, y, cw, ch = spec["crop"]
        img = img.crop((x, y, x + cw, y + ch))
    src_ratio, dst_ratio = img.width / img.height, w / h
    if src_ratio > dst_ratio:
        new_w = int(img.height * dst_ratio)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    else:
        new_h = int(img.width / dst_ratio)
        top = (img.height - new_h) // 2
        img = img.crop((0, top, img.width, top + new_h))
    return img.resize((w, h), Image.LANCZOS)


def pill(draw, fonts, text, cx, cy, size, bg=(255, 255, 255, 235), fg=(17, 17, 17)):
    font = fonts.get(size)
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    pad_x, pad_y = int(size * 0.55), int(size * 0.3)
    box = (cx - (r - l) / 2 - pad_x, cy - (b - t) / 2 - pad_y,
           cx + (r - l) / 2 + pad_x, cy + (b - t) / 2 + pad_y)
    draw.rounded_rectangle(box, radius=int(size * 0.45), fill=bg)
    draw.text((cx, cy), text, font=font, fill=fg, anchor="mm")


def render_compare(spec, base_dir, fonts, W, H):
    canvas = Image.new("RGB", (W, H), "white")
    half = W // 2
    canvas.paste(load_slot(spec["left"], base_dir, half, H), (0, 0))
    canvas.paste(load_slot(spec["right"], base_dir, W - half, H), (half, 0))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rectangle((half - 3, 0, half + 3, H), fill="white")
    label_size = int(H * 0.085)
    for side, cx in (("left", W / 4), ("right", W * 3 / 4)):
        if spec[side].get("label"):
            pill(d, fonts, spec[side]["label"], cx, H * 0.11, label_size)
    center = spec.get("center")
    if center:
        size = int(H * 0.072)
        font = fonts.get(size)
        l, t, r, b = d.multiline_textbbox((0, 0), center, font=font, spacing=size // 3, align="center")
        bw, bh = (r - l) + size * 1.4, (b - t) + size * 1.1
        cy = H / 2 - H * 0.03
        box = (half - bw / 2, cy - bh / 2, half + bw / 2, cy + bh / 2)
        d.rounded_rectangle(box, radius=22, fill=(17, 17, 17), outline="white", width=5)
        d.multiline_text((half, cy), center, font=font, fill="white", anchor="mm",
                         spacing=size // 3, align="center")
        # block arrow under the badge, pointing from input to output
        ay = box[3] + H * 0.04
        s = H * 0.045
        pts = [(half - 2.4 * s, ay), (half + 0.6 * s, ay), (half + 0.6 * s, ay - 0.6 * s),
               (half + 2.4 * s, ay + 0.8 * s), (half + 0.6 * s, ay + 2.2 * s),
               (half + 0.6 * s, ay + 1.6 * s), (half - 2.4 * s, ay + 1.6 * s)]
        d.polygon(pts, fill=(17, 17, 17), outline="white", width=4)
    canvas.paste(overlay, (0, 0), overlay)
    return canvas


def dashed_arc(d, start, end, lift, colour, width=5, dash=14, gap=10):
    """Quadratic curve below the step row, drawn dashed, with an arrowhead at `end`."""
    (x0, y0), (x2, y2) = start, end
    x1, y1 = (x0 + x2) / 2, max(y0, y2) + lift
    pts = []
    steps = 200
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * x1 + t ** 2 * x2
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * y1 + t ** 2 * y2
        pts.append((x, y))
    run, on = 0.0, True
    for a, b in zip(pts, pts[1:]):
        seg = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        if on:
            d.line((a, b), fill=colour, width=width)
        run += seg
        if run >= (dash if on else gap):
            run, on = 0.0, not on
    tip = pts[-1]
    d.polygon([(tip[0] - 16, tip[1] + 22), tip, (tip[0] + 10, tip[1] + 26)], fill=colour)


def render_showcase(spec, base_dir, fonts, W, H):
    bg = hex_rgb(spec.get("background", "#14161b"))
    accent = hex_rgb(spec.get("accent", "#e8913a"))
    warn = hex_rgb(spec.get("warn", "#ff5a5a"))
    canvas = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(canvas)

    # right: cropped screenshot with accent border
    right_x = W
    if spec.get("image"):
        img_spec = spec["image"]
        path = os.path.join(base_dir, img_spec["path"])
        src = Image.open(path).convert("RGB")
        if img_spec.get("crop"):
            x, y, cw, ch = img_spec["crop"]
            src = src.crop((x, y, x + cw, y + ch))
        dh = H - 80
        dw = int(src.width * dh / src.height)
        dw = min(dw, int(W * 0.48))
        src = src.resize((dw, int(src.height * dw / src.width)), Image.LANCZOS)
        dx, dy = W - dw - 40, (H - src.height) // 2
        mask = Image.new("L", src.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, src.width - 1, src.height - 1), radius=18, fill=255)
        canvas.paste(src, (dx, dy), mask)
        d.rounded_rectangle((dx, dy, dx + src.width, dy + src.height), radius=18, outline=accent, width=4)
        right_x = dx

    left, avail = 60, right_x - 60 - 30
    d.text((left, H * 0.06), spec.get("title", ""), font=fonts.get(int(H * 0.15)), fill="white")
    if spec.get("subtitle"):
        d.text((left + 4, H * 0.27), spec["subtitle"], font=fonts.get(int(H * 0.062)), fill=accent)

    steps = spec.get("steps", [])
    if steps:
        n = len(steps)
        gap = 26
        bw = (avail - gap * (n - 1)) / n
        bh = H * 0.115
        y0 = H * 0.47
        size = int(min(bh * 0.5, bw / max(len(s) for s in steps) * 0.9))
        centres = []
        for i, s in enumerate(steps):
            x = left + i * (bw + gap)
            on = i == spec.get("highlight")
            d.rounded_rectangle((x, y0, x + bw, y0 + bh), radius=14, fill=accent if on else (42, 47, 58))
            d.text((x + bw / 2, y0 + bh / 2), s, font=fonts.get(size), anchor="mm",
                   fill=bg if on else "white")
            centres.append(x + bw / 2)
            if i < n - 1:
                ax, ay = x + bw + 5, y0 + bh / 2
                d.polygon([(ax, ay - 9), (ax + 14, ay), (ax, ay + 9)], fill=(138, 147, 166))
        skip = spec.get("skip")
        if skip:
            dashed_arc(d, (centres[skip["from"]], y0 + bh + 12), (centres[skip["to"]], y0 + bh + 14),
                       H * 0.16, warn)
            if skip.get("label"):
                d.text((left + 10, y0 + bh + H * 0.2), skip["label"], font=fonts.get(int(H * 0.06)), fill=warn)
    if spec.get("footer"):
        d.text((left + 4, H * 0.88), spec["footer"], font=fonts.get(int(H * 0.047)), fill=(184, 192, 207))
    return canvas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("out")
    ap.add_argument("--preview", help="also write a 400 px wide thumbnail to check legibility")
    ap.add_argument("--font")
    args = ap.parse_args()

    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    base_dir = os.path.dirname(os.path.abspath(args.spec))
    W, H = spec.get("size", [1600, 640])
    fonts = Fonts(find_font(args.font or spec.get("font")))

    layouts = {"compare": render_compare, "showcase": render_showcase}
    if spec.get("layout") not in layouts:
        sys.exit(f"layout must be one of {sorted(layouts)}")
    img = layouts[spec["layout"]](spec, base_dir, fonts, W, H)
    img.save(args.out, quality=88)
    print(f"wrote {args.out} ({W}x{H})")
    if args.preview:
        thumb = img.resize((400, int(400 * H / W)), Image.LANCZOS)
        thumb.save(args.preview)
        print(f"wrote {args.preview} (400 px wide: every word on the cover should still read here)")


if __name__ == "__main__":
    main()
