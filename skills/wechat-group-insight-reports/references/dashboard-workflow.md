# Local Insight Dashboard

Use this workflow when the user wants to browse, filter, or review important group-chat information visually. The dashboard is a private local review surface; it does not replace either report and should not be published to Feishu as a public document.

## What The Dashboard Must Support

- Filter by one day or a date range.
- Show daily effective-message, question-like-message, active-speaker, and topic trends.
- List semantically consolidated important signals with an explicit explanation of importance.
- Open one signal to view anonymous evidence items and evidence gaps.
- Mark a signal as an internal-insight candidate, a Q&A candidate, or unselected.

## Build The Insight Index

After inspecting `group_analysis.json` and `evidence_digest.md`, write `insight_index.json`. This is a working interchange format, not a frozen public contract. Prefer 5–20 well-supported signals over a long keyword-derived list.

Each signal should connect repeated evidence to a mechanism or decision:

```json
{
  "insights": [
    {
      "id": "I001",
      "title": "A concise relationship or problem statement",
      "summary": "What changed or why the signal matters",
      "kind": "question",
      "importance": "high",
      "candidate": "none",
      "status": "Partially answered",
      "topics": ["Actual group topic"],
      "dates": ["2026-08-26", "2026-08-28"],
      "importanceFactors": {
        "repeatCount": 12,
        "speakerCount": 7,
        "crossDayCount": 2,
        "unresolved": true,
        "actionability": "high",
        "reason": "Explain why this deserves attention without relying on a hidden score."
      },
      "action": "A concrete next step or deliverable",
      "boundaries": ["A self-report has not been independently verified"],
      "evidenceRefs": ["M001024", "M001166", "M001408"]
    }
  ]
}
```

Allowed `kind` values are `question`, `method`, `case`, `risk`, `resource`, `trend`, and `decision`. Allowed importance values are `high`, `medium`, and `low`.

Use ordinary evidence references emitted by `prepare_group_chat.py`; do not invent references. A signal without evidence may remain only when the missing evidence is itself important, and its boundary must say that it is not yet supported.

Importance is explainable judgment, not a mechanical score. Consider:

- repeated semantically similar signals;
- how many distinct speakers are represented;
- persistence across days;
- whether the question or conflict remains unresolved;
- whether a decision, reusable method, risk, or deliverable follows;
- whether concentrated participation, missing media, self-reporting, or time sensitivity weakens the conclusion.

## Generate The Dashboard

Run:

```bash
python scripts/build_dashboard.py \
  --analysis <run-dir>/group_analysis.json \
  --insights <run-dir>/insight_index.json \
  --output <run-dir>/group_insight_dashboard.html
```

Open the generated HTML locally and verify date filters, both trend charts, signal filters, evidence details, and all three candidate-marking states. Candidate choices are stored in the browser and can be downloaded with **Export candidate marks** as `review_decisions.json`.

Use reviewed candidate marks as editorial input, not as automatic publication approval. The internal report and Q&A still require their own evidence review, privacy validation, and, when requested, Feishu write verification.

## Privacy And Evidence Boundaries

- The builder replaces known member names, platform IDs, phone numbers, email addresses, credential-like strings, and local paths in displayed evidence.
- Speakers are shown as `成员01`, `成员02`, and so on.
- The dashboard remains private because anonymization cannot prove that every free-form personal detail has been removed.
- Do not embed `evidence_digest.md`, member lists, raw chats, credentials, or saved Feishu state into the HTML.
- If voice records exist without files, keep the visible media warning. Do not imply that the voice content was reviewed.
- Keep different groups in separate dashboard files and separate browser review state.
