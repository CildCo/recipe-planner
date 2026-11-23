from __future__ import annotations

import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
DATA_DIR = BASE_DIR / "data"
RUNTIME_DIR = BASE_DIR / "runtime"
UPLOAD_DIR = BASE_DIR / "uploads"
STATIC_DIR = APP_DIR / "static"
TEMPLATE_DIR = APP_DIR / "templates"
RECIPE_SEED = APP_DIR / "data" / "recipes.json"


def _load_env_file() -> None:
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        return
    for raw in env_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file()

APP_ENV = os.getenv("APP_ENV", "dev").strip().lower()
IS_PRODUCTION = APP_ENV == "production"
ALLOW_DEV_LOGIN = os.getenv("ALLOW_DEV_LOGIN", "0" if IS_PRODUCTION else "1") == "1"
WECHAT_APPID = os.getenv("WECHAT_APPID", "").strip()
WECHAT_SECRET = os.getenv("WECHAT_SECRET", "").strip()
ADMIN_USER = os.getenv("ADMIN_USER", "admin").strip() or "admin"
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

DATA_DIR.mkdir(parents=True, exist_ok=True)
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
(UPLOAD_DIR / "covers").mkdir(parents=True, exist_ok=True)

if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{(DATA_DIR / 'app.db').as_posix()}"

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8020"))


def _runtime_secret(name: str, length: int = 32) -> str:
    path = RUNTIME_DIR / name
    if path.exists():
        value = path.read_text(encoding="utf-8").strip()
        if value:
            return value
    value = secrets.token_urlsafe(length)
    path.write_text(value + "\n", encoding="utf-8")
    return value


SECRET_KEY = os.getenv("SECRET_KEY", "").strip() or _runtime_secret("secret.key", 40)
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "").strip() or _runtime_secret("admin-password.txt", 12)
