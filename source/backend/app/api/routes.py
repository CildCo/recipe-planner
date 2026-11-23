from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session, select

from ..auth import create_token, new_invite_code, parse_token, resolve_openid
from ..db import get_session
from ..models import Favorite, Household, PlanItem, Recipe, Setting, ShoppingItem, User
from ..schemas import CopyWeekIn, CustomItemIn, HouseholdIn, JoinIn, LoginIn, PlanItemIn, ToggleIn
from ..services.catalog import CATEGORIES, GROUP_ORDER, MEALS
from ..services.plans import (
    add_plan_item,
    copy_week,
    generate_shopping,
    get_week_plan,
    remove_plan_item,
    shopping_payload,
    week_start_for,
)
from ..services.recipes import serialize_recipe

router = APIRouter(prefix="/api")


def ok(data):
    return {"ok": True, "data": data}


def current_user(request: Request, session: Session = Depends(get_session)) -> User:
    header = request.headers.get("Authorization", "")
    token = header[7:].strip() if header.lower().startswith("bearer ") else ""
    user_id = parse_token(token)
    user = session.get(User, user_id) if user_id else None
    if user is None:
        raise HTTPException(status_code=401, detail="登录已过期，请重新进入")
    return user


def settings_map(session: Session) -> dict[str, str]:
    return {item.key: item.value for item in session.exec(select(Setting)).all()}


def household_payload(session: Session, household: Household | None) -> dict | None:
    if household is None:
        return None
    members = session.exec(select(User).where(User.household_id == household.id)).all()
    return {
        "id": household.id,
        "name": household.name,
        "inviteCode": household.invite_code,
        "members": [
            {
                "id": user.id,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "initial": user.nickname[:1] if user.nickname else "饭",
            }
            for user in members
        ],
    }


def user_payload(user: User) -> dict:
    return {
        "id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "householdId": user.household_id,
    }


def require_household(user: User) -> int:
    if not user.household_id:
        raise HTTPException(status_code=409, detail="还没有加入饭桌")
    return user.household_id


@router.get("/health")
def health():
    return {"ok": True, "data": {"status": "ok"}}


@router.post("/auth/login")
def login(payload: LoginIn, session: Session = Depends(get_session)):
    openid = resolve_openid(payload.code, payload.devOpenid)
    if not openid:
        raise HTTPException(status_code=401, detail="微信登录未配置，开发环境请使用本地模式")
    user = session.exec(select(User).where(User.openid == openid)).first()
    if user is None:
        nickname = (payload.nickname or "饭友").strip()[:20] or "饭友"
        user = User(openid=openid, nickname=nickname, avatar=payload.avatar or "")
        session.add(user)
        session.commit()
        session.refresh(user)
    elif payload.nickname and payload.nickname.strip() and payload.nickname.strip() != user.nickname:
        user.nickname = payload.nickname.strip()[:20]
        user.avatar = payload.avatar or user.avatar
        session.add(user)
        session.commit()
        session.refresh(user)

    if not user.household_id:
        household = Household(name=f"{user.nickname}的饭桌", invite_code=new_invite_code(), owner_id=user.id)
        session.add(household)
        session.commit()
        session.refresh(household)
        user.household_id = household.id
        session.add(user)
        session.commit()
        session.refresh(user)

    household = session.get(Household, user.household_id) if user.household_id else None
    return ok(
        {
            "token": create_token(user.id),
            "user": user_payload(user),
            "household": household_payload(session, household),
        }
    )


@router.get("/site")
def site(session: Session = Depends(get_session)):
    recipes = session.exec(select(Recipe).where(Recipe.published == True)).all()  # noqa: E712
    counts = {item["id"]: 0 for item in CATEGORIES}
    for recipe in recipes:
        if recipe.category in counts:
            counts[recipe.category] += 1
    return ok(
        {
            "settings": settings_map(session),
            "categories": [dict(item, count=counts.get(item["id"], 0)) for item in CATEGORIES],
            "meals": MEALS,
            "recipeCount": len(recipes),
        }
    )


@router.get("/recipes")
def list_recipes(
    category: str = "",
    q: str = "",
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=100),
    session: Session = Depends(get_session),
):
    statement = select(Recipe).where(Recipe.published == True)  # noqa: E712
    if category and category != "all":
        statement = statement.where(Recipe.category == category)
    recipes = session.exec(statement.order_by(Recipe.id)).all()
    keyword = q.strip()
    if keyword:
        recipes = [
            recipe
            for recipe in recipes
            if keyword in recipe.title or keyword in recipe.summary or keyword in recipe.tags
        ]
    start = (page - 1) * size
    selected = recipes[start : start + size]
    return ok(
        {
            "items": [serialize_recipe(recipe) for recipe in selected],
            "total": len(recipes),
            "page": page,
            "hasMore": start + size < len(recipes),
        }
    )


@router.get("/recipes/{recipe_id}")
def recipe_detail(recipe_id: int, session: Session = Depends(get_session)):
    recipe = session.get(Recipe, recipe_id)
    if recipe is None or not recipe.published:
        raise HTTPException(status_code=404, detail="菜谱不存在")
    return ok(serialize_recipe(recipe, detail=True))


