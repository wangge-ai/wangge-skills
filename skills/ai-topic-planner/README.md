# AI 热点选题

从热点来源发现、去重并核验事件，按实际价值、证据与制作成本生成选题简报。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $ai-topic-planner。从这些近期 AI 新闻链接筛选适合实操教程的选题，核验事件日期及一手来源并指出证据缺口。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

需要网络检索或用户提供的来源；AIHot 为可选外部来源，接口和能力以使用时核验为准。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 参考资料

- [references/aihot-source.md ](references/aihot-source.md)
- [references/topic-planning.md ](references/topic-planning.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
