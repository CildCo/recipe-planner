const store = require("../../services/store");
const dateUtil = require("../../utils/date");
const mealUtil = require("../../utils/meal");

Page({
  data: {
    id: 0,
    recipe: null,
    checked: [],
    favorite: false,
    sheetOpen: false,
    days: [],
    selectedDay: "",
    selectedMeal: "dinner",
    servings: 2,
    meals: mealUtil.MEALS,
    toast: "",
  },

  onLoad(options) {
    this.setData({ id: Number(options.id) });
    this.load();
  },

  load() {
    Promise.all([store.getRecipe(this.data.id), store.getFavorites()])
      .then(([recipe, favorites]) => {
        if (!recipe) {
          wx.showToast({ title: "菜谱不存在", icon: "none" });
          return;
        }
        this.setData({
          recipe,
          checked: (recipe.ingredients || []).map(() => false),
          favorite: (favorites.ids || []).indexOf(recipe.id) > -1,
          servings: recipe.servings,
          days: dateUtil.nextDays(7),
          selectedDay: dateUtil.todayKey(),
        });
        wx.setNavigationBarTitle({ title: recipe.title });
      })
      .catch((error) => {
        wx.showToast({ title: error.message || "加载失败", icon: "none" });
      });
  },

  toggleIngredient(event) {
    const index = Number(event.currentTarget.dataset.index);
    const checked = this.data.checked.slice();
    checked[index] = !checked[index];
    this.setData({ checked });
  },

  toggleFavorite() {
    store.toggleFavorite(this.data.id).then((result) => {
      this.setData({ favorite: !!result.favorite });
      wx.showToast({ title: result.favorite ? "已收藏" : "已取消收藏", icon: "none" });
    });
  },

  openSheet() {
    this.setData({ sheetOpen: true });
  },

  closeSheet() {
    this.setData({ sheetOpen: false });
  },

  chooseDay(event) {
    this.setData({ selectedDay: event.currentTarget.dataset.key });
  },

  chooseMeal(event) {
    this.setData({ selectedMeal: event.currentTarget.dataset.id });
  },

  changeServings(event) {
    const delta = Number(event.currentTarget.dataset.delta);
    const next = Math.min(12, Math.max(1, this.data.servings + delta));
    this.setData({ servings: next });
  },

  confirmAdd() {
    store
      .addPlan({
        date: this.data.selectedDay,
        meal: this.data.selectedMeal,
        recipeId: this.data.id,
        servings: this.data.servings,
      })
      .then(() => {
        this.setData({ sheetOpen: false });
        wx.showToast({ title: "已放进菜单", icon: "success" });
      })
      .catch((error) => {
        wx.showToast({ title: error.message || "添加失败", icon: "none" });
      });
  },

  goPlan() {
    wx.switchTab({ url: "/pages/plan/plan" });
  },

  onShareAppMessage() {
    const recipe = this.data.recipe;
    return {
      title: recipe ? recipe.title + " · 饭桌" : "饭桌",
      path: "/pages/recipe/recipe?id=" + this.data.id,
    };
  },
});
