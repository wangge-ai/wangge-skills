---
name: rpa-flow-architect
description: Diagnose, audit, redesign, and guide implementation of GUI-based RPA workflows from business requirements, key screenshots, full-flow screenshots, run logs, state files, output artifacts, or exported workflow definitions. Use for ShadowBot/影刀, UiBot, Power Automate Desktop, UiPath, and similar tools when reconstructing control flow, identifying failure points, designing state/retry/idempotency logic, handling dynamic elements and downloads, planning schedules and multi-item execution, producing node-by-node modification guidance, defining stable error codes, accepting a run, or writing a handoff. Also use when the user has only an RPA requirement plus a few key screenshots and wants an implementable architecture. Do not use to bypass CAPTCHA, anti-bot, access controls, or platform security mechanisms.
---

# RPA Flow Architect

Treat an RPA as a recoverable state machine around fragile UI operations, not as a long click script. Reconstruct what is known, separate evidence from inference, then produce the smallest safe design, diagnosis, node edit, acceptance decision, or handoff the user currently needs.

## Start Here

1. Read the nearest project instructions and handoff before inspecting or changing anything.
2. Preserve capabilities that the user says are complete or that real evidence already verifies. Do not rebuild them incidentally.
3. Classify the task:
   - **Greenfield**: requirements and a few key screens.
   - **Diagnosis**: an existing flow behaves incorrectly.
   - **Incident**: logs, state, and outputs are primary evidence.
   - **Retrofit**: add batching, idempotency, scheduling, or retry to a working flow.
   - **Acceptance**: decide whether a modified flow meets its contract.
   - **Handoff**: preserve exact progress and the next safe action.
4. Assign the available evidence an E0-E3 level using [evidence-and-control-flow.md](references/evidence-and-control-flow.md).
5. State only the minimum assumptions needed to proceed. Label findings as **confirmed**, **inferred**, or **pending evidence**.
6. Redact credentials, account identifiers, tokens, phone numbers, and business data from examples and logs.

## Choose the Output Mode

Return only the modes useful to the current request.

### Architecture

Use when requirements are sufficient but an existing flow is absent or irrelevant. Produce:

- business task model and task keys;
- control-flow hierarchy;
- variables and configuration boundaries;
- state machine and stable error codes;
- layered retry and cleanup policy;
- file/archive contract;
- implementation order and acceptance matrix.

Never invent the location or exact fields of unseen nodes. A complete target architecture is allowed at E0; a claim about the current editor is not.

### Diagnosis

Use when the user supplies an existing flow, screenshots, or failure evidence. Produce:

- one-sentence outcome;
- reconstructed current topology;
- confirmed facts and bounded inferences;
- problem, evidence, impact, confidence, and root cause;
- already-complete boundaries that must remain untouched;
- minimal modification queue;
- the next smallest evidence request if exact placement is still unknown.

Reconstruct nesting before recommending a node move. Check the real scope of Continue, Exit Loop, Exit Flow, Close Page, subprocess calls, and error handlers.

### One-Node Guidance

Use for fragile visual editors or when the user requests screenshot-by-screenshot guidance. Give exactly one current node modification card:

```text
Location:
Operation: add | modify | move | disable
Node type:
Required parent and neighbors:
Field values:
Error handling:
Reason:
Expected editor appearance:
Screenshot to return:
Rollback:
```

After the screenshot returns, verify indentation, parent/child scope, order, value mode, variable type, output names, and error handling before giving the next card. Follow [screenshot-node-guidance.md](references/screenshot-node-guidance.md).

### Acceptance

Use logs, state, and artifacts together. Report:

- expected and actual counts by status;
- RUN/SKIP/RETRY timeline and pass count;
- unfinished or stale `running` items;
- state-to-artifact mismatches;
- pass, conditional pass, or fail;
- the next smallest corrective or verification action.

Screenshots of the editor alone never prove runtime success. Use [logging-and-acceptance.md](references/logging-and-acceptance.md).

### Handoff

Record current truth rather than retelling the whole history:

- objective and current real state;
- completed and protected boundaries;
- outstanding work in order;
- key files and editor-only components;
- tests and real-run evidence;
- exact next node or command;
- prohibitions, privacy rules, and unresolved decisions.

