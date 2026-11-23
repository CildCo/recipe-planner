from __future__ import annotations

import secrets
from collections import OrderedDict
from datetime import date, timedelta
from typing import Any

from sqlmodel import Session, select

from ..models import PlanItem, Recipe, ShoppingItem
from .catalog import GROUP_ORDER, MEALS, meal_name
from .recipes import amount_text, loads, serialize_recipe

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def as_date(value: str | date | None) -> date:
    if isinstance(value, date):
        return value
    if value:
        try:
            return date.fromisoformat(str(value)[:10])
        except ValueError:
            pass
    return date.today()


def week_start_for(value: str | date | None = None) -> date:
    current = as_date(value)
    return current - timedelta(days=current.weekday())


def week_key(value: str | date | None = None) -> str:
    return week_start_for(value).isoformat()


def format_day(value: date) -> str:
    return f"{value.month}月{value.day}日"


def get_week_plan(session: Session, household_id: int, week_start: str | date | None = None) -> dict[str, Any]:
    start = week_start_for(week_start)
    end = start + timedelta(days=7)
    items = session.exec(
        select(PlanItem)
        .where(PlanItem.household_id == household_id)
        .where(PlanItem.date >= start.isoformat())
        .where(PlanItem.date < end.isoformat())
        .order_by(PlanItem.date, PlanItem.position, PlanItem.id)
    ).all()

    cache: dict[int, Recipe] = {}
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for item in items:
        recipe = cache.get(item.recipe_id)
        if recipe is None:
            recipe = session.get(Recipe, item.recipe_id)
            if recipe is None:
                continue
            cache[item.recipe_id] = recipe
        bucket = grouped.setdefault(item.date, {meal["id"]: [] for meal in MEALS})
        bucket.setdefault(item.meal, []).append(
            {
                "id": item.id,
                "recipeId": recipe.id,
                "title": recipe.title,
                "cover": serialize_recipe(recipe)["cover"],
                "time": recipe.time_minutes,
                "category": recipe.category,
                "servings": item.servings,
                "meal": item.meal,
                "mealName": meal_name(item.meal),
                "date": item.date,
            }
        )

    today = date.today().isoformat()
    days = []
    total = 0
    for offset in range(7):
        current = start + timedelta(days=offset)
        key = current.isoformat()
        meals = grouped.get(key, {meal["id"]: [] for meal in MEALS})
        count = sum(len(meals.get(meal["id"], [])) for meal in MEALS)
        total += count
        days.append(
            {
                "date": key,
                "day": current.day,
                "month": current.month,
                "label": format_day(current),
                "weekday": WEEKDAYS[offset],
                "today": key == today,
                "meals": [{"id": meal["id"], "name": meal["name"], "items": meals.get(meal["id"], [])} for meal in MEALS],
                "count": count,
            }
        )

    return {
        "weekStart": start.isoformat(),
        "weekEnd": (start + timedelta(days=6)).isoformat(),
        "label": f"{start.month}月{start.day}日 — {(start + timedelta(days=6)).month}月{(start + timedelta(days=6)).day}日",
        "days": days,
        "total": total,
    }


