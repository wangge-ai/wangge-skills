# Evidence and Control-Flow Reconstruction

Use this reference when diagnosing an existing RPA flow from requirements, screenshots, exported definitions, logs, state, or output artifacts.

## Grade the evidence

Assign the highest grade actually supported. Treat grades as cumulative; do not promote a conclusion merely because more files were supplied.

| Grade | Available evidence | Allowed output | Required restraint |
|---|---|---|---|
| E0 | Requirement or verbal description only | Propose a platform-neutral topology, state contract, risk hypotheses, and acceptance matrix | Mark all current-flow claims `待核对`; do not invent nodes, variables, selectors, or platform fields |
| E1 | Flow overview or long screenshot | Reconstruct visible nesting, major branches, loops, subflows, and obvious scope risks | Treat collapsed regions and off-screen connections as unknown |
| E2 | Node configuration, error-handling views, or machine-readable flow export | Give field-level or node-level changes and verify variable/output contracts | Distinguish visible settings from defaults not shown |
| E3 | Runtime logs plus state/output evidence | Judge observed paths, retry/skip behavior, and acceptance outcomes | Do not generalize one successful run to unobserved failure branches |

Downgrade confidence when sources conflict. Prefer the current editor or current machine-readable flow over old screenshots and narrative notes. Prefer runtime evidence for what executed, but use configuration evidence to explain why.

## Label every material claim

Use exactly one evidence label:

- `已确认`: directly visible in current configuration, export, log, state, or output evidence.
- `推断`: the evidence supports the claim, but an unseen setting or branch could change it.
- `待核对`: the evidence is absent, cropped, stale, contradictory, or illegible.

Attach the source briefly, for example `已确认（运行日志）`. Never convert `推断` into `已确认` through repetition. State what single artifact would resolve each important `待核对` item.

## Reconstruct control flow from screenshots

1. Identify the outermost visible container before interpreting individual nodes.
2. Read indentation and connector lines as scope evidence; ignore displayed line numbers as stable identifiers.
3. Record each container in order: sequence, loop, branch, try/catch, subflow, or human-interaction block.
4. Pair every `Else`, `End IF`, and loop-end marker with its nearest compatible opener at the same indentation.
5. Mark collapsed blocks as opaque subtrees with their displayed node count; do not infer their contents.
6. For stitched or long screenshots, use overlapping node names to join segments. Flag any gap without overlap.
7. Track control-transfer nodes explicitly: continue item, break loop, return/exit subflow, terminate run, throw, and ignored exception.
8. Determine the scope affected by each transfer from its parent container, not from its label alone.
9. Track resource lifecycle separately: page/session creation, reassignment, close, and cleanup on every exit.
10. Track state lifecycle separately: claim/start, terminal commit, retryable failure, and any path that can leave an in-progress state.

Normalize the result before recommending changes:

```text
Trigger
└─ task-plan loop
   └─ bounded retry loop
      └─ work-item loop
         ├─ idempotency gate
         ├─ UI subflow
         ├─ terminal or retryable state commit
         └─ resource cleanup
```

Use this tree only as a comparison model. Preserve a different existing structure when it already satisfies the contracts.

## Audit scope and exits

Build a compact scope table for every consequential branch:

| Path or condition | State written | Page/session closed | Transfer action | Effective destination | Evidence label |
|---|---|---|---|---|---|

Check especially:

- A technical failure must not remain indefinitely in an in-progress state.
- A business-empty result must not be conflated with a technical failure.
- A recoverable item failure must return to the intended item loop, not terminate the full run.
- A foundational planning/configuration failure should fail closed, not continue with a partial task list.
- Cleanup must run on success, business-empty, retryable failure, fatal failure, and timeout paths.
- Retry delay must occur after terminal-item skip and immediately before a real retry.

## Produce an evidence-led diagnosis

Return these sections in order:

1. `证据等级`: state E0-E3 and list supplied artifacts.
2. `控制流重建`: show the visible tree and opaque/unknown regions.
3. `事实台账`: separate `已确认`, `推断`, and `待核对`.
4. `作用域风险`: identify wrong-loop, wrong-branch, wrong-return, and leaked-resource risks.
5. `最小下一证据`: request only the screenshot or artifact needed to resolve the highest-risk unknown.
6. `建议边界`: provide architecture-level advice at E0-E1; provide executable node changes only at E2; give an acceptance verdict only for E3-observed paths.

Do not expose credentials, account identifiers, personal data, or business-sensitive values. Replace them with roles, anonymous sequence numbers, or hashes already designed for that purpose.
