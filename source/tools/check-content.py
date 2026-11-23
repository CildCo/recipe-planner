"""检查饭桌源码包的完整性。

用法：
    python tools/check-content.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
RECIPES = ROOT / "backend" / "app" / "data" / "recipes.json"
COVERS = ROOT / "backend" / "app" / "static" / "covers"
MINI = ROOT / "miniprogram"
MINI_DATA = MINI / "data" / "recipes.js"

SKIP_PARTS = {".venv", "__pycache__", ".pytest_cache", "node_modules", "dist", "runtime", "data"}

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def check_recipes() -> list[dict]:
    recipes = json.loads(RECIPES.read_text(encoding="utf-8"))
    if len(recipes) < 20:
        fail(f"菜谱只有 {len(recipes)} 道，少于 20 道")
    slugs = set()
    for recipe in recipes:
        slug = recipe.get("slug", "")
        if not slug or slug in slugs:
            fail(f"slug 为空或重复：{slug}")
        slugs.add(slug)
        for key in ("title", "category", "summary", "ingredients", "steps"):
            if not recipe.get(key):
                fail(f"{slug} 缺少 {key}")
        if recipe.get("category") not in {"quick", "home", "soup", "staple", "breakfast"}:
            fail(f"{slug} 分类不正确")
        if not isinstance(recipe.get("servings"), int) or recipe["servings"] < 1:
            fail(f"{slug} 人份不正确")
        for ingredient in recipe.get("ingredients", []):
            if not ingredient.get("name"):
                fail(f"{slug} 有空食材")
            if ingredient.get("group") not in {"蔬菜", "肉蛋", "主食", "调料", "其他"}:
                fail(f"{slug} 食材分类不正确：{ingredient.get('group')}")
        if len(recipe.get("steps", [])) < 2:
            fail(f"{slug} 步骤少于 2 步")
    return recipes


def check_covers(recipes: list[dict]) -> None:
    for recipe in recipes:
        path = COVERS / f"{recipe['slug']}.jpg"
        if not path.exists():
            fail(f"缺少封面：{path.name}")
            continue
        size = path.stat().st_size
        if size > 500 * 1024:
            fail(f"{path.name} 超过 500KB")
        try:
            with Image.open(path) as image:
                if image.size != (1200, 900):
                    fail(f"{path.name} 不是 1200x900：{image.size}")
                if image.mode != "RGB":
                    fail(f"{path.name} 不是 RGB：{image.mode}")
        except Exception as error:
            fail(f"{path.name} 无法读取：{error}")


def check_mini(recipes: list[dict]) -> None:
    app = json.loads((MINI / "app.json").read_text(encoding="utf-8"))
    for page in app.get("pages", []):
        for suffix in (".js", ".json", ".wxml", ".wxss"):
            path = MINI / (page + suffix)
            if not path.exists():
                fail(f"页面缺文件：{path.relative_to(ROOT)}")
    for item in app.get("tabBar", {}).get("list", []):
        for key in ("iconPath", "selectedIconPath"):
            path = MINI / item[key]
            if not path.exists():
                fail(f"tabBar 图标缺失：{path.relative_to(ROOT)}")

    text = MINI_DATA.read_text(encoding="utf-8")
    if not text.startswith("module.exports = "):
        fail("recipes.js 格式不正确")
        return
    payload = json.loads(text[len("module.exports = ") :].rstrip().rstrip(";"))
    slugs = {item["slug"] for item in payload.get("recipes", [])}
    for recipe in recipes:
        if recipe["slug"] not in slugs:
            fail(f"小程序数据缺少：{recipe['slug']}")
    for item in payload.get("recipes", []):
        cover = MINI / "assets" / "covers" / (item["slug"] + ".jpg")
        if not cover.exists():
            fail(f"小程序封面缺失：{cover.name}")


def check_js() -> None:
    files = [path for path in MINI.rglob("*.js") if "node_modules" not in path.parts]
    for path in files:
        result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
        if result.returncode != 0:
            fail(f"JS 语法错误 {path.relative_to(ROOT)}：{result.stderr.strip()[:160]}")


def check_readme() -> None:
    for name in ("README.md", "LICENSE.md", "PROVENANCE.md"):
        if not (ROOT / name).exists():
            fail(f"缺少 {name}")


def main() -> None:
    recipes = check_recipes()
    check_covers(recipes)
    check_mini(recipes)
    check_js()
    check_readme()
    if errors:
        print("检查未通过：")
        for message in errors:
            print(" -", message)
        sys.exit(1)
    print(f"检查通过：{len(recipes)} 道菜谱、{len(list(COVERS.glob('*.jpg')))} 张封面、小程序页面完整。")


if __name__ == "__main__":
    main()
