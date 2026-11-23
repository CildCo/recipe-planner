const store = require("../../services/store");
const dateUtil = require("../../utils/date");

Page({
  data: {
    weekStart: "",
    weekLabel: "",
    days: [],
    total: 0,
    todayKey: "",
    loading: true,
  },

  onShow() {
    const weekStart = this.data.weekStart || dateUtil.weekStart(dateUtil.todayKey());
    this.setData({ weekStart });
    this.load(weekStart);
  },

  load(weekStart) {
    this.setData({ loading: true });
    store
      .getPlan(weekStart)
      .then((plan) => {
        this.setData({
          weekStart: plan.weekStart,
          weekLabel: plan.label,
          days: plan.days || [],
          total: plan.total || 0,
          todayKey: dateUtil.todayKey(),
          loading: false,
        });
      })
      .catch((error) => {
        this.setData({ loading: false });
        wx.showToast({ title: error.message || "加载失败", icon: "none" });
      });
  },

  prevWeek() {
    this.load(dateUtil.addDays(this.data.weekStart, -7));
  },

  nextWeek() {
    this.load(dateUtil.addDays(this.data.weekStart, 7));
  },

  addDish(event) {
    const date = event.currentTarget.dataset.date;
    const meal = event.currentTarget.dataset.meal;
    wx.navigateTo({
      url: "/pages/recipes/recipes?pick=1&date=" + date + "&meal=" + meal,
    });
  },

  openRecipe(event) {
    const id = event.currentTarget.dataset.id;
    wx.navigateTo({ url: "/pages/recipe/recipe?id=" + id });
  },

  removeDish(event) {
    const id = Number(event.currentTarget.dataset.id);
    wx.showModal({
      title: "移出菜单",
      content: "把这道菜从这一餐里拿掉？",
      confirmColor: "#c94f3d",
      success: (res) => {
        if (!res.confirm) return;
        store
          .removePlan(id)
          .then(() => this.load(this.data.weekStart))
          .catch((error) => wx.showToast({ title: error.message || "删除失败", icon: "none" }));
      },
    });
  },

  copyLastWeek() {
    const source = dateUtil.addDays(this.data.weekStart, -7);
    wx.showModal({
      title: "复制上周",
      content: "把上周的菜单复制到这一周？已经有的菜不会重复。",
      success: (res) => {
        if (!res.confirm) return;
        store
          .copyWeek(source, this.data.weekStart)
          .then((result) => {
            wx.showToast({ title: "复制了 " + (result.copied || 0) + " 道", icon: "none" });
            this.load(this.data.weekStart);
          })
          .catch((error) => wx.showToast({ title: error.message || "复制失败", icon: "none" }));
      },
    });
  },

  goShopping() {
    wx.switchTab({ url: "/pages/shopping/shopping" });
  },
});
