# 跨平台资料采集编排

发现并去重链接，组织可恢复采集、来源与资产记录，交付离线可读的资料合集。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $web-collection-orchestrator。整理这个页面中的资料链接，保留来源和失败原因，再汇总成可离线阅读的目录。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

基础整理与打包仅需 Python；采集需用户已授权浏览器及相应平台工具；不附带账号、Cookie 或私有导出。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [build_feishu_bundle.py](scripts/build_feishu_bundle.py)：先运行 `python scripts/build_feishu_bundle.py --help` 查看参数。
- [normalize_link_queue.py](scripts/normalize_link_queue.py)：先运行 `python scripts/normalize_link_queue.py --help` 查看参数。

## 参考资料

- [references/artifact-contracts.md ](references/artifact-contracts.md)
- [references/end-to-end-workflow.md ](references/end-to-end-workflow.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
