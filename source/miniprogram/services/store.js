const config = require("../config/index");
const api = require("./api");
const data = require("../data/recipes");
const dateUtil = require("../utils/date");
const mealUtil = require("../utils/meal");

const PLAN_KEY = "fz_plan_v1";
const SHOP_KEY = "fz_shopping_v1";
const HOUSEHOLD_KEY = "fz_household_v1";
const FAVORITE_KEY = "fz_favorites_v1";
const SEED_KEY = "fz_seeded_v1";

const isMock = config.mode !== "server";

function read(key, fallback) {
  const value = wx.getStorageSync(key);
  return value === "" || value === null || value === undefined ? fallback : value;
}

function write(key, value) {
  wx.setStorageSync(key, value);
}

function normalizeRecipe(recipe) {
  if (!recipe) return recipe;
  return Object.assign({}, recipe, { cover: api.absolute(recipe.cover) });
}

function normalizePlan(plan) {
  if (!plan || !plan.days) return plan;
  const days = plan.days.map((day) =>
    Object.assign({}, day, {
      meals: (day.meals || []).map((meal) =>
        Object.assign({}, meal, {
          items: (meal.items || []).map((item) => Object.assign({}, item, { cover: api.absolute(item.cover) })),
        })
      ),
    })
  );
  return Object.assign({}, plan, { days });
}

let lastId = 0;

function nextId() {
  const now = Date.now();
  lastId = now > lastId ? now : lastId + 1;
  return lastId;
}

function ensureSeed() {
  if (!isMock || read(SEED_KEY, false)) return;
  const start = dateUtil.weekStart(dateUtil.todayKey());
  const seedPlan = [
    { offset: 0, meal: "dinner", recipeId: 1, servings: 2 },
    { offset: 0, meal: "dinner", recipeId: 19, servings: 2 },
    { offset: 1, meal: "lunch", recipeId: 2, servings: 2 },
    { offset: 1, meal: "dinner", recipeId: 8, servings: 3 },
    { offset: 2, meal: "dinner", recipeId: 10, servings: 2 },
    { offset: 3, meal: "lunch", recipeId: 18, servings: 2 },
    { offset: 3, meal: "dinner", recipeId: 14, servings: 3 },
    { offset: 4, meal: "dinner", recipeId: 12, servings: 3 },
    { offset: 5, meal: "breakfast", recipeId: 24, servings: 1 },
    { offset: 5, meal: "dinner", recipeId: 7, servings: 4 },
    { offset: 6, meal: "breakfast", recipeId: 23, servings: 2 },
    { offset: 6, meal: "dinner", recipeId: 21, servings: 2 },
  ].map((item) => ({
    id: nextId(),
    date: dateUtil.addDays(start, item.offset),
    meal: item.meal,
    recipeId: item.recipeId,
    servings: item.servings,
  }));
  const plans = {};
  plans[start] = seedPlan;
  write(PLAN_KEY, plans);
  write(HOUSEHOLD_KEY, {
    id: 1,
    name: "小满的饭桌",
    inviteCode: "FANZHUO",
    members: [
      { id: 1, nickname: "小满", initial: "小" },
      { id: 2, nickname: "阿岚", initial: "阿" },
    ],
  });
  write(FAVORITE_KEY, [1, 7, 18]);
  write(SEED_KEY, true);
}

function planMap() {
  return read(PLAN_KEY, {});
}

function savePlanMap(map) {
  write(PLAN_KEY, map);
}

