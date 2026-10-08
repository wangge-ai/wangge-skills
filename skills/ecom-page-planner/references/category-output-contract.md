# 输出合同

本 Skill 的结果是营销策划交付，不是 EvidencePack，也不改变任何输入 Pack。

## 文件

所有文件只能写入当前 Job 目录：

1. `类目多链接营销定位矩阵.md`
2. `category-link-positioning-matrix.json`
3. `补证与待核实宣称清单.md`

不生成图片、视频、页面或工作簿。

## JSON 顶层字段

只允许以下字段：

- `schema_version`: 固定为 `1`
- `category`: 非空类目名称
- `business_status`: `success`、`partial` 或 `needs_input`
- `evidence_pack_refs`: 输入 Pack 引用数组
- `rows`: 正式定位行数组
- `held_claims`: 全局待核实声明
- `missing_evidence`: 全局证据缺口

每个 Pack 引用只包含 `pack_id`、`pack_type`、`version`、`scope`。`pack_type` 仅允许 `competitor_market`、`keywords`、`voc`，`scope` 固定为 `project`。

## 独立证据条目索引

正式校验还必须读取一份单独固定的 evidence-item index。顶层键必须正好是 `schema_version` 和 `evidence_packs`；`schema_version` 固定为 `1`。每个 `evidence_packs` 条目必须正好包含：

- `pack_id`
- `pack_type`
- `version`
- `scope`
- `item_ids`

索引中的 Pack 集合必须与输出 `evidence_pack_refs` 完全一致，四个身份字段必须逐项相同。Pack ID 不得重复；每个 `item_ids` 必须是非空字符串数组，条目 ID 在整个索引内必须唯一。不存在的条目、属于其他 Pack 的条目、格式错误的 `pack_id:item_id` 均拒绝。引用原始字符串、原始 `pack_id` 和原始 `item_id` 必须分别等于各自的 `strip()` 结果，不得用首尾空白填充；每个引用必须正好包含一个冒号。

## 定位行字段

每行只允许：

- `position_id`
- `segment`
- `title_direction`
- `keyword_roots`
- `user_problem`
- `desired_outcome`
- `differentiation`
- `main_copy`
- `secondary_copy`
- `composition_task`
- `main_image_positioning`
- `detail_page_tasks`
- `micro_detail_tasks`
- `evidence_refs`
- `held_claims`
- `missing_evidence`

`micro_detail_tasks` 必须正好包含五项任务。`evidence_refs` 使用严格、无填充空白且正好一个冒号的 `pack_id:item_id` 形式，且每个 `pack_id` 必须在顶层 `evidence_pack_refs` 和独立索引中声明。每个正式行至少引用一个 `competitor_market` 条目和一个 `keywords` 条目；若声明 `voc`，每行还必须引用一个 `voc` 条目。

## 状态规则

- `needs_input` 当且仅当缺少 `competitor_market` 或 `keywords` 至少一类；此时 `rows` 必须为空，顶层 `held_claims` 和 `missing_evidence` 必须都非空。
- 缺少任一必需 Pack 却使用非 `needs_input` 状态，或必需 Pack 齐全却使用 `needs_input`，均拒绝。
- 必需 Pack 齐全但缺少 `voc`: `partial`，顶层和每行的 `held_claims`、`missing_evidence` 都必须非空。
- 三类 Pack 齐全且所有行通过门禁: 可以是 `success`。
- `success` 的顶层和每行都不得包含 `held_claims` 或 `missing_evidence`。

## Markdown 顺序

1. 业务状态与证据范围
2. 输入 Pack 清单
3. 多链接定位矩阵
4. 链接间分工与去重说明
5. 待核实声明
6. 缺失证据与下一步

## 合规示例

```json
{
  "schema_version": 1,
  "category": "示例类目",
  "business_status": "success",
  "evidence_pack_refs": [
    {"pack_id": "market-pack", "pack_type": "competitor_market", "version": 1, "scope": "project"},
    {"pack_id": "keyword-pack", "pack_type": "keywords", "version": 1, "scope": "project"},
    {"pack_id": "voc-pack", "pack_type": "voc", "version": 1, "scope": "project"}
  ],
  "rows": [
    {
      "position_id": "P01",
      "segment": "功能入口",
      "title_direction": "示例类目核心功能",
      "keyword_roots": ["核心功能"],
      "user_problem": "来源于 VOC 条目的问题",
      "desired_outcome": "来源于 VOC 条目的期望",
      "differentiation": "只描述证据支持的差异",
      "main_copy": "证据支持的短句",
      "secondary_copy": "补充适用边界",
      "composition_task": "展示产品与证据对应细节",
      "main_image_positioning": "搜索入口与首屏表达任务",
      "detail_page_tasks": ["解释问题", "展示证据", "说明边界"],
      "micro_detail_tasks": ["核心功能", "证据细节", "使用场景", "规格说明", "转化补充"],
      "evidence_refs": ["market-pack:item-1", "keyword-pack:item-2", "voc-pack:item-3"],
      "held_claims": [],
      "missing_evidence": []
    }
  ],
  "held_claims": [],
  "missing_evidence": []
}
```

交付前必须运行：

```powershell
python scripts/validate_output.py --input category-link-positioning-matrix.json --evidence-index evidence-items.json
```
