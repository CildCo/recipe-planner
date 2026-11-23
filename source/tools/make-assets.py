"""生成饭桌的封面和 tabBar 图标。

用法：
    python tools/make-assets.py

输出：
    backend/app/static/covers/<slug>.jpg   1200x900 封面
    miniprogram/assets/covers/<slug>.jpg   小程序本地封面
    miniprogram/assets/tabbar/*.png        81x81 图标
"""
from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

import sys

from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
RECIPES = ROOT / "backend" / "app" / "data" / "recipes.json"
STATIC_COVERS = ROOT / "backend" / "app" / "static" / "covers"
MINI_COVERS = ROOT / "miniprogram" / "assets" / "covers"
TABBAR = ROOT / "miniprogram" / "assets" / "tabbar"

FONT_SERIF = "C:/Windows/Fonts/NotoSerifSC-VF.ttf"
FONT_SANS = "C:/Windows/Fonts/NotoSansSC-VF.ttf"
FONT_SERIF_FALLBACK = "C:/Windows/Fonts/simsun.ttc"
FONT_SANS_FALLBACK = "C:/Windows/Fonts/simhei.ttf"

PALETTES = {
    "tomato": {"bg": "#F1DCD4", "ink": "#5B2A22", "accent": "#C94F3D", "second": "#D9A441", "green": "#65704B"},
    "olive": {"bg": "#E5E5D0", "ink": "#39422C", "accent": "#65704B", "second": "#C9943F", "green": "#4F7A6A"},
    "mustard": {"bg": "#F2E3C4", "ink": "#6C4A1B", "accent": "#C9943F", "second": "#C94F3D", "green": "#65704B"},
    "plum": {"bg": "#E8D4D9", "ink": "#542A34", "accent": "#7C4A56", "second": "#C9943F", "green": "#65704B"},
    "jade": {"bg": "#D9E7DE", "ink": "#2C4A3E", "accent": "#4F7A6A", "second": "#C9943F", "green": "#65704B"},
}

CATEGORY_LABELS = {
    "quick": "快手菜",
    "home": "家常菜",
    "soup": "汤羹",
    "staple": "主食",
    "breakfast": "早餐",
}


