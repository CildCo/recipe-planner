from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOURCE))

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("ALLOW_DEV_LOGIN", "1")
os.environ.setdefault("ADMIN_USER", "admin")
os.environ.setdefault("ADMIN_PASSWORD", "test-password")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402


def extract_csrf(html: str) -> str:
    found = re.search(r'name="csrf" value="([^"]+)"', html)
    if not found:
        raise AssertionError("页面里没有 csrf")
    return found.group(1)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def token(client):
    response = client.post("/api/auth/login", json={"devOpenid": "pytest-user"})
    assert response.status_code == 200
    return response.json()["data"]["token"]


@pytest.fixture(scope="session")
def auth(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def admin(client):
    page = client.get("/admin/login")
    csrf = extract_csrf(page.text)
    response = client.post(
        "/admin/login",
        data={"username": "admin", "password": "test-password", "csrf": csrf},
        follow_redirects=False,
    )
    assert response.status_code == 303
    return client