@router.get("/favorites")
def list_favorites(user: User = Depends(current_user), session: Session = Depends(get_session)):
    rows = session.exec(select(Favorite).where(Favorite.user_id == user.id).order_by(Favorite.id.desc())).all()
    result = []
    for row in rows:
        recipe = session.get(Recipe, row.recipe_id)
        if recipe and recipe.published:
            result.append(serialize_recipe(recipe))
    return ok({"items": result, "ids": [item["id"] for item in result]})


@router.post("/recipes/{recipe_id}/favorite")
def toggle_favorite(recipe_id: int, user: User = Depends(current_user), session: Session = Depends(get_session)):
    recipe = session.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="菜谱不存在")
    row = session.exec(
        select(Favorite).where(Favorite.user_id == user.id).where(Favorite.recipe_id == recipe_id)
    ).first()
    if row:
        session.delete(row)
        session.commit()
        return ok({"favorite": False})
    session.add(Favorite(user_id=user.id, recipe_id=recipe_id))
    session.commit()
    return ok({"favorite": True})


@router.get("/plan")
def get_plan(
    week: str = "",
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    household_id = require_household(user)
    return ok(get_week_plan(session, household_id, week or None))


@router.post("/plan/items")
def create_plan_item(
    payload: PlanItemIn,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    household_id = require_household(user)
    try:
        date.fromisoformat(payload.date)
    except ValueError as error:
        raise HTTPException(status_code=400, detail="日期格式不正确") from error
    try:
        item = add_plan_item(
            session,
            household_id,
            date_value=payload.date,
            meal=payload.meal,
            recipe_id=payload.recipeId,
            servings=payload.servings,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return ok({"id": item.id, "week": week_start_for(payload.date).isoformat()})


@router.delete("/plan/items/{item_id}")
def delete_plan_item(
    item_id: int,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    household_id = require_household(user)
    if not remove_plan_item(session, household_id, item_id):
        raise HTTPException(status_code=404, detail="菜单项不存在")
    return ok({"removed": True})


@router.post("/plan/copy")
def copy_plan(
    payload: CopyWeekIn,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    household_id = require_household(user)
    count = copy_week(session, household_id, payload.fromWeek, payload.toWeek)
    return ok({"copied": count, "week": week_start_for(payload.toWeek).isoformat()})


@router.get("/shopping")
def shopping(
    week: str = "",
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    household_id = require_household(user)
    return ok(shopping_payload(session, household_id, week or None))


@router.post("/shopping/generate")
def regenerate_shopping(
    week: str = "",
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    household_id = require_household(user)
    generate_shopping(session, household_id, week or None)
    return ok(shopping_payload(session, household_id, week or None))


@router.patch("/shopping/{item_id}")
def toggle_shopping(
    item_id: int,
    payload: ToggleIn,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    household_id = require_household(user)
    item = session.get(ShoppingItem, item_id)
    if item is None or item.household_id != household_id:
        raise HTTPException(status_code=404, detail="清单项不存在")
    item.checked = payload.checked
    session.add(item)
    session.commit()
    return ok({"id": item.id, "checked": item.checked})


@router.post("/shopping/items")
def add_shopping_item(
    payload: CustomItemIn,
    week: str = "",
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    household_id = require_household(user)
    category = payload.category if payload.category in GROUP_ORDER else "其他"
    item = ShoppingItem(
        household_id=household_id,
        week_start=week_start_for(week or None).isoformat(),
        name=payload.name.strip(),
        amount=payload.amount.strip(),
        unit=payload.unit.strip(),
        category=category,
        custom=True,
        source_key=f"custom|{date.today().isoformat()}|{payload.name.strip()}",
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return ok({"id": item.id})


@router.delete("/shopping/items/{item_id}")
def delete_shopping_item(
    item_id: int,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    household_id = require_household(user)
    item = session.get(ShoppingItem, item_id)
    if item is None or item.household_id != household_id:
        raise HTTPException(status_code=404, detail="清单项不存在")
    session.delete(item)
    session.commit()
    return ok({"removed": True})


@router.get("/household")
def get_household(user: User = Depends(current_user), session: Session = Depends(get_session)):
    household = session.get(Household, user.household_id) if user.household_id else None
    return ok(household_payload(session, household))


@router.post("/household/create")
def create_household(
    payload: HouseholdIn,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    household = Household(name=payload.name.strip() or "我的饭桌", invite_code=new_invite_code(), owner_id=user.id)
    session.add(household)
    session.commit()
    session.refresh(household)
    user.household_id = household.id
    session.add(user)
    session.commit()
    return ok(household_payload(session, household))


@router.post("/household/join")
def join_household(
    payload: JoinIn,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    code = payload.code.strip().upper()
    household = session.exec(select(Household).where(Household.invite_code == code)).first()
    if household is None:
        raise HTTPException(status_code=404, detail="邀请码不存在")
    user.household_id = household.id
    session.add(user)
    session.commit()
    return ok(household_payload(session, household))
