const config = require("../config/index");

const TOKEN_KEY = "fz_token";

function baseUrl() {
  return String(config.apiBaseUrl || "").replace(/\/$/, "");
}

function absolute(url) {
  if (!url) return url;
  if (/^https?:\/\//.test(url) || url.indexOf("wxfile://") === 0) return url;
  if (url.charAt(0) === "/") return baseUrl() + url;
  return url;
}

function getToken() {
  return wx.getStorageSync(TOKEN_KEY) || "";
}

function setToken(token) {
  wx.setStorageSync(TOKEN_KEY, token || "");
}

function request(path, options) {
  const opts = options || {};
  return new Promise((resolve, reject) => {
    wx.request({
      url: baseUrl() + path,
      method: opts.method || "GET",
      data: opts.data || {},
      timeout: config.requestTimeout || 8000,
      header: Object.assign(
        { "content-type": "application/json" },
        getToken() ? { Authorization: "Bearer " + getToken() } : {}
      ),
      success(res) {
        const body = res.data || {};
        if (res.statusCode === 401 && !opts.retried) {
          setToken("");
          login()
            .then(() => request(path, Object.assign({}, opts, { retried: true })))
            .then(resolve)
            .catch(reject);
          return;
        }
        if (res.statusCode >= 200 && res.statusCode < 300 && body.ok !== false) {
          resolve(body.data);
          return;
        }
        const message = (body.error && body.error.message) || body.detail || "网络开小差了";
        reject(new Error(message));
      },
      fail() {
        reject(new Error("连不上服务器，请检查接口地址"));
      },
    });
  });
}

function login() {
  return new Promise((resolve, reject) => {
    wx.login({
      success(res) {
        const devId = wx.getStorageSync("fz_dev_id") || "local-guest";
        wx.setStorageSync("fz_dev_id", devId);
        request("/api/auth/login", {
          method: "POST",
          data: { code: res.code || "", devOpenid: devId },
        })
          .then((data) => {
            setToken(data.token);
            resolve(data);
          })
          .catch(reject);
      },
      fail() {
        reject(new Error("微信登录失败"));
      },
    });
  });
}

function ensureLogin() {
  if (getToken()) return Promise.resolve();
  return login();
}

module.exports = {
  baseUrl,
  absolute,
  getToken,
  setToken,
  request,
  login,
  ensureLogin,
};
