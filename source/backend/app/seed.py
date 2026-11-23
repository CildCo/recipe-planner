from __future__ import annotations

import json
from datetime import date, timedelta

from sqlmodel import Session, select

from .config import RECIPE_SEED
from .models import Favorite, Household, PlanItem, Recipe, Setting, User
from .services.plans import generate_shopping, week_start_for

DEFAULT_SETTINGS = {
    "site_name": "饭桌",
    "tagline": "把一周的饭安排好",
    "intro": "菜谱、一周菜单和买菜清单放在一起，少想一点，好好吃饭。",
    "default_servings": "2",
}


def ensure_settings(session: Session) -> None:
    existing = {item.key for item in session.exec(select(Setting)).all()}
    for key, value in DEFAULT_SETTINGS.items():
        if key not in existing:
            session.add(Setting(key=key, value=value))
    session.commit()


def load_seed_recipes() -> list[dict]:
    return json.loads(RECIPE_SEED.read_text(encoding="utf-8"))


def ensure_recipes(session: Session) -> None:
    if session.exec(select(Recipe)).first():
        return
    for index, raw in enumerate(load_seed_recipes(), start=1):
        recipe = Recipe(
            slug=raw["slug"],
            title=raw["title"],
            summary=raw.get("summary", ""),
            category=raw.get("category", "home"),
            tags=json.dumps(raw.get("tags", []), ensure_ascii=False),
            time_minutes=int(raw.get("time", 20)),
            servings=int(raw.get("servings", 2)),
            difficulty=raw.get("difficulty", "容易"),
            cover=f"covers/{raw['slug']}.jpg",
            ingredients=json.dumps(raw.get("ingredients", []), ensure_ascii=False),
            steps=json.dumps(raw.get("steps", []), ensure_ascii=False),
            tips=raw.get("tips", ""),
            published=True,
        )
        session.add(recipe)
        if index % 8 == 0:
            session.commit()
    session.commit()


def ensure_demo_household(session: Session) -> None:
    if session.exec(select(User).where(User.openid == "demo-openid")).first():
        return
    user = User(openid="demo-openid", nickname="小满", household_id=None)
    session.add(user)
    session.commit()
    session.refresh(user)

    household = Household(name="小满的饭桌", invite_code="FANZHUO", owner_id=user.id)
    session.add(household)
    session.commit()
    session.refresh(household)
    user.household_id = household.id
    session.add(user)
    session.commit()

    recipes = {recipe.slug: recipe for recipe in session.exec(select(Recipe)).all()}
    monday = week_start_for(date.today())
    demo = [
        (0, "dinner", "tomato-egg", 2),
        (0, "dinner", "egg-fried-rice", 2),
        (1, "lunch", "garlic-broccoli", 2),
        (1, "dinner", "cola-wings", 3),
        (2, "dinner", "mapo-tofu", 2),
        (3, "lunch", "scallion-noodles", 2),
        (3, "dinner", "winter-melon-ribs", 3),
        (4, "dinner", "steamed-fish", 3),
        (5, "breakfast", "ham-sandwich", 1),
        (5, "dinner", "braised-pork", 4),
        (6, "breakfast", "millet-porridge", 2),
        (6, "dinner", "pumpkin-congee", 2),
    ]
    for offset, meal, slug, servings in demo:
        recipe = recipes.get(slug)
        if not recipe:
            continue
        session.add(
            PlanItem(
                household_id=household.id,
                date=(monday + timedelta(days=offset)).isoformat(),
                meal=meal,
                recipe_id=recipe.id,
                servings=servings,
            )
        )
    session.commit()

    for slug in ("tomato-egg", "braised-pork", "scallion-noodles"):
        recipe = recipes.get(slug)
        if recipe:
            session.add(Favorite(user_id=user.id, recipe_id=recipe.id))
    session.commit()

    generate_shopping(session, household.id, monday)


def seed_database(session: Session) -> None:
    ensure_settings(session)
    ensure_recipes(session)
    ensure_demo_household(session)
