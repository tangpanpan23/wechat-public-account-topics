# WeChat Public Account Topics Skill

微信公众号选题与内容生成 AgentSkill。

当需要为公众号创作内容、结合热点新闻生成选题、制作公众号文章或视频脚本时使用。

## 功能

- 热点新闻收集与分析（虎嗅、36氪）
- 结合公众号定位生成多角度选题
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

| 账号 | 定位 | 受众 |
|------|------|------|
| 码农世界 CodePanda | 程序员/技术 | 开发者 |
| 旧青年 | 情怀/生活 | 文艺青年 |
| 北漂答卷人 | 北漂/奋斗 | 打工人 |

## 安装

将 skill 放置到 OpenClaw skills 目录：

```bash
cp -r wechat-public-account-topics ~/.openclaw/skills/
```

或使用 OpenClaw 命令：

```bash
openclaw skills install wechat-public-account-topics
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
├── SKILL.md              # 主文件
└── references/
    ├── accounts.md       # 账号矩阵
    └── templates.md      # 内容模板
```

## License

MIT
