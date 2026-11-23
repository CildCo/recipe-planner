# 饭桌 · 菜谱、一周菜单与买菜清单

一个小程序 + FastAPI 后端 + 管理后台的完整成品。把菜谱排进一周菜单，自动合并食材生成买菜清单；家人用邀请码加入同一张饭桌。

代码、界面、示例菜谱均为独立实现。示例菜谱用于演示，正式使用时请换成自己的内容。

## 功能

- **菜谱**：分类、搜索、标签、食材、步骤、小提示、收藏；
- **一周菜单**：周一为一周开始，早/午/晚都能放多道菜，支持复制上周；
- **买菜清单**：按菜单合并同类食材，同单位自动相加；可勾选、手动添加、复制文本；
- **家庭共享**：6 位邀请码加入同一张饭桌，共用菜单和清单；
- **管理后台**：菜谱增删改查、封面上传、饭桌与成员、清单导出 CSV、站点设置；
- **两种运行模式**：小程序默认本地演示（不连后端也能点），也可以切到真实接口；
- **开箱数据**：26 道原创示例菜谱、26 张 1200×900 插画封面、初始菜单和清单。

## 快速开始

```bash
python -m pip install -r requirements.txt
python start.py
```

打开 <http://127.0.0.1:8020/admin>。

- 管理员账号默认 `admin`；
- 首次启动的密码在 `backend/runtime/admin-password.txt`；
- 也可以在 `backend/.env` 里设置 `ADMIN_PASSWORD`；
- 小程序接口在 <http://127.0.0.1:8020/api>。

跑全量检查：

```bash
python run_all.py
```

它会生成封面、导出小程序数据、检查内容，并跑后端测试。

## 小程序

用微信开发者工具打开 `miniprogram/`。

默认 `config/index.js` 里是：

```js
mode: "mock",
apiBaseUrl: "http://127.0.0.1:8020"
```

- `mock`：使用本地 26 道菜和 `wx.storage`，不依赖后端，适合先看界面；
- `server`：调用 FastAPI，需要后端已启动；开发者工具里勾选“不校验合法域名”。

首次用 `mock` 会写入一份示例菜单、清单和收藏。想恢复初始状态：我的 → 重置演示数据。

正式发布前，把 `project.config.json` 的 `appid` 换成自己的小程序 AppID，把 `apiBaseUrl` 换成 HTTPS 域名。

## 管理后台

| 页面 | 用途 |
|---|---|
| 总览 | 本周安排、今日菜单、清单进度、分类结构 |
| 菜谱 | 搜索、筛选、发布/下架、编辑、删除、导出 JSON |
| 新建/编辑菜谱 | 基本信息、封面（上传自动裁成 1200×900）、食材、步骤、小提示 |
| 饭桌 | 成员、邀请码、每周菜单、清单进度 |
| 买菜清单 | 按周查看、勾选、手动添加、重新生成、导出 CSV |
| 设置 | 站点名字、一句话、介绍、默认人份 |
| 使用说明 | 本地运行、连小程序、上线前检查 |

## 目录

```text
source/
├── start.py                 启动后端
├── run_all.py               全量检查
├── requirements.txt
├── backend/
│   ├── app/
│   │   ├── main.py          FastAPI 入口
│   │   ├── models.py        Recipe / Household / PlanItem / ShoppingItem
│   │   ├── api/routes.py    小程序接口
│   │   ├── admin/routes.py  管理后台
│   │   ├── services/        菜单、清单、序列化
│   │   ├── templates/       后台页面
│   │   ├── static/          后台样式、封面
│   │   └── data/recipes.json 示例菜谱
│   ├── tests/               pytest
│   ├── uploads/             后台上传的封面
│   └── runtime/             首次启动生成的密码和密钥
├── miniprogram/
│   ├── pages/               今天、菜单、清单、我的、菜谱、详情、饭桌、收藏、关于
│   ├── components/          菜谱卡、空状态
│   ├── services/            api / store
│   ├── utils/               日期、餐次、食材合并
│   ├── data/                导出的本地演示数据
│   └── assets/              封面、tabBar 图标
├── tools/                   生成封面、导出数据、内容检查
└── docs/DEPLOY.md           部署说明
```

## 数据

- 菜谱的用量写数字（如 `2` + `个`），生成清单时会按人份缩放并相加；
- 写“适量”“半个”这类文字也可以，会原样保留；
- 食材分类固定为：蔬菜、肉蛋、主食、调料、其他；
- 一周从周一开始；
- 同一张饭桌的成员共享菜单和清单。

## 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/auth/login` | 微信 code 登录；开发环境可用 `devOpenid` |
| GET | `/api/site` | 站点信息、分类、餐次 |
| GET | `/api/recipes` | 菜谱列表，支持 `category`、`q` |
| GET | `/api/recipes/{id}` | 菜谱详情 |
| GET | `/api/plan?week=` | 一周菜单 |
| POST | `/api/plan/items` | 加入菜单 |
| DELETE | `/api/plan/items/{id}` | 移出菜单 |
| POST | `/api/plan/copy` | 复制一周 |
| GET | `/api/shopping?week=` | 买菜清单 |
| POST | `/api/shopping/generate` | 重新生成 |
| PATCH | `/api/shopping/{id}` | 勾选/取消 |
| POST | `/api/shopping/items` | 手动添加 |
| GET | `/api/favorites` | 收藏列表 |
| POST | `/api/recipes/{id}/favorite` | 收藏/取消 |
| GET | `/api/household` | 当前饭桌 |
| POST | `/api/household/create` | 新建饭桌 |
| POST | `/api/household/join` | 邀请码加入 |

接口统一返回 `{"ok": true, "data": ...}` 或 `{"ok": false, "error": {...}}`。

## 配置

复制 `.env.example` 为 `backend/.env`：

```text
APP_ENV=production
ADMIN_USER=admin
ADMIN_PASSWORD="请替换"
SECRET_KEY=换成随机字符串
WECHAT_APPID=小程序 AppID
WECHAT_SECRET=小程序 AppSecret
ALLOW_DEV_LOGIN=0
DATABASE_URL=mysql+pymysql://user:password@127.0.0.1:3306/fanzhuo
```

不配置微信凭证时，开发环境会用 `devOpenid` 模拟登录；生产环境请关掉 `ALLOW_DEV_LOGIN`。

## 常见问题

**小程序打开是空白或没有数据？**  
默认是 `mock` 模式，数据在 `miniprogram/data/recipes.js`。如果刚改过菜谱，运行 `python tools/export-mini-data.py`。

**改了后台菜谱，小程序没变？**  
`mock` 模式读本地数据；切到 `server` 模式并启动后端，小程序下拉刷新。

**封面被裁了？**  
后台统一裁成 1200×900（4:3）。主体放中间，四周留一点空间。

**邀请码在哪里？**  
小程序“我的”或“饭桌与成员”页面；后台“饭桌”列表也能看到。

**能商用吗？**  
代码 MIT。示例菜谱和插画可以一起用，正式上线前建议换成自己的菜谱内容。

## 许可

MIT，见 `LICENSE.md`。第三方库许可见 `PROVENANCE.md`。
