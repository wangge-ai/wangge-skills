---
name: ecom-market-insight-table
description: Use when 用户提供电商商品列表 Excel、CSV 或表格导出，需要判断市场进入机会、类目结构、价格带、标题词根、店铺集中度、卖点同质化和第一步测试动作；公开分享版只分析已提供的表格，不自行抓取平台。
---

# 电商市场洞察表

## 核心原则

把用户提供的商品列表转成运营可执行的市场判断。先确认字段、样本范围和缺失情况，再谈价格带、竞争密度和机会；不能把一份有限样本写成全市场结论。

## 能做什么

- 清洗 Excel、CSV 或结构化表格中的商品、价格、销量、店铺、标题、卖点和排名字段。
- 统计价格带结构、店铺或品牌集中度、标题词根、卖点饱和度和异常值。
- 判断拥挤区域、可验证的细分机会、风险和首轮测试动作。
- 生成结构化 Markdown 数据画像，并可渲染为 HTML 洞察报告。

## 输入要求

优先提供商品链接、标题、价格、销量或评价量、店铺、平台、采集时间和排序规则。字段不足时，先按 `references/input-and-evidence.md` 标记“可分析、有限分析、无法分析”，不要补造缺失数据。

## 确定性工具

先运行 10 秒事实层脚本：

```powershell
python scripts/profile_market_table.py --input "<商品表.xlsx或csv>" --out-dir "<输出目录>" --category "<品类>" --source-note "<平台、采集时间、关键词和排序口径>"
```

任务资料中已经给出品类、平台、采集时间、关键词或排序口径时，必须传入 `--category` 和 `--source-note`；不要让报告在已有上下文时仍显示“未填写”。

脚本固定生成：

- `market_table_profile.json`：兼容的基础统计画像。
- `market_table_profile.md`：便于人工检查的统计摘要。
- `market_facts.json`：事实层正式契约，包含字段覆盖率、广告和重复项、标题短语、代表样本及稳定的 `FACT_*` 证据编号。

事实层完成后即可先渲染可核对页面：

```powershell
python scripts/render_market_html_report.py --profile "<market_table_profile.json>" --facts "<market_facts.json>" --out "<market-facts.html>"
```

运营决策层必须严格符合 `references/market-decision.schema.json`，输出为 `market_decision.json`。每个结论、机会、定位、实验动作、风险和限制都必须引用事实层已经存在的证据编号；不得引用不存在的证据，不得补造表外行业数据。决策生成阶段不得调用工具、文件、命令或浏览器。

完整报告仍由同一个官方渲染器生成：

```powershell
python scripts/render_market_html_report.py --profile "<market_table_profile.json>" --facts "<market_facts.json>" --decision "<market_decision.json>" --out "<market-insight-report.html>"
```

当 `analysis-report-orchestrator` 已完成任务卡、资料审计、模型选择和正式正文时，仍使用同一官方渲染器，并额外传入结构化编排报告：

```powershell
python scripts/render_market_html_report.py `
  --profile "<market_table_profile.json>" `
  --facts "<market_facts.json>" `
  --decision "<market_decision.json>" `
  --analysis-report "<analysis-report.json>" `
  --markdown-out "<analysis-report.md>" `
  --out "<market-insight-report.html>"
```

`--analysis-report` 模式将第一阶段四个固定章节、第二阶段正式报告和既有确定性证据附录合并进同一 HTML；`--markdown-out` 生成供编排器结构校验的 Markdown。不要把 Markdown 或 HTML 作为第二套手工事实源。

HTML 由确定性脚本完整生成。不要手工修改生成后的 HTML；需要调整内容时先修正画像输入或参数，再重新渲染，避免重复 patch 产生不一致和额外耗时。

最终 HTML 必须由 `scripts/render_market_html_report.py` 生成。不得新建替代渲染脚本，也不得用 Python、JavaScript 或其他方式重新实现另一套 HTML。常规报告交付不创建浏览器用户数据目录；如确需截图，完成前必须清理临时目录，成品目录只保留截图，不得残留浏览器用户配置。

本地表格洞察任务只读取用户给定文件，不启动浏览器，也不创建、导入或选择浏览器配置。

本 Skill 不自带 Kimi WebBridge，也不负责登录平台采集。输入表可以来自平台导出、合规插件、内部数据或人工整理，但报告必须写明来源、采集时间和样本量。

## 工作台统一事实与报告

从工作台分析本地 CSV、JSON 或表格时：

- 不得由模型手工计算汇总数字；样本数、广告/自然/未知分母、价格带和价格统计只从确定性事实文件读取。
- 工作台确定性质量门负责检查必填字段、重复样本、无效价格和证据引用，并生成统一 Markdown/HTML；脚本或模型正文中的旧统计不得覆盖。
- 模型只补充绑定现有证据编号的定性判断，不在备注中写平台总数、中位价或价格带。
- 公开报告不得出现内部工具名称、调试过程或模型思索过程。

本地表格不要求实时采集的 `collection_evidence_manifest.json` 或登录预检；只有实时平台采集任务才使用原始页面证据合同。

## 分析流程

1. 检查编码、表头、重复行、空值、货币单位、销量口径和时间范围。
2. 生成字段覆盖率和样本画像，区分展示价、活动价、SKU 价和到手价。
3. 按 `references/analysis-playbook.md` 分析价格、店铺、词根和卖点结构。
4. 将结论分为“表内事实、基于样本的推断、仍需验证”。
5. 按 `references/output-contract.md` 输出机会、风险、证据和下一步测试。

## 不能做什么

- 不从表格之外推断实时全网销量、市场份额、搜索量或转化率。
- 不把排序位置直接等同于官方榜单排名。
- 不混淆标价、券后价、SKU 价和结算价。
- 样本量或字段不足时，不给出确定性的入场承诺。
