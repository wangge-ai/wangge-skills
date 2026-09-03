# 旺哥 Skills

> 来自真实业务现场的 AI Skills：电商、数据分析、内容生产与自动化。

这里是旺哥开源 Skill 生态的总索引。目标不是堆放提示词，而是把经过实战、能够复用、边界清楚的工作方法整理成标准 `SKILL.md`。

## 项目结构

生态采用两层结构：

- 成熟、完整、需要独立迭代的旗舰 Skill，使用单独的 GitHub 仓库。
- 轻量 Skill 与配套工作流收录在本仓库，并通过 [`skills.json`](skills.json) 提供机器可读索引。

## 首批开源项目

- [github-repo-dissector](https://github.com/wangge-ai/github-repo-dissector)：拆解 GitHub 仓库的定位、架构、维护状态、使用成本与落地方式。
- [ecom-main-image-diagnosis](https://github.com/wangge-ai/ecom-main-image-diagnosis)：诊断电商主图、搜索结果卡和广告素材中的视觉问题。
- [rpa-flow-architect](https://github.com/wangge-ai/rpa-flow-architect)：从业务目标、界面证据和运行日志出发设计、审计与验收 RPA 流程。
- [ecom-market-insight-table](https://github.com/wangge-ai/ecom-market-insight-table)：把商品列表表格转成可追溯的市场洞察与测试建议。
- [ecommerce-competitor-analyzer](https://github.com/wangge-ai/ecommerce-competitor-analyzer)：基于商品链接、表格和截图完成竞品分析与证据化报告。

当前飞书分享库中的内容正在逐项做源码去重、许可证确认、隐私检查和跨 Agent 适配。压缩包、安装程序、平台截图和来源不明的第三方内容不会直接进入公开仓库。

## 使用方式

每个正式发布的 Skill 都会在 `skills.json` 中记录仓库、目录、分类、依赖和安装方式。首批条目发布后，可以按对应仓库的说明安装到 Claude Code、Codex、WorkBuddy 或其他支持 `SKILL.md` 的 Agent 环境。

## 关注旺哥

- [旺哥 AI 电商实战群 / 飞书入口](https://t2vq6a99kv.feishuapp.com/app/app_17a7exe7wzv/)
- [GitHub 组织：wangge-ai](https://github.com/wangge-ai)

## 开源协议

本仓库自身的原创内容采用 [MIT License](LICENSE)。独立 Skill 仓库及第三方衍生内容以各自仓库中的许可证为准。
