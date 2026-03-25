#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理 docx 文件，转换为 md 格式并保存到 historys 目录
"""

import os
import re
from pathlib import Path
from docx import Document

SOURCE_DIR = "/Users/tal/Desktop/个人随笔"
TARGET_DIR = "/Users/tal/Desktop/个人随笔/historys"

# 跳过临时文件
SKIP_PREFIX = [".~", "~$"]

# 跳过的文件名（如授权书模板等）
SKIP_KEYWORDS = ["肖像权", "授权书", "模板"]

def clean_filename(name):
"""清理文件名，生成安全的 md 文件名"""
# 移除特殊字符
name = re.sub(r'[<>:"/\\|？*]', '', name)
name = re.sub(r'\s+', ' ', name).strip()
# 移除 .docx 扩展名
if name.endswith('.docx'):
name = name[:-5]
# 移除"副本"等字样
name = re.sub(r'_?副本', '', name)
# 限制长度
if len(name) > 100:
name = name[:100]
return name + ".md"

def extract_text_from_docx(filepath):
"""从 docx 文件提取文本"""
try:
doc = Document(filepath)
paragraphs = []
for para in doc.paragraphs:
text = para.text.strip()
if text:
paragraphs.append(text)

# 处理表格
tables = []
for table in doc.tables:
for row in table.rows:
row_text = []
for cell in row.cells:
cell_text = cell.text.strip()
if cell_text:
row_text.append(cell_text)
if row_text:
tables.append(' | '.join(row_text))

return '\n\n'.join(paragraphs), tables
except Exception as e:
print(f"读取 docx 文件失败 {filepath}: {e}")
return None, []

def normalize_content(content, filename):
"""规范化内容为公众号格式"""
if not content:
return ""

lines = content.split('\n')
new_lines = []

# 检查是否已有标题
has_title = False
for line in lines[:5]:
if line.strip().startswith('# '):
has_title = True
break

# 添加标题
if not has_title:
title = Path(filename).stem
# 清理标题
title = re.sub(r'_?副本', '', title)
title = re.sub(r'[<>:"/\\|？*]', '', title)
title = re.sub(r'\s+', ' ', title).strip()
new_lines.append(f"# {title}")
new_lines.append('')

# 处理段落
for line in lines:
stripped = line.strip()
if stripped:
# 跳过可能的模板内容
if any(kw in stripped for kw in ["授权书", "模板", "肖像权", "本人同意"]):
continue
new_lines.append(stripped)
else:
new_lines.append('')

# 清理多余空行
result = '\n'.join(new_lines)
result = re.sub(r'\n{4,}', '\n\n', result)

return result.strip()

def process_docx_files():
"""主处理函数"""
stats = {
'total': 0,
'processed': 0,
'skipped': 0,
'errors': 0
}

# 确保目标目录存在
os.makedirs(TARGET_DIR, exist_ok=True)

# 查找所有 docx 文件
docx_files = []
for filename in os.listdir(SOURCE_DIR):
filepath = os.path.join(SOURCE_DIR, filename)

if not os.path.isfile(filepath):
continue

# 跳过临时文件
if any(filename.startswith(prefix) for prefix in SKIP_PREFIX):
print(f"跳过临时文件：{filename}")
stats['skipped'] += 1
continue

# 跳过非 docx 文件
if not filename.endswith('.docx'):
continue

# 跳过授权书模板等
if any(kw in filename for kw in SKIP_KEYWORDS):
print(f"跳过模板文件：{filename}")
stats['skipped'] += 1
continue

docx_files.append(filepath)
stats['total'] += 1

print(f"找到 {stats['total']} 个需要处理的 docx 文件\n")

# 处理每个文件
for filepath in docx_files:
filename = os.path.basename(filepath)
print(f"处理：{filename}")

# 提取内容
content, tables = extract_text_from_docx(filepath)

if not content or len(content.strip()) < 50:
print(f"  ⚠️  内容为空或太短，跳过")
stats['errors'] += 1
continue

# 规范化格式
md_content = normalize_content(content, filename)

# 添加表格（如果有）
if tables:
md_content += "\n\n## 附录\n\n"
for table in tables:
md_content += f"- {table}\n"

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
print("DOCX 文件处理报告")
print("="*60)
print(f"总文件数：{stats['total']}")
print(f"处理成功：{stats['processed']}")
print(f"跳过（模板/临时）：{stats['skipped']}")
print(f"处理失败：{stats['errors']}")
print(f"目标目录：{TARGET_DIR}")
print("="*60)

return stats

if __name__ == "__main__":
process_docx_files()