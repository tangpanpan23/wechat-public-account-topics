---
name: wechat-public-account-topics
description: 微信公众号选题与内容生成工具。当用户需要为公众号创作内容、结合热点新闻生成选题、制作公众号文章或视频脚本时使用。包括：(1) 热点新闻收集与分析 (2) 结合公众号定位生成多角度选题 (3) 输出完整文章/视频脚本 (4) 自动化发布脚本。触发词：公众号选题、热点选题、生成文章、热点文章、视频脚本、选题简报、发布公众号。
---

# 微信公众号选题与内容生成

## 功能概览

| 功能 | 说明 |
|------|------|
| 热点收集 | 虎嗅、36氪等新闻源 |
| 账号匹配 | 3个账号差异化定位 |
| 历史文章参考 | 582篇历史文章 |
| 选题生成 | P0/P1/P2 优先级 |
| 内容输出 | 文章 + 视频脚本 |
| 自动化发布 | 草稿箱发布脚本 |

## 快速开始

### 工作流程

1. **收集热点** → 使用 `web_fetch` 获取虎嗅、36氪等新闻源
2. **匹配账号定位** → 读取 `references/accounts.md` 了解账号矩阵
3. **参考历史文章** → 读取 `references/articles/` 下的历史文章
4. **生成多角度内容** → 为每个账号生成差异化选题
5. **输出内容** → 完整文章 + 视频脚本
6. **发布** → 使用 `scripts/wechat-publisher.py` 发布到草稿箱

### 热点收集

```bash
# 虎嗅
web_fetch(url="https://www.huxiu.com", maxChars=3000)

# 36氪快讯
web_fetch(url="https://36kr.com/newsflashes", maxChars=2000)
```

## 账号矩阵

| 账号 | 定位 | 受众 | 历史文章 |
|------|------|------|----------|
| 码农世界 CodePanda | 程序员/技术 | 开发者 | 467篇 |
| 旧青年 | 情怀/生活 | 文艺青年 | 110篇 |
| 北漂答卷人 | 北漂/奋斗 | 打工人 | 5篇 |

## 历史文章库

**位置**: `references/articles/`

| 目录 | 账号 | 文章数 |
|------|------|--------|
| `codepanda/` | 码农世界 | 467篇 |
| `oldyouth/` | 旧青年 | 110篇 |
| `dreamers/` | 北漂答卷人 | 5篇 |

## 自动化脚本

**位置**: `scripts/`

### 1. wechat-publisher.py

微信公众号文章发布脚本。

```bash
# 安装依赖
pip3 install requests

# 基本用法
python3 scripts/wechat-publisher.py

# 指定文章文件
python3 scripts/wechat-publisher.py --article /path/to/article.md

# 指定账号
python3 scripts/wechat-publisher.py --account codepanda

# Dry-run 模式（仅转换不发布）
python3 scripts/wechat-publisher.py --dry-run
```

**配置**: `~/.openclaw/wechat-config.json`
```json
{
  "accounts": {
    "codepanda": {
      "name": "码农世界 CodePanda",
      "appid": "your_appid",
      "appsecret": "your_appsecret"
    }
  }
}
```

### 2. db-sync.sh

数据库表同步脚本（测试环境 → 本地）。

```bash
# 导出变量
export SOURCE_PASS='测试环境密码'
export TARGET_PASS='本地密码'

# Dry-run
./scripts/db-sync.sh --dry-run

# 执行同步
./scripts/db-sync.sh

# 同步指定表
./scripts/db-sync.sh --table h_message_logs
```

## 内容差异化策略

| 维度 | 码农世界 | 旧青年 | 北漂答卷人 |
|------|----------|--------|------------|
| 角度 | 技术/理性 | 情感/温度 | 奋斗/现实 |
| 受众 | 程序员 | 文艺青年 | 打工人 |
| 风格 | 干货分析 | 情怀叙事 | 接地气 |

## 飞书消息发送

发送选题简报到飞书群：

```javascript
message(action="send", channel="feishu", target="oc_c6c4c089c8128fc56b6796bc103771d3", message="标题", card={
  "config": {"widget": {"京:nl2br": true}},
  "elements": [{"tag": "markdown", "content": "内容"}]
})
```

## 参考文档

- `references/accounts.md` - 账号矩阵详细画像
- `references/templates.md` - 内容模板与示例
- `references/articles/README.md` - 历史文章索引
- `references/articles/codepanda/` - 码农世界历史文章
- `references/articles/oldyouth/` - 旧青年历史文章
- `references/articles/dreamers/` - 北漂答卷人历史文章
- `scripts/README.md` - 脚本使用说明
