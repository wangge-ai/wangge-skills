# 旺哥 Skills

> 来自真实业务现场的 AI Skills：电商、数据分析、内容生产与自动化。

这里是旺哥开源 Skill 生态的总索引。目标不是堆放提示词，而是把经过实战、能够复用、边界清楚的工作方法整理成标准 `SKILL.md`。

## 项目结构

首批可公开的 Skill 直接收录在本仓库的 [`skills/`](skills/) 目录中，并通过 [`skills.json`](skills.json) 提供机器可读索引。后续某个 Skill 需要独立版本、发布节奏或 Issue 管理时，再拆为独立仓库。

## 首批开源项目

- [github-repo-dissector](skills/github-repo-dissector)：拆解 GitHub 仓库的定位、架构、维护状态、使用成本与落地方式。
- [github-content-radar](skills/github-content-radar)：发现、去重和筛选值得实测、分享或写成公众号文章的 GitHub 项目。
- [ecom-main-image-diagnosis](skills/ecom-main-image-diagnosis)：诊断电商主图、搜索结果卡和广告素材中的视觉问题。
- [frontend-design-system](skills/frontend-design-system)：为网页、报告和工作台提供主题优先的设计与视觉验收方法。
- [rpa-flow-architect](skills/rpa-flow-architect)：从业务目标、界面证据和运行日志出发设计、审计与验收 RPA 流程。
- [ecom-market-insight-table](skills/ecom-market-insight-table)：把商品列表表格转成可追溯的市场洞察与测试建议。
- [ecommerce-competitor-analyzer](skills/ecommerce-competitor-analyzer)：基于商品链接、表格和截图完成竞品分析与证据化报告。

以上 7 个目录已经包含可阅读、可安装的 `SKILL.md` 及必要脚本和参考资料。

## 文章配套资料包

[飞书 Skill 资料库](https://my.feishu.cn/wiki/DJMRwTyK2ifkkmk5FHPcZeP3nwc?table=tbl1SvuqTb3Vmeq4&view=vew95iuRuH) 当前收录 24 个文章配套资料包，包括 Skill、工作流、教程、课件和素材。每项资料的公开状态和处置说明见 [文章资料包公开目录](catalog/article-packs.md)。

飞书里的历史压缩包是文章发布时的分享快照；GitHub 优先发布经过源码去重、许可证确认、隐私检查和跨 Agent 适配的当前版本。压缩包、安装程序、平台截图和来源不明的第三方内容不会直接进入公开仓库。

## 使用方式

每个正式发布的 Skill 都在 `skills.json` 中记录目录、分类和用途。克隆本仓库后，把需要的 `skills/<skill-name>/` 目录复制到 Agent 的 Skills 目录即可；也可以直接阅读各目录中的说明。

macOS / Linux：

```bash
git clone https://github.com/wangge-ai/wangge-skills.git
cp -R wangge-skills/skills/<skill-name> ~/.agents/skills/<skill-name>
```

Windows PowerShell：

```powershell
git clone https://github.com/wangge-ai/wangge-skills.git
Copy-Item -Recurse wangge-skills/skills/<skill-name> "$HOME/.agents/skills/<skill-name>"
```

脚本需要 Python 3.10 或更高版本，除 XLSX 读取外均只使用 Python 标准库。`ecom-market-insight-table` 读取 XLSX 时按其 README 安装可选依赖 `openpyxl`；CSV 路径无需第三方包。

## 安全与贡献

- 安全问题与披露方式见 [SECURITY.md](SECURITY.md)。
- 提交 Skill、脚本或参考资料前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 正式公开或发布版本前按 [轻量发布检查表](docs/release-checklist.md) 复核。
- 最近一次公开发布检查见 [2026-09-03 审计记录](docs/audits/2026-09-03-public-release-audit.md)。

## 关注旺哥

- [旺哥 AI 电商实战群](https://t2vq6a99kv.feishuapp.com/app/app_17a7exe7wzv/)
- [飞书 Skill 资料库](https://my.feishu.cn/wiki/DJMRwTyK2ifkkmk5FHPcZeP3nwc?table=tbl1SvuqTb3Vmeq4&view=vew95iuRuH)
- [GitHub 组织：wangge-ai](https://github.com/wangge-ai)

## 开源协议

本仓库及 `skills/` 下未另行声明的原创内容采用 [MIT License](LICENSE)。独立仓库或明确标注的第三方衍生内容以其各自许可证为准。
