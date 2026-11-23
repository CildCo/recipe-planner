from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .admin.routes import router as admin_router
from .api.routes import router as api_router
from .config import APP_ENV, IS_PRODUCTION, SECRET_KEY, STATIC_DIR, UPLOAD_DIR
from .db import engine, init_db
from .seed import seed_database
from sqlmodel import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with Session(engine) as session:
        seed_database(session)
    yield


app = FastAPI(title="饭桌", description="菜谱、一周菜单与买菜清单", lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    same_site="lax",
    https_only=IS_PRODUCTION,
    max_age=14 * 24 * 3600,
)
if APP_ENV != "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)
app.include_router(admin_router)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


@app.exception_handler(HTTPException)
async def http_error(request: Request, error: HTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=error.status_code,
            content={"ok": False, "error": {"code": error.status_code, "message": str(error.detail)}},
        )
    return JSONResponse(status_code=error.status_code, content={"detail": str(error.detail)})


@app.exception_handler(Exception)
async def unhandled_error(request: Request, error: Exception):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": {"code": 500, "message": "服务暂时不可用"}},
        )
    raise error


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/admin/login", status_code=303)


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok", "app": "饭桌"}
