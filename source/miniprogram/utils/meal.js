const data = require("../data/recipes");

const MEALS = data.meals;
const CATEGORIES = data.categories;
const RECIPES = data.recipes;
const CATEGORY_NAMES = {};
const MEAL_NAMES = {};
const GROUP_ORDER = ["蔬菜", "肉蛋", "主食", "调料", "其他"];

CATEGORIES.forEach((item) => {
  CATEGORY_NAMES[item.id] = item.name;
});
MEALS.forEach((item) => {
  MEAL_NAMES[item.id] = item.name;
});

function recipeById(id) {
  return RECIPES.find((item) => item.id === Number(id)) || null;
}

function amountText(amount, unit) {
  if (amount === null || amount === undefined || amount === "") return unit || "";
  if (typeof amount === "number") {
    const text = Number.isInteger(amount) ? String(amount) : String(Math.round(amount * 100) / 100);
    return text + (unit || "");
  }
  const text = String(amount);
  if (unit && text.indexOf(unit) === -1) return text + unit;
  return text;
}

function mergeAmounts(values, unit) {
  let numeric = 0;
  const texts = [];
  values.forEach((value) => {
    if (typeof value === "number") {
      numeric += value;
    } else if (value !== null && value !== undefined && value !== "") {
      const text = String(value).trim();
      if (text && texts.indexOf(text) === -1) texts.push(text);
    }
  });
  let base = "";
  if (numeric > 0) base = amountText(Math.round(numeric * 100) / 100, unit);
  if (texts.length) {
    const tail = texts.join("、");
    return base ? base + " + " + tail : tail;
  }
  return base || unit || "";
}

function aggregate(planItems) {
  const map = {};
  planItems.forEach((plan) => {
    const recipe = recipeById(plan.recipeId);
    if (!recipe) return;
    const scale = Math.max(1, plan.servings || recipe.servings) / Math.max(1, recipe.servings);
    (recipe.ingredients || []).forEach((raw) => {
      const name = String(raw.name || "").trim();
      if (!name) return;
      const unit = String(raw.unit || "").trim();
      const group = String(raw.group || "其他").trim() || "其他";
      const key = name + "|" + unit + "|" + group;
      if (!map[key]) {
        map[key] = { name, unit, group, values: [], key };
      }
      if (typeof raw.amount === "number") {
        map[key].values.push(raw.amount * scale);
      } else {
        map[key].values.push(raw.amount);
      }
    });
  });
  const rows = Object.keys(map).map((key) => {
    const entry = map[key];
    return {
      name: entry.name,
      unit: entry.unit,
      category: entry.group,
      amount: mergeAmounts(entry.values, entry.unit),
      key,
    };
  });
  const groups = GROUP_ORDER.map((name) => ({
    name,
    items: rows.filter((row) => row.category === name),
  })).filter((group) => group.items.length);
  return { rows, groups };
}

module.exports = {
  MEALS,
  CATEGORIES,
  RECIPES,
  CATEGORY_NAMES,
  MEAL_NAMES,
  GROUP_ORDER,
  recipeById,
  amountText,
  mergeAmounts,
  aggregate,
};
