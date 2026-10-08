# Input And Evidence

## Accepted Inputs

`prepare_group_chat.py` accepts:

- `.json`: WeFlow/ChatLab-style objects, nested message lists, or a root message list.
- `.jsonl` / `.ndjson`: one message object per line.
- `.csv`: common time, sender, content, and type columns.
- `.txt` / `.log`: lines such as `[2026-08-31 10:20:30] 张三: 内容` or `2026/08/31 10:20 张三：内容`.

Automatic field aliases cover common names such as:

- time: `timestamp`, `time`, `createTime`, `create_time`, `datetime`, `date`
- sender: `accountName`, `senderName`, `nickname`, `name`, `speaker`, `sender`
- content: `content`, `text`, `message`, `msg`, `body`
- type: `type`, `msgType`, `messageType`, `kind`

For an unknown schema, inspect the first records and normalize them into message dictionaries before analysis. Do not silently discard most rows because field names differ.

## Incremental Cutoff

- New group: omit `--cutoff` or use an epoch value.
- Existing group: use the verified `latest_processed_at` from the saved state.
- Selection is strictly `message_time > cutoff`.
- If the export is a partial time window, preserve the historical cumulative baseline; never replace it with the current file's row count.
- If timestamps are absent, analyze the full file and state that safe incremental selection was impossible.

## Evidence Package

The preparation script writes:

- `group_analysis.json`: counts, ranges, speakers, question candidates, topic retrieval aids, daily message/question/speaker/topic aggregates, media inventory, names, and platform IDs.
- `evidence_digest.md`: human-readable local evidence index.

Question and evidence items receive ordinary run-local references such as `M001024`. Use these references to connect an insight to its supporting messages in the local dashboard. They are evidence locators for the current prepared export, not durable cross-export message IDs.

The digest is private working material. It may contain names and representative chat text for evidence retrieval. Do not upload it as the public/group-facing report.

## Evidence Method

For each important conclusion, retain this chain:

1. **Repeated signal**: repeated questions, a recurring task, or a concrete event.
2. **Context**: who is trying to do what, under which constraint.
3. **Mechanism**: why the problem persists or what trade-off creates it.
4. **Action**: a deliverable, decision rule, experiment, or safe answer.
5. **Boundary**: missing media, self-report, sparse sample, uncertain identity, or time-sensitive fact.

Keyword and topic counts are retrieval aids only. A high count does not prove importance, demand, satisfaction, or causality.

## Media

- Inventory adjacent `media`, `images`, `videos`, `voices`, `files`, and emoji folders.
- If voice records and voice files both exist, transcribe them with an available ASR workflow before drawing voice-dependent conclusions.
- If message records reference media but files are absent, report the gap.
- Do not evaluate images or videos from filenames or placeholders alone.

## Privacy Boundary

Published documents should not contain ordinary member names, WeChat IDs, phone numbers, email addresses, credentials, local filesystem paths, or raw private quotations. Named-expert analysis is an explicit exception that requires the user's request and should remain separate from anonymous Q&A.
