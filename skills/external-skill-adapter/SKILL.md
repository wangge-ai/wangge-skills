---
name: external-skill-adapter
description: 把外部 Skill 或提示词包适配到目标 Agent，核对来源、工具、输出和验证边界。
license: MIT
metadata:
  source_pack: '5'
---

# External Skill Adapter

Use this skill to turn an outside skill into a local 目标 Agent skill without copying it blindly. The goal is to preserve the useful job-to-be-done, rewrite the workflow for 目标 Agent, add boundaries, add testable outputs, and leave a shareable package if the user wants to publish the process.

## Adaptation Workflow

1. **Capture the source**
   - Save the source URL, page HTML, README, screenshots, or pasted skill text.
   - Extract only facts needed for adaptation: name, intended users, inputs, outputs, commands, platform scope, dependencies, risks, and missing implementation details.
   - If the source is a webpage, keep a local evidence copy in the project `work/` folder.

2. **Separate intent from implementation**
   - Intent: what work the skill helps users finish.
   - Implementation: command wording, platform claims, dependencies, scripts, and examples.
   - Preserve intent when useful. Rewrite implementation for 目标 Agent, local files, available tools, and the user's workflow.

3. **Decide the 目标 Agent shape**
   - Choose one narrow entrypoint before writing files.
   - Prefer a result-oriented 目标 Agent workflow over broad marketplace claims.
   - Add scripts only for repeated deterministic work, such as CSV normalization, report generation, validation, or packaging.
   - Put longer rubrics, templates, and checklists in `references/`.

4. **Change the skill enough**
   - Do not reuse the source `SKILL.md` structure verbatim.
   - Rename the skill if the new scope is different.
   - Replace generic feature lists with a concrete router, output contract, quality bar, and failure handling.
   - Remove unsupported claims such as real-time monitoring, alerts, platform coverage, scraping, or export formats unless the local skill actually implements them.

5. **Add boundaries**
   - Say what the skill will not do.
   - Avoid credentials, hidden browser profiles, CAPTCHA bypass, private data, or background monitoring unless the user explicitly owns and authorizes that system.
   - Label public-page samples, user-provided exports, screenshots, and estimates honestly.

6. **Create the local skill**
   - Put the skill under `~/.agents/skills/<skill-name>/` unless the user asks for another location.
   - Include `SKILL.md` with 目标 Agent-adapted frontmatter.
   - Include `README.md` with usage instructions.
   - Include only useful `scripts/`, `references/`, or `assets/`.

7. **Test**
   - Validate the skill structure:
     ```bash
     ls -la ~/.agents/skills/<skill-name>/
     cat ~/.agents/skills/<skill-name>/SKILL.md | head -20
     ```
   - Run at least one smoke test with a realistic sample input if the skill includes a script or output format.
   - Record test command, result, and generated artifacts in the share package, not inside `SKILL.md`.

8. **Package for handoff or article**
   - Keep install path, test command, source evidence path, adapted differences, and known limits.
   - For public writing, lead with the result. Put implementation notes, blocked attempts, and regeneration commands in README or handoff files.

## Adaptation Checklist

Read `references/adaptation-checklist.md` when the source skill is vague, overbroad, or likely copied from a marketplace page.

Before calling the adaptation finished, confirm:

- The new skill has a different name or clearly narrower scope.
- The trigger description says when to use it.
- The workflow has input routing, output contract, quality bar, and boundaries.
- Unsupported source claims were removed or downgraded.
- Validation passed.
- At least one realistic test or dry run exists.
- User-facing article material is separate from reusable skill instructions.

## Output Summary Format

When reporting back, use:

```markdown
已适配：
- 新 skill：<path>
- 来源证据：<path or URL>
- 改动重点：<3-5 bullets>
- 测试：<command + pass/fail>
- 分享包：<path, if any>
```


## Common Adaptation Patterns

### Pattern 1: Web Search Skills
- Replace API calls with WebSearch tool usage
- Add fallback instructions when search fails
- Specify topic parameter for better results

### Pattern 2: File Operation Skills
- Map file reads to Read tool
- Map file writes to Write tool
- Add path validation and error handling

### Pattern 3: Code Execution Skills
- Map commands to Bash tool execution
- Add timeout considerations
- Specify working directory requirements

### Pattern 4: Image Processing Skills
- Enable Read tool's image mode capability
- Add image format support documentation
- Specify output format options

## Anti-Patterns to Avoid

- ❌ Copying original SKILL.md without modification
- ❌ Keeping platform-specific paths (e.g., Codex-specific)
- ❌ Removing boundaries and safety checks
- ❌ Adding unsupported capability claims
- ❌ Forgetting to update frontmatter metadata
