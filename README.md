# WeChat Public Account Topics Skill

微信公众号选题与内容生成 AgentSkill，支持热点收集、选题生成、文章发布自动化。

## 功能

- ✅ 热点新闻收集（虎嗅、36氪）
- ✅ 结合公众号定位生成多角度选题
- ✅ 参考 582 篇历史文章生成内容
- ✅ 输出完整文章 + 视频脚本
- ✅ 自动化发布到微信草稿箱
- ✅ 数据库表同步脚本

## 触发词

- 公众号选题
- 热点选题
- 生成文章
- 热点文章
- 视频脚本
- 选题简报
- 发布公众号

## 账号矩阵

| 账号 | 定位 | 受众 | 历史文章 |
|------|------|------|----------|
| 码农世界 CodePanda | 程序员/技术 | 开发者 | 467篇 |
| 旧青年 | 情怀/生活 | 文艺青年 | 110篇 |
| 北漂答卷人 | 北漂/奋斗 | 打工人 | 5篇 |

## 安装

```bash
# 克隆仓库
git clone https://github.com/tangpanpan23/wechat-public-account-topics.git

# 放置到 skills 目录
cp -r wechat-public-account-topics ~/.openclaw/skills/
```

## 使用

```
用户: 帮我生成今日热点选题
→ Skill 自动收集热点
→ 匹配账号定位
→ 输出差异化选题
```

## 项目结构

```
wechat-public-account-topics/
├── SKILL.md                      # Skill 主文件
├── references/
│   ├── accounts.md               # 账号矩阵
│   ├── templates.md             # 内容模板
│   └── articles/                 # 历史文章库
│       ├── README.md            # 文章索引
│       ├── codepanda/          # 467篇
│       ├── oldyouth/           # 110篇
│       └── dreamers/            # 5篇
└── scripts/                     # 自动化脚本
    ├── README.md                # 脚本说明
    ├── wechat-publisher.py      # 公众号发布
    └── db-sync.sh               # 数据库同步
```

## 自动化脚本

### 公众号发布 (wechat-publisher.py)

```bash
# 安装依赖
pip3 install requests

# 运行
python3 scripts/wechat-publisher.py

# 指定文章
python3 scripts/wechat-publisher.py --article /path/to/article.md
```

### 数据库同步 (db-sync.sh)

```bash
export SOURCE_PASS='test_password'
export TARGET_PASS='local_password'
./scripts/db-sync.sh --dry-run
./scripts/db-sync.sh
```

## License

MIT