## Apply the Reliability Invariants

Audit every design and diagnosis against these invariants:

1. Every started item reaches a terminal status or an explicit retryable failure. Never leave `running` indefinitely.
2. `success` is written only after the downloaded artifact is validated and archived to its final path.
3. Every exit path closes or safely relinquishes its page, window, process, lock, and temporary resource.
4. Skipping is based on the same task key and a declared terminal status, not merely on a similarly named file.
5. Retry is bounded and separated into node retry, item retry, and batch replay. Calculate the worst-case attempt count.
6. Credential error, login timeout, CAPTCHA/risk control, page change, no-data, download failure, and archive failure have distinct states or stable error codes.
7. Password or credential failures do not silently become infinite retry; confirm policy before changing their retryability.
8. Task-plan generation sits outside each task's retry and item loops. Each date or business task owns an independent task key and state scope.
9. Business end date and UI query end date remain separate when the target system uses a right-open interval.
10. Foundational configuration or planning errors fail closed; one business-item failure cleans up and returns to its owning loop.
11. Logs identify items with safe sequence numbers or aliases, never credentials or sensitive operating data.
12. CAPTCHA and access-control handling uses only official verification, permitted human intervention, bounded retry, or fail-and-continue. Never design a bypass.

The default topology is:

```text
entry
  -> task-plan generation
  -> task loop
     -> bounded batch-pass loop
        -> business-item loop
           -> should-run / idempotency decision
           -> mark running
           -> UI subprocess
           -> validate and archive artifact
           -> commit terminal or retryable state
           -> cleanup page/resources
  -> reconciliation and acceptance summary
```

Read [state-retry-idempotency.md](references/state-retry-idempotency.md) before changing state, rerun, batch-pass, or date-task logic. Read [ui-auth-downloads.md](references/ui-auth-downloads.md) before changing login, CAPTCHA, waits, selectors, downloads, or page cleanup.

## Use a Minimum State Contract

Projects may extend this table, but they must make deviations explicit.

| Status | Terminal | Default retryable | Required cleanup |
|---|---:|---:|---|
| `success` | yes | no | close page; artifact exists |
| `no_data` | yes | no | close page |
| `running` | no | yes after timeout | recover or replace; never persist forever |
| `captcha_failed` | no | yes, bounded | close page |
| `failed` | policy by error code | policy by error code | close page |
| `credential_failed` | policy decision | no until confirmed | close page |

Use stable codes such as `credential_error`, `login_timeout`, `captcha_failed`, `element_not_found`, `download_timeout`, `archive_failed`, and `state_write_failed`. Keep human messages separate from machine-stable codes.

## Use the Bundled Auditors

Run scripts against copies or sanitized evidence. They are read-only unless an explicit output path is supplied.

- `python scripts/parse_run_log.py <log>` normalizes CSV, JSONL, or text logs and finds item timelines and open RUN events.
- `python scripts/audit_state.py <state.json> [--artifact-root DIR]` finds illegal statuses, stale running items, and state/artifact mismatches.
- `python scripts/validate_rpa_spec.py <spec.json>` statically audits a normalized target design for bounded retry, cleanup, state closure, archive ordering, and security violations.

Treat script output as evidence, not as a substitute for inspecting the relevant flow or business contract.

## Route Platform Details

For ShadowBot/影刀, read [shadowbot-adapter.md](references/shadowbot-adapter.md) before naming nodes or interpreting editor screenshots. Platform versions differ: verify the node's normal tab, error-handling tab, output variables, and visible nesting rather than relying on memory.

For another platform, translate semantics instead of copying ShadowBot labels. The universal questions are: what owns the loop, what is mutated, how failure exits, what is cleaned up, and what evidence commits success.

## Finish with an Evidence-Gated Next Step

End with one of the following:

- a complete architecture plus its assumptions;
- one verified diagnosis and the smallest safe fix;
- one node modification card and the screenshot needed next;
- an acceptance verdict supported by logs, state, and artifacts;
- a handoff that another task can continue without reconstructing history.

Do not claim completion because the diagram looks correct. Claim completion only when the requested design or change exists and its proportional verification has passed.
