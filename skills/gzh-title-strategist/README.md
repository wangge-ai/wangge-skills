# 公众号标题策划

按读者任务、文章证据和推荐场景生成、比较及评分标题，避免无法兑现的数字和结果。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $gzh-title-strategist。给这篇文章设计不同路线的公众号标题，所有数字和结果都必须能在正文找到证据。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

Python；脚本评分是表达检查，不能预测推荐量或替代正文证据核对。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [title_workflow.py](scripts/title_workflow.py)：先运行 `python scripts/title_workflow.py --help` 查看参数。

## 参考资料

- [references/content-types.md ](references/content-types.md)
- [references/empirical-signals.md ](references/empirical-signals.md)
- [references/heat-research.md ](references/heat-research.md)
- [references/legacy-gzh-title-strategist.md ](references/legacy-gzh-title-strategist.md)
- [references/title-mechanics.md ](references/title-mechanics.md)
- [references/wechat-recommendation-dissector.md ](references/wechat-recommendation-dissector.md)
- [references/wechat-title-workflow.md ](references/wechat-title-workflow.md)
- [references/workflow-title-scoring-rubric.md ](references/workflow-title-scoring-rubric.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。

脚本输出是模板候选，默认不补写作者亲历、附件或固定成果数量；候选仍需结合正文事实人工核对。
