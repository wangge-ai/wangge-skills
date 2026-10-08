# 商品页定位与策划

从商品事实、竞品表达、关键词和反馈策划定位、卖点、1+5 主图序列及详情页。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $ecom-page-planner。根据这些商品事实和参考资料，策划六张主图及详情页，每个卖点说明证据与缺口。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

Python + openpyxl。脚手架只登记证据和输出任务，不自动产生完整策划结论。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [build_planning_artifact.py](scripts/build_planning_artifact.py)：先运行 `python scripts/build_planning_artifact.py --help` 查看参数。
- [validate_output.py](scripts/validate_output.py)：先运行 `python scripts/validate_output.py --help` 查看参数。

## 参考资料

- [references/category-output-contract.md ](references/category-output-contract.md)
- [references/ecom-category-link-positioning-matrix.md ](references/ecom-category-link-positioning-matrix.md)
- [references/ecom-detail-page-planner.md ](references/ecom-detail-page-planner.md)
- [references/ecom-main-image-marketing-positioning.md ](references/ecom-main-image-marketing-positioning.md)
- [references/ecom-main-image-selling-point-analysis.md ](references/ecom-main-image-selling-point-analysis.md)
- [references/ecom-main-image-series-planner.md ](references/ecom-main-image-series-planner.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
