# Feishu Base Visualization

Use this route when the user asks for 飞书可视化, 多维表格, Base, a Feishu dashboard, or a workbench that collaborators can filter and update inside Feishu.

## Product Shape

Create one private Base per group. Keep its token in private state outside this Skill. Design it as two layers:

1. **Reader surface at the Base root:** one dashboard and one `今日重点` table. Put the dashboard first. A reader should understand the three to five most important items without opening a helper table or scrolling through analysis metadata.
2. **Internal data layer:** put `匿名证据`, `每日趋势`, `每日主题`, and any helper resources inside one folder named `内部数据（不用看）`. Preserve these resources for traceability and chart calculation, but do not expose them as peer navigation items.

`今日重点` keeps the full analytical schema internally: stable signal ID, title, type, priority, first/latest date, repetition, speaker spread, cross-day persistence, unresolved status, actionability, mechanism, evidence gap, evidence link, and candidate mark. Its default visible columns are limited to:

- `重点`
- `日期`
- `优先级`
- `一句话判断`
- `对你有什么用`
- `下一步`
- `加入输出`

The default view shows only the high-priority items. Keep one unfiltered `全部重点` view and editorial candidate views only when they are actively used. Evidence counts, speaker counts, cross-day counts, raw type labels, mechanisms, gaps, boundaries, hit counts, IDs, and backlink fields are internal by default.

Use a bidirectional link between `匿名证据` and `今日重点`, so a reviewer can still drill down when needed. Evidence references are run-local locators, not durable message IDs.

## Views And Candidate Workflow

Keep the default grid view focused on the three to five high-priority items and retain the visible date field so the user can apply one-day or date-range filters. Put the unfiltered view second. Candidate views may follow. Do not make an unresolved/evidence-oriented view the default reader entry point.

`候选标记` should normally offer `未标记`, `洞察候选`, `Q&A候选`, and `两者`. Candidate marks are editorial state, not approval to publish.

On an incremental update, preserve existing records and user-edited candidate marks. Append new daily/topic rows only for dates not already present. Add or update new signal/evidence records without clearing prior views, fields, links, or dashboard components.

## Dashboard

The dashboard is a decision surface, not a mirror of every available column. Start with one text block containing three current conclusions and one synthesis sentence. Then add at most two compact KPI cards and at most two charts, each answering an explicit reader question.

Recommended defaults:

- `必看重点`: count of high-priority items;
- `日均问题率`: average of `疑问式消息 ÷ 有效消息`;
- `每日讨论热度`: effective messages by date, with partial days labelled;
- `问题率趋势`: question-like share by date.

Do not use a multi-series topic spaghetti chart, raw topic-hit table, evidence-count ranking, generic signal-type pie, unresolved-count card, or repeated-evidence card as the default dashboard. These describe the analysis process more than the reader's decision. If a chart cannot complete the sentence “This chart helps the reader decide ___,” omit it.

Use real table and field names returned by `lark-base`; create dashboard components serially. Arrange a newly created or explicitly redesigned dashboard once after all components exist. Do not recreate a component with the same purpose when updating an existing dashboard, except when replacement is required to fix an immutable component type or malformed text block.

## Privacy

- Create the Base with user identity and keep it private unless the user separately requests sharing.
- Never upload raw chat exports, member lists, platform IDs, contacts, credentials, local paths, or full private quotations.
- Use stable anonymous labels within one run, such as `P01`, and short paraphrased evidence summaries.
- Put uncertainty next to the evidence: self-report, missing media, sparse sample, concentration, or time-sensitive platform fact.
- A link to the private Base may be added to the internal report. Do not place it in a broadly shared Q&A document unless the user requests that access path.

## Existing Versus New Base

Before creation, read the saved group state:

- Saved Base token exists: resolve its tables, views, and dashboard and update in place.
- No saved Base token: create one private Base for that group, then save the token only after records, views, links, and dashboard data verify.
- Authorization fails: do not create a replacement Base. Complete the local workbench and reports, report publication as pending, and resume against the saved token after authorization is restored.

## Verification

Verify observable results, not only command success:

1. The Base root contains the dashboard, `今日重点`, and one internal-data folder; helper tables are inside that folder.
2. The default view exposes no more than seven reader-facing fields and returns only the intended high-priority items.
3. A sampled signal contains its one-sentence judgment, value, action, and candidate state; its hidden backlink still reaches anonymous evidence.
4. Dashboard cards and charts reproduce their selected values and date dimensions. Partial-day caveats are visible.
5. The dashboard contains actual current conclusions, not operating instructions or analysis metadata.
6. The internal report's Base link resolves to the saved Base.
7. Only after the Base and both report updates verify should the private state advance `latest_processed_at`.
