const store = require("../../services/store");
const dateUtil = require("../../utils/date");
const site = require("../../data/site");

function interleave(rows) {
  const buckets = {};
  rows.forEach((recipe) => {
    buckets[recipe.category] = buckets[recipe.category] || [];
    buckets[recipe.category].push(recipe);
  });
  const order = ["quick", "home", "soup", "staple", "breakfast"];
  const result = [];
  let index = 0;
  while (result.length < 8) {
    let added = false;
    order.forEach((key) => {
      if (result.length >= 8) return;
      const bucket = buckets[key] || [];
      if (bucket[index]) {
        result.push(bucket[index]);
        added = true;
      }
    });
    index += 1;
    if (!added) break;
  }
  return result;
}

Page({
  data: {
    site,
    todayKey: "",
    dateLabel: "",
    week: null,
    weekDays: [],
    todayMeals: [],
    recommended: [],
    categories: [],
    planCount: 0,
    recipeCount: 0,
  },

  onShow() {
    this.load();
  },

  load() {
    const todayKey = dateUtil.todayKey();
    Promise.all([store.getSite(), store.getPlan(todayKey), store.getRecipes({})])
      .then(([siteData, plan, recipes]) => {
        const today = (plan.days || []).find((day) => day.date === todayKey);
        this.setData({
          site: siteData.settings || site,
          categories: siteData.categories || [],
          recipeCount: siteData.recipeCount || 0,
          todayKey,
          dateLabel: dateUtil.dateLong(todayKey),
          week: plan,
          weekDays: plan.days || [],
          todayMeals: today ? today.meals : [],
          planCount: plan.total || 0,
          recommended: interleave(recipes.items || []),
        });
      })
      .catch((error) => {
        wx.showToast({ title: error.message || "加载失败", icon: "none" });
      });
  },

  goPlan() {
    wx.switchTab({ url: "/pages/plan/plan" });
  },

  goShopping() {
    wx.switchTab({ url: "/pages/shopping/shopping" });
  },

  goRecipes(event) {
    const category = event.currentTarget.dataset.category || "";
    wx.navigateTo({ url: "/pages/recipes/recipes" + (category ? "?category=" + category : "") });
  },

  goRecipe(event) {
    const id = event.detail ? event.detail.id : event.currentTarget.dataset.id;
    wx.navigateTo({ url: "/pages/recipe/recipe?id=" + id });
  },

  onShareAppMessage() {
    return {
      title: "饭桌 · 把一周的饭安排好",
      path: "/pages/home/home",
    };
  },
});