def add_plan_item(
    session: Session,
    household_id: int,
    *,
    date_value: str,
    meal: str,
    recipe_id: int,
    servings: int | None = None,
) -> PlanItem:
    recipe = session.get(Recipe, recipe_id)
    if recipe is None or not recipe.published:
        raise ValueError("菜谱不存在")
    if meal not in {item["id"] for item in MEALS}:
        raise ValueError("餐次不正确")
    current = session.exec(
        select(PlanItem)
        .where(PlanItem.household_id == household_id)
        .where(PlanItem.date == date_value)
        .where(PlanItem.meal == meal)
    ).all()
    item = PlanItem(
        household_id=household_id,
        date=date_value,
        meal=meal,
        recipe_id=recipe_id,
        servings=max(1, int(servings or recipe.servings)),
        position=len(current),
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def remove_plan_item(session: Session, household_id: int, item_id: int) -> bool:
    item = session.get(PlanItem, item_id)
    if item is None or item.household_id != household_id:
        return False
    session.delete(item)
    session.commit()
    return True


def copy_week(session: Session, household_id: int, source: str, target: str) -> int:
    source_start = week_start_for(source)
    target_start = week_start_for(target)
    items = session.exec(
        select(PlanItem)
        .where(PlanItem.household_id == household_id)
        .where(PlanItem.date >= source_start.isoformat())
        .where(PlanItem.date < (source_start + timedelta(days=7)).isoformat())
    ).all()
    count = 0
    for item in items:
        offset = (date.fromisoformat(item.date) - source_start).days
        new_date = (target_start + timedelta(days=offset)).isoformat()
        exists = session.exec(
            select(PlanItem)
            .where(PlanItem.household_id == household_id)
            .where(PlanItem.date == new_date)
            .where(PlanItem.meal == item.meal)
            .where(PlanItem.recipe_id == item.recipe_id)
        ).first()
        if exists:
            continue
        session.add(
            PlanItem(
                household_id=household_id,
                date=new_date,
                meal=item.meal,
                recipe_id=item.recipe_id,
                servings=item.servings,
                position=item.position,
            )
        )
        count += 1
    session.commit()
    return count


def _ingredient_key(name: str, unit: str, group: str) -> str:
    return f"{name}|{unit}|{group}"


def _merge_amounts(values: list[Any], unit: str) -> str:
    numeric = 0.0
    texts: list[str] = []
    for value in values:
        if isinstance(value, (int, float)):
            numeric += float(value)
        elif value not in (None, ""):
            text = str(value).strip()
            if text and text not in texts:
                texts.append(text)
    if numeric > 0:
        base = amount_text(round(numeric, 2), unit)
        if texts:
            return f"{base} + {'、'.join(texts)}"
        return base
    return "、".join(texts) if texts else unit


def generate_shopping(session: Session, household_id: int, week_start: str | date | None = None) -> list[ShoppingItem]:
    start = week_start_for(week_start)
    start_key = start.isoformat()
    end = start + timedelta(days=7)

    existing = session.exec(
        select(ShoppingItem)
        .where(ShoppingItem.household_id == household_id)
        .where(ShoppingItem.week_start == start_key)
    ).all()
    checked = {item.source_key: item.checked for item in existing if not item.custom}
    custom = [item for item in existing if item.custom]

    for item in existing:
        if not item.custom:
            session.delete(item)

    plan_items = session.exec(
        select(PlanItem)
        .where(PlanItem.household_id == household_id)
        .where(PlanItem.date >= start_key)
        .where(PlanItem.date < end.isoformat())
    ).all()

    aggregated: OrderedDict[str, dict[str, Any]] = OrderedDict()
    recipe_cache: dict[int, Recipe] = {}
    for plan in plan_items:
        recipe = recipe_cache.get(plan.recipe_id)
        if recipe is None:
            recipe = session.get(Recipe, plan.recipe_id)
            if recipe is None:
                continue
            recipe_cache[plan.recipe_id] = recipe
        scale = max(1, plan.servings) / max(1, recipe.servings)
        for raw in loads(recipe.ingredients, []):
            name = str(raw.get("name", "")).strip()
            if not name:
                continue
            unit = str(raw.get("unit", "")).strip()
            group = str(raw.get("group", "其他")).strip() or "其他"
            key = _ingredient_key(name, unit, group)
            entry = aggregated.setdefault(
                key,
                {"name": name, "unit": unit, "group": group, "values": []},
            )
            amount = raw.get("amount", "")
            if isinstance(amount, (int, float)):
                entry["values"].append(float(amount) * scale)
            else:
                entry["values"].append(amount)

    created: list[ShoppingItem] = []
    for key, entry in aggregated.items():
        item = ShoppingItem(
            household_id=household_id,
            week_start=start_key,
            name=entry["name"],
            amount=_merge_amounts(entry["values"], entry["unit"]),
            unit=entry["unit"],
            category=entry["group"],
            checked=checked.get(key, False),
            custom=False,
            source_key=key,
        )
        session.add(item)
        created.append(item)

    for item in custom:
        if not item.source_key:
            item.source_key = f"custom|{item.id}|{secrets.token_hex(3)}"
            session.add(item)

    session.commit()
    for item in created:
        session.refresh(item)
    return created


def get_shopping(session: Session, household_id: int, week_start: str | date | None = None, *, auto: bool = True) -> list[ShoppingItem]:
    start_key = week_start_for(week_start).isoformat()
    items = session.exec(
        select(ShoppingItem)
        .where(ShoppingItem.household_id == household_id)
        .where(ShoppingItem.week_start == start_key)
        .order_by(ShoppingItem.checked, ShoppingItem.category, ShoppingItem.name)
    ).all()
    if auto and not items:
        generated = generate_shopping(session, household_id, start_key)
        if generated:
            items = session.exec(
                select(ShoppingItem)
                .where(ShoppingItem.household_id == household_id)
                .where(ShoppingItem.week_start == start_key)
                .order_by(ShoppingItem.checked, ShoppingItem.category, ShoppingItem.name)
            ).all()
    return list(items)


def shopping_payload(session: Session, household_id: int, week_start: str | date | None = None) -> dict[str, Any]:
    start_key = week_start_for(week_start).isoformat()
    items = get_shopping(session, household_id, start_key)
    groups: OrderedDict[str, list[dict[str, Any]]] = OrderedDict((group, []) for group in GROUP_ORDER)
    for item in items:
        groups.setdefault(item.category, []).append(
            {
                "id": item.id,
                "name": item.name,
                "amount": item.amount,
                "unit": item.unit,
                "category": item.category,
                "checked": item.checked,
                "custom": item.custom,
            }
        )
    checked = sum(1 for item in items if item.checked)
    return {
        "weekStart": start_key,
        "items": [entry for group in groups.values() for entry in group],
        "groups": [{"name": name, "items": entries} for name, entries in groups.items() if entries],
        "total": len(items),
        "checked": checked,
        "progress": round(checked / len(items) * 100) if items else 0,
    }
