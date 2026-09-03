# Screenshot-Guided Node Changes

Use this reference when the RPA editor is the only source of truth and changes must be performed by the user through screenshots.

## Request the minimum evidence

Ask for only what unlocks the next decision:

1. Request one overview showing the target node, its parent container, indentation, and nearby branch/end markers.
2. Request the target node's main configuration view.
3. Request its error-handling view only when failure behavior or default outputs matter.
4. Request advanced settings only when selectors, retry, timeout, input method, or execution context is relevant.
5. Request a short runtime log around the node only when validating execution or diagnosing a failure.

For a long flow, request one expanded vertical screenshot with readable node names and nesting. If text becomes unreadable, request overlapping segments instead. Require at least one repeated anchor node between adjacent segments.

Never request an account dictionary, password field contents, tokens, cookies, full customer data, or an unredacted business report. Ask the user to crop or mask sensitive values while preserving node names, variable names, indentation, status, and error codes.

## Locate without guessing

Identify a node with this tuple:

```text
flow/subflow + parent container + branch + node name + nearest preceding/following anchor
```

Do not use a line number as the primary locator; edits can renumber the flow. Do not infer a current node from a stale screenshot. If the parent scope or branch is not visible, request a wider view before instructing a move or insertion.

## Issue one node-change card

Give exactly one small change before asking for confirmation. Use this format:

```text
目标：<one observable behavior>
位置：<flow + parent + branch + anchor>
操作：<add/edit/move/disable exactly one node>
主设置：<field = value or platform-neutral intent>
输出：<variable names and expected types, if any>
错误处理：<policy and explicit fallback outputs, if needed>
保持不变：<nearby verified nodes/contracts>
回传：<the one or two screenshots required for verification>
```

Keep expressions on one line when the editor truncates multiline input. Quote literal strings explicitly and distinguish them from expressions. Do not invent a platform field; describe the required behavior and ask for the relevant settings view when the UI is unknown.

Split structural work into separate cards. For example: create loop, verify loop, move one existing block, verify nesting, then edit the loop item reference. Never combine a new container, a mass move, variable rewrites, and error-policy changes into one instruction.

## Verify before advancing

Check the returned screenshot against all applicable items:

- The node name and action match the card.
- The node is inside the intended parent, loop, and branch.
- The nearest start/end markers prove the intended scope.
- Inputs use the intended literals, expressions, and variable types.
- Output variable names are exact and do not shadow unrelated variables.
- Timeout, retry count, and wait placement match the behavior being designed.
- Error handling is visible when required; fallback outputs have the intended types.
- Continue, return, exit, break, or terminate affects the intended scope.
- Cleanup follows state marking and occurs before leaving the item subflow.
- Nearby verified nodes remain unchanged.
- No sensitive value appears in the screenshot or proposed log.

Respond with one of these decisions:

- `通过`: cite the visible evidence and issue the next one-node card.
- `需修正`: identify one mismatch and issue a correction card for the same node.
- `无法核对`: state what is cropped or unreadable and request the smallest additional view.

Do not advance on an ambiguous screenshot.

## Use runtime confirmation deliberately

After completing a coherent branch, request the smallest safe run that exercises it. Define the expected log/state/output before the run. Classify the result:

- `配置已核对`: screenshots confirm settings, but execution is unobserved.
- `路径已运行`: logs confirm that path executed.
- `结果已验收`: logs plus state/output confirm the promised outcome.

Do not call a branch complete after configuration screenshots alone. Do not require a naturally rare event immediately; allow a pending real-world acceptance case while verifying non-occurrence does not break the normal path.

## Preserve a modification ledger

Maintain a short running ledger:

| Step | Node and scope | Change | Screenshot verdict | Runtime verdict | Remaining risk |
|---|---|---|---|---|---|

Record only stable identifiers and sanitized behavior. Use the ledger to create the final handoff, including completed capabilities, pending natural-event tests, non-destructive boundaries, and the exact next node.
