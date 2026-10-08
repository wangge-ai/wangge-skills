# 证据型分析报告

按决策任务选择监测、诊断、比较、预测等报告类型，审计资料、选择模型并检查结论边界。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $analysis-report-orchestrator。用这些表格和文档写分析报告，先说明决策目标、资料口径及缺失，再形成有证据的建议。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

Python；报告结构检查器不评判商业结论是否正确，核心结论仍需证据和人工复核。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [validate_report.py](scripts/validate_report.py)：先运行 `python scripts/validate_report.py --help` 查看参数。

## 参考资料

- [assets/analysis-plan-template.md ](assets/analysis-plan-template.md)
- [assets/report-template.md ](assets/report-template.md)
- [assets/task-card-template.md ](assets/task-card-template.md)
- [references/ecommerce-report-recipes.md ](references/ecommerce-report-recipes.md)
- [references/evidence-and-quality-rules.md ](references/evidence-and-quality-rules.md)
- [references/model-selector.md ](references/model-selector.md)
- [references/open-report-fallback.md ](references/open-report-fallback.md)
- [references/report-routing.md ](references/report-routing.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
