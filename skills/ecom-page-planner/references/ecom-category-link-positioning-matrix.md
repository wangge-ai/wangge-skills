---
name: ecom-category-link-positioning-matrix
description: 当用户已经有类目竞品市场、关键词和可选用户反馈证据，希望规划多条商品链接的搜索入口、卖点分工、主图任务、详情页任务和微详情任务时使用。
---

# 类目多链接营销定位矩阵

所有新文件只能写入当前 Job 目录。只读取任务已经固定的项目级 EvidencePack，不自行联网、浏览、登录、发布或补采。

## 执行前支持文件漂移门禁

每次正式执行都必须先完成本门禁。在读取或使用这三个支持文件之前，只定位文件并对原始字节计算 SHA-256，与下列值逐项比较：

- `agents/openai.yaml`: `3f07e940375e0172545a6842fea8c0923342451c721dac43f5e880c9f0dbf422`
- [category-output-contract.md](category-output-contract.md): `ca55e074c8d4d2f3ee5ac7a2cb2cdec9ec29796c738013ea60f96d48f7f60a8c`
- [validate_output.py](../scripts/validate_output.py): `a0d88fc80d3d7fd4d8b364696d53e924af92471b1e0cc5e485819bf6181b69f3`

任一文件缺失或哈希不同，立即停止正式执行；不得读取或使用这三个支持文件中的任何一个，不得生成正式交付，只报告支持文件漂移并等待重新审阅。三项全部一致后才可继续。

## 输入合同

- required: `competitor_market`, scope `project`
- required: `keywords`, scope `project`
- optional: `voc`, scope `project`
- produces: []
- writeScope: job_only
- required validator input: 单独固定的 evidence-item index，包含与上述 Pack 身份完全一致的 `pack_id`、`pack_type`、`version`、`scope` 和显式 `item_ids`

先核对输出中的 Pack ID、版本、范围与独立索引完全一致，再核对每个原始 `pack_id:item_id` 引用及其两侧组成部分均无首尾空白、只含一个冒号，且条目确实存在并归属于该 Pack。仅当 `competitor_market` 或 `keywords` 至少缺少一类时才返回 `needs_input`；此时 `rows` 必须为空，顶层 `held_claims` 和 `missing_evidence` 必须都非空。任一 required Pack 缺失而状态不是 `needs_input`，或 required Pack 齐全却使用 `needs_input`，均拒绝。缺少 `voc` 时可以生成受限版本，但必须返回 `partial`，并让顶层及每行的 `held_claims`、`missing_evidence` 都非空。

## 执行步骤

1. 从 `competitor_market` 识别可见类目结构、样本边界、竞争表达和价格信息，不外推全市场。
2. 从 `keywords` 识别人群、场景、功能、款式或材质入口；没有搜索量时不写搜索量或流量等级。
3. 仅在 `voc` 存在时归纳真实用户问题、购买阻力和期望结果；每条结论保留索引中存在且归属正确的 EvidenceItem 引用。
4. 建立不重复的链接定位行。行数由证据决定，不固定为 30。
5. 为每行定义标题方向、差异化、主副文案、构图任务、主图定位、详情页任务和五项微详情任务。
6. 把功效、检测、专利、认证、材质、安全、适用人群和量化效果等未验证内容放入 `held_claims`，不得写成事实。
7. 按 [category-output-contract.md](category-output-contract.md) 输出 `类目多链接营销定位矩阵.md`、`category-link-positioning-matrix.json` 和 `补证与待核实宣称清单.md`，并用 [validate_output.py](../scripts/validate_output.py) `--input <JSON> --evidence-index <固定索引>` 校验 JSON。

## 质量门禁

- 每个正式策略行至少有一个 `competitor_market` 条目和一个 `keywords` 条目；若声明 `voc`，每行还必须有一个 `voc` 条目。
- `evidence_refs` 的原始字符串、`pack_id` 和 `item_id` 均不得带首尾空白，且引用必须正好使用一个冒号。
- 同一搜索入口和同一定位不得机械复制成多行。
- `红海`、`蓝海`、`高转化`、`高复购` 等判断必须有输入证据；否则使用中性分组或 `evidence_insufficient`。
- 链接 ID、图片 ID、价格、销量、占比、搜索量和竞争等级不得补造。
- `success` 的顶层和每行都不得包含 `held_claims` 或 `missing_evidence`；缺少可选 VOC 时只能是 `partial`。

## 边界

- 禁止网络、浏览器、登录、外部 API、外部模型或生成服务、发布、消息和店铺后台写入。
- 不生成图片、视频、页面或工作簿。
- 不把营销策划注册成 EvidencePack。
- 不读取当前任务明确提供范围以外的本地文件。
