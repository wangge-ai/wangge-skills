# 文档批量转 Markdown

调用 MarkItDown 转换文档、表格及网页，支持批量输出、保留原稿与 PDF 中文断行清理。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $document-to-markdown。把这个文件夹的文档批量转换为 Markdown，保留原文件，并列出转换失败和需要 OCR 的文件。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

Python + markitdown；所选格式需相应扩展依赖。扫描件 OCR、音频识别和旧版 DOC 转换需另配工具。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [convert_to_markdown.py](scripts/convert_to_markdown.py)：先运行 `python scripts/convert_to_markdown.py --help` 查看参数。

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
