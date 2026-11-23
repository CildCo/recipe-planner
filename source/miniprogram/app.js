const site = require("./data/site");

App({
  globalData: {
    site,
    statusBarHeight: 20,
  },
  onLaunch() {
    try {
      const info = wx.getWindowInfo ? wx.getWindowInfo() : wx.getSystemInfoSync();
      this.globalData.statusBarHeight = info.statusBarHeight || 20;
    } catch (error) {
      this.globalData.statusBarHeight = 20;
    }
  },
});
