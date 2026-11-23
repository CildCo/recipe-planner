"""把后端菜谱导出成小程序本地演示数据。

用法：
    python tools/export-mini-data.py

生成：
    miniprogram/data/recipes.js
    miniprogram/data/site.js
"""
from __future__ import annotations

import json
from pathlib import Path

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
RECIPES = ROOT / "backend" / "app" / "data" / "recipes.json"
OUT_DIR = ROOT / "miniprogram" / "data"

CATEGORIES = [
    {"id": "quick", "name": "快手菜", "note": "二十分钟内上桌", "color": "tomato"},
    {"id": "home", "name": "家常菜", "note": "一锅一灶的熟悉味道", "color": "plum"},
    {"id": "soup", "name": "汤羹", "note": "小火慢慢煨", "color": "jade"},
    {"id": "staple", "name": "主食", "note": "面、饭、饺子", "color": "olive"},
    {"id": "breakfast", "name": "早餐", "note": "把早晨安顿好", "color": "mustard"},
]
MEALS = [
    {"id": "breakfast", "name": "早餐"},
    {"id": "lunch", "name": "午餐"},
    {"id": "dinner", "name": "晚餐"},
]
CATEGORY_NAMES = {item["id"]: item["name"] for item in CATEGORIES}


def main() -> None:
    recipes = json.loads(RECIPES.read_text(encoding="utf-8"))
    rows = []
    for index, recipe in enumerate(recipes, start=1):
        rows.append(
            {
                "id": index,
                "slug": recipe["slug"],
                "title": recipe["title"],
                "summary": recipe.get("summary", ""),
                "category": recipe.get("category", "home"),
                "categoryName": CATEGORY_NAMES.get(recipe.get("category", "home"), "家常菜"),
                "tags": recipe.get("tags", []),
                "time": recipe.get("time", 20),
                "servings": recipe.get("servings", 2),
                "difficulty": recipe.get("difficulty", "容易"),
                "cover": f"/assets/covers/{recipe['slug']}.jpg",
                "ingredients": recipe.get("ingredients", []),
                "steps": recipe.get("steps", []),
                "tips": recipe.get("tips", ""),
            }
        )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"categories": CATEGORIES, "meals": MEALS, "recipes": rows}
    text = "module.exports = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    (OUT_DIR / "recipes.js").write_text(text, encoding="utf-8")

    site = {
        "siteName": "饭桌",
        "tagline": "把一周的饭安排好",
        "intro": "菜谱、一周菜单和买菜清单放在一起，少想一点，好好吃饭。",
        "defaultServings": 2,
    }
    (OUT_DIR / "site.js").write_text(
        "module.exports = " + json.dumps(site, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"已导出 {len(rows)} 道菜谱到 {OUT_DIR}")


if __name__ == "__main__":
    main()
