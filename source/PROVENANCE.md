# 来源与示例说明

## 需求参考

- 菜谱 / 周计划 / 买菜清单的产品形态参考了 Mealie、longshu-canteen 等公开项目，只用于确认功能边界和常见问题。
- 没有复制上述项目的代码、数据结构、界面、文案或示例数据。

## 独立实现

- 后端：FastAPI + SQLModel + SQLite，接口、数据模型、菜单合并、清单聚合、周计算均为自己编写。
- 管理后台：Jinja 模板 + 原生 CSS/JS，版式、交互、文案自行设计。
- 小程序：原生小程序，页面、组件、样式、交互自行设计。
- 示例菜谱：26 道家常菜的食材和步骤为示例中文描述，不取自菜谱网站或受版权保护的数据库。
- 封面插画：由 `tools/make-assets.py` 用 Pillow 绘制，包含盘子、锅、碗、食材等几何图形，不使用外部图片。
- tabBar 图标：同一脚本绘制。

## 第三方依赖

| 依赖 | 许可 |
|---|---|
| FastAPI | MIT |
| Starlette | BSD-3-Clause |
| SQLModel | MIT |
| SQLAlchemy | MIT |
| Jinja2 | BSD-3-Clause |
| Pillow | HPND |
| Uvicorn | BSD-3-Clause |
| pytest | MIT |

## 字体

封面生成使用本机 Noto Serif SC / Noto Sans SC 渲染文字，生成的图片随源码附带；没有打包字体文件。小程序和后台使用系统字体栈。

## 内容提醒

示例菜谱只用于演示排版和功能，不构成饮食、营养或食品安全建议。正式运营时请替换为自己的菜谱，并确认图片、文字和数据的授权。
