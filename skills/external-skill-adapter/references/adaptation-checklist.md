# External Skill Adaptation Checklist

Use this checklist when adapting a marketplace skill, copied prompt, README, or tool page into a Codex skill.

## Source Reading

- What exact task does the source skill promise to finish?
- What inputs does it expect?
- What outputs does it promise?
- Which claims are only marketing copy?
- Which dependencies or tools are implied but not implemented?
- Which parts could create compliance, privacy, credential, or background-execution risk?

## Codex Redesign

- Make the trigger specific enough for Codex to invoke at the right time.
- Replace broad claims with a narrow workflow Codex can execute.
- Keep platform support conditional on actual data the user provides or public pages that can be inspected.
- Add a local output contract: Markdown, CSV, JSON, HTML, README, screenshots, or report files.
- Add deterministic scripts only where they save repeated work.

## Difference Requirement

The adapted skill should differ from the source in at least three ways:

- narrower or clearer scope
- Codex-specific workflow steps
- explicit boundaries and failure handling
- local scripts or templates
- tested output contract
- share-package or article workflow

## Testing

- Run `quick_validate.py`.
- If scripts exist, run them on a sample file.
- If the skill is workflow-only, run a dry-use pass and check whether another Codex instance would know what to do.
- Save test inputs and outputs outside the skill folder when they are user/project artifacts.

## Article Notes

For WeChat/share articles:

- Lead with the result, not with the tool's internal design.
- Show the adapted skill's output.
- Explain the old pain point in plain words.
- Explain the workflow as "input -> processing -> report/share package".
- Move commands, caveats, and regeneration details to README.
