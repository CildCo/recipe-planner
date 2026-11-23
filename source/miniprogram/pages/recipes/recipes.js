const store = require("../../services/store");
const dateUtil = require("../../utils/date");
const mealUtil = require("../../utils/meal");

Page({
  data: {
    categories: [],
    active: "all",
    q: "",
    list: [],
    total: 0,
    pickMode: false,
    pickDate: "",
    pickMeal: "dinner",
    pickLabel: "",
    loading: true,
  },

  onLoad(options) {
    const pickMode = options.pick === "1";
    this.setData({
      active: options.category || "all",
      pickMode,
      pickDate: options.date || dateUtil.todayKey(),
      pickMeal: options.meal || "dinner",
      pickLabel: pickMode
        ? dateUtil.dateLong(options.date || dateUtil.todayKey()) + " " + (mealUtil.MEAL_NAMES[options.meal] || "晚餐")
        : "",
    });
    store.getSite().then((site) => {
      this.setData({ categories: site.categories || [] });
    });
    this.load();
  },

  load() {
    this.setData({ loading: true });
    store
      .getRecipes({ category: this.data.active, q: this.data.q })
      .then((result) => {
        this.setData({ list: result.items || [], total: result.total || 0, loading: false });
      })
      .catch((error) => {
        this.setData({ loading: false });
        wx.showToast({ title: error.message || "加载失败", icon: "none" });
      });
  },

  onSearch(event) {
    const value = event.detail.value;
    this.setData({ q: value });
    clearTimeout(this._timer);
    this._timer = setTimeout(() => this.load(), 260);
  },

  clearSearch() {
    this.setData({ q: "" });
    this.load();
  },

  chooseCategory(event) {
    const id = event.currentTarget.dataset.id;
    this.setData({ active: id });
    this.load();
  },

  openRecipe(event) {
    const id = event.detail ? event.detail.id : event.currentTarget.dataset.id;
    if (!this.data.pickMode) {
      wx.navigateTo({ url: "/pages/recipe/recipe?id=" + id });
      return;
    }
    store
      .getRecipe(id)
      .then((recipe) => {
        return store.addPlan({
          date: this.data.pickDate,
          meal: this.data.pickMeal,
          recipeId: id,
          servings: recipe.servings,
        });
      })
      .then(() => {
        wx.showToast({ title: "已放进菜单", icon: "success" });
        setTimeout(() => wx.navigateBack(), 450);
      })
      .catch((error) => {
        wx.showToast({ title: error.message || "添加失败", icon: "none" });
      });
  },

  goBack() {
    wx.navigateBack();
  },
});
