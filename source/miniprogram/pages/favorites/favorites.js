const store = require("../../services/store");

Page({
  data: {
    items: [],
    loading: true,
  },

  onShow() {
    store
      .getFavorites()
      .then((result) => this.setData({ items: result.items || [], loading: false }))
      .catch((error) => {
        this.setData({ loading: false });
        wx.showToast({ title: error.message || "加载失败", icon: "none" });
      });
  },

  openRecipe(event) {
    const id = event.detail ? event.detail.id : event.currentTarget.dataset.id;
    wx.navigateTo({ url: "/pages/recipe/recipe?id=" + id });
  },

  goRecipes() {
    wx.navigateTo({ url: "/pages/recipes/recipes" });
  },
});
