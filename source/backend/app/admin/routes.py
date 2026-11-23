from __future__ import annotations

import csv
import hmac
import io
import json
import re
import secrets
import time
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from PIL import Image, ImageOps
from sqlmodel import Session, select

from ..config import ADMIN_PASSWORD, ADMIN_USER, APP_ENV, UPLOAD_DIR
from ..db import get_session
from ..models import Favorite, Household, PlanItem, Recipe, Setting, ShoppingItem, User, utcnow
from ..services.catalog import CATEGORIES, CATEGORY_LABELS, GROUP_ORDER, MEALS
from ..services.plans import generate_shopping, get_week_plan, shopping_payload, week_start_for
from ..services.recipes import cover_url, loads
from .templating import templates

router = APIRouter(prefix="/admin")

COVER_SIZE = (1200, 900)
MAX_UPLOAD = 8 * 1024 * 1024
_attempts: dict[str, list[float]] = {}


def csrf_token(request: Request) -> str:
    token = request.session.get("csrf")
    if not token:
        token = secrets.token_urlsafe(24)
        request.session["csrf"] = token
    return token


def csrf_valid(request: Request, value: str | None) -> bool:
    expected = request.session.get("csrf", "")
    return bool(value and expected and hmac.compare_digest(str(value), expected))


def rate_limited(ip: str) -> bool:
    now = time.time()
    history = [stamp for stamp in _attempts.get(ip, []) if now - stamp < 600]
    _attempts[ip] = history
    return len(history) >= 8


def note_failure(ip: str) -> None:
    _attempts.setdefault(ip, []).append(time.time())


def settings_map(session: Session) -> dict[str, str]:
    return {item.key: item.value for item in session.exec(select(Setting)).all()}


def render(request: Request, template: str, session: Session, active: str = "", **context):
    context.setdefault("csrf", csrf_token(request))
    context.setdefault("active", active)
    context.setdefault("admin_user", request.session.get("admin", ""))
    context.setdefault("settings", settings_map(session))
    context.setdefault("categories", CATEGORIES)
    context.setdefault("meals", MEALS)
    context.setdefault("app_env", APP_ENV)
    return templates.TemplateResponse(request, template, context)


