# 自然中文写作与改稿

按现实与虚构边界组织中文长文、教程、故事和口播，并提供语体与重复表达检查。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $human-writing。根据这些材料写一篇自然中文文章，保留具体动作和事实，材料不足时缩小题目，不虚构亲历。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

Python；风格检查仅覆盖明确的规则，不证明事实正确。默认风格可由用户当前文体要求覆盖。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 随包脚本

- [check_prose.py](scripts/check_prose.py)：先运行 `python scripts/check_prose.py --help` 查看参数。

## 参考资料

- [references/fiction.md ](references/fiction.md)
- [references/formats.md ](references/formats.md)
- [references/forum-prose.md ](references/forum-prose.md)
- [references/reality.md ](references/reality.md)
- [references/revision.md ](references/revision.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