function buildPlan(startKey, items) {
  const days = dateUtil.weekDays(startKey).map((day) => {
    const dateKey = day.date || day.key;
    const meals = mealUtil.MEALS.map((meal) => {
      const mealItems = items
        .filter((item) => item.date === dateKey && item.meal === meal.id)
        .map((item) => {
          const recipe = mealUtil.recipeById(item.recipeId);
          return {
            id: item.id,
            recipeId: item.recipeId,
            title: recipe ? recipe.title : "菜谱已删除",
            cover: recipe ? recipe.cover : "",
            time: recipe ? recipe.time : 0,
            category: recipe ? recipe.category : "",
            servings: item.servings,
            meal: meal.id,
            mealName: meal.name,
            date: day.key,
          };
        });
      return { id: meal.id, name: meal.name, items: mealItems };
    });
    return Object.assign({}, day, {
      meals,
      count: meals.reduce((sum, meal) => sum + meal.items.length, 0),
    });
  });
  const total = days.reduce((sum, day) => sum + day.count, 0);
  return {
    weekStart: startKey,
    weekEnd: dateUtil.addDays(startKey, 6),
    label: dateUtil.weekLabel(startKey),
    days,
    total,
  };
}

function getSite() {
  if (!isMock) return api.request("/api/site");
  const counts = {};
  data.recipes.forEach((recipe) => {
    counts[recipe.category] = (counts[recipe.category] || 0) + 1;
  });
  return Promise.resolve({
    settings: require("../data/site"),
    categories: data.categories.map((item) => Object.assign({}, item, { count: counts[item.id] || 0 })),
    meals: data.meals,
    recipeCount: data.recipes.length,
  });
}

function getRecipes(options) {
  const opts = options || {};
  if (!isMock) {
    const params = [];
    if (opts.category && opts.category !== "all") params.push("category=" + encodeURIComponent(opts.category));
    if (opts.q) params.push("q=" + encodeURIComponent(opts.q));
    return api.request("/api/recipes?" + params.join("&")).then((result) => {
      result.items = (result.items || []).map(normalizeRecipe);
      return result;
    });
  }
  let rows = data.recipes.slice();
  if (opts.category && opts.category !== "all") {
    rows = rows.filter((recipe) => recipe.category === opts.category);
  }
  if (opts.q) {
    const keyword = opts.q.trim();
    rows = rows.filter(
      (recipe) =>
        recipe.title.indexOf(keyword) > -1 ||
        (recipe.summary || "").indexOf(keyword) > -1 ||
        (recipe.tags || []).join(" ").indexOf(keyword) > -1
    );
  }
  return Promise.resolve({ items: rows, total: rows.length, page: 1, hasMore: false });
}

function getRecipe(id) {
  if (!isMock) {
    return api.request("/api/recipes/" + Number(id)).then(normalizeRecipe);
  }
  return Promise.resolve(mealUtil.recipeById(id));
}

function getPlan(week) {
  if (!isMock) {
    return api.ensureLogin()
      .then(() => api.request("/api/plan?week=" + encodeURIComponent(week || "")))
      .then(normalizePlan);
  }
  ensureSeed();
  const start = dateUtil.weekStart(week || dateUtil.todayKey());
  const map = planMap();
  return Promise.resolve(buildPlan(start, map[start] || []));
}

function addPlan(item) {
  if (!isMock) {
    return api.request("/api/plan/items", { method: "POST", data: item });
  }
  ensureSeed();
  const start = dateUtil.weekStart(item.date);
  const map = planMap();
  map[start] = map[start] || [];
  map[start].push({
    id: nextId(),
    date: item.date,
    meal: item.meal,
    recipeId: Number(item.recipeId),
    servings: Number(item.servings) || 2,
  });
  savePlanMap(map);
  return Promise.resolve({ ok: true });
}

function removePlan(id) {
  if (!isMock) {
    return api.request("/api/plan/items/" + Number(id), { method: "DELETE" });
  }
  const map = planMap();
  Object.keys(map).forEach((week) => {
    map[week] = map[week].filter((item) => item.id !== id);
  });
  savePlanMap(map);
  return Promise.resolve({ removed: true });
}

