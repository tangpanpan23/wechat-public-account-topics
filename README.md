# WeChat Public Account Topics Skill

微信公众号选题与内容生成 AgentSkill。

当需要为公众号创作内容、结合热点新闻生成选题、制作公众号文章或视频脚本时使用。

## 功能

- 热点新闻收集与分析（虎嗅、36氪）
- 结合公众号定位生成多角度选题
- 参考历史文章生成内容
- 输出完整文章/视频脚本
- 发送选题简报到飞书群

## 触发词

- 公众号选题
- 热点选题
- 生成文章
- 热点文章
- 视频脚本
- 选题简报

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

## 项目结构

```
wechat-public-account-topics/
├── SKILL.md                      # Skill 主文件
└── references/
    ├── accounts.md               # 账号矩阵
    ├── templates.md              # 内容模板
    └── articles/                 # 历史文章库
        ├── README.md            # 文章索引
        ├── codepanda/          # 码农世界 (467篇)
        ├── oldyouth/           # 旧青年 (110篇)
        └── dreamers/           # 北漂答卷人 (5篇)
```

## License

MIT
