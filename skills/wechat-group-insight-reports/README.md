# 群聊需求与问答分析

从群聊导出生成匿名洞察工作台、内部需求报告及高频问答，支持原文定位和增量更新。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $wechat-group-insight-reports。分析这份群聊导出，生成匿名本地看板、内部需求报告和隐私安全的高频问答。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

本地处理仅需 Python；飞书发布需用户自己的连接器或 CLI 与权限。群聊原文、账号及状态文件不得上传公开仓库。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [build_dashboard.py](scripts/build_dashboard.py)：先运行 `python scripts/build_dashboard.py --help` 查看参数。
- [prepare_group_chat.py](scripts/prepare_group_chat.py)：先运行 `python scripts/prepare_group_chat.py --help` 查看参数。
- [validate_reports.py](scripts/validate_reports.py)：先运行 `python scripts/validate_reports.py --help` 查看参数。

## 参考资料

- [assets/dashboard-template.html ](assets/dashboard-template.html)
- [references/dashboard-workflow.md ](references/dashboard-workflow.md)
- [references/feishu-publishing.md ](references/feishu-publishing.md)
- [references/feishu-visualization.md ](references/feishu-visualization.md)
- [references/input-and-evidence.md ](references/input-and-evidence.md)
- [references/report-contracts.md ](references/report-contracts.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
