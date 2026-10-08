---
name: document-to-markdown
description: 将本地文档和网页文件转换为 Markdown，支持 PDF、DOCX、PPTX、XLSX/CSV、HTML、可 OCR 的图片，以及其他
  MarkItDown 支持的格式。用户要求把 Word、PDF、PPT、表格、网页、图片、音频或类似文件转成 .md，批量转 Markdown，或清理 PDF
  中文断行时使用。
license: MIT
---

# 文档转 Markdown

## 工作流程

1. 先确认源文件路径存在，再选择输出位置。在 Codex 的无项目聊天里，面向用户交付的 Markdown 文件优先写入当前线程的 `outputs/` 目录。
2. 优先使用 `scripts/convert_to_markdown.py`；它会调用已安装的 `markitdown` 命令，并处理输出路径、批量转换和 PDF 断行清理。
3. 转换完成后做一次快速质量检查：文件存在、大小不是空壳、文本不是大面积空白、没有明显乱码替换符，并抽看开头和结尾是否可读。
4. 如实说明转换器警告。PDF 的字体边界警告通常不影响正文提取，只要 Markdown 文本完整即可。

## 脚本用法

单个文件转到指定 Markdown 路径：

```bash
python path/to/document-to-markdown/scripts/convert_to_markdown.py "input.pdf" -o "output.md" --keep-raw
```

一个或多个文件转到文件夹：

```bash
python path/to/document-to-markdown/scripts/convert_to_markdown.py "a.pdf" "b.docx" -o "markdown/"
```

批量转换某个目录：

```bash
python path/to/document-to-markdown/scripts/convert_to_markdown.py "docs/" -o "markdown/" --recursive
```

常用选项：

- `--clean auto`：只对 PDF 自动清理断行，这是默认值。
- `--clean always`：对所有转换结果都应用断行清理。
- `--clean never` 或 `--no-clean`：完全保留 MarkItDown 原始输出。
- `--keep-raw`：启用清理时，同时保留一份 `.raw.md` 原始转换稿，方便对照。

## 转换说明

- `.pdf`、`.docx`、`.pptx`、`.xlsx`、`.csv`、`.html`、`.htm`、常见图片格式、音频格式和 URL，优先使用 MarkItDown。
- 旧版 `.doc` 可能需要先用 LibreOffice 或其他工具转成 `.docx`。
- 扫描版 PDF 需要 OCR 支持。如果转换结果为空或几乎全是图片，说明需要 OCR；只有本机已安装可用 OCR 工具时再尝试。
- 加密文件或需要登录的网页，需要用户提供已导出的本地文件或合法访问材料；不要索要密码。
