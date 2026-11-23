from __future__ import annotations

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Recipe(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    title: str
    summary: str = ""
    category: str = "home"
    tags: str = "[]"
    time_minutes: int = 20
    servings: int = 2
    difficulty: str = "容易"
    cover: str = ""
    ingredients: str = "[]"
    steps: str = "[]"
    tips: str = ""
    published: bool = True
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class Setting(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str = ""


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    openid: str = Field(index=True, unique=True)
    nickname: str = "饭友"
    avatar: str = ""
    household_id: int | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=utcnow)


class Household(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = "我的饭桌"
    invite_code: str = Field(index=True, unique=True)
    owner_id: int | None = Field(default=None)
    created_at: datetime = Field(default_factory=utcnow)


class PlanItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    household_id: int = Field(index=True)
    date: str = Field(index=True)
    meal: str = "dinner"
    recipe_id: int = Field(index=True)
    servings: int = 2
    position: int = 0
    created_at: datetime = Field(default_factory=utcnow)


class ShoppingItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    household_id: int = Field(index=True)
    week_start: str = Field(index=True)
    name: str
    amount: str = ""
    unit: str = ""
    category: str = "其他"
    checked: bool = False
    custom: bool = False
    source_key: str = ""
    created_at: datetime = Field(default_factory=utcnow)


class Favorite(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    recipe_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=utcnow)
