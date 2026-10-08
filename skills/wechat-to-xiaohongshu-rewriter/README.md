# 公众号文章转小红书

筛选长文、收束单一读者任务，制作逐页脚本、3:4 卡片及可上传发布包。

## 开始使用

将本目录完整复制到 Agent 使用的 Skills 目录，然后请求：

> 使用 $wechat-to-xiaohongshu-rewriter。把这篇公众号文章改成小红书笔记，先建立证据地图，再给逐页脚本与发布文案。

详细步骤：[SKILL.md](SKILL.md)。[安装说明](../../README.md#安装)。

## 输入与依赖

文字方案不需脚本依赖；PNG 导出需用户可用的浏览器截图工具，新增位图素材需生图工具；本包不自动发布。

以用户指定的项目目录保存输出。示例中的 `inputs/`、`outputs/` 是可替换位置。包内不附带业务数据、个人账号、客户端安装程序或 API 密钥。

## 参考资料

- [references/conversion-workflow.md ](references/conversion-workflow.md)
- [references/eligibility-and-routing.md ](references/eligibility-and-routing.md)
- [references/real-assets-and-hd.md ](references/real-assets-and-hd.md)
- [references/render-and-qa.md ](references/render-and-qa.md)
- [references/visual-system.md ](references/visual-system.md)

## 来源与验证边界

由维护者本地持续维护的方法整理为公开版本，包含必要脚本、参考资料或模板；已调整本机路径和默认账号名称。独立安装、文件引用、脚本入口及离线样例的验证记录见[扩充检查记录](../../docs/audits/2026-10-08-local-expansion.md)。外部服务、模型输出、真实平台采集和业务效果须在使用环境中实际验证，不能由离线样例推定。

原创方法和脚本采用 [MIT License](LICENSE)。第三方平台、工具、字体及资料仍遵循各自许可和服务条款。
