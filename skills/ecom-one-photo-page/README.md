# 一张产品图做商品页

从一张产品照片建立 SKU 与数量约束，交付六张主图和详情页方案、独立提示词及产品一致性检查。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $ecom-one-photo-page。用这张产品图规划主图和详情页，先交方案及提示词，缺少证据的结构和功效保持待核实。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

基础脚本仅需 Python；生成成品需要用户可用的生图工具，结构检查不能替代目视检查。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [init_job.py](scripts/init_job.py)：先运行 `python scripts/init_job.py --help` 查看参数。
- [validate_pack.py](scripts/validate_pack.py)：先运行 `python scripts/validate_pack.py --help` 查看参数。

## 参考资料

- [references/category-routing.md ](references/category-routing.md)
- [references/copy-and-claims.md ](references/copy-and-claims.md)
- [references/decision-engine.md ](references/decision-engine.md)
- [references/method-provenance.md ](references/method-provenance.md)
- [references/page-architecture.md ](references/page-architecture.md)
- [references/product-consistency.md ](references/product-consistency.md)
- [references/production-and-qa.md ](references/production-and-qa.md)
- [references/prompt-contract.md ](references/prompt-contract.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
