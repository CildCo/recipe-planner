const store = require("../../services/store");
const dateUtil = require("../../utils/date");

Page({
  data: {
    weekStart: "",
    weekLabel: "",
    groups: [],
    total: 0,
    checked: 0,
    progress: 0,
    showAdd: false,
    name: "",
    amount: "",
    category: "蔬菜",
    categories: ["蔬菜", "肉蛋", "主食", "调料", "其他"],
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
      .getShopping(weekStart)
      .then((data) => {
        this.setData({
          weekStart: data.weekStart,
          weekLabel: dateUtil.weekLabel(data.weekStart),
          groups: data.groups || [],
          total: data.total || 0,
          checked: data.checked || 0,
          progress: data.progress || 0,
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

  toggleItem(event) {
    const id = Number(event.currentTarget.dataset.id);
    const checked = !event.currentTarget.dataset.checked;
    store
      .toggleShopping(id, checked, this.data.weekStart)
      .then((data) => {
        this.setData({
          groups: data.groups || [],
          total: data.total || 0,
          checked: data.checked || 0,
          progress: data.progress || 0,
        });
      })
      .catch((error) => wx.showToast({ title: error.message || "更新失败", icon: "none" }));
  },

  toggleAdd() {
    this.setData({ showAdd: !this.data.showAdd });
  },

  onName(event) { this.setData({ name: event.detail.value }); },
  onAmount(event) { this.setData({ amount: event.detail.value }); },

  chooseCategory(event) {
    this.setData({ category: event.currentTarget.dataset.name });
  },

  addItem() {
    const name = this.data.name.trim();
    if (!name) {
      wx.showToast({ title: "写个名字", icon: "none" });
      return;
    }
    store
      .addShoppingItem(
        { name, amount: this.data.amount.trim(), unit: "", category: this.data.category },
        this.data.weekStart
      )
      .then((data) => {
        this.setData({
          groups: data.groups || [],
          total: data.total || 0,
          checked: data.checked || 0,
          progress: data.progress || 0,
          name: "",
          amount: "",
          showAdd: false,
        });
        wx.showToast({ title: "已加入", icon: "success" });
      })
      .catch((error) => wx.showToast({ title: error.message || "添加失败", icon: "none" }));
  },

  generate() {
    wx.showModal({
      title: "重新生成清单",
      content: "会按这一周的菜单重新合并食材，手动加的东西会保留。",
      confirmColor: "#c94f3d",
      success: (res) => {
        if (!res.confirm) return;
        store
          .generateShopping(this.data.weekStart)
          .then((data) => {
            this.setData({
              groups: data.groups || [],
              total: data.total || 0,
              checked: data.checked || 0,
              progress: data.progress || 0,
            });
            wx.showToast({ title: "已重新生成", icon: "none" });
          })
          .catch((error) => wx.showToast({ title: error.message || "生成失败", icon: "none" }));
      },
    });
  },

  copyList() {
    const lines = ["买菜清单 · " + this.data.weekLabel];
    this.data.groups.forEach((group) => {
      lines.push("");
      lines.push("【" + group.name + "】");
      group.items.forEach((item) => {
        lines.push((item.checked ? "✓ " : "· ") + item.name + "  " + (item.amount || ""));
      });
    });
    wx.setClipboardData({
      data: lines.join("\n"),
      success: () => wx.showToast({ title: "已复制清单", icon: "success" }),
    });
  },

  goPlan() {
    wx.switchTab({ url: "/pages/plan/plan" });
  },
});
