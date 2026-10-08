# Feishu Publishing

Use the `lark-doc` capability or `lark-cli docs` with user identity. Writing requires the user's authorization at the time of publication.

## New Group

1. Validate both local reports first.
2. Create two private documents, one for the internal report and one for Q&A.
3. Fetch each document outline and confirm expected headings.
4. Save document IDs, URLs, revisions, source fingerprint, and `latest_processed_at` in a state file outside the Skill.
5. Add navigation links only when the user requests an entry page.

Do not make documents public automatically.

## Existing Group

1. Read the current outline and revision for both document IDs.
2. Confirm the next internal section number and Q&A number.
3. Append the dated internal increment and Q&A increment using the latest revision.
4. Re-fetch the inserted headings and last Q&A item.
5. Advance the cutoff only after both writes verify successfully.

Never create replacement documents merely because authorization expired or a write failed. Refresh authorization and resume against the saved IDs.

## Suggested State File

Keep one JSON file per group outside the Skill:

```json
{
  "group_name": "示例群",
  "source": "path/to/export.json",
  "latest_processed_at": "2026-01-31 18:00:00",
  "cumulative_messages": 1200,
  "internal_doc": {
    "id": "document-token",
    "url": "https://.../docx/...",
    "revision": 2,
    "last_section": 4
  },
  "qa_doc": {
    "id": "document-token",
    "url": "https://.../docx/...",
    "revision": 2,
    "last_question": 18
  },
  "media_boundary": "2 voice records, 0 voice files"
}
```

Do not put credentials, access tokens, raw chats, or private media into the Skill or state file.

## Verification

A successful CLI response is not enough. Fetch by outline or a unique keyword and confirm:

- internal section title exists;
- first and last new Q&A numbers exist;
- content belongs to the correct group;
- document revisions are recorded from the verified fetch;
- no duplicate section was created.
