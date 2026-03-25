---
name: wechat-public-account-topics
description: 微信公众号选题与内容生成工具。当用户需要为公众号创作内容、结合热点新闻生成选题、制作公众号文章或视频脚本时使用。包括：(1) 热点新闻收集与分析 (2) 结合公众号定位生成多角度选题 (3) 输出完整文章/视频脚本。触发词：公众号选题、热点选题、生成文章、热点文章、视频脚本、选题简报。
---

# 微信公众号选题与内容生成

## 快速开始

### 工作流程

1. **收集热点** → 使用 `web_fetch` 获取虎嗅、36氪等新闻源
2. **匹配账号定位** → 读取 `references/accounts.md` 了解账号矩阵
3. **参考历史文章** → 读取 `references/articles/` 下的历史文章作为参考
4. **生成多角度内容** → 为每个账号生成差异化选题
5. **输出内容** → 完整文章 + 视频脚本

### 热点收集

```bash
# 虎嗅
web_fetch(url="https://www.huxiu.com", maxChars=3000)

# 36氪快讯
web_fetch(url="https://36kr.com/newsflashes", maxChars=2000)
```

## 账号矩阵

账号定位信息存储在 `references/accounts.md`，包含：
- 码农世界 CodePanda（程序员/技术）- 467篇历史文章
- 旧青年（情怀/生活）- 110篇历史文章
- 北漂答卷人（北漂/奋斗）- 5篇历史文章

读取参考文档：
```
references/accounts.md - 完整账号画像
references/templates.md - 内容模板
references/articles/ - 历史文章库
```

## 历史文章库

**位置**: `references/articles/`

| 目录 | 账号 | 文章数 | 内容特点 |
|------|------|--------|----------|
| `codepanda/` | 码农世界 | 467篇 | 技术干货、北漂生活、自传 |
| `oldyouth/` | 旧青年 | 110篇 | 情怀叙事、青春回忆 |
| `dreamers/` | 北漂答卷人 | 5篇 | 北漂感悟、职场思考 |

**索引文件**: `references/articles/README.md` - 文章目录和热门选题

## 输出格式

### 选题清单格式

```
📱 [账号名]

**选题方向**: [一句话定位]

**标题**: 《主标题》

**正文结构**:
1. [开头钩子 - 抓眼球]
2. [核心论述 - 有深度]
3. [结尾升华 - 有温度]

**标签**: #标签1 #标签2
```

### 文章正文要求

- 开头要有冲击力（数据/冲突/反差）
- 中间要有干货（案例/分析/观点）
- 结尾要有温度（情感/呼吁/思考）
- 字数控制：1500-2500字

### 视频脚本格式

```
【开场 0:00-0:30】
*画面：xxx*
旁白：xxx

【第一部分 0:30-1:30】
*画面：xxx*
旁白：xxx

【结尾 3:30-4:00】
*画面：黑屏白字*
旁白：xxx
```

## 内容差异化策略

同一热点，不同账号的角度：

| 维度 | 码农世界 | 旧青年 | 北漂答卷人 |
|------|----------|--------|------------|
| 角度 | 技术/理性 | 情感/温度 | 奋斗/现实 |
| 受众 | 程序员 | 文艺青年 | 打工人 |
| 风格 | 干货分析 | 情怀叙事 | 接地气 |
| 参考文章 | codepanda/* | oldyouth/* | dreamers/* |

## 飞书消息发送

发送选题简报到飞书群：

```javascript
message(action="send", channel="feishu", target="oc_c6c4c089c8128fc56b6796bc103771d3", message="标题", card={
  "config": {"widget": {"京:nl2br": true}},
  "elements": [{"tag": "markdown", "content": "内容"}]
})
```

**注意**：飞书 card 必须使用 `config` + `elements` 格式。

## 参考文档

- `references/accounts.md` - 账号矩阵详细画像
- `references/templates.md` - 内容模板与示例
- `references/articles/README.md` - 历史文章索引
- `references/articles/codepanda/` - 码农世界历史文章
- `references/articles/oldyouth/` - 旧青年历史文章
- `references/articles/dreamers/` - 北漂答卷人历史文章