def font(size: int, serif: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_SERIF if serif else FONT_SANS
    fallback = FONT_SERIF_FALLBACK if serif else FONT_SANS_FALLBACK
    for candidate in (path, fallback):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def ellipse(draw: ImageDraw.ImageDraw, box, fill, outline=None, width=3):
    draw.ellipse(box, fill=fill, outline=outline, width=width)


def steam(draw: ImageDraw.ImageDraw, x: int, y: int, color: str, scale: float = 1.0):
    for offset in (0, 42, 84):
        points = []
        for step in range(13):
            t = step / 12
            px = x + offset * scale + math.sin(t * math.pi * 2) * 12 * scale
            py = y - t * 76 * scale
            points.append((px, py))
        draw.line(points, fill=color, width=max(2, int(4 * scale)), joint="curve")


def motif_wok(draw, cx, cy, p, scale=1.0):
    w, h = 430 * scale, 230 * scale
    draw.rounded_rectangle(
        (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
        radius=int(70 * scale),
        fill=p["ink"],
    )
    draw.ellipse((cx + w / 2 - 30 * scale, cy - 16 * scale, cx + w / 2 + 170 * scale, cy + 18 * scale), fill=p["ink"])
    ellipse(draw, (cx - w / 2 + 22, cy - h / 2 + 20, cx + w / 2 - 22, cy + h / 2 - 22), "#FFF9EE")
    # 食材
    ellipse(draw, (cx - 96 * scale, cy - 56 * scale, cx - 12 * scale, cy + 28 * scale), p["accent"], p["ink"], 3)
    draw.rounded_rectangle(
        (cx + 6 * scale, cy - 48 * scale, cx + 96 * scale, cy + 18 * scale),
        radius=int(14 * scale),
        fill=p["second"],
        outline=p["ink"],
        width=3,
    )
    for dx, dy, r in [(-40, 58, 16), (4, 66, 12), (46, 54, 18), (78, 72, 9)]:
        ellipse(draw, (cx + dx * scale - r, cy + dy * scale - r, cx + dx * scale + r, cy + dy * scale + r), p["green"])
    steam(draw, cx - 20, cy - 80, p["ink"], 0.9)


def motif_pot(draw, cx, cy, p, scale=1.0):
    w, h = 400 * scale, 230 * scale
    draw.rounded_rectangle(
        (cx - w / 2, cy - h / 2 + 24, cx + w / 2, cy + h / 2),
        radius=int(54 * scale),
        fill=p["ink"],
    )
    draw.rectangle((cx - w / 2 - 46 * scale, cy - 10 * scale, cx - w / 2 + 10 * scale, cy + 18 * scale), fill=p["ink"])
    draw.rectangle((cx + w / 2 - 10 * scale, cy - 10 * scale, cx + w / 2 + 46 * scale, cy + 18 * scale), fill=p["ink"])
    ellipse(draw, (cx - w / 2 + 24, cy - h / 2 + 28, cx + w / 2 - 24, cy + h / 2 - 26), "#FFF9EE")
    ellipse(draw, (cx - w / 2 + 28, cy - h / 2 + 8, cx + w / 2 - 28, cy - h / 2 + 56), p["accent"], p["ink"], 3)
    ellipse(draw, (cx - 14 * scale, cy - h / 2 - 2, cx + 14 * scale, cy - h / 2 + 26), p["paper"] if "paper" in p else p["bg"], p["ink"], 3)
    for dx, dy, r in [(-60, 34, 20), (-8, 46, 14), (48, 36, 22), (84, 64, 10)]:
        ellipse(draw, (cx + dx * scale - r, cy + dy * scale - r, cx + dx * scale + r, cy + dy * scale + r), p["second"])
    steam(draw, cx - 10, cy - 100, p["ink"], 0.85)


def motif_plate(draw, cx, cy, p, scale=1.0):
    ellipse(draw, (cx - 270 * scale, cy - 170 * scale, cx + 270 * scale, cy + 170 * scale), "#FFF9EE", p["ink"], 4)
    ellipse(draw, (cx - 210 * scale, cy - 120 * scale, cx + 210 * scale, cy + 120 * scale), p["bg"], p["ink"], 2)
    # 鱼
    draw.ellipse((cx - 150 * scale, cy - 54 * scale, cx + 108 * scale, cy + 56 * scale), fill=p["accent"], outline=p["ink"], width=3)
    draw.polygon(
        [
            (cx + 94 * scale, cy),
            (cx + 186 * scale, cy - 62 * scale),
            (cx + 186 * scale, cy + 62 * scale),
        ],
        fill=p["accent"],
        outline=p["ink"],
    )
    ellipse(draw, (cx - 112 * scale, cy - 22 * scale, cx - 92 * scale, cy - 2 * scale), "#FFF9EE", p["ink"], 2)
    for offset in (-70, -20, 30, 80):
        draw.arc(
            (cx + offset * scale - 18, cy - 30 * scale, cx + offset * scale + 18, cy + 30 * scale),
            250,
            110,
            fill=p["ink"],
            width=3,
        )
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x = cx + math.cos(rad) * 232 * scale
        y = cy + math.sin(rad) * 138 * scale
        ellipse(draw, (x - 7, y - 7, x + 7, y + 7), p["green"])
    steam(draw, cx - 10, cy - 170, p["ink"], 0.7)


def motif_soup(draw, cx, cy, p, scale=1.0):
    ellipse(draw, (cx - 250 * scale, cy - 90 * scale, cx + 250 * scale, cy + 190 * scale), p["ink"])
    ellipse(draw, (cx - 234 * scale, cy - 96 * scale, cx + 234 * scale, cy + 150 * scale), "#FFF9EE")
    ellipse(draw, (cx - 208 * scale, cy - 78 * scale, cx + 208 * scale, cy + 116 * scale), p["accent"])
    for offset in (-90, -30, 30, 90):
        draw.arc(
            (cx + offset * scale - 40 * scale, cy - 40 * scale, cx + offset * scale + 40 * scale, cy + 60 * scale),
            200,
            340,
            fill="#FFF9EE",
            width=4,
        )
    for dx, dy, r in [(-110, 20, 14), (70, -6, 10), (120, 60, 16), (-20, 74, 8)]:
        ellipse(draw, (cx + dx * scale - r, cy + dy * scale - r, cx + dx * scale + r, cy + dy * scale + r), p["green"])
    steam(draw, cx - 20, cy - 120, p["ink"], 0.85)


def motif_noodles(draw, cx, cy, p, scale=1.0):
    ellipse(draw, (cx - 250 * scale, cy - 100 * scale, cx + 250 * scale, cy + 190 * scale), p["ink"])
    ellipse(draw, (cx - 230 * scale, cy - 106 * scale, cx + 230 * scale, cy + 150 * scale), "#FFF9EE")
    ellipse(draw, (cx - 200 * scale, cy - 84 * scale, cx + 200 * scale, cy + 112 * scale), p["second"])
    for index in range(5):
        points = []
        for step in range(20):
            t = step / 19
            x = cx - 170 * scale + t * 340 * scale
            y = cy - 20 * scale + math.sin(t * math.pi * 5 + index) * 16 * scale + index * 9 * scale
            points.append((x, y))
        draw.line(points, fill="#FFF9EE", width=5)
    draw.line((cx - 170 * scale, cy - 90 * scale, cx + 190 * scale, cy - 130 * scale), fill=p["ink"], width=7)
    draw.line((cx - 170 * scale, cy - 70 * scale, cx + 190 * scale, cy - 110 * scale), fill=p["ink"], width=7)
    for dx, dy, r in [(-100, 50, 12), (20, 60, 9), (120, 40, 15)]:
        ellipse(draw, (cx + dx * scale - r, cy + dy * scale - r, cx + dx * scale + r, cy + dy * scale + r), p["green"])
    steam(draw, cx - 10, cy - 120, p["ink"], 0.8)


def motif_rice(draw, cx, cy, p, scale=1.0):
    ellipse(draw, (cx - 250 * scale, cy - 100 * scale, cx + 250 * scale, cy + 190 * scale), p["ink"])
    ellipse(draw, (cx - 230 * scale, cy - 106 * scale, cx + 230 * scale, cy + 150 * scale), "#FFF9EE")
    ellipse(draw, (cx - 190 * scale, cy - 70 * scale, cx + 190 * scale, cy + 90 * scale), "#FFF9EE", p["ink"], 3)
    ellipse(draw, (cx - 110 * scale, cy - 24 * scale, cx + 130 * scale, cy + 76 * scale), p["second"])
    ellipse(draw, (cx + 34 * scale, cy - 8 * scale, cx + 110 * scale, cy + 54 * scale), "#FFF9EE", p["ink"], 2)
    ellipse(draw, (cx + 54 * scale, cy + 4 * scale, cx + 92 * scale, cy + 38 * scale), "#E9A93C")
    for dx, dy, r in [(-120, 40, 8), (-70, 58, 6), (-160, 6, 6), (140, 32, 10)]:
        ellipse(draw, (cx + dx * scale - r, cy + dy * scale - r, cx + dx * scale + r, cy + dy * scale + r), p["green"])
    steam(draw, cx - 20, cy - 120, p["ink"], 0.75)


def motif_sandwich(draw, cx, cy, p, scale=1.0):
    draw.polygon(
        [(cx - 210 * scale, cy + 50 * scale), (cx + 20 * scale, cy + 50 * scale), (cx - 96 * scale, cy - 120 * scale)],
        fill=p["second"],
        outline=p["ink"],
    )
    draw.polygon(
        [(cx - 190 * scale, cy + 34 * scale), (cx, cy + 34 * scale), (cx - 96 * scale, cy - 104 * scale)],
        fill="#FFF9EE",
    )
    draw.polygon(
        [(cx - 40 * scale, cy + 70 * scale), (cx + 200 * scale, cy + 70 * scale), (cx + 80 * scale, cy - 100 * scale)],
        fill=p["accent"],
        outline=p["ink"],
    )
    draw.polygon(
        [(cx - 20 * scale, cy + 54 * scale), (cx + 180 * scale, cy + 54 * scale), (cx + 80 * scale, cy - 84 * scale)],
        fill="#FFF9EE",
    )
    for dx, dy in [(-130, 42), (110, 48), (-40, 16), (40, 12)]:
        ellipse(draw, (cx + dx * scale - 9, cy + dy * scale - 9, cx + dx * scale + 9, cy + dy * scale + 9), p["green"])
    steam(draw, cx + 20, cy - 120, p["ink"], 0.6)


def motif_glass(draw, cx, cy, p, scale=1.0):
    draw.rounded_rectangle(
        (cx - 120 * scale, cy - 140 * scale, cx + 120 * scale, cy + 160 * scale),
        radius=int(26 * scale),
        fill="#FFF9EE",
        outline=p["ink"],
        width=4,
    )
    draw.rectangle((cx - 108 * scale, cy + 10 * scale, cx + 108 * scale, cy + 146 * scale), fill=p["second"])
    draw.rectangle((cx - 108 * scale, cy + 78 * scale, cx + 108 * scale, cy + 146 * scale), fill=p["accent"])
    for index in range(5):
        ellipse(draw, (cx - 88 * scale + index * 42 * scale, cy + 42 * scale, cx - 62 * scale + index * 42 * scale, cy + 68 * scale), "#FFF9EE")
    draw.line((cx + 46 * scale, cy - 200 * scale, cx + 8 * scale, cy - 120 * scale), fill=p["ink"], width=8)
    draw.arc((cx - 120 * scale, cy - 140 * scale, cx + 120 * scale, cy - 70 * scale), 180, 360, fill=p["ink"], width=4)


def motif_dumpling(draw, cx, cy, p, scale=1.0):
    ellipse(draw, (cx - 270 * scale, cy - 160 * scale, cx + 270 * scale, cy + 170 * scale), "#FFF9EE", p["ink"], 4)
    positions = [(-160, -40), (-60, -76), (44, -78), (148, -46), (-108, 42), (0, 26), (110, 38), (-18, 96)]
    for dx, dy in positions:
        x = cx + dx * scale
        y = cy + dy * scale
        draw.chord((x - 52 * scale, y - 28 * scale, x + 52 * scale, y + 52 * scale), 180, 360, fill="#FFF9EE", outline=p["ink"], width=3)
        for step in range(4):
            px = x - 34 * scale + step * 23 * scale
            draw.arc((px - 8, y - 30 * scale, px + 8, y + 2 * scale), 200, 340, fill=p["ink"], width=2)
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        ellipse(draw, (cx + math.cos(rad) * 230 * scale - 6, cy + math.sin(rad) * 140 * scale - 6, cx + math.cos(rad) * 230 * scale + 6, cy + math.sin(rad) * 140 * scale + 6), p["green"])


def motif_bowl(draw, cx, cy, p, scale=1.0):
    ellipse(draw, (cx - 260 * scale, cy - 80 * scale, cx + 260 * scale, cy + 190 * scale), p["ink"])
    ellipse(draw, (cx - 240 * scale, cy - 86 * scale, cx + 240 * scale, cy + 140 * scale), "#FFF9EE")
    ellipse(draw, (cx - 210 * scale, cy - 68 * scale, cx + 210 * scale, cy + 108 * scale), p["second"])
    for dx, dy, r in [(-84, -10, 18), (-16, 22, 12), (66, -6, 20), (116, 42, 10), (-130, 48, 9)]:
        ellipse(draw, (cx + dx * scale - r, cy + dy * scale - r, cx + dx * scale + r, cy + dy * scale + r), p["green"])
    steam(draw, cx - 10, cy - 110, p["ink"], 0.9)


MOTIFS = {
    "wok": motif_wok,
    "pot": motif_pot,
    "plate": motif_plate,
    "soup": motif_soup,
    "noodles": motif_noodles,
    "rice": motif_rice,
    "sandwich": motif_sandwich,
    "glass": motif_glass,
    "dumpling": motif_dumpling,
    "bowl": motif_bowl,
}


def draw_cover(index: int, recipe: dict, output: Path, total: int = 26) -> None:
    palette = dict(PALETTES.get(recipe.get("palette", "tomato"), PALETTES["tomato"]))
    palette["paper"] = "#FFF9EE"
    image = Image.new("RGB", (1200, 900), palette["bg"])
    draw = ImageDraw.Draw(image)

    # 纸面边框和横线
    draw.rectangle((36, 36, 1164, 864), outline=palette["ink"], width=2)
    draw.line((36, 108, 1164, 108), fill=palette["ink"], width=1)
    draw.text((68, 64), CATEGORY_LABELS.get(recipe.get("category", "home"), "家常菜"), font=font(22), fill=palette["ink"])
    draw.text((1030, 64), f"{index:02d} / {total}", font=font(20), fill=palette["ink"])

    cx = 590 if index % 2 else 610
    cy = 500 if index % 3 else 480
    motif = MOTIFS.get(recipe.get("art", "plate"), motif_plate)
    motif(draw, cx, cy, palette, 1.0)

    # 边角的小记号
    for angle in (18, 162, 198, 342):
        rad = math.radians(angle)
        x = 600 + math.cos(rad) * 480
        y = 486 + math.sin(rad) * 290
        draw.line((x - 8, y, x + 8, y), fill=palette["ink"], width=2)

    # 落款
    draw.rectangle((1038, 742, 1128, 832), fill=palette["accent"])
    draw.text((1083, 787), "饭桌", font=font(26, serif=True), fill="#FFF9EE", anchor="mm")
    draw.text((70, 806), "一周菜单 · 买菜清单", font=font(18), fill=palette["ink"])

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, "JPEG", quality=87, optimize=True, progressive=True)


def tabbar_icon(kind: str, active: bool, output: Path) -> None:
    size = 81
    color = "#C94F3D" if active else "#8A8070"
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if kind == "home":
        draw.arc((16, 30, 65, 70), 0, 180, fill=color, width=4)
        draw.line((12, 50, 69, 50), fill=color, width=4)
        draw.arc((26, 12, 40, 34), 210, 330, fill=color, width=3)
        draw.arc((42, 8, 56, 30), 210, 330, fill=color, width=3)
    elif kind == "plan":
        draw.rounded_rectangle((14, 20, 67, 68), radius=5, outline=color, width=4)
        draw.line((14, 34, 67, 34), fill=color, width=4)
        draw.line((27, 12, 27, 26), fill=color, width=4)
        draw.line((54, 12, 54, 26), fill=color, width=4)
        for row in range(2):
            for col in range(3):
                draw.rectangle((24 + col * 15, 43 + row * 13, 31 + col * 15, 50 + row * 13), fill=color)
    elif kind == "shopping":
        draw.line((18, 30, 63, 30), fill=color, width=4)
        draw.line((24, 30, 29, 67), fill=color, width=4)
        draw.line((57, 30, 52, 67), fill=color, width=4)
        draw.line((29, 67, 52, 67), fill=color, width=4)
        draw.arc((30, 14, 51, 34), 180, 360, fill=color, width=4)
        draw.line((37, 42, 37, 57), fill=color, width=3)
        draw.line((45, 42, 45, 57), fill=color, width=3)
    elif kind == "mine":
        draw.ellipse((29, 14, 52, 37), outline=color, width=4)
        draw.arc((18, 38, 63, 72), 180, 360, fill=color, width=4)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, "PNG")


def main() -> None:
    recipes = json.loads(RECIPES.read_text(encoding="utf-8"))
    STATIC_COVERS.mkdir(parents=True, exist_ok=True)
    MINI_COVERS.mkdir(parents=True, exist_ok=True)
    for index, recipe in enumerate(recipes, start=1):
        target = STATIC_COVERS / f"{recipe['slug']}.jpg"
        draw_cover(index, recipe, target, len(recipes))
        shutil.copyfile(target, MINI_COVERS / target.name)
    for kind in ("home", "plan", "shopping", "mine"):
        tabbar_icon(kind, False, TABBAR / f"{kind}.png")
        tabbar_icon(kind, True, TABBAR / f"{kind}-active.png")
    print(f"已生成 {len(recipes)} 张封面和 8 个 tabBar 图标。")


if __name__ == "__main__":
    main()
