from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
import urllib.parse
import urllib.request

from .config import ALLOW_DEV_LOGIN, SECRET_KEY, WECHAT_APPID, WECHAT_SECRET

TOKEN_TTL = 30 * 24 * 3600
INVITE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64decode(text: str) -> bytes:
    padding = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + padding)


def create_token(user_id: int) -> str:
    payload = _b64encode(json.dumps({"uid": user_id, "exp": int(time.time()) + TOKEN_TTL}).encode("utf-8"))
    signature = hmac.new(SECRET_KEY.encode("utf-8"), payload.encode("ascii"), hashlib.sha256).digest()
    return f"{payload}.{_b64encode(signature)}"


def parse_token(token: str | None) -> int | None:
    if not token:
        return None
    try:
        payload, signature = token.split(".", 1)
        expected = hmac.new(SECRET_KEY.encode("utf-8"), payload.encode("ascii"), hashlib.sha256).digest()
        if not hmac.compare_digest(_b64decode(signature), expected):
            return None
        data = json.loads(_b64decode(payload))
        if int(data.get("exp", 0)) < time.time():
            return None
        return int(data.get("uid"))
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None


def new_invite_code() -> str:
    return "".join(secrets.choice(INVITE_ALPHABET) for _ in range(6))


def wechat_openid(code: str) -> str | None:
    if not (WECHAT_APPID and WECHAT_SECRET and code):
        return None
    query = urllib.parse.urlencode(
        {
            "appid": WECHAT_APPID,
            "secret": WECHAT_SECRET,
            "js_code": code,
            "grant_type": "authorization_code",
        }
    )
    url = f"https://api.weixin.qq.com/sns/jscode2session?{query}"
    try:
        with urllib.request.urlopen(url, timeout=6) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception:
        return None
    if data.get("errcode"):
        return None
    return data.get("openid")


def resolve_openid(code: str | None, dev_openid: str | None = None) -> str | None:
    if code:
        openid = wechat_openid(code)
        if openid:
            return openid
    if ALLOW_DEV_LOGIN:
        seed = (dev_openid or code or "local-guest").strip()
        digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16]
        return f"dev-{digest}"
    return None
