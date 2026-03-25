#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章发布脚本
支持多账号配置，自动获取 access_token，Markdown 转 HTML，保存到草稿箱

用法：
    python3 scripts/wechat-publisher.py
    ARTICLE_PATH="/path/to/article.md" python3 scripts/wechat-publisher.py
    ACCOUNT="codepanda" python3 scripts/wechat-publisher.py
"""

import requests
import json
import re
import os
import sys
import argparse

# ==================== 配置区域 ====================
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.openclaw/wechat-config.json")
DEFAULT_ARTICLE_PATH = os.path.expanduser("~/Desktop/AI 时代我们该如何自处 - 优化版.md")

# ==================== 函数定义 ====================
def load_config(config_path=None, account_name=None):
    """加载公众号配置"""
    config_path = config_path or DEFAULT_CONFIG_PATH
    
    if not os.path.exists(config_path):
        # 尝试 TOOLS.md 中的配置
        tools_config = os.path.expanduser("~/.openclaw/workspace/TOOLS.md")
        if os.path.exists(tools_config):
            print(f"使用 TOOLS.md 配置")
            return load_config_from_tools(tools_config, account_name)
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    accounts = config.get("accounts", {})
    
    # 如果指定了账号名，直接返回
    if account_name and account_name in accounts:
        return accounts[account_name]
    
    # 如果只有一个账号，返回那个
    if len(accounts) == 1:
        return list(accounts.values())[0]
    
    # 如果有多个账号，让用户选择
    print("\n请选择要发布的账号：")
    for i, name in enumerate(accounts.keys(), 1):
        print(f"  {i}. {name}")
    
    choice = input("\n请输入编号 (默认 1): ").strip() or "1"
    try:
        selected = list(accounts.keys())[int(choice) - 1]
        return accounts[selected]
    except (ValueError, IndexError):
        return list(accounts.values())[0]


def load_config_from_tools(tools_path, account_name=None):
    """从 TOOLS.md 解析配置（兼容旧配置）"""
    # 这个函数用于兼容旧格式，实际使用建议用 wechat-config.json
    raise NotImplementedError("请使用 ~/.openclaw/wechat-config.json 配置文件")


def get_access_token(appid, appsecret):
    """获取 access_token"""
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
    
    try:
        response = requests.get(token_url, timeout=10)
        result = response.json()
    except Exception as e:
        print(f"✗ access_token 请求失败: {e}")
        return None
    
    if "access_token" not in result:
        print(f"✗ access_token 获取失败")
        print(f"  errcode: {result.get('errcode')}")
        print(f"  errmsg: {result.get('errmsg')}")
        return None
    
    return result["access_token"]


def markdown_to_html(md):
    """Markdown 转 HTML（简单实现）"""
    html = md
    
    # 标题
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # 加粗
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 斜体
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 引用
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # 列表
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # 链接
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    # 代码块
    html = re.sub(r'```(\w*)\n(.+?)```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
    
    # 段落
    lines = html.split('\n')
    processed_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('<') and not stripped.endswith('>'):
            if not stripped.startswith('-') and not stripped.startswith('#'):
                processed_lines.append(f'<p>{stripped}</p>')
            else:
                processed_lines.append(line)
        else:
            processed_lines.append(line)
    html = '\n'.join(processed_lines)
    
    return html


def save_to_draft(access_token, title, content, author, digest, thumb_media_id=""):
    """保存到草稿箱"""
    draft_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    draft_data = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "show_cover_pic": 1 if thumb_media_id else 0
            }
        ]
    }
    
    try:
        response = requests.post(draft_url, json=draft_data, timeout=10)
        return response.json()
    except Exception as e:
        return {"errcode": -1, "errmsg": str(e)}


def extract_metadata(markdown_content):
    """从 Markdown 提取元数据"""
    # 提取标题
    title_match = re.search(r'^# (.+)$', markdown_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "无标题"
    
    # 提取摘要（第一行引用或前100字）
    digest_match = re.search(r'^> (.+)$', markdown_content, re.MULTILINE)
    if digest_match:
        digest = digest_match.group(1).strip()[:120]
    else:
        # 取前100个字符
        clean_text = re.sub(r'[#*>`\[\]]', '', markdown_content)
        digest = clean_text[:100].strip() + "..."
    
    return title, digest


# ==================== 主流程 ====================
def main():
    parser = argparse.ArgumentParser(description='微信公众号文章发布脚本')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--account', '-a', help='账号名 (如 codepanda)')
    parser.add_argument('--article', help='文章文件路径')
    parser.add_argument('--dry-run', help='仅转换不发布', action='store_true')
    args = parser.parse_args()
    
    print("=" * 60)
    print("微信公众号草稿箱发布脚本")
    print("=" * 60)
    
    # 1. 加载配置
    print(f"\n步骤 1: 加载公众号配置...")
    try:
        config = load_config(args.config, args.account)
        appid = config["appid"]
        appsecret = config["appsecret"]
        account_name = config.get("name", "未知账号")
        print(f"✓ 配置加载成功")
        print(f"  公众号：{account_name}")
        print(f"  AppID: {appid}")
    except Exception as e:
        print(f"✗ 配置加载失败：{e}")
        return
    
    # 2. 获取 access_token
    print(f"\n步骤 2: 获取 access_token...")
    access_token = get_access_token(appid, appsecret)
    if not access_token:
        print("请检查 AppID 和 AppSecret 是否正确，以及 IP 是否在白名单中")
        return
    print(f"✓ access_token 获取成功")
    
    # 3. 读取文章
    article_path = args.article or DEFAULT_ARTICLE_PATH
    if 'ARTICLE_PATH' in os.environ:
        article_path = os.environ['ARTICLE_PATH']
    
    print(f"\n步骤 3: 读取文章内容...")
    print(f"  文件：{article_path}")
    try:
        with open(article_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
        print(f"✓ 文章读取成功，长度：{len(markdown_content)} 字符")
    except FileNotFoundError:
        print(f"✗ 文件不存在：{article_path}")
        print(f"\n请指定文章路径：")
        print(f"  python3 scripts/wechat-publisher.py --article /path/to/article.md")
        return
    except Exception as e:
        print(f"✗ 文章读取失败：{e}")
        return
    
    # 4. 提取元数据
    title, digest = extract_metadata(markdown_content)
    print(f"\n文章信息:")
    print(f"  标题：{title}")
    print(f"  摘要：{digest[:50]}...")
    
    # 5. 转换 HTML
    print(f"\n步骤 4: Markdown 转 HTML...")
    html_content = markdown_to_html(markdown_content)
    print(f"✓ HTML 转换完成，长度：{len(html_content)} 字符")
    
    # 6. Dry-run 模式
    if args.dry_run:
        print(f"\n[DRY-RUN] 跳过发布，HTML 内容预览：")
        print("-" * 40)
        print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
        print("-" * 40)
        return
    
    # 7. 保存到草稿箱
    print(f"\n步骤 5: 保存到草稿箱...")
    result = save_to_draft(
        access_token,
        title,
        html_content,
        config.get("author", "公众号作者"),
        digest
    )
    
    # 8. 输出结果
    if "media_id" in result:
        media_id = result["media_id"]
        print("\n" + "=" * 60)
        print("✓ 草稿保存成功！")
        print("=" * 60)
        print(f"  草稿 ID (media_id): {media_id}")
        print(f"\n请登录微信公众号后台查看和编辑草稿:")
        print(f"  https://mp.weixin.qq.com/")
        print(f"\n后续操作:")
        print(f"  1. 登录公众号后台")
        print(f"  2. 进入「内容与互动」→「新的创作」→「草稿箱」")
        print(f"  3. 找到标题为「{title}」的草稿")
        print(f"  4. 编辑排版、添加封面图")
        print(f"  5. 预览并群发")
        
        # 保存 media_id 到文件供后续使用
        try:
            with open("/tmp/last_draft_id.txt", "w") as f:
                f.write(media_id)
        except:
            pass
    else:
        print(f"\n✗ 草稿保存失败")
        print(f"  errcode: {result.get('errcode')}")
        print(f"  errmsg: {result.get('errmsg')}")
        print(f"\n常见问题:")
        print(f"  1. IP 不在白名单 → 公众号后台 → 设置与开发 → 基本配置 → IP 白名单")
        print(f"  2. access_token 过期 → 重新运行脚本即可")
        print(f"  3. 内容格式问题 → 检查 HTML 内容是否符合微信规范")


if __name__ == "__main__":
    main()
