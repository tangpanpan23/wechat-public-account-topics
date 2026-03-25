#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理无扩展名的文本文件，转换为 md 格式并保存到 historys 目录
"""

import os
import re
from pathlib import Path

SOURCE_DIR = "/Users/tal/Desktop/个人随笔"
TARGET_DIR = "/Users/tal/Desktop/个人随笔/historys"

# 跳过的文件
SKIP_PREFIX = [".~", "~$", "✨"]
SKIP_EXTENSIONS = [".md", ".docx", ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".xlsx", ".xls"]

def is_text_file(filepath):
"""检查文件是否为文本文件"""
try:
with open(filepath, 'r', encoding='utf-8') as f:
f.read(1024)
return True
except:
return False

def clean_filename(name):
"""清理文件名，生成安全的 md 文件名"""
# 移除特殊字符
name = re.sub(r'[<>:"/\\|？*]', '', name)
name = re.sub(r'\s+', ' ', name).strip()
# 限制长度
if len(name) > 100:
name = name[:100]
return name + ".md"

def normalize_content(content, filename):
"""规范化内容为公众号格式"""
if not content:
return ""

lines = content.split('\n')
new_lines = []

# 检查是否已有标题
has_title = False
for line in lines[:5]:
stripped = line.strip()
if stripped.startswith('# ') or (len(stripped) < 50 and len(stripped) > 5 and not any(c in stripped for c in '，。,.!?')):
has_title = True
break

# 添加标题
if not has_title:
title = Path(filename).stem
title = re.sub(r'[<>:"/\\|？*]', '', title)
title = re.sub(r'\s+', ' ', title).strip()
if len(title) > 50:
title = title[:50] + "..."
new_lines.append(f"# {title}")
new_lines.append('')

# 处理段落
for line in lines:
stripped = line.strip()
if stripped:
new_lines.append(stripped)
else:
new_lines.append('')

# 清理多余空行
result = '\n'.join(new_lines)
result = re.sub(r'\n{4,}', '\n\n', result)

return result.strip()

def process_text_files():
"""主处理函数"""
stats = {
'total': 0,
'processed': 0,
'skipped': 0,
'errors': 0
}

# 确保目标目录存在
os.makedirs(TARGET_DIR, exist_ok=True)

# 查找所有文本文件
text_files = []
for filename in os.listdir(SOURCE_DIR):
filepath = os.path.join(SOURCE_DIR, filename)

if not os.path.isfile(filepath):
continue

# 跳过临时文件
if any(filename.startswith(prefix) for prefix in SKIP_PREFIX):
print(f"跳过特殊文件：{filename}")
stats['skipped'] += 1
continue

# 跳过已有扩展名的文件
if any(filename.endswith(ext) for ext in SKIP_EXTENSIONS):
continue

# 检查是否为文本文件
if not is_text_file(filepath):
continue

# 检查文件大小
try:
file_size = os.path.getsize(filepath)
if file_size < 100:
print(f"跳过小文件：{filename}")
stats['skipped'] += 1
continue
except:
continue

text_files.append(filepath)
stats['total'] += 1

print(f"找到 {stats['total']} 个需要处理的文本文件\n")

# 处理每个文件
for filepath in text_files:
filename = os.path.basename(filepath)
print(f"处理：{filename}")

# 读取内容
try:
with open(filepath, 'r', encoding='utf-8') as f:
content = f.read()
except Exception as e:
print(f"  ❌ 读取失败：{e}")
stats['errors'] += 1
continue

if len(content.strip()) < 50:
print(f"  ⚠️  内容太短，跳过")
stats['errors'] += 1
continue

# 规范化格式
md_content = normalize_content(content, filename)

# 生成目标文件名
safe_name = clean_filename(filename)
target_path = os.path.join(TARGET_DIR, safe_name)

# 检查是否已存在
if os.path.exists(target_path):
import time
timestamp = time.strftime('%Y%m%d%H%M%S')
base, ext = os.path.splitext(safe_name)
target_path = os.path.join(TARGET_DIR, f"{base}_{timestamp}{ext}")
print(f"  ⚠️  文件已存在，添加时间戳")

# 保存
try:
with open(target_path, 'w', encoding='utf-8') as f:
f.write(md_content)
print(f"  ✅ 保存到：{os.path.basename(target_path)}")
stats['processed'] += 1
except Exception as e:
print(f"  ❌ 保存失败：{e}")
stats['errors'] += 1

# 输出报告
print("\n" + "="*60)
print("文本文件处理报告")
print("="*60)
print(f"总文件数：{stats['total']}")
print(f"处理成功：{stats['processed']}")
print(f"跳过（特殊/小文件）：{stats['skipped']}")
print(f"处理失败：{stats['errors']}")
print(f"目标目录：{TARGET_DIR}")
print("="*60)

return stats

if __name__ == "__main__":
process_text_files()