#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
非 MD 文件整理脚本
- 处理 .docx 文件（转换为 md）
- 处理无扩展名的文本文件
- 处理 .txt 文件
- 跳过临时文件、图片、过小文件
"""

import os
import re
import subprocess
from pathlib import Path

SOURCE_DIR = "/Users/tal/Desktop/个人随笔"
TARGET_DIR = "/Users/tal/Desktop/个人随笔/historys"

# 临时文件前缀
TEMP_PREFIXES = [".~", "~$"]

# 跳过图片扩展名
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".heic"]

# 跳过其他非文档扩展名
SKIP_EXTENSIONS = [".apk", ".zip", ".sql", ".html", ".htm"]

def is_temp_file(filename):
"""检查是否为临时文件"""
for prefix in TEMP_PREFIXES:
if filename.startswith(prefix):
return True
return False

def is_image_file(filename):
"""检查是否为图片文件"""
ext = Path(filename).suffix.lower()
return ext in IMAGE_EXTENSIONS

def is_skip_file(filename):
"""检查是否应该跳过的文件"""
ext = Path(filename).suffix.lower()
return ext in SKIP_EXTENSIONS

def extract_text_from_docx(filepath):
"""从 docx 文件提取文本（使用 python-docx）"""
try:
from docx import Document
doc = Document(filepath)
paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
return '\n\n'.join(paragraphs)
except ImportError:
print(f"  ⚠️  未安装 python-docx，尝试使用 pandoc...")
return extract_text_with_pandoc(filepath)
except Exception as e:
print(f"  ❌ 读取 docx 失败：{e}")
return None

def extract_text_with_pandoc(filepath):
"""使用 pandoc 转换 docx 为 markdown"""
try:
result = subprocess.run(
["pandoc", filepath, "-t", "markdown", "-o", "-"],
capture_output=True,
text=True,
timeout=30
)
if result.returncode == 0:
return result.stdout
else:
print(f"  ⚠️  pandoc 转换失败：{result.stderr}")
return None
except FileNotFoundError:
print(f"  ⚠️  pandoc 未安装")
return None
except Exception as e:
print(f"  ❌ pandoc 错误：{e}")
return None

def extract_title_from_filename(filename):
"""从文件名提取标题"""
# 移除扩展名
name = Path(filename).stem

# 移除特殊字符
name = re.sub(r'^[#*_]+', '', name)  # 移除开头的 # * _
name = re.sub(r'[<>:"/\\|？*]', '', name)
name = re.sub(r'\s+', ' ', name).strip()

# 如果是日期开头，保留日期
date_match = re.match(r'^(\d{4}[-年]\d{0,2}[-月]?\d{0,2}[日号]?)', name)
if date_match:
return name

return name

def normalize_content(content, filename):
"""规范化内容格式"""
if not content:
return None

# 清理空白行
lines = content.split('\n')
cleaned_lines = []

prev_empty = False
for line in lines:
stripped = line.strip()

if not stripped:
if not prev_empty:
cleaned_lines.append('')
prev_empty = True
else:
cleaned_lines.append(stripped)
prev_empty = False

# 移除连续超过 3 个的空白行
result = '\n'.join(cleaned_lines)
result = re.sub(r'\n{4,}', '\n\n', result)

# 确保以标题开头
result = result.strip()
if not result.startswith('#'):
title = extract_title_from_filename(filename)
if title:
result = f"# {title}\n\n{result}"

return result

def safe_filename(name):
"""生成安全的文件名"""
name = re.sub(r'[<>:"/\\|？*]', '', name)
name = re.sub(r'\s+', ' ', name).strip()
# 限制长度
if len(name) > 100:
name = name[:100]
return name + ".md"

def process_files():
"""主处理函数"""
stats = {
'docx_processed': 0,
'txt_processed': 0,
'skipped_temp': 0,
'skipped_small': 0,
'skipped_image': 0,
'skipped_other': 0,
'errors': 0
}

processed_files = []

# 遍历源目录
for filename in os.listdir(SOURCE_DIR):
filepath = os.path.join(SOURCE_DIR, filename)

# 跳过目录
if os.path.isdir(filepath):
continue

# 跳过临时文件
if is_temp_file(filename):
stats['skipped_temp'] += 1
continue

# 跳过图片
if is_image_file(filename):
stats['skipped_image'] += 1
continue

# 跳过其他不处理的扩展名
if is_skip_file(filename):
stats['skipped_other'] += 1
continue

# 跳过 .md 文件（已处理过）
if filename.endswith('.md'):
continue

# 检查文件大小
try:
file_size = os.path.getsize(filepath)
if file_size < 100:
stats['skipped_small'] += 1
continue
except Exception as e:
print(f"无法获取文件大小 {filename}: {e}")
stats['errors'] += 1
continue

content = None
file_type = None

# 处理 .docx 文件
if filename.endswith('.docx'):
print(f"处理 DOCX: {filename}")
content = extract_text_from_docx(filepath)
file_type = 'docx'
if content:
stats['docx_processed'] += 1

# 处理文本文件（无扩展名或 .txt）
elif not Path(filename).suffix or filename.endswith('.txt'):
try:
with open(filepath, 'r', encoding='utf-8') as f:
content = f.read()
file_type = 'txt'
if len(content.strip()) > 200:  # 内容完整
stats['txt_processed'] += 1
print(f"处理 TXT: {filename}")
else:
print(f"跳过内容不完整：{filename}")
continue
except Exception as e:
print(f"读取文本文件失败 {filename}: {e}")
stats['errors'] += 1
continue

# 其他文件尝试读取为文本
else:
try:
with open(filepath, 'r', encoding='utf-8') as f:
content = f.read()
if len(content.strip()) > 200:
file_type = 'text'
stats['txt_processed'] += 1
print(f"处理文本：{filename}")
else:
continue
except:
stats['skipped_other'] += 1
continue

if not content:
stats['errors'] += 1
continue

# 规范化内容
normalized = normalize_content(content, filename)
if not normalized:
stats['errors'] += 1
continue

# 生成安全文件名
safe_name = safe_filename(extract_title_from_filename(filename))

# 检查目标文件是否存在
target_path = os.path.join(TARGET_DIR, safe_name)
if os.path.exists(target_path):
import time
timestamp = time.strftime('%Y%m%d%H%M%S')
base_name = Path(safe_name).stem
target_path = os.path.join(TARGET_DIR, f"{base_name}_{timestamp}.md")

# 保存文件
try:
with open(target_path, 'w', encoding='utf-8') as f:
f.write(normalized)
processed_files.append(target_path)
print(f"  ✓ 保存：{os.path.basename(target_path)}")
except Exception as e:
print(f"  ❌ 保存失败：{e}")
stats['errors'] += 1

# 输出报告
print("\n" + "="*60)
print("非 MD 文件整理报告")
print("="*60)
print(f"DOCX 处理：{stats['docx_processed']}")
print(f"文本处理：{stats['txt_processed']}")
print(f"跳过临时文件：{stats['skipped_temp']}")
print(f"跳过图片：{stats['skipped_image']}")
print(f"跳过小文件：{stats['skipped_small']}")
print(f"跳过其他：{stats['skipped_other']}")
print(f"错误数量：{stats['errors']}")
print(f"保存文件：{len(processed_files)}")
print("="*60)

return stats, processed_files

if __name__ == "__main__":
process_files()