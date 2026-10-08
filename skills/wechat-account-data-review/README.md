# 公众号后台数据复盘

合并公众号趋势与用户增长导出、文章档案，区分文章指标、每日信号和版式线索。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $wechat-account-data-review。复盘这些公众号后台导出和文章档案，缺失的文章阅读量保留未知，不将每日涨粉归因给某一篇。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

Python + pandas + openpyxl + xlrd + beautifulsoup4 + lxml + tabulate；输入需要用户导出的后台表及约定文章档案。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [analyze_wechat_exports.py](scripts/analyze_wechat_exports.py)：先运行 `python scripts/analyze_wechat_exports.py --help` 查看参数。

## 参考资料

- [references/export-data-contract.md ](references/export-data-contract.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
