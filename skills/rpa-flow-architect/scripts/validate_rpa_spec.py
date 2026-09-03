#!/usr/bin/env python3
"""Statically validate a normalized RPA architecture specification.

The JSON contract is intentionally small. Important fields are:

  task_plan.outside_retry_loop: bool
  task_plan.date_interval: "inclusive" | "right_open"
  task_plan.business_end_field / query_end_field: str
  retry.bounded: bool
  retry.node_max / item_max / batch_passes: non-negative integers
  state.terminal / retryable: arrays of statuses
  state.running_timeout_seconds: positive number
  logging.safe_item_id: bool
  security.bypass_controls: false
  security.captcha_policy: "official" | "manual" | "fail_and_continue"
  steps: ordered objects with id, role, type, and on_failure arrays

Recognized roles include should_run, mark_running, ui, archive, mark_success,
mark_failure, close_page, and continue_item. on_failure may contain a role or a
step id. The script does not execute or modify an RPA.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_CAPTCHA_POLICIES = {"official", "manual", "fail_and_continue"}


def validate_spec(spec: Any) -> dict[str, Any]:
    issues: list[dict[str, str]] = []

    def add(code: str, severity: str, message: str) -> None:
        issues.append({"code": code, "severity": severity, "message": message})

    if not isinstance(spec, dict):
        add("root_type", "error", "spec root must be an object")
        return _result(issues)

    task_plan = spec.get("task_plan")
    if not isinstance(task_plan, dict):
        add("missing_task_plan", "error", "task_plan object is required")
        task_plan = {}
    if task_plan.get("outside_retry_loop") is not True:
        add(
            "task_plan_scope",
            "error",
            "task-plan generation must be explicitly outside task retry and item loops",
        )
    if task_plan.get("date_interval") == "right_open":
        if not task_plan.get("business_end_field") or not task_plan.get("query_end_field"):
            add(
                "right_open_dates",
                "error",
                "right-open dates require separate business_end_field and query_end_field",
            )
        elif task_plan.get("business_end_field") == task_plan.get("query_end_field"):
            add(
                "date_field_collision",
                "error",
                "business and query end dates must use distinct fields",
            )

    retry = spec.get("retry")
    if not isinstance(retry, dict):
        add("missing_retry", "error", "retry object is required")
        retry = {}
    if retry.get("bounded") is not True:
        add("unbounded_retry", "error", "retry.bounded must be true")
    for key in ("node_max", "item_max", "batch_passes"):
        value = retry.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            add("invalid_retry_count", "error", f"retry.{key} must be a non-negative integer")
    if isinstance(retry.get("batch_passes"), int) and retry["batch_passes"] > 3:
        add(
            "large_batch_replay",
            "warning",
            "batch_passes above 3 needs an explicit risk and worst-case-attempt review",
        )

    state = spec.get("state")
    if not isinstance(state, dict):
        add("missing_state", "error", "state object is required")
        state = {}
    terminal = _string_set(state.get("terminal"))
    retryable = _string_set(state.get("retryable"))
    if not {"success", "no_data"}.issubset(terminal):
        add("terminal_contract", "error", "state.terminal must include success and no_data")
    if "running" in terminal:
        add("running_terminal", "error", "running cannot be terminal")
    overlap = terminal & retryable
    if overlap:
        add(
            "terminal_retry_overlap",
            "error",
            "terminal and retryable states overlap: " + ", ".join(sorted(overlap)),
        )
    timeout = state.get("running_timeout_seconds")
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0:
        add("running_timeout", "error", "state.running_timeout_seconds must be positive")

    logging = spec.get("logging")
    if not isinstance(logging, dict) or logging.get("safe_item_id") is not True:
        add("unsafe_logging", "error", "logging.safe_item_id must be true")

    security = spec.get("security")
    if not isinstance(security, dict):
        add("missing_security", "error", "security object is required")
        security = {}
    if security.get("bypass_controls") is True:
        add("security_bypass", "error", "security or CAPTCHA bypass is prohibited")
    captcha_policy = security.get("captcha_policy")
    if captcha_policy not in ALLOWED_CAPTCHA_POLICIES:
        add(
            "captcha_policy",
            "error",
            "security.captcha_policy must be official, manual, or fail_and_continue",
        )

    steps = spec.get("steps")
    if not isinstance(steps, list) or not steps:
        add("missing_steps", "error", "steps must be a non-empty array")
        return _result(issues)

    ids: set[str] = set()
    role_positions: dict[str, list[int]] = {}
    roles: set[str] = set()
    for position, step in enumerate(steps):
        if not isinstance(step, dict):
            add("step_type", "error", f"steps[{position}] must be an object")
            continue
        step_id = step.get("id")
        role = step.get("role")
        if not isinstance(step_id, str) or not step_id.strip():
            add("step_id", "error", f"steps[{position}] has no valid id")
        elif step_id in ids:
            add("duplicate_step_id", "error", f"duplicate step id: {step_id}")
        else:
            ids.add(step_id)
        if not isinstance(role, str) or not role.strip():
            add("step_role", "error", f"steps[{position}] has no valid role")
            continue
        roles.add(role)
        role_positions.setdefault(role, []).append(position)

    for required in ("should_run", "mark_running", "archive", "mark_success"):
        if required not in roles:
            add("missing_role", "error", f"required step role is missing: {required}")

    if role_positions.get("archive") and role_positions.get("mark_success"):
        if min(role_positions["mark_success"]) < min(role_positions["archive"]):
            add("success_before_archive", "error", "mark_success occurs before archive")

    known_targets = roles | ids
    for position, step in enumerate(steps):
        if not isinstance(step, dict):
            continue
        is_ui = step.get("type") == "ui" or step.get("role") == "ui" or step.get("changes_ui") is True
        if not is_ui:
            continue
        on_failure = step.get("on_failure")
        if not isinstance(on_failure, list):
            add("ui_failure_handler", "error", f"UI step {step.get('id', position)} needs on_failure")
            continue
        targets = {str(value) for value in on_failure}
        unknown = targets - known_targets
        if unknown:
            add(
                "unknown_failure_target",
                "error",
                f"UI step {step.get('id', position)} references unknown targets: {', '.join(sorted(unknown))}",
            )
        if "close_page" not in targets and not _targets_role(targets, steps, "close_page"):
            add("missing_cleanup", "error", f"UI step {step.get('id', position)} failure does not close page")
        if "mark_failure" not in targets and not _targets_role(targets, steps, "mark_failure"):
            add("missing_failure_mark", "error", f"UI step {step.get('id', position)} failure does not mark state")
        if not ({"continue_item", "exit_task"} & targets) and not (
            _targets_role(targets, steps, "continue_item") or _targets_role(targets, steps, "exit_task")
        ):
            add(
                "missing_failure_exit",
                "error",
                f"UI step {step.get('id', position)} failure has no bounded control-flow exit",
            )

    if "mark_running" in roles and "mark_failure" not in roles:
        add("running_without_failure_mark", "error", "mark_running exists but mark_failure is absent")
    if "close_page" not in roles:
        add("missing_close_page", "error", "no close_page role exists")

    return _result(issues)


def _string_set(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item).strip().lower() for item in value if str(item).strip()}


def _targets_role(targets: set[str], steps: list[Any], role: str) -> bool:
    return any(
        isinstance(step, dict) and step.get("id") in targets and step.get("role") == role
        for step in steps
    )


def _result(issues: list[dict[str, str]]) -> dict[str, Any]:
    errors = sum(issue["severity"] == "error" for issue in issues)
    warnings = sum(issue["severity"] == "warning" for issue in issues)
    return {
        "ok": errors == 0,
        "error_count": errors,
        "warning_count": warnings,
        "issues": issues,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "fatal": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    result = validate_spec(spec)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