function copyWeek(fromWeek, toWeek) {
  if (!isMock) {
    return api.request("/api/plan/copy", { method: "POST", data: { fromWeek, toWeek } });
  }
  const sourceStart = dateUtil.weekStart(fromWeek);
  const targetStart = dateUtil.weekStart(toWeek);
  const map = planMap();
  const source = map[sourceStart] || [];
  const target = map[targetStart] || [];
  let copied = 0;
  source.forEach((item) => {
    const offset = Math.round((dateUtil.parseKey(item.date) - dateUtil.parseKey(sourceStart)) / 86400000);
    const date = dateUtil.addDays(targetStart, offset);
    const exists = target.some((row) => row.date === date && row.meal === item.meal && row.recipeId === item.recipeId);
    if (exists) return;
    target.push({
      id: nextId(),
      date,
      meal: item.meal,
      recipeId: item.recipeId,
      servings: item.servings,
    });
    copied += 1;
  });
  map[targetStart] = target;
  savePlanMap(map);
  return Promise.resolve({ copied, week: targetStart });
}

function shoppingMap() {
  return read(SHOP_KEY, {});
}

function saveShoppingMap(map) {
  write(SHOP_KEY, map);
}

function buildShopping(weekKey, items) {
  const groups = mealUtil.GROUP_ORDER.map((name) => ({
    name,
    items: items.filter((item) => item.category === name),
  })).filter((group) => group.items.length);
  const checked = items.filter((item) => item.checked).length;
  return {
    weekStart: weekKey,
    items,
    groups,
    total: items.length,
    checked,
    progress: items.length ? Math.round((checked / items.length) * 100) : 0,
  };
}

function generateShopping(week) {
  if (!isMock) {
    return api.request("/api/shopping/generate?week=" + encodeURIComponent(week || ""), { method: "POST" });
  }
  const start = dateUtil.weekStart(week || dateUtil.todayKey());
  const map = planMap();
  const planItems = map[start] || [];
  const previous = shoppingMap()[start] || { items: [] };
  const checked = {};
  const custom = [];
  previous.items.forEach((item) => {
    if (item.custom) custom.push(item);
    else checked[item.key] = item.checked;
  });
  const aggregated = mealUtil.aggregate(planItems);
  const items = aggregated.rows.map((row) => ({
    id: nextId(),
    name: row.name,
    amount: row.amount,
    unit: row.unit,
    category: row.category,
    checked: !!checked[row.key],
    custom: false,
    key: row.key,
  }));
  const all = items.concat(custom);
  const shopping = shoppingMap();
  shopping[start] = { weekStart: start, items: all };
  saveShoppingMap(shopping);
  return Promise.resolve(buildShopping(start, all));
}

function getShopping(week) {
  if (!isMock) {
    return api.ensureLogin()
      .then(() => api.request("/api/shopping?week=" + encodeURIComponent(week || "")));
  }
  const start = dateUtil.weekStart(week || dateUtil.todayKey());
  const map = shoppingMap();
  if (!map[start]) return generateShopping(start);
  return Promise.resolve(buildShopping(start, map[start].items));
}

function toggleShopping(id, checked, week) {
  if (!isMock) {
    return api.request("/api/shopping/" + Number(id), { method: "PATCH", data: { checked: !!checked } });
  }
  const start = dateUtil.weekStart(week || dateUtil.todayKey());
  const map = shoppingMap();
  const bucket = map[start];
  if (bucket) {
    bucket.items.forEach((item) => {
      if (item.id === id) item.checked = !!checked;
    });
    saveShoppingMap(map);
    return Promise.resolve(buildShopping(start, bucket.items));
  }
  return Promise.resolve(buildShopping(start, []));
}

