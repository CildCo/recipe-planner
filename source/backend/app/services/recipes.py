from __future__ import annotations

import json
from typing import Any

from ..models import Recipe
from .catalog import category_name

PUBLIC_COVER_PREFIX = "/static/"


def loads(value: str | None, fallback: Any) -> Any:
    if not value:
        return fallback
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return fallback


def cover_url(cover: str) -> str:
    if not cover:
        return ""
    if cover.startswith("http://") or cover.startswith("https://"):
        return cover
    if cover.startswith("/"):
        return cover
    if cover.startswith("uploads/"):
        return "/" + cover
    return PUBLIC_COVER_PREFIX + cover


def serialize_recipe(recipe: Recipe, *, detail: bool = False) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": recipe.id,
        "slug": recipe.slug,
        "title": recipe.title,
        "summary": recipe.summary,
        "category": recipe.category,
        "categoryName": category_name(recipe.category),
        "tags": loads(recipe.tags, []),
        "time": recipe.time_minutes,
        "servings": recipe.servings,
        "difficulty": recipe.difficulty,
        "cover": cover_url(recipe.cover),
        "published": recipe.published,
    }
    if detail:
        data["ingredients"] = loads(recipe.ingredients, [])
        data["steps"] = loads(recipe.steps, [])
        data["tips"] = recipe.tips
    return data


def normalize_ingredient(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": str(raw.get("name", "")).strip(),
        "amount": raw.get("amount", ""),
        "unit": str(raw.get("unit", "")).strip(),
        "group": str(raw.get("group", "其他")).strip() or "其他",
    }


def amount_text(amount: Any, unit: str = "") -> str:
    if amount is None or amount == "":
        return unit
    if isinstance(amount, (int, float)):
        if float(amount).is_integer():
            text = str(int(amount))
        else:
            text = f"{amount:.2f}".rstrip("0").rstrip(".")
        return f"{text}{unit}"
    text = str(amount).strip()
    if unit and unit not in text:
        return f"{text}{unit}"
    return text
