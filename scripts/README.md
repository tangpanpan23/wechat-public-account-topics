# 公众号自动化脚本集

本目录包含公众号选题和发布的自动化脚本。

## 脚本列表

### 1. wechat-publisher.py

微信公众号文章发布脚本。

**功能**：
- 自动获取 access_token
- Markdown 转 HTML
- 保存到草稿箱
- 支持多账号配置

**用法**：
```bash
# 安装依赖
pip3 install requests

# 运行脚本
python3 scripts/wechat-publisher.py

# 指定文章文件
ARTICLE_PATH="/path/to/article.md" python3 scripts/wechat-publisher.py
```

**配置**：
- 配置文件：`~/.openclaw/wechat-config.json`
- 格式：
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

**常见问题**：
- IP 不在白名单 → 登录公众号后台添加 IP
- access_token 过期 → 重新运行脚本

---

### 2. db-sync.sh (数据库同步)

将测试环境数据库表同步到本地环境。

**功能**：
- 从 RDS 测试环境同步表数据到本地
- 支持 dry-run 模式
- 支持指定表同步
- 自动关闭/开启外键检查

**用法**：
```bash
# 同步所有表（先 dry-run）
./scripts/db-sync.sh --dry-run
./scripts/db-sync.sh

# 同步指定表
./scripts/db-sync.sh --table h_message_logs --table h_todo_events
```

**环境变量**：
```bash
export SOURCE_PASS='测试环境库密码'
export TARGET_PASS='本地库密码'
./scripts/db-sync.sh
```

**配置**（脚本内写死）：
- 源库：RDS `rm-2zef2q80yoia39816.mysql.rds.aliyuncs.com`，库名 `hps`
- 目标库：`127.0.0.1:3306`，库名 `hps`

---

## 依赖

### Python 依赖 (wechat-publisher.py)
```
requests>=2.25.0
```

### MySQL 依赖 (db-sync.sh)
```
mysqldump
mysql
```

---

## 注意事项

1. **密码安全**：数据库密码通过环境变量传入，不要写死在脚本中
2. **IP 白名单**：公众号 API 需要在后台添加服务器 IP 到白名单
3. **access_token 有效期**：微信 access_token 有效期 2 小时，脚本会自动刷新
