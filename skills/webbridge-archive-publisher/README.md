# 网页与飞书资料归档

通过授权浏览器保存原始证据、Markdown、截图和阅读入口，记录失败及资源对应关系。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $webbridge-archive-publisher。归档我已授权访问的这些网页资料，保存正文、来源和素材，访问受限时记录并停止该项。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

Python + Pillow；PowerShell 兼容采集脚本需用户另装并授权 Kimi WebBridge，其本地接口可能随版本变化。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [build_archive_reader.py](scripts/build_archive_reader.py)：先运行 `python scripts/build_archive_reader.py --help` 查看参数。
- [l6_antibot_router.ps1](scripts/l6_antibot_router.ps1)：Windows PowerShell 脚本，使用前检查参数与依赖。
- [webbridge_archive.ps1](scripts/webbridge_archive.ps1)：Windows PowerShell 脚本，使用前检查参数与依赖。

## 参考资料

- [references/legacy-webbridge-archive.md ](references/legacy-webbridge-archive.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
