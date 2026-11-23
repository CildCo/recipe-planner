const store = require("../../services/store");
const dateUtil = require("../../utils/date");
const site = require("../../data/site");

Page({
  data: {
    site,
    household: null,
    favoriteCount: 0,
    planCount: 0,
    shoppingCount: 0,
    isMock: store.isMock,
  },

  onShow() {
    const weekStart = dateUtil.weekStart(dateUtil.todayKey());
    Promise.all([store.getHousehold(), store.getFavorites(), store.getPlan(weekStart), store.getShopping(weekStart), store.getSite()])
      .then(([household, favorites, plan, shopping, siteData]) => {
        this.setData({
          site: siteData.settings || site,
          household,
          favoriteCount: (favorites.ids || []).length,
          planCount: plan.total || 0,
          shoppingCount: shopping.total || 0,
        });
      })
      .catch((error) => {
        wx.showToast({ title: error.message || "加载失败", icon: "none" });
      });
  },

  copyCode() {
    if (!this.data.household) return;
    wx.setClipboardData({
      data: this.data.household.inviteCode,
      success: () => wx.showToast({ title: "邀请码已复制", icon: "success" }),
    });
  },

  goHousehold() {
    wx.navigateTo({ url: "/pages/household/household" });
  },

  goFavorites() {
    wx.navigateTo({ url: "/pages/favorites/favorites" });
  },

  goAbout() {
    wx.navigateTo({ url: "/pages/about/about" });
  },

  goPlan() {
    wx.switchTab({ url: "/pages/plan/plan" });
  },

  goShopping() {
    wx.switchTab({ url: "/pages/shopping/shopping" });
  },

  resetDemo() {
    wx.showModal({
      title: "重置演示数据",
      content: "会清空本地菜单、清单和收藏，恢复成初始示例。",
      confirmColor: "#c94f3d",
      success: (res) => {
        if (!res.confirm) return;
        store.resetDemo();
        wx.showToast({ title: "已重置", icon: "success" });
        this.onShow();
      },
    });
  },
});
