module.exports = {
  "categories": [
    {
      "id": "quick",
      "name": "快手菜",
      "note": "二十分钟内上桌",
      "color": "tomato"
    },
    {
      "id": "home",
      "name": "家常菜",
      "note": "一锅一灶的熟悉味道",
      "color": "plum"
    },
    {
      "id": "soup",
      "name": "汤羹",
      "note": "小火慢慢煨",
      "color": "jade"
    },
    {
      "id": "staple",
      "name": "主食",
      "note": "面、饭、饺子",
      "color": "olive"
    },
    {
      "id": "breakfast",
      "name": "早餐",
      "note": "把早晨安顿好",
      "color": "mustard"
    }
  ],
  "meals": [
    {
      "id": "breakfast",
      "name": "早餐"
    },
    {
      "id": "lunch",
      "name": "午餐"
    },
    {
      "id": "dinner",
      "name": "晚餐"
    }
  ],
  "recipes": [
    {
      "id": 1,
      "slug": "tomato-egg",
      "title": "番茄炒蛋",
      "summary": "酸甜的汁水裹住嫩蛋，十分钟就能端上桌。",
      "category": "quick",
      "categoryName": "快手菜",
      "tags": [
        "十分钟",
        "家常",
        "下饭"
      ],
      "time": 12,
      "servings": 2,
      "difficulty": "容易",
      "cover": "/assets/covers/tomato-egg.jpg",
      "ingredients": [
        {
          "name": "番茄",
          "amount": 2,
          "unit": "个",
          "group": "蔬菜"
        },
        {
          "name": "鸡蛋",
          "amount": 3,
          "unit": "个",
          "group": "肉蛋"
        },
        {
          "name": "小葱",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "白糖",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "番茄洗净切滚刀块，小葱切末；鸡蛋加一小撮盐打散。"
        },
        {
          "text": "锅烧热，放一大勺油，倒入蛋液。边缘凝固后用铲子推散，盛出备用。",
          "tip": "蛋液刚凝固就盛出，回锅后还会再熟一点。"
        },
        {
          "text": "锅里补一小勺油，下番茄翻炒到出汁，加白糖和盐。"
        },
        {
          "text": "倒回鸡蛋，快速翻匀，撒葱花出锅。"
        }
      ],
      "tips": "番茄选熟一点的，汁水足，不用额外加水。"
    },
    {
      "id": 2,
      "slug": "garlic-broccoli",
      "title": "蒜蓉西兰花",
      "summary": "焯水后大火快炒，蒜香清亮，颜色也好看。",
      "category": "quick",
      "categoryName": "快手菜",
      "tags": [
        "清淡",
        "快手",
        "少油"
      ],
      "time": 15,
      "servings": 2,
      "difficulty": "容易",
      "cover": "/assets/covers/garlic-broccoli.jpg",
      "ingredients": [
        {
          "name": "西兰花",
          "amount": 1,
          "unit": "颗",
          "group": "蔬菜"
        },
        {
          "name": "大蒜",
          "amount": 4,
          "unit": "瓣",
          "group": "蔬菜"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "生抽",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "西兰花切成小朵，用清水冲净；大蒜拍碎切末。"
        },
        {
          "text": "水烧开，加半小勺盐和几滴油，西兰花焯 40 秒，捞出沥干。",
          "tip": "水里滴油，焯出来的颜色更绿。"
        },
        {
          "text": "锅烧热放油，下蒜末小火炒香，倒入西兰花大火翻炒。"
        },
        {
          "text": "加盐和生抽，翻匀即可出锅。"
        }
      ],
      "tips": "焯水时间别太久，后面还要回锅炒。"
    },
    {
      "id": 3,
      "slug": "potato-shreds",
      "title": "青椒土豆丝",
      "summary": "土豆丝先泡水，炒出来才脆爽不粘锅。",
      "category": "quick",
      "categoryName": "快手菜",
      "tags": [
        "下饭",
        "素菜",
        "脆爽"
      ],
      "time": 18,
      "servings": 2,
      "difficulty": "容易",
      "cover": "/assets/covers/potato-shreds.jpg",
      "ingredients": [
        {
          "name": "土豆",
          "amount": 2,
          "unit": "个",
          "group": "蔬菜"
        },
        {
          "name": "青椒",
          "amount": 1,
          "unit": "个",
          "group": "蔬菜"
        },
        {
          "name": "大蒜",
          "amount": 2,
          "unit": "瓣",
          "group": "蔬菜"
        },
        {
          "name": "白醋",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "土豆去皮切细丝，放进清水里泡 5 分钟，洗掉表面淀粉。"
        },
        {
          "text": "青椒去籽切丝，大蒜切末。"
        },
        {
          "text": "锅烧热放油，下蒜末炒香，倒入土豆丝大火翻炒 1 分钟。"
        },
        {
          "text": "加青椒丝、盐和白醋，再炒 1 分钟，断生就出锅。",
          "tip": "白醋沿锅边淋，酸香更明显。"
        }
      ],
      "tips": "土豆丝切得粗细一致，成熟时间才一致。"
    },
    {
      "id": 4,
      "slug": "cucumber-salad",
      "title": "凉拌黄瓜",
      "summary": "拍碎的黄瓜更容易入味，冰箱里拿出来就能吃。",
      "category": "quick",
      "categoryName": "快手菜",
      "tags": [
        "凉菜",
        "开胃",
        "零油烟"
      ],
      "time": 10,
      "servings": 2,
      "difficulty": "容易",
      "cover": "/assets/covers/cucumber-salad.jpg",
      "ingredients": [
        {
          "name": "黄瓜",
          "amount": 2,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "大蒜",
          "amount": 3,
          "unit": "瓣",
          "group": "蔬菜"
        },
        {
          "name": "香醋",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "生抽",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "香油",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "白糖",
          "amount": "半小勺",
          "unit": "",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "黄瓜洗净，用刀背拍裂，再切成小段。"
        },
        {
          "text": "大蒜切末，和香醋、生抽、香油、白糖调成料汁。"
        },
        {
          "text": "料汁倒进黄瓜里拌匀，放冰箱冷藏 5 分钟更入味。"
        }
      ],
      "tips": "黄瓜先拍后切，断面粗糙，挂汁更好。"
    },
    {
      "id": 5,
      "slug": "mushroom-greens",
      "title": "香菇青菜",
      "summary": "香菇的鲜味渗进青菜里，简单却不下饭桌。",
      "category": "quick",
      "categoryName": "快手菜",
      "tags": [
        "素菜",
        "清淡",
        "家常"
      ],
      "time": 15,
      "servings": 2,
      "difficulty": "容易",
      "cover": "/assets/covers/mushroom-greens.jpg",
      "ingredients": [
        {
          "name": "上海青",
          "amount": 4,
          "unit": "颗",
          "group": "蔬菜"
        },
        {
          "name": "鲜香菇",
          "amount": 6,
          "unit": "朵",
          "group": "蔬菜"
        },
        {
          "name": "大蒜",
          "amount": 2,
          "unit": "瓣",
          "group": "蔬菜"
        },
        {
          "name": "蚝油",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "上海青掰开洗净，香菇去蒂切片，大蒜切末。"
        },
        {
          "text": "锅烧热放油，下蒜末和香菇片，中火炒到香菇变软。"
        },
        {
          "text": "倒入上海青，大火翻炒到叶子塌下去。"
        },
        {
          "text": "加蚝油和盐，翻匀出锅。"
        }
      ],
      "tips": "香菇先下锅炒出香味，再放青菜，顺序别反。"
    },
    {
      "id": 6,
      "slug": "shrimp-egg",
      "title": "虾仁滑蛋",
      "summary": "虾仁弹、鸡蛋嫩，火候只在几十秒之间。",
      "category": "quick",
      "categoryName": "快手菜",
      "tags": [
        "高蛋白",
        "快手",
        "孩子爱吃"
      ],
      "time": 16,
      "servings": 2,
      "difficulty": "中等",
      "cover": "/assets/covers/shrimp-egg.jpg",
      "ingredients": [
        {
          "name": "虾仁",
          "amount": 150,
          "unit": "克",
          "group": "肉蛋"
        },
        {
          "name": "鸡蛋",
          "amount": 3,
          "unit": "个",
          "group": "肉蛋"
        },
        {
          "name": "小葱",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "料酒",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "虾仁加料酒和一小撮盐抓匀，腌 5 分钟；鸡蛋打散，小葱切末。"
        },
        {
          "text": "锅烧热放油，虾仁下锅炒到变色，盛出。"
        },
        {
          "text": "转中小火，倒入蛋液，等底部微微凝固后用铲子从边缘往中间推。"
        },
        {
          "text": "蛋液还有一点流动时倒回虾仁，撒葱花，翻两下就关火。",
          "tip": "关火后余温会继续把蛋焖熟。"
        }
      ],
      "tips": "全程中小火，火大了蛋会老。"
    },
    {
      "id": 7,
      "slug": "braised-pork",
      "title": "红烧肉",
      "summary": "慢慢收汁，肥肉透亮，瘦肉不柴，一锅能配两碗饭。",
      "category": "home",
      "categoryName": "家常菜",
      "tags": [
        "硬菜",
        "周末",
        "下饭"
      ],
      "time": 75,
      "servings": 4,
      "difficulty": "中等",
      "cover": "/assets/covers/braised-pork.jpg",
      "ingredients": [
        {
          "name": "五花肉",
          "amount": 600,
          "unit": "克",
          "group": "肉蛋"
        },
        {
          "name": "生姜",
          "amount": 4,
          "unit": "片",
          "group": "蔬菜"
        },
        {
          "name": "大葱",
          "amount": 1,
          "unit": "段",
          "group": "蔬菜"
        },
        {
          "name": "冰糖",
          "amount": 25,
          "unit": "克",
          "group": "调料"
        },
        {
          "name": "生抽",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "老抽",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "料酒",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "五花肉切 3 厘米见方的块，冷水下锅，加姜片和料酒焯 3 分钟，捞出洗净。"
        },
        {
          "text": "锅里放少量油和冰糖，小火炒到冰糖融化、变成琥珀色。"
        },
        {
          "text": "倒入肉块翻炒上色，加葱段、姜片、生抽和老抽。"
        },
        {
          "text": "加热水没过肉，大火烧开后转小火炖 50 分钟。",
          "tip": "一定加热水，冷水会让肉紧缩。"
        },
        {
          "text": "开大火收汁，汤汁浓稠挂在肉上就关火。"
        }
      ],
      "tips": "炒糖色宁浅勿深，发黑会发苦。"
    },
    {
      "id": 8,
      "slug": "cola-wings",
      "title": "可乐鸡翅",
      "summary": "不用炒糖色，靠可乐收出亮晶晶的酱汁。",
      "category": "home",
      "categoryName": "家常菜",
      "tags": [
        "下饭",
        "孩子爱吃",
        "零失败"
      ],
      "time": 35,
      "servings": 3,
      "difficulty": "容易",
      "cover": "/assets/covers/cola-wings.jpg",
      "ingredients": [
        {
          "name": "鸡中翅",
          "amount": 10,
          "unit": "只",
          "group": "肉蛋"
        },
        {
          "name": "可乐",
          "amount": 330,
          "unit": "毫升",
          "group": "其他"
        },
        {
          "name": "生姜",
          "amount": 3,
          "unit": "片",
          "group": "蔬菜"
        },
        {
          "name": "生抽",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "料酒",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "鸡翅两面各划一刀，冷水下锅焯水，捞出擦干。"
        },
        {
          "text": "锅里放少许油，鸡翅下锅煎到两面微黄。"
        },
        {
          "text": "加姜片、生抽、料酒和可乐，大火烧开。"
        },
        {
          "text": "转中小火焖 15 分钟，再开大火收汁，加盐调味。"
        }
      ],
      "tips": "可乐已经够甜，不用再放糖。"
    },
    {
      "id": 9,
      "slug": "fish-fragrant-pork",
      "title": "鱼香肉丝",
      "summary": "没有鱼，靠泡椒、糖醋和蒜姜调出复合的香味。",
      "category": "home",
      "categoryName": "家常菜",
      "tags": [
        "川味",
        "下饭",
        "家常"
      ],
      "time": 30,
      "servings": 3,
      "difficulty": "中等",
      "cover": "/assets/covers/fish-fragrant-pork.jpg",
      "ingredients": [
        {
          "name": "猪里脊",
          "amount": 250,
          "unit": "克",
          "group": "肉蛋"
        },
        {
          "name": "木耳",
          "amount": 6,
          "unit": "朵",
          "group": "蔬菜"
        },
        {
          "name": "胡萝卜",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "青椒",
          "amount": 1,
          "unit": "个",
          "group": "蔬菜"
        },
        {
          "name": "泡椒",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "香醋",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "白糖",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "生抽",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "淀粉",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "里脊切丝，加生抽、淀粉和一勺清水抓匀，腌 10 分钟。"
        },
        {
          "text": "木耳泡发切丝，胡萝卜和青椒切丝；香醋、白糖、生抽、淀粉加两勺水调成碗汁。"
        },
        {
          "text": "锅烧热多放一点油，肉丝下锅快速滑散，变色后盛出。"
        },
        {
          "text": "锅里留底油，下泡椒炒出红油，放木耳、胡萝卜和青椒翻炒。"
        },
        {
          "text": "倒回肉丝，淋入碗汁，大火翻匀收汁。"
        }
      ],
      "tips": "碗汁提前调好，最后一步才不会手忙脚乱。"
    },
    {
      "id": 10,
      "slug": "mapo-tofu",
      "title": "麻婆豆腐",
      "summary": "豆腐嫩、肉末香，花椒的麻在最后撒下去。",
      "category": "home",
      "categoryName": "家常菜",
      "tags": [
        "川味",
        "下饭",
        "豆腐"
      ],
      "time": 25,
      "servings": 3,
      "difficulty": "中等",
      "cover": "/assets/covers/mapo-tofu.jpg",
      "ingredients": [
        {
          "name": "嫩豆腐",
          "amount": 400,
          "unit": "克",
          "group": "其他"
        },
        {
          "name": "猪肉末",
          "amount": 100,
          "unit": "克",
          "group": "肉蛋"
        },
        {
          "name": "豆瓣酱",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "花椒粉",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "大蒜",
          "amount": 3,
          "unit": "瓣",
          "group": "蔬菜"
        },
        {
          "name": "小葱",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "淀粉",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "豆腐切 2 厘米方块，放进淡盐水里泡 5 分钟，捞出沥干。"
        },
        {
          "text": "锅烧热放油，肉末下锅炒散，加蒜末和豆瓣酱炒出红油。"
        },
        {
          "text": "加一小碗水烧开，轻轻推入豆腐，中小火煮 5 分钟。"
        },
        {
          "text": "淀粉加水调匀，分两次淋入锅里，轻推收汁。"
        },
        {
          "text": "出锅撒葱花和花椒粉。"
        }
      ],
      "tips": "用铲子背面推豆腐，别来回翻，块才不容易碎。"
    },
    {
      "id": 11,
      "slug": "beef-potato-stew",
      "title": "土豆炖牛腩",
      "summary": "牛腩炖到软烂，土豆吸饱汤汁，适合冷天。",
      "category": "home",
      "categoryName": "家常菜",
      "tags": [
        "炖菜",
        "周末",
        "暖胃"
      ],
      "time": 100,
      "servings": 4,
      "difficulty": "中等",
      "cover": "/assets/covers/beef-potato-stew.jpg",
      "ingredients": [
        {
          "name": "牛腩",
          "amount": 700,
          "unit": "克",
          "group": "肉蛋"
        },
        {
          "name": "土豆",
          "amount": 3,
          "unit": "个",
          "group": "蔬菜"
        },
        {
          "name": "胡萝卜",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "洋葱",
          "amount": 1,
          "unit": "个",
          "group": "蔬菜"
        },
        {
          "name": "生姜",
          "amount": 4,
          "unit": "片",
          "group": "蔬菜"
        },
        {
          "name": "八角",
          "amount": 2,
          "unit": "颗",
          "group": "调料"
        },
        {
          "name": "生抽",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "料酒",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "牛腩切块，冷水下锅焯水，撇去浮沫后捞出。"
        },
        {
          "text": "锅里放油，洋葱和姜片炒香，倒入牛腩翻炒。"
        },
        {
          "text": "加料酒、生抽和八角，添热水没过牛腩，小火炖 60 分钟。"
        },
        {
          "text": "土豆和胡萝卜切块，放进锅里再炖 25 分钟。"
        },
        {
          "text": "加盐调味，开大火收一收汤汁。"
        }
      ],
      "tips": "土豆晚点放，炖太久会化在汤里。"
    },
    {
      "id": 12,
      "slug": "steamed-fish",
      "title": "清蒸鲈鱼",
      "summary": "一条鱼、几片姜，蒸好后淋一勺热油，鲜味就出来了。",
      "category": "home",
      "categoryName": "家常菜",
      "tags": [
        "清淡",
        "宴客",
        "高蛋白"
      ],
      "time": 30,
      "servings": 3,
      "difficulty": "中等",
      "cover": "/assets/covers/steamed-fish.jpg",
      "ingredients": [
        {
          "name": "鲈鱼",
          "amount": 1,
          "unit": "条",
          "group": "肉蛋"
        },
        {
          "name": "生姜",
          "amount": 5,
          "unit": "片",
          "group": "蔬菜"
        },
        {
          "name": "小葱",
          "amount": 2,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "蒸鱼豉油",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "料酒",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "鲈鱼处理干净，两面各划两刀，抹上料酒，鱼腹里塞两片姜。"
        },
        {
          "text": "盘底铺葱段和姜片，放上鱼，水开后上锅蒸 8 分钟。",
          "tip": "鱼眼凸出、鱼肉刚能离骨，就是熟了。"
        },
        {
          "text": "倒掉盘里的水，拣掉旧葱姜，铺上新的葱丝。"
        },
        {
          "text": "淋蒸鱼豉油，再浇一勺烧到冒烟的热油。"
        }
      ],
      "tips": "蒸鱼的水一定要先烧开，再放鱼。"
    },
    {
      "id": 13,
      "slug": "tomato-egg-soup",
      "title": "番茄蛋花汤",
      "summary": "十分钟的一碗热汤，蛋花要细，番茄要炒出沙。",
      "category": "soup",
      "categoryName": "汤羹",
      "tags": [
        "快手",
        "暖胃",
        "清淡"
      ],
      "time": 12,
      "servings": 3,
      "difficulty": "容易",
      "cover": "/assets/covers/tomato-egg-soup.jpg",
      "ingredients": [
        {
          "name": "番茄",
          "amount": 2,
          "unit": "个",
          "group": "蔬菜"
        },
        {
          "name": "鸡蛋",
          "amount": 2,
          "unit": "个",
          "group": "肉蛋"
        },
        {
          "name": "小葱",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "香油",
          "amount": "几滴",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "番茄切小块，鸡蛋打散，小葱切末。"
        },
        {
          "text": "锅里放少许油，番茄下锅炒到出沙，加两碗水烧开。"
        },
        {
          "text": "转小火，蛋液沿筷子慢慢淋进锅里，停两秒再轻轻推动。"
        },
        {
          "text": "加盐，关火，撒葱花，滴几滴香油。"
        }
      ],
      "tips": "蛋液淋下去别马上搅，蛋花才成片。"
    },
    {
      "id": 14,
      "slug": "winter-melon-ribs",
      "title": "冬瓜排骨汤",
      "summary": "排骨先焯水，冬瓜后下锅，汤清不浑浊。",
      "category": "soup",
      "categoryName": "汤羹",
      "tags": [
        "清淡",
        "汤",
        "夏天"
      ],
      "time": 70,
      "servings": 4,
      "difficulty": "容易",
      "cover": "/assets/covers/winter-melon-ribs.jpg",
      "ingredients": [
        {
          "name": "排骨",
          "amount": 500,
          "unit": "克",
          "group": "肉蛋"
        },
        {
          "name": "冬瓜",
          "amount": 500,
          "unit": "克",
          "group": "蔬菜"
        },
        {
          "name": "生姜",
          "amount": 4,
          "unit": "片",
          "group": "蔬菜"
        },
        {
          "name": "小葱",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "料酒",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "排骨冷水下锅，加姜片和料酒，焯水后洗净。"
        },
        {
          "text": "排骨放进汤锅，加足量热水和姜片，大火烧开转小火炖 40 分钟。"
        },
        {
          "text": "冬瓜去皮切厚片，放进锅里再煮 15 分钟。"
        },
        {
          "text": "加盐调味，撒葱花。"
        }
      ],
      "tips": "冬瓜皮别削太深，靠近皮的一层最清甜。"
    },
    {
      "id": 15,
      "slug": "seaweed-egg-soup",
      "title": "紫菜蛋花汤",
      "summary": "五分钟能做好的一碗汤，紫菜和虾皮自带鲜味。",
      "category": "soup",
      "categoryName": "汤羹",
      "tags": [
        "快手",
        "清淡",
        "零失败"
      ],
      "time": 8,
      "servings": 2,
      "difficulty": "容易",
      "cover": "/assets/covers/seaweed-egg-soup.jpg",
      "ingredients": [
        {
          "name": "紫菜",
          "amount": 1,
          "unit": "小把",
          "group": "其他"
        },
        {
          "name": "鸡蛋",
          "amount": 2,
          "unit": "个",
          "group": "肉蛋"
        },
        {
          "name": "虾皮",
          "amount": 1,
          "unit": "小把",
          "group": "其他"
        },
        {
          "name": "小葱",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "香油",
          "amount": "几滴",
          "unit": "",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "紫菜撕小片，鸡蛋打散，小葱切末。"
        },
        {
          "text": "锅里加两碗水烧开，放虾皮和紫菜煮 1 分钟。"
        },
        {
          "text": "转小火淋入蛋液，加盐，关火后滴香油、撒葱花。"
        }
      ],
      "tips": "紫菜本身有咸味，盐先少放，尝过再补。"
    },
    {
      "id": 16,
      "slug": "corn-ribs-soup",
      "title": "玉米排骨汤",
      "summary": "玉米和胡萝卜把汤熬出自然的甜，不用放糖。",
      "category": "soup",
      "categoryName": "汤羹",
      "tags": [
        "清甜",
        "汤",
        "孩子爱喝"
      ],
      "time": 80,
      "servings": 4,
      "difficulty": "容易",
      "cover": "/assets/covers/corn-ribs-soup.jpg",
      "ingredients": [
        {
          "name": "排骨",
          "amount": 500,
          "unit": "克",
          "group": "肉蛋"
        },
        {
          "name": "甜玉米",
          "amount": 2,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "胡萝卜",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "生姜",
          "amount": 4,
          "unit": "片",
          "group": "蔬菜"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "排骨冷水下锅焯水，捞出洗净。"
        },
        {
          "text": "玉米切段，胡萝卜切滚刀块。"
        },
        {
          "text": "排骨、姜片和足量热水放进汤锅，小火炖 40 分钟。"
        },
        {
          "text": "加玉米和胡萝卜，再炖 25 分钟，加盐调味。"
        }
      ],
      "tips": "玉米须洗干净可以一起煮，汤更清甜。"
    },
    {
      "id": 17,
      "slug": "pear-snow-fungus",
      "title": "银耳雪梨羹",
      "summary": "银耳炖到出胶，雪梨最后放，口感才不烂。",
      "category": "soup",
      "categoryName": "汤羹",
      "tags": [
        "甜品",
        "润燥",
        "秋冬"
      ],
      "time": 90,
      "servings": 4,
      "difficulty": "容易",
      "cover": "/assets/covers/pear-snow-fungus.jpg",
      "ingredients": [
        {
          "name": "干银耳",
          "amount": 1,
          "unit": "朵",
          "group": "其他"
        },
        {
          "name": "雪梨",
          "amount": 2,
          "unit": "个",
          "group": "蔬菜"
        },
        {
          "name": "冰糖",
          "amount": 30,
          "unit": "克",
          "group": "调料"
        },
        {
          "name": "枸杞",
          "amount": 1,
          "unit": "小把",
          "group": "其他"
        },
        {
          "name": "清水",
          "amount": 1200,
          "unit": "毫升",
          "group": "其他"
        }
      ],
      "steps": [
        {
          "text": "银耳提前用冷水泡 2 小时，去根撕小朵。"
        },
        {
          "text": "银耳和清水放进锅里，大火烧开转小火炖 60 分钟。"
        },
        {
          "text": "雪梨去核切块，和冰糖一起下锅，再炖 20 分钟。"
        },
        {
          "text": "出锅前放枸杞，焖 5 分钟。"
        }
      ],
      "tips": "银耳撕得越小，越容易出胶。"
    },
    {
      "id": 18,
      "slug": "scallion-noodles",
      "title": "葱油拌面",
      "summary": "葱油一次多熬一点，拌面、拌饭都香。",
      "category": "staple",
      "categoryName": "主食",
      "tags": [
        "面食",
        "上海味",
        "快手"
      ],
      "time": 25,
      "servings": 2,
      "difficulty": "中等",
      "cover": "/assets/covers/scallion-noodles.jpg",
      "ingredients": [
        {
          "name": "细面条",
          "amount": 200,
          "unit": "克",
          "group": "主食"
        },
        {
          "name": "小葱",
          "amount": 8,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "生抽",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "老抽",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "白糖",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 4,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "小葱洗净擦干，切成 5 厘米长段。"
        },
        {
          "text": "冷油下葱段，小火慢慢熬到葱叶焦黄，捞出葱段。"
        },
        {
          "text": "葱油里加生抽、老抽和白糖，小火煮到糖化开。"
        },
        {
          "text": "面条煮熟捞出，淋两勺葱油酱汁，拌匀后放上葱段。"
        }
      ],
      "tips": "熬葱油全程小火，葱香才出得来。"
    },
    {
      "id": 19,
      "slug": "egg-fried-rice",
      "title": "蛋炒饭",
      "summary": "隔夜饭打散，鸡蛋先炒后拌，粒粒分明。",
      "category": "staple",
      "categoryName": "主食",
      "tags": [
        "快手",
        "剩饭",
        "一人食"
      ],
      "time": 15,
      "servings": 2,
      "difficulty": "容易",
      "cover": "/assets/covers/egg-fried-rice.jpg",
      "ingredients": [
        {
          "name": "隔夜米饭",
          "amount": 2,
          "unit": "碗",
          "group": "主食"
        },
        {
          "name": "鸡蛋",
          "amount": 2,
          "unit": "个",
          "group": "肉蛋"
        },
        {
          "name": "小葱",
          "amount": 2,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "胡萝卜",
          "amount": "半根",
          "unit": "",
          "group": "蔬菜"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "生抽",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "米饭提前用手抓散；鸡蛋打散，胡萝卜切小丁，小葱切末。"
        },
        {
          "text": "锅烧热放油，倒蛋液炒到半凝固，盛出。"
        },
        {
          "text": "锅里补油，下胡萝卜丁炒软，倒入米饭大火翻炒。"
        },
        {
          "text": "米饭炒散后倒回鸡蛋，加盐和生抽，撒葱花翻匀。"
        }
      ],
      "tips": "米饭太湿就提前摊开晾十分钟。"
    },
    {
      "id": 20,
      "slug": "pork-cabbage-dumplings",
      "title": "猪肉白菜饺子",
      "summary": "白菜先杀水，肉馅顺一个方向搅，包出来才抱团。",
      "category": "staple",
      "categoryName": "主食",
      "tags": [
        "面食",
        "周末",
        "全家一起"
      ],
      "time": 90,
      "servings": 4,
      "difficulty": "中等",
      "cover": "/assets/covers/pork-cabbage-dumplings.jpg",
      "ingredients": [
        {
          "name": "饺子皮",
          "amount": 500,
          "unit": "克",
          "group": "主食"
        },
        {
          "name": "猪肉末",
          "amount": 400,
          "unit": "克",
          "group": "肉蛋"
        },
        {
          "name": "大白菜",
          "amount": 600,
          "unit": "克",
          "group": "蔬菜"
        },
        {
          "name": "小葱",
          "amount": 3,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "生姜",
          "amount": 1,
          "unit": "块",
          "group": "蔬菜"
        },
        {
          "name": "生抽",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "香油",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "白菜切碎，加一小勺盐拌匀，静置 15 分钟，挤干水分。"
        },
        {
          "text": "肉末加姜末、生抽和盐，顺一个方向搅到发黏。"
        },
        {
          "text": "拌入白菜、葱花和香油，馅料调好。"
        },
        {
          "text": "取饺子皮包馅，边缘捏紧。"
        },
        {
          "text": "水开下饺子，点两次凉水，饺子浮起后再煮 1 分钟。"
        }
      ],
      "tips": "白菜水挤得越干，饺子越不容易破。"
    },
    {
      "id": 21,
      "slug": "pumpkin-congee",
      "title": "南瓜粥",
      "summary": "南瓜蒸软后压进粥里，颜色金黄，口感绵密。",
      "category": "staple",
      "categoryName": "主食",
      "tags": [
        "早餐",
        "养胃",
        "孩子爱吃"
      ],
      "time": 40,
      "servings": 3,
      "difficulty": "容易",
      "cover": "/assets/covers/pumpkin-congee.jpg",
      "ingredients": [
        {
          "name": "南瓜",
          "amount": 300,
          "unit": "克",
          "group": "蔬菜"
        },
        {
          "name": "大米",
          "amount": 80,
          "unit": "克",
          "group": "主食"
        },
        {
          "name": "清水",
          "amount": 1000,
          "unit": "毫升",
          "group": "其他"
        }
      ],
      "steps": [
        {
          "text": "大米淘洗后浸泡 20 分钟；南瓜去皮切小块。"
        },
        {
          "text": "大米和清水放进锅里，大火烧开转小火煮 20 分钟。"
        },
        {
          "text": "加入南瓜块，继续煮 10 分钟。"
        },
        {
          "text": "用勺子把南瓜压碎，搅匀再煮 2 分钟。"
        }
      ],
      "tips": "南瓜本身甜，不用加糖。"
    },
    {
      "id": 22,
      "slug": "tomato-bolognese",
      "title": "番茄肉酱意面",
      "summary": "肉酱多熬十分钟，番茄的酸味会变得柔和。",
      "category": "staple",
      "categoryName": "主食",
      "tags": [
        "西式",
        "一人食",
        "周末"
      ],
      "time": 40,
      "servings": 2,
      "difficulty": "中等",
      "cover": "/assets/covers/tomato-bolognese.jpg",
      "ingredients": [
        {
          "name": "意大利面",
          "amount": 200,
          "unit": "克",
          "group": "主食"
        },
        {
          "name": "牛肉末",
          "amount": 200,
          "unit": "克",
          "group": "肉蛋"
        },
        {
          "name": "番茄",
          "amount": 2,
          "unit": "个",
          "group": "蔬菜"
        },
        {
          "name": "洋葱",
          "amount": "半个",
          "unit": "",
          "group": "蔬菜"
        },
        {
          "name": "大蒜",
          "amount": 3,
          "unit": "瓣",
          "group": "蔬菜"
        },
        {
          "name": "番茄酱",
          "amount": 2,
          "unit": "大勺",
          "group": "调料"
        },
        {
          "name": "盐",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "黑胡椒",
          "amount": "适量",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 1,
          "unit": "大勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "洋葱和大蒜切末，番茄切小丁。"
        },
        {
          "text": "锅里放油，洋葱和蒜末炒香，下牛肉末炒散。"
        },
        {
          "text": "加番茄丁和番茄酱，中小火熬 15 分钟，用盐和黑胡椒调味。"
        },
        {
          "text": "意面按包装时间煮熟，捞出留半碗面汤。"
        },
        {
          "text": "意面放进肉酱里，加两勺面汤拌匀，让酱汁挂住面条。"
        }
      ],
      "tips": "面汤里有淀粉，是让酱汁浓稠的关键。"
    },
    {
      "id": 23,
      "slug": "millet-porridge",
      "title": "小米粥配水煮蛋",
      "summary": "小米粥熬出米油，配一颗刚刚凝固的水煮蛋。",
      "category": "breakfast",
      "categoryName": "早餐",
      "tags": [
        "早餐",
        "养胃",
        "简单"
      ],
      "time": 35,
      "servings": 2,
      "difficulty": "容易",
      "cover": "/assets/covers/millet-porridge.jpg",
      "ingredients": [
        {
          "name": "小米",
          "amount": 80,
          "unit": "克",
          "group": "主食"
        },
        {
          "name": "鸡蛋",
          "amount": 2,
          "unit": "个",
          "group": "肉蛋"
        },
        {
          "name": "清水",
          "amount": 900,
          "unit": "毫升",
          "group": "其他"
        },
        {
          "name": "盐",
          "amount": "少许",
          "unit": "",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "小米淘洗两遍，冷水浸泡 10 分钟。"
        },
        {
          "text": "水烧开，倒入小米，大火煮开后转小火。"
        },
        {
          "text": "保持微沸煮 25 分钟，中途搅动两次，防止粘底。"
        },
        {
          "text": "鸡蛋冷水下锅，水开后煮 7 分钟，过凉水剥壳。"
        }
      ],
      "tips": "小米下锅前水一定要开，粥才容易出米油。"
    },
    {
      "id": 24,
      "slug": "ham-sandwich",
      "title": "火腿蛋三明治",
      "summary": "吐司烤脆，鸡蛋煎到半熟，五分钟装进包里带走。",
      "category": "breakfast",
      "categoryName": "早餐",
      "tags": [
        "早餐",
        "带走",
        "快手"
      ],
      "time": 10,
      "servings": 1,
      "difficulty": "容易",
      "cover": "/assets/covers/ham-sandwich.jpg",
      "ingredients": [
        {
          "name": "吐司",
          "amount": 2,
          "unit": "片",
          "group": "主食"
        },
        {
          "name": "鸡蛋",
          "amount": 1,
          "unit": "个",
          "group": "肉蛋"
        },
        {
          "name": "火腿片",
          "amount": 2,
          "unit": "片",
          "group": "肉蛋"
        },
        {
          "name": "生菜",
          "amount": 2,
          "unit": "片",
          "group": "蔬菜"
        },
        {
          "name": "沙拉酱",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "食用油",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "吐司放进平底锅，小火烘到两面微脆。"
        },
        {
          "text": "锅里放油，煎一个鸡蛋，火腿片也煎一下。"
        },
        {
          "text": "吐司抹沙拉酱，依次放生菜、火腿和鸡蛋。"
        },
        {
          "text": "盖上另一片吐司，压紧后对角切开。"
        }
      ],
      "tips": "生菜洗净后用厨房纸吸干水，吐司才不会软。"
    },
    {
      "id": 25,
      "slug": "oatmeal-cup",
      "title": "燕麦牛奶杯",
      "summary": "前一晚拌好放冰箱，早上拿起就能走。",
      "category": "breakfast",
      "categoryName": "早餐",
      "tags": [
        "早餐",
        "免煮",
        "带走"
      ],
      "time": 5,
      "servings": 1,
      "difficulty": "容易",
      "cover": "/assets/covers/oatmeal-cup.jpg",
      "ingredients": [
        {
          "name": "即食燕麦",
          "amount": 50,
          "unit": "克",
          "group": "主食"
        },
        {
          "name": "牛奶",
          "amount": 200,
          "unit": "毫升",
          "group": "其他"
        },
        {
          "name": "香蕉",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "蜂蜜",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "坚果",
          "amount": 1,
          "unit": "小把",
          "group": "其他"
        }
      ],
      "steps": [
        {
          "text": "燕麦和牛奶放进带盖的杯子，搅匀。"
        },
        {
          "text": "香蕉切片铺在上面，淋蜂蜜，撒坚果。"
        },
        {
          "text": "盖好放冰箱冷藏一夜，第二天直接吃。"
        }
      ],
      "tips": "用厚一点的燕麦，泡一夜口感更好。"
    },
    {
      "id": 26,
      "slug": "steamed-egg-custard",
      "title": "蒸蛋羹",
      "summary": "蛋液和温水按 1:1.5 调，蒸出来像布丁一样嫩。",
      "category": "breakfast",
      "categoryName": "早餐",
      "tags": [
        "早餐",
        "孩子爱吃",
        "清淡"
      ],
      "time": 18,
      "servings": 2,
      "difficulty": "容易",
      "cover": "/assets/covers/steamed-egg-custard.jpg",
      "ingredients": [
        {
          "name": "鸡蛋",
          "amount": 2,
          "unit": "个",
          "group": "肉蛋"
        },
        {
          "name": "温水",
          "amount": 150,
          "unit": "毫升",
          "group": "其他"
        },
        {
          "name": "生抽",
          "amount": 1,
          "unit": "小勺",
          "group": "调料"
        },
        {
          "name": "香油",
          "amount": "几滴",
          "unit": "",
          "group": "调料"
        },
        {
          "name": "小葱",
          "amount": 1,
          "unit": "根",
          "group": "蔬菜"
        },
        {
          "name": "盐",
          "amount": "少许",
          "unit": "",
          "group": "调料"
        }
      ],
      "steps": [
        {
          "text": "鸡蛋加盐打散，倒入温水搅匀。"
        },
        {
          "text": "蛋液过筛两遍，倒进碗里，撇掉表面气泡。"
        },
        {
          "text": "碗上盖盘子，水开后中小火蒸 10 分钟。"
        },
        {
          "text": "出锅淋生抽和香油，撒葱花。"
        }
      ],
      "tips": "盖住碗口，水蒸气滴下来就不会有蜂窝。"
    }
  ]
};
