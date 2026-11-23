from __future__ import annotations

from datetime import date

from fastapi.templating import Jinja2Templates

from ..config import TEMPLATE_DIR
from ..services.catalog import CATEGORIES, CATEGORY_LABELS, MEALS, category_name, meal_name
from ..services.recipes import cover_url, loads

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
templates.env.filters["cover_url"] = cover_url
templates.env.filters["json_loads"] = lambda value: loads(value, [])
templates.env.filters["category_name"] = category_name
templates.env.filters["meal_name"] = meal_name
templates.env.globals["CATEGORIES"] = CATEGORIES
templates.env.globals["MEALS"] = MEALS
templates.env.globals["CATEGORY_LABELS"] = CATEGORY_LABELS


def date_label(value: str) -> str:
    try:
        day = date.fromisoformat(str(value)[:10])
    except ValueError:
        return str(value)
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][day.weekday()]
    return f"{day.month}月{day.day}日 {weekday}"


templates.env.filters["date_label"] = date_label
