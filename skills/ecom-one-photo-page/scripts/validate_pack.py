from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_SECTIONS = (
    "PRODUCT_LOCK",
    "CONSISTENCY_ROUTE",
    "SCREEN_JOB",
    "BENEFIT_AND_PROOF",
    "COMPOSITION",
    "ALLOWED_COPY",
    "EVIDENCE_LIMITS",
    "NEGATIVE_CONSTRAINTS",
    "OUTPUT_SPEC",
)

REQUIRED_PRODUCT_CARD_MARKERS = (
    "identity_anchor:",
    "target_sku:",
    "target_instance_count:",
    "fragile_identity_details:",
    "visible_facts:",
    "user_provided_facts:",
    "proposals:",
    "missing_or_unverified:",
)

REQUIRED_PROMPT_MARKERS = (
    "identity_anchor:",
    "target_sku:",
    "target_instance_count:",
)

REQUIRED_QA_MARKERS = (
    "identity_status:",
    "inventory_status:",
    "consistency_route:",
    "claim_status:",
    "text_status:",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a one-photo ecommerce prompt pack.")
    parser.add_argument("job", help="Job directory created by init_job.py.")
    parser.add_argument("--min-main", type=int, default=6)
    parser.add_argument("--min-detail", type=int, default=6)
    return parser.parse_args()


def missing_markers(path: Path, markers: tuple[str, ...]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [marker for marker in markers if marker not in text]


def inspect_prompt(path: Path) -> list[str]:
    return missing_markers(path, REQUIRED_SECTIONS + REQUIRED_PROMPT_MARKERS)


def main() -> int:
    args = parse_args()
    root = Path(args.job).resolve()
    errors: list[str] = []

    required_files = (
        root / "job.json",
        root / "strategy" / "product-card.md",
        root / "strategy" / "page-map.md",
        root / "qa" / "qa-report.md",
    )
    for path in required_files:
        if not path.is_file():
            errors.append(f"missing file: {path}")

    structured_files = (
        (root / "strategy" / "product-card.md", REQUIRED_PRODUCT_CARD_MARKERS),
        (root / "qa" / "qa-report.md", REQUIRED_QA_MARKERS),
    )
    for path, markers in structured_files:
        if path.is_file():
            missing = missing_markers(path, markers)
            if missing:
                errors.append(f"{path}: missing markers {', '.join(missing)}")

    channels = {
        "main": sorted((root / "prompts" / "main").glob("*.md")),
        "detail": sorted((root / "prompts" / "detail").glob("*.md")),
    }
    minimums = {"main": args.min_main, "detail": args.min_detail}
    for channel, files in channels.items():
        if len(files) < minimums[channel]:
            errors.append(f"{channel} prompt count {len(files)} < {minimums[channel]}")
        for path in files:
            missing = inspect_prompt(path)
            if missing:
                errors.append(f"{path}: missing sections or markers {', '.join(missing)}")

    result = {
        "status": "passed" if not errors else "failed",
        "job": str(root),
        "main_prompt_count": len(channels["main"]),
        "detail_prompt_count": len(channels["detail"]),
        "errors": errors,
        "note": "Structural validation does not replace visual QA.",
    }
    report_dir = root / "qa"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "validation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
