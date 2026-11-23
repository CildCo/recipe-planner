CATEGORIES = [
    {"id": "quick", "name": "快手菜", "note": "二十分钟内上桌", "color": "tomato"},
    {"id": "home", "name": "家常菜", "note": "一锅一灶的熟悉味道", "color": "plum"},
    {"id": "soup", "name": "汤羹", "note": "小火慢慢煨", "color": "jade"},
    {"id": "staple", "name": "主食", "note": "面、饭、饺子", "color": "olive"},
    {"id": "breakfast", "name": "早餐", "note": "把早晨安顿好", "color": "mustard"},
]

MEALS = [
    {"id": "breakfast", "name": "早餐"},
    {"id": "lunch", "name": "午餐"},
    {"id": "dinner", "name": "晚餐"},
]

MEAL_LABELS = {item["id"]: item["name"] for item in MEALS}
CATEGORY_LABELS = {item["id"]: item["name"] for item in CATEGORIES}
GROUP_ORDER = ["蔬菜", "肉蛋", "主食", "调料", "其他"]


def category_name(category_id: str) -> str:
    return CATEGORY_LABELS.get(category_id, category_id)


def meal_name(meal_id: str) -> str:
    return MEAL_LABELS.get(meal_id, meal_id)