def guard(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse("/admin/login", status_code=303)
    return None


def normalize_cover(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if value.startswith("/static/"):
        return value[len("/static/") :]
    if value.startswith("/uploads/"):
        return value[len("/") :]
    if value.startswith("/"):
        return value[1:]
    return value


def save_cover(upload, slug: str) -> str:
    raw = upload.file.read()
    if not raw:
        raise ValueError("封面文件是空的")
    if len(raw) > MAX_UPLOAD:
        raise ValueError("封面不能超过 8MB")
    try:
        image = Image.open(io.BytesIO(raw))
        image.load()
    except Exception as error:
        raise ValueError("不是可识别的图片") from error
    image = image.convert("RGB")
    image = ImageOps.fit(image, COVER_SIZE, Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    folder = UPLOAD_DIR / "covers"
    folder.mkdir(parents=True, exist_ok=True)
    filename = f"{slug}-{int(time.time())}.jpg"
    image.save(folder / filename, "JPEG", quality=86, optimize=True)
    return f"uploads/covers/{filename}"


def parse_tags(value: str) -> list[str]:
    parts = re.split(r"[,，、\s]+", value or "")
    seen: list[str] = []
    for part in parts:
        part = part.strip()
        if part and part not in seen:
            seen.append(part)
    return seen[:6]


def parse_ingredients(form) -> list[dict]:
    names = form.getlist("ingredient_name")
    amounts = form.getlist("ingredient_amount")
    units = form.getlist("ingredient_unit")
    groups = form.getlist("ingredient_group")
    result = []
    for index, name in enumerate(names):
        name = str(name).strip()
        if not name:
            continue
        result.append(
            {
                "name": name,
                "amount": str(amounts[index]).strip() if index < len(amounts) else "",
                "unit": str(units[index]).strip() if index < len(units) else "",
                "group": str(groups[index]).strip() if index < len(groups) and str(groups[index]).strip() in GROUP_ORDER else "其他",
            }
        )
    return result


def parse_steps(form) -> list[dict]:
    texts = form.getlist("step_text")
    tips = form.getlist("step_tip")
    result = []
    for index, text in enumerate(texts):
        text = str(text).strip()
        if not text:
            continue
        tip = str(tips[index]).strip() if index < len(tips) else ""
        result.append({"text": text, "tip": tip})
    return result


def unique_slug(session: Session, base: str, current_id: int | None = None) -> str:
    base = re.sub(r"[^a-z0-9-]+", "-", base.lower()).strip("-") or f"recipe-{int(time.time())}"
    candidate = base
    index = 2
    while True:
        found = session.exec(select(Recipe).where(Recipe.slug == candidate)).first()
        if found is None or found.id == current_id:
            return candidate
        candidate = f"{base}-{index}"
        index += 1


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, session: Session = Depends(get_session)):
    if request.session.get("admin"):
        return RedirectResponse("/admin", status_code=303)
    return render(request, "login.html", session, error="")


@router.post("/login")
async def login(request: Request, session: Session = Depends(get_session)):
    form = await request.form()
    if not csrf_valid(request, form.get("csrf")):
        return render(request, "login.html", session, error="页面已过期，请重试")
    ip = request.client.host if request.client else "unknown"
    if rate_limited(ip):
        return render(request, "login.html", session, error="尝试次数过多，请十分钟后再试")
    username = str(form.get("username", "")).strip()
    password = str(form.get("password", ""))
    if hmac.compare_digest(username, ADMIN_USER) and hmac.compare_digest(password, ADMIN_PASSWORD):
        request.session["admin"] = username
        request.session["csrf"] = secrets.token_urlsafe(24)
        return RedirectResponse("/admin", status_code=303)
    note_failure(ip)
    return render(request, "login.html", session, error="账号或密码不正确")


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin/login", status_code=303)


@router.get("", response_class=HTMLResponse)
def dashboard(request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    recipes = session.exec(select(Recipe).order_by(Recipe.updated_at.desc())).all()
    households = session.exec(select(Household)).all()
    users = session.exec(select(User)).all()
    household = households[0] if households else None
    week = get_week_plan(session, household.id, week_start_for(date.today())) if household else None
    shopping = shopping_payload(session, household.id, week_start_for(date.today())) if household else None
    category_counts = []
    for category in CATEGORIES:
        count = sum(1 for recipe in recipes if recipe.category == category["id"])
        category_counts.append(dict(category, count=count, percent=round(count / len(recipes) * 100) if recipes else 0))
    today = date.today().isoformat()
    today_items = []
    if week:
        for day in week["days"]:
            if day["date"] == today:
                today_items = day["meals"]
                break
    return render(
        request,
        "dashboard.html",
        session,
        active="dashboard",
        recipes=recipes,
        recent=recipes[:6],
        households=households,
        users=users,
        household=household,
        week=week,
        shopping=shopping,
        category_counts=category_counts,
        today_items=today_items,
        published=sum(1 for recipe in recipes if recipe.published),
    )


@router.get("/recipes", response_class=HTMLResponse)
def recipes_page(
    request: Request,
    q: str = "",
    category: str = "",
    status: str = "",
    session: Session = Depends(get_session),
):
    if response := guard(request):
        return response
    rows = session.exec(select(Recipe).order_by(Recipe.updated_at.desc())).all()
    keyword = q.strip()
    if keyword:
        rows = [row for row in rows if keyword in row.title or keyword in row.summary or keyword in row.tags]
    if category and category != "all":
        rows = [row for row in rows if row.category == category]
    if status == "published":
        rows = [row for row in rows if row.published]
    elif status == "draft":
        rows = [row for row in rows if not row.published]
    return render(
        request,
        "recipes.html",
        session,
        active="recipes",
        rows=rows,
        q=q,
        category=category,
        status=status,
        total=len(session.exec(select(Recipe)).all()),
    )


@router.get("/recipes/new", response_class=HTMLResponse)
def recipe_new(request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    return render(
        request,
        "recipe_form.html",
        session,
        active="recipes",
        recipe=None,
        ingredient_rows=[],
        step_rows=[],
        tag_text="",
        error="",
    )


@router.get("/recipes/{recipe_id}/edit", response_class=HTMLResponse)
def recipe_edit(recipe_id: int, request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    recipe = session.get(Recipe, recipe_id)
    if recipe is None:
        return RedirectResponse("/admin/recipes", status_code=303)
    return render(
        request,
        "recipe_form.html",
        session,
        active="recipes",
        recipe=recipe,
        ingredient_rows=loads(recipe.ingredients, []),
        step_rows=loads(recipe.steps, []),
        tag_text="、".join(loads(recipe.tags, [])),
        error="",
    )


@router.post("/recipes/save")
async def recipe_save(request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    form = await request.form()
    if not csrf_valid(request, form.get("csrf")):
        return RedirectResponse("/admin/recipes", status_code=303)
    recipe_id = form.get("recipe_id")
    recipe = session.get(Recipe, int(recipe_id)) if recipe_id else None
    title = str(form.get("title", "")).strip()
    if not title:
        return render(
            request,
            "recipe_form.html",
            session,
            active="recipes",
            recipe=recipe,
            ingredient_rows=parse_ingredients(form),
            step_rows=parse_steps(form),
            tag_text=str(form.get("tags", "")),
            error="菜名不能为空",
        )
    slug_input = str(form.get("slug", "")).strip()
    slug = unique_slug(session, slug_input or title, recipe.id if recipe else None)
    category = str(form.get("category", "home"))
    if category not in CATEGORY_LABELS:
        category = "home"
    tags = parse_tags(str(form.get("tags", "")))
    ingredients = parse_ingredients(form)
    steps = parse_steps(form)
    if not ingredients:
        ingredients = []
    if not steps:
        steps = []
    cover = normalize_cover(str(form.get("cover", "")))
    upload = form.get("cover_file")
    if upload is not None and getattr(upload, "filename", ""):
        try:
            cover = save_cover(upload, slug)
        except ValueError as error:
            return render(
                request,
                "recipe_form.html",
                session,
                active="recipes",
                recipe=recipe,
                ingredient_rows=ingredients,
                step_rows=steps,
                tag_text="、".join(tags),
                error=str(error),
            )
    if not cover:
        cover = f"covers/{slug}.jpg"
    values = dict(
        slug=slug,
        title=title,
        summary=str(form.get("summary", "")).strip(),
        category=category,
        tags=json.dumps(tags, ensure_ascii=False),
        time_minutes=max(1, int(str(form.get("time", "20") or 20))),
        servings=max(1, int(str(form.get("servings", "2") or 2))),
        difficulty=str(form.get("difficulty", "容易")),
        cover=cover,
        ingredients=json.dumps(ingredients, ensure_ascii=False),
        steps=json.dumps(steps, ensure_ascii=False),
        tips=str(form.get("tips", "")).strip(),
        published=form.get("published") == "on",
        updated_at=utcnow(),
    )
    if recipe is None:
        recipe = Recipe(**values)
        session.add(recipe)
    else:
        for key, value in values.items():
            setattr(recipe, key, value)
        session.add(recipe)
    session.commit()
    return RedirectResponse(f"/admin/recipes?msaved={recipe.id}", status_code=303)


@router.post("/recipes/{recipe_id}/toggle")
async def recipe_toggle(recipe_id: int, request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    form = await request.form()
    if not csrf_valid(request, form.get("csrf")):
        return RedirectResponse("/admin/recipes", status_code=303)
    recipe = session.get(Recipe, recipe_id)
    if recipe:
        recipe.published = not recipe.published
        recipe.updated_at = utcnow()
        session.add(recipe)
        session.commit()
    return RedirectResponse("/admin/recipes", status_code=303)


@router.post("/recipes/{recipe_id}/delete")
async def recipe_delete(recipe_id: int, request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    form = await request.form()
    if not csrf_valid(request, form.get("csrf")):
        return RedirectResponse("/admin/recipes", status_code=303)
    recipe = session.get(Recipe, recipe_id)
    if recipe:
        for item in session.exec(select(PlanItem).where(PlanItem.recipe_id == recipe_id)).all():
            session.delete(item)
        for item in session.exec(select(Favorite).where(Favorite.recipe_id == recipe_id)).all():
            session.delete(item)
        if recipe.cover.startswith("uploads/covers/"):
            path = UPLOAD_DIR / recipe.cover[len("uploads/") :]
            if path.exists():
                path.unlink()
        session.delete(recipe)
        session.commit()
    return RedirectResponse("/admin/recipes", status_code=303)


@router.get("/recipes.json")
def recipes_json(request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    rows = session.exec(select(Recipe).order_by(Recipe.id)).all()
    payload = []
    for recipe in rows:
        payload.append(
            {
                "slug": recipe.slug,
                "title": recipe.title,
                "summary": recipe.summary,
                "category": recipe.category,
                "tags": loads(recipe.tags, []),
                "time": recipe.time_minutes,
                "servings": recipe.servings,
                "difficulty": recipe.difficulty,
                "cover": recipe.cover,
                "ingredients": loads(recipe.ingredients, []),
                "steps": loads(recipe.steps, []),
                "tips": recipe.tips,
                "published": recipe.published,
            }
        )
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    return HTMLResponse(
        body,
        media_type="application/json; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="recipes.json"'},
    )


@router.get("/households", response_class=HTMLResponse)
def households_page(request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    households = session.exec(select(Household).order_by(Household.id)).all()
    rows = []
    for household in households:
        members = session.exec(select(User).where(User.household_id == household.id)).all()
        plans = session.exec(select(PlanItem).where(PlanItem.household_id == household.id)).all()
        rows.append({"household": household, "members": members, "planCount": len(plans)})
    return render(request, "households.html", session, active="households", rows=rows)


@router.get("/households/{household_id}", response_class=HTMLResponse)
def household_detail(household_id: int, request: Request, week: str = "", session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    household = session.get(Household, household_id)
    if household is None:
        return RedirectResponse("/admin/households", status_code=303)
    start = week_start_for(week or date.today())
    plan = get_week_plan(session, household.id, start)
    members = session.exec(select(User).where(User.household_id == household.id)).all()
    shopping = shopping_payload(session, household.id, start)
    return render(
        request,
        "household_detail.html",
        session,
        active="households",
        household=household,
        members=members,
        plan=plan,
        shopping=shopping,
        prev_week=week_start_for(start - timedelta(days=7)),
        next_week=week_start_for(start + timedelta(days=7)),
    )


@router.get("/shopping", response_class=HTMLResponse)
def shopping_page(
    request: Request,
    week: str = "",
    household: int = 0,
    session: Session = Depends(get_session),
):
    if response := guard(request):
        return response
    households = session.exec(select(Household).order_by(Household.id)).all()
    selected = session.get(Household, household) if household else (households[0] if households else None)
    start = week_start_for(week or date.today())
    data = shopping_payload(session, selected.id, start) if selected else {"groups": [], "total": 0, "checked": 0, "progress": 0}
    return render(
        request,
        "shopping.html",
        session,
        active="shopping",
        households=households,
        selected=selected,
        data=data,
        week=start,
    )


@router.post("/shopping/generate")
async def shopping_generate(request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    form = await request.form()
    if not csrf_valid(request, form.get("csrf")):
        return RedirectResponse("/admin/shopping", status_code=303)
    household_id = int(str(form.get("household", "0")) or 0)
    week = str(form.get("week", ""))
    household = session.get(Household, household_id)
    if household:
        generate_shopping(session, household.id, week or date.today())
    return RedirectResponse(f"/admin/shopping?household={household_id}&week={week_start_for(week or date.today()).isoformat()}", status_code=303)


@router.post("/shopping/{item_id}/toggle")
async def shopping_toggle(item_id: int, request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    form = await request.form()
    if not csrf_valid(request, form.get("csrf")):
        return RedirectResponse("/admin/shopping", status_code=303)
    item = session.get(ShoppingItem, item_id)
    if item:
        item.checked = not item.checked
        session.add(item)
        session.commit()
    target = str(form.get("next", "/admin/shopping"))
    if not target.startswith("/admin/shopping"):
        target = "/admin/shopping"
    return RedirectResponse(target, status_code=303)


@router.post("/shopping/items")
async def shopping_add_item(request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    form = await request.form()
    if not csrf_valid(request, form.get("csrf")):
        return RedirectResponse("/admin/shopping", status_code=303)
    household_id = int(str(form.get("household", "0")) or 0)
    week = str(form.get("week", ""))
    household = session.get(Household, household_id)
    name = str(form.get("name", "")).strip()
    if household and name:
        category = str(form.get("category", "其他"))
        item = ShoppingItem(
            household_id=household.id,
            week_start=week_start_for(week or date.today()).isoformat(),
            name=name,
            amount=str(form.get("amount", "")).strip(),
            category=category if category in GROUP_ORDER else "其他",
            custom=True,
            source_key=f"custom|{date.today().isoformat()}|{name}",
        )
        session.add(item)
        session.commit()
    return RedirectResponse(f"/admin/shopping?household={household_id}&week={week_start_for(week or date.today()).isoformat()}", status_code=303)


@router.get("/shopping.csv")
def shopping_csv(request: Request, week: str = "", household: int = 0, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    households = session.exec(select(Household).order_by(Household.id)).all()
    selected = session.get(Household, household) if household else (households[0] if households else None)
    if selected is None:
        return RedirectResponse("/admin/shopping", status_code=303)
    start = week_start_for(week or date.today())
    data = shopping_payload(session, selected.id, start)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["分类", "食材", "用量", "已买"])
    for group in data["groups"]:
        for item in group["items"]:
            writer.writerow([group["name"], item["name"], item["amount"], "是" if item["checked"] else "否"])
    content = "﻿" + buffer.getvalue()
    filename = f"shopping-{start.isoformat()}.csv"
    return StreamingResponse(
        io.BytesIO(content.encode("utf-8")),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    return render(request, "settings.html", session, active="settings", saved=False)


@router.post("/settings")
async def settings_save(request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    form = await request.form()
    if not csrf_valid(request, form.get("csrf")):
        return RedirectResponse("/admin/settings", status_code=303)
    for key in ("site_name", "tagline", "intro", "default_servings"):
        value = str(form.get(key, "")).strip()
        if not value:
            continue
        row = session.get(Setting, key)
        if row:
            row.value = value
        else:
            row = Setting(key=key, value=value)
        session.add(row)
    session.commit()
    return render(request, "settings.html", session, active="settings", saved=True)


@router.get("/help", response_class=HTMLResponse)
def help_page(request: Request, session: Session = Depends(get_session)):
    if response := guard(request):
        return response
    return render(request, "help.html", session, active="help")
