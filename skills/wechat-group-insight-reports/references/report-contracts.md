# Report Contracts

## Output 1: Internal Reader-Demand Insight Report

Suggested title:

`<群名>｜读者需求洞察报告（内部）`

Required content:

1. **One-page conclusion**: what changed, what matters, and what not to overclaim.
2. **Data scope**: source type, selected time range, selected/effective messages, active speakers, question-like messages, concentration, and media coverage.
3. **Demand structure**: 4–8 demand clusters ranked by evidence strength, not keyword volume alone.
4. **Key insights**: each with signal, context, mechanism, action, confidence, and boundary.
5. **Reader segments**: segment by jobs, constraints, and decision stage; avoid personality stereotypes.
6. **Content/product opportunities**: concrete deliverable, target reader, trigger, and validation metric.
7. **Risks and compliance**: unsupported claims, platform rules, privacy, account permissions, and media gaps.
8. **Update baseline**: exact latest processed timestamp and whether the current export is full or partial.

For incremental updates, append one dated section and preserve previous sections. State both the current increment and the historical cumulative baseline.

Validate section fragments with `validate_reports.py --incremental`; full new documents should keep an H1 title and omit that flag.

## Output 2: High-Frequency Q&A

Suggested title:

`<群名>｜高频问题 Q&A（持续更新）`

Rules:

- Cluster semantically equivalent questions across wording variants.
- Continue existing numbering on updates; never restart at Q1 unless this is a new document.
- Use the actual group's topics. Do not reuse a fixed generic list.
- Keep ordinary member names and raw chat quotations out.
- Answer in this order:
  1. direct conclusion;
  2. practical steps or decision rule;
  3. failure conditions and boundaries;
  4. safe fallback when relevant.
- Separate time-sensitive product facts from stable decision methods.
- Refuse or redirect fake transactions, account trading, bypass, evasion, and unauthorized collection.

## Quality Review

Before delivery, check:

- Does every headline insight explain a relationship or mechanism rather than repeat a topic label?
- Can a reader tell what to do differently?
- Are active-speaker concentration and self-report bias visible?
- Are opportunities measurable rather than generic “make a course/article/tool” suggestions?
- Are missing media and missing business data disclosed?
- Are questions deduplicated and answers distinct?
- Did the report keep facts, inferences, and hypotheses separate?
