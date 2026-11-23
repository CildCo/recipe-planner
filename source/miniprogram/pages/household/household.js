const store = require("../../services/store");

Page({
  data: {
    household: null,
    name: "",
    code: "",
  },

  onShow() {
    store
      .getHousehold()
      .then((household) => this.setData({ household }))
      .catch((error) => wx.showToast({ title: error.message || "加载失败", icon: "none" }));
  },

  onName(event) { this.setData({ name: event.detail.value }); },
  onCode(event) { this.setData({ code: event.detail.value.toUpperCase() }); },

  copyCode() {
    if (!this.data.household) return;
    wx.setClipboardData({
      data: this.data.household.inviteCode,
      success: () => wx.showToast({ title: "邀请码已复制", icon: "success" }),
    });
  },

  create() {
    const name = this.data.name.trim() || "我的饭桌";
    store
      .createHousehold(name)
      .then((household) => {
        this.setData({ household, name: "" });
        wx.showToast({ title: "饭桌已创建", icon: "success" });
      })
      .catch((error) => wx.showToast({ title: error.message || "创建失败", icon: "none" }));
  },

  join() {
    const code = this.data.code.trim();
    if (code.length < 4) {
      wx.showToast({ title: "邀请码不对", icon: "none" });
      return;
    }
    store
      .joinHousehold(code)
      .then((household) => {
        this.setData({ household, code: "" });
        wx.showToast({ title: "已加入", icon: "success" });
      })
      .catch((error) => wx.showToast({ title: error.message || "加入失败", icon: "none" }));
  },
});