function addShoppingItem(item, week) {
  if (!isMock) {
    return api.request("/api/shopping/items?week=" + encodeURIComponent(week || ""), {
      method: "POST",
      data: item,
    });
  }
  const start = dateUtil.weekStart(week || dateUtil.todayKey());
  const map = shoppingMap();
  const bucket = map[start] || { weekStart: start, items: [] };
  bucket.items.push({
    id: nextId(),
    name: item.name,
    amount: item.amount || "",
    unit: item.unit || "",
    category: item.category || "其他",
    checked: false,
    custom: true,
    key: "custom|" + nextId() + "|" + item.name,
  });
  map[start] = bucket;
  saveShoppingMap(map);
  return Promise.resolve(buildShopping(start, bucket.items));
}

function deleteShoppingItem(id, week) {
  if (!isMock) {
    return api.request("/api/shopping/items/" + Number(id), { method: "DELETE" });
  }
  const start = dateUtil.weekStart(week || dateUtil.todayKey());
  const map = shoppingMap();
  const bucket = map[start];
  if (bucket) {
    bucket.items = bucket.items.filter((item) => item.id !== id);
    saveShoppingMap(map);
    return Promise.resolve(buildShopping(start, bucket.items));
  }
  return Promise.resolve(buildShopping(start, []));
}

function getHousehold() {
  if (!isMock) {
    return api.ensureLogin().then(() => api.request("/api/household"));
  }
  ensureSeed();
  return Promise.resolve(read(HOUSEHOLD_KEY, null));
}

function createHousehold(name) {
  if (!isMock) {
    return api.request("/api/household/create", { method: "POST", data: { name } });
  }
  const members = [{ id: 1, nickname: "我", initial: "我" }];
  const household = { id: nextId(), name: name || "我的饭桌", inviteCode: "FZ" + String(nextId()).slice(-4), members };
  write(HOUSEHOLD_KEY, household);
  return Promise.resolve(household);
}

function joinHousehold(code) {
  if (!isMock) {
    return api.request("/api/household/join", { method: "POST", data: { code } });
  }
  const current = read(HOUSEHOLD_KEY, null);
  if (!current) return createHousehold("我的饭桌");
  const members = current.members.slice();
  if (!members.some((member) => member.nickname === "家人")) {
    members.push({ id: nextId(), nickname: "家人", initial: "家" });
  }
  const household = Object.assign({}, current, { members });
  write(HOUSEHOLD_KEY, household);
  return Promise.resolve(household);
}

function getFavorites() {
  if (!isMock) {
    return api.ensureLogin().then(() =>
      api.request("/api/favorites").then((result) => ({
        ids: result.ids || [],
        items: (result.items || []).map(normalizeRecipe),
      }))
    );
  }
  const ids = read(FAVORITE_KEY, []);
  const items = ids.map((id) => mealUtil.recipeById(id)).filter(Boolean);
  return Promise.resolve({ ids, items });
}

function toggleFavorite(id) {
  if (!isMock) {
    return api.request("/api/recipes/" + Number(id) + "/favorite", { method: "POST" });
  }
  const ids = read(FAVORITE_KEY, []);
  const numeric = Number(id);
  const index = ids.indexOf(numeric);
  if (index > -1) ids.splice(index, 1);
  else ids.push(numeric);
  write(FAVORITE_KEY, ids);
  return Promise.resolve({ favorite: index === -1 });
}

function resetDemo() {
  if (!isMock) return;
  wx.removeStorageSync(PLAN_KEY);
  wx.removeStorageSync(SHOP_KEY);
  wx.removeStorageSync(HOUSEHOLD_KEY);
  wx.removeStorageSync(FAVORITE_KEY);
  wx.removeStorageSync(SEED_KEY);
  ensureSeed();
}

module.exports = {
  isMock,
  getSite,
  getRecipes,
  getRecipe,
  getPlan,
  addPlan,
  removePlan,
  copyWeek,
  getShopping,
  generateShopping,
  toggleShopping,
  addShoppingItem,
  deleteShoppingItem,
  getHousehold,
  createHousehold,
  joinHousehold,
  getFavorites,
  toggleFavorite,
  resetDemo,
};
