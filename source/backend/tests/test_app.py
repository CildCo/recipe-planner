from __future__ import annotations

from datetime import date, timedelta


def test_health_and_seed(client):
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["data"]["status"] == "ok"

    site = client.get("/api/site").json()["data"]
    assert site["recipeCount"] == 26
    assert {item["id"] for item in site["categories"]} == {"quick", "home", "soup", "staple", "breakfast"}

    recipes = client.get("/api/recipes").json()["data"]
    assert recipes["total"] == 26
    assert recipes["items"][0]["cover"].startswith("/static/covers/")


def test_recipe_detail(client):
    response = client.get("/api/recipes/1")
    assert response.status_code == 200
    recipe = response.json()["data"]
    assert recipe["title"] == "番茄炒蛋"
    assert recipe["ingredients"]
    assert recipe["steps"]
    assert recipe["tips"]


def test_login_plan_shopping(client, auth):
    token = client.post("/api/auth/login", json={"devOpenid": "plan-user"}).json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    house = client.get("/api/household", headers=headers).json()["data"]
    assert house["inviteCode"]

    monday = date.today() - timedelta(days=date.today().weekday())
    added = client.post(
        "/api/plan/items",
        headers=headers,
        json={"date": monday.isoformat(), "meal": "lunch", "recipeId": 2, "servings": 2},
    )
    assert added.status_code == 200
    plan = client.get("/api/plan", headers=headers).json()["data"]
    assert plan["total"] >= 1

    shopping = client.post("/api/shopping/generate", headers=headers).json()["data"]
    assert shopping["total"] > 0
    first = shopping["items"][0]
    toggled = client.patch(f"/api/shopping/{first['id']}", headers=headers, json={"checked": True})
    assert toggled.status_code == 200
    assert toggled.json()["data"]["checked"] is True

    custom = client.post(
        "/api/shopping/items",
        headers=headers,
        params={"week": monday.isoformat()},
        json={"name": "厨房纸", "amount": "1 包", "category": "其他"},
    )
    assert custom.status_code == 200

    favorite = client.post("/api/recipes/3/favorite", headers=headers).json()["data"]
    assert favorite["favorite"] is True
    favorites = client.get("/api/favorites", headers=headers).json()["data"]
    assert 3 in favorites["ids"]


def test_household_join(client):
    token = client.post("/api/auth/login", json={"devOpenid": "join-user"}).json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    demo = client.get("/api/household", headers=headers).json()["data"]
    assert demo["name"]
    joined = client.post("/api/household/join", headers=headers, json={"code": "FANZHUO"})
    assert joined.status_code == 200
    assert joined.json()["data"]["name"] == "小满的饭桌"


def test_admin_requires_login(client):
    response = client.get("/admin", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/admin/login"


def test_admin_pages(admin):
    for path in (
        "/admin",
        "/admin/recipes",
        "/admin/recipes/new",
        "/admin/recipes/1/edit",
        "/admin/households",
        "/admin/households/1",
        "/admin/shopping",
        "/admin/settings",
        "/admin/help",
        "/admin/recipes.json",
    ):
        response = admin.get(path)
        assert response.status_code == 200, path


def test_admin_recipe_crud(admin):
    from tests.conftest import extract_csrf

    page = admin.get("/admin/recipes/new")
    csrf = extract_csrf(page.text)
    form = {
        "csrf": csrf,
        "title": "测试菜",
        "slug": "test-dish",
        "summary": "测试用的一道菜。",
        "category": "quick",
        "time": "12",
        "servings": "2",
        "difficulty": "容易",
        "tags": "测试、快手",
        "cover": "covers/tomato-egg.jpg",
        "published": "on",
        "ingredient_name": ["鸡蛋", "盐"],
        "ingredient_amount": ["2", "适量"],
        "ingredient_unit": ["个", ""],
        "ingredient_group": ["肉蛋", "调料"],
        "step_text": ["打散鸡蛋。", "下锅炒熟。"],
        "step_tip": ["", "小火。"],
    }
    created = admin.post("/admin/recipes/save", data=form, follow_redirects=False)
    assert created.status_code == 303

    rows = admin.get("/admin/recipes.json").json()
    recipe = next(item for item in rows if item["slug"] == "test-dish")
    assert recipe["title"] == "测试菜"
    assert recipe["ingredients"][0]["name"] == "鸡蛋"

    edit_page = admin.get("/admin/recipes")
    assert "测试菜" in edit_page.text

    delete_csrf = extract_csrf(admin.get("/admin/recipes/1/edit").text)
    deleted = admin.post("/admin/recipes/1/delete", data={"csrf": delete_csrf}, follow_redirects=False)
    assert deleted.status_code == 303
    assert admin.get("/api/recipes/1").status_code == 404


def test_admin_settings_and_csv(admin):
    from tests.conftest import extract_csrf

    csrf = extract_csrf(admin.get("/admin/settings").text)
    response = admin.post(
        "/admin/settings",
        data={"csrf": csrf, "site_name": "饭桌", "tagline": "把一周的饭安排好", "intro": "测试", "default_servings": "2"},
    )
    assert response.status_code == 200
    assert "设置已保存" in response.text

    csv = admin.get("/admin/shopping.csv")
    assert csv.status_code == 200
    assert "分类" in csv.text
