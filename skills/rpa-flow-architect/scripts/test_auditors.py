#!/usr/bin/env python3
"""Unit tests for the deterministic RPA evidence auditors."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from audit_state import audit_state
from parse_run_log import parse_log, summarize
from validate_rpa_spec import validate_spec


class ParseRunLogTests(unittest.TestCase):
    def test_plain_log_extracts_pass_items_and_open_run(self) -> None:
        text = "\n".join(
            [
                "batch_pass=1/2 status=START",
                "店铺序号=1 status=SKIP",
                "店铺序号=2 status=RUN stage=login",
                "batch_pass=2/2 status=START",
                "店铺序号=2 status=SUCCESS",
                "店铺序号=3 status=RUN",
            ]
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run.log"
            path.write_text(text, encoding="utf-8")
            result = summarize(parse_log(path))
        self.assertEqual(result["record_count"], 6)
        self.assertEqual(result["pass_counts"], {"1/2": 1, "2/2": 1})
        self.assertEqual(result["items"]["2"]["last_status"], "SUCCESS")
        self.assertEqual(result["items"]["2"]["events"][0]["stage"], "login")
        self.assertEqual([item["item"] for item in result["open_run_candidates"]], ["3"])

    def test_csv_maps_shadowbot_style_headers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run.csv"
            path.write_text(
                "时间,内容,流程名称\n2026-01-01 08:00:00,店铺序号=7 status=SKIP,主流程\n",
                encoding="utf-8-sig",
            )
            result = summarize(parse_log(path))
        self.assertEqual(result["status_counts"], {"SKIP": 1})
        self.assertIn("7", result["items"])


class AuditStateTests(unittest.TestCase):
    def test_finds_stale_running_and_missing_success_artifact(self) -> None:
        data = {
            "items": {
                "sensitive-key-not-emitted": {
                    "status": "running",
                    "updated_at": "2026-01-01T00:00:00Z",
                    "item_seq": 1,
                },
                "another-sensitive-key": {
                    "status": "success",
                    "item_seq": 2,
                    "artifact": "missing.xlsx",
                },
            }
        }
        with tempfile.TemporaryDirectory() as directory:
            result = audit_state(
                data,
                artifact_root=Path(directory),
                stale_minutes=30,
                now=datetime(2026, 1, 1, 1, 0, tzinfo=timezone.utc),
            )
        codes = {issue["code"] for issue in result["issues"]}
        self.assertFalse(result["ok"])
        self.assertIn("stale_running", codes)
        self.assertIn("artifact_missing", codes)
        rendered = json.dumps(result, ensure_ascii=False)
        self.assertNotIn("sensitive-key-not-emitted", rendered)

    def test_accepts_no_data_without_artifact(self) -> None:
        result = audit_state({"items": [{"status": "no_data", "item_seq": 1}]})
        self.assertTrue(result["ok"])

    def test_same_task_key_with_distinct_items_is_not_a_collision(self) -> None:
        result = audit_state(
            {
                "items": [
                    {"status": "no_data", "task_key": "task-a", "item_key": "item-1"},
                    {"status": "no_data", "task_key": "task-a", "item_key": "item-2"},
                ]
            }
        )
        self.assertNotIn(
            "duplicate_task_item_key",
            {issue["code"] for issue in result["issues"]},
        )


def valid_spec() -> dict:
    failure = ["mark_failure", "close_page", "continue_item"]
    return {
        "task_plan": {
            "outside_retry_loop": True,
            "date_interval": "right_open",
            "business_end_field": "business_end",
            "query_end_field": "query_end",
        },
        "retry": {"bounded": True, "node_max": 2, "item_max": 1, "batch_passes": 2},
        "state": {
            "terminal": ["success", "no_data"],
            "retryable": ["captcha_failed", "failed"],
            "running_timeout_seconds": 900,
        },
        "logging": {"safe_item_id": True},
        "security": {"bypass_controls": False, "captcha_policy": "official"},
        "steps": [
            {"id": "decide", "role": "should_run", "type": "decision"},
            {"id": "claim", "role": "mark_running", "type": "state"},
            {"id": "login", "role": "ui", "type": "ui", "on_failure": failure},
            {"id": "fail", "role": "mark_failure", "type": "state"},
            {"id": "close", "role": "close_page", "type": "cleanup"},
            {"id": "continue", "role": "continue_item", "type": "control"},
            {"id": "archive", "role": "archive", "type": "file"},
            {"id": "success", "role": "mark_success", "type": "state"},
        ],
    }


class ValidateSpecTests(unittest.TestCase):
    def test_valid_spec_passes(self) -> None:
        result = validate_spec(valid_spec())
        self.assertTrue(result["ok"], result)

    def test_detects_unbounded_retry_early_success_and_missing_cleanup(self) -> None:
        spec = valid_spec()
        spec["retry"]["bounded"] = False
        spec["steps"][2]["on_failure"] = ["mark_failure", "continue_item"]
        spec["steps"][-2], spec["steps"][-1] = spec["steps"][-1], spec["steps"][-2]
        result = validate_spec(spec)
        codes = {issue["code"] for issue in result["issues"]}
        self.assertIn("unbounded_retry", codes)
        self.assertIn("missing_cleanup", codes)
        self.assertIn("success_before_archive", codes)

    def test_rejects_security_bypass(self) -> None:
        spec = valid_spec()
        spec["security"]["bypass_controls"] = True
        result = validate_spec(spec)
        self.assertIn("security_bypass", {issue["code"] for issue in result["issues"]})


if __name__ == "__main__":
    unittest.main()
