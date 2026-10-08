# 旺哥 Skills

来自实际工作资料的 AI Skill：电商、数据分析、内容、研究与协作。

**当前可安装：18 个 Skill。** 2026-10-08 对照飞书资料库补齐 11 个，保留原有 7 个。每个包都包含 `SKILL.md`、README、许可证及 Agent 配置，所需脚本和参考资料随包提供。

[飞书资料库](https://my.feishu.cn/wiki/DJMRwTyK2ifkkmk5FHPcZeP3nwc?table=tbl1SvuqTb3Vmeq4&view=vew95iuRuH)当前有 27 个有编号资料项；全部对应关系与尚未公开原因见[文章资料包目录](catalog/article-packs.md)。资料包包含课件、素材和工具，所以数量与可安装 Skill 数量不同。

## 选择 Skill

| Skill | 用途 |
|---|---|
| [github-repo-dissector](skills/github-repo-dissector) | 拆解 GitHub 仓库的定位、架构、维护状态、使用成本与落地方式。 |
| [github-content-radar](skills/github-content-radar) | 发现、去重和筛选值得实测、分享或写成公众号文章的 GitHub 项目。 |
| [ecom-main-image-diagnosis](skills/ecom-main-image-diagnosis) | 诊断电商主图、搜索结果卡和广告素材中的视觉与点击问题。 |
| [frontend-design-system](skills/frontend-design-system) | 为网页、报告、工作台和多页面产品提供主题优先的设计与视觉验收方法。 |
| [rpa-flow-architect](skills/rpa-flow-architect) | 设计、诊断、改造和验收影刀等 GUI RPA 流程。 |
| [ecom-market-insight-table](skills/ecom-market-insight-table) | 把商品列表表格转成价格带、竞争结构、词根和市场机会洞察。 |
| [ecommerce-competitor-analyzer](skills/ecommerce-competitor-analyzer) | 基于商品链接、表格、截图和评论证据完成竞品分析。 |
| [ecom-image-reverse-sop-share](skills/ecom-image-reverse-sop-share) | 把产品图和竞品图拆成图位任务、购买疑问、画面结构及自家商品提示词。 |
| [external-skill-adapter](skills/external-skill-adapter) | 把外部 Skill 或提示词包适配到目标 Agent，核对来源、工具、输出和验证边界。 |
| [wechat-article-knowledge-pack](skills/wechat-article-knowledge-pack) | 把公众号文章链接或本地导出文件整理为原文档案、元数据和可追溯知识卡。 |
| [beginner-tutorial-writer](skills/beginner-tutorial-writer) | 从产品名与官方资料生成可操作的新手教程，配搜索查询脚本和独立 HTML 渲染脚本。 |
| [full-spectrum-distiller](skills/full-spectrum-distiller) | 按行业、品牌、网站或话题组织来源、竞品、知识地图与机会研究。 |
| [chatlab-analyzer](skills/chatlab-analyzer) | 使用 ChatLab 分析用户已有聊天导出，组织统计、搜索、SQL 和证据报告。 |
| [ecommerce-data-analysis-workflow](skills/ecommerce-data-analysis-workflow) | 从电商导出表和维护表重建明细、重算业务公式、对账并输出报告。 |
| [ecommerce-review-analysis](skills/ecommerce-review-analysis) | 按数据质量、清洗、分类、人群、归因、参照物与报告七步分析评论。 |
| [kolsprite-tiktok-ops](skills/kolsprite-tiktok-ops) | 用已授权的达人精灵 MCP 做视频、商品、店铺与达人研究，输出可追溯运营方案。 |
| [sellersprite-amazon-ops](skills/sellersprite-amazon-ops) | 用卖家精灵 MCP 做机会词扫描、竞品拆解、词库搭建和 Listing 方案。 |
| [feishu-project-weekly-report](skills/feishu-project-weekly-report) | 从群聊、文档和多维表格收集证据，生成周报、跟进表及催办消息草稿。 |

目录与依赖的机器可读版本：[skills.json](skills.json)。每个包的 README 说明来源、安装条件和验证边界。

## 安装

克隆后，把所需目录复制到 Agent 使用的 Skills 目录；以下以 `~/.agents/skills` 为例。不同 Agent 的目录以其设置为准。不要把已有同名目录直接覆盖，升级前保留自己的修改。

macOS / Linux：

```bash
git clone https://github.com/wangge-ai/wangge-skills.git
mkdir -p ~/.agents/skills
cp -R wangge-skills/skills/<skill-name> ~/.agents/skills/<skill-name>
```

Windows PowerShell：

```powershell
git clone https://github.com/wangge-ai/wangge-skills.git
New-Item -ItemType Directory -Force "$HOME/.agents/skills"
Copy-Item -Recurse "wangge-skills/skills/<skill-name>" "$HOME/.agents/skills/<skill-name>"
```

脚本使用 Python 3.10+。CSV 分析和 HTML 渲染无需第三方包；XLSX 读取需 `openpyxl`；教程查询清单需 `PyYAML`。完整报告所用的图表或表格库由 Agent 按实际需要选择，详见各包说明。

## 外部依赖与验证范围

- ChatLab 分析需要另行安装官方 `chatlab-cli`；不附带聊天导出客户端或安装程序。
- 达人精灵、卖家精灵方法需要用户自己的服务账号和 MCP 权限；本仓库提供原创操作方法。
- 飞书周报需要用户已授权的飞书连接器或 CLI，发送消息遵循用户的具体授权。
- 本次完成安装结构、引用、脚本帮助和新增脚本最小样例验证；未复测外部服务的账号流程、模型生成质量或真实业务效果。

## 维护与许可

[CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) · [发布检查表](docs/release-checklist.md) · [本次检查记录](docs/audits/2026-10-08-library-sync.md)

本仓库原创内容采用 [MIT License](LICENSE)。第三方服务遵循各自条款；来源或再发布许可未核清的第三方素材与 Skill 不直接转载。

## 关注旺哥

- [旺哥 AI 电商实战群](https://t2vq6a99kv.feishuapp.com/app/app_17fgnu76fy9/)
- [飞书 Skill 资料库](https://my.feishu.cn/wiki/DJMRwTyK2ifkkmk5FHPcZeP3nwc?table=tbl1SvuqTb3Vmeq4&view=vew95iuRuH)
- [GitHub 组织：wangge-ai](https://github.com/wangge-ai)
