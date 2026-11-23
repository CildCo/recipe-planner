from __future__ import annotations

from pydantic import BaseModel, Field


class LoginIn(BaseModel):
    code: str | None = None
    devOpenid: str | None = None
    nickname: str | None = None
    avatar: str | None = None


class PlanItemIn(BaseModel):
    date: str
    meal: str = "dinner"
    recipeId: int
    servings: int | None = None


class CopyWeekIn(BaseModel):
    fromWeek: str
    toWeek: str


class ToggleIn(BaseModel):
    checked: bool


class CustomItemIn(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    amount: str = ""
    unit: str = ""
    category: str = "其他"


class HouseholdIn(BaseModel):
    name: str = Field(default="我的饭桌", max_length=30)


class JoinIn(BaseModel):
    code: str = Field(min_length=4, max_length=10)
