from __future__ import annotations

import argparse
import json
import shutil
from datetime import date
from pathlib import Path


DEFAULT_ROOT = Path.cwd() / "outputs" / "one-photo-page"
INVALID = '<>:"/\\|?*'


def safe_name(value: str) -> str:
    cleaned = "".join("_" if char in INVALID else char for char in value).strip(" ._")
    return cleaned or "product"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a one-photo ecommerce page job.")
    parser.add_argument("--product", required=True, help="Product name used in the job folder.")
    parser.add_argument("--anchor", help="Optional local product image to copy into input/.")
    parser.add_argument("--output", help="Exact job directory; defaults under ./outputs/ecommerce\\one-photo-page.")
    parser.add_argument("--mode", choices=("plan", "produce"), default="plan")
    parser.add_argument("--reuse", action="store_true", help="Allow an existing job directory without overwriting files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    product = safe_name(args.product)
    output = Path(args.output).resolve() if args.output else (DEFAULT_ROOT / f"{product}_{date.today().isoformat()}")

    if output.exists() and any(output.iterdir()) and not args.reuse:
        raise SystemExit(f"Refusing to reuse non-empty directory without --reuse: {output}")

    directories = (
        "input",
        "strategy",
        "prompts/main",
        "prompts/detail",
        "qa",
    )
    if args.mode == "produce":
        directories += ("renders/main", "renders/detail", "preview")
    for relative in directories:
        (output / relative).mkdir(parents=True, exist_ok=True)

    anchor_target = None
    if args.anchor:
        anchor = Path(args.anchor).resolve()
        if not anchor.is_file():
            raise SystemExit(f"Anchor image not found: {anchor}")
        anchor_target = output / "input" / f"anchor{anchor.suffix.lower()}"
        if not anchor_target.exists():
            shutil.copy2(anchor, anchor_target)

    anchor_label = str(anchor_target) if anchor_target else "pending"
    manifest = {
        "schema_version": 2,
        "product": args.product,
        "mode": args.mode,
        "created_date": date.today().isoformat(),
        "job_directory": str(output),
        "anchor_image": str(anchor_target) if anchor_target else None,
        "source_roles": {
            "identity_anchor": str(anchor_target) if anchor_target else None,
            "fact_evidence": [],
            "style_reference": [],
            "exclude_from_generation": [],
        },
        "target_sku": None,
        "target_instance_count": None,
        "consistency_route": None,
        "evidence_states": [
            "visible_facts",
            "user_provided_facts",
            "proposals",
            "missing_or_unverified",
        ],
    }
    manifest_path = output / "job.json"
    if not manifest_path.exists():
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    templates = {
        output / "strategy" / "product-card.md": f"""# Product Card

product_name: {args.product}
identity_anchor: {anchor_label}
target_sku: pending visual inspection
target_instance_count: pending visual inspection
fragile_identity_details: pending visual inspection
consistency_route: pending preflight

visible_facts:

user_provided_facts:

proposals:

missing_or_unverified:
""",
        output / "strategy" / "page-map.md": """# Page Map

Create one record per image with:

```text
id:
channel: main | detail
buyer_question:
screen_job:
primary_message:
proof_used:
composition_family:
headline:
support_copy:
facts_used:
proposal_used:
risk_notes:
```
""",
        output / "qa" / "qa-report.md": f"""# QA Report

mode: {args.mode}
anchor_used: {anchor_label}
primary_purchase_reason: pending
generated_count: 0
accepted_count: 0
rejected_or_downgraded: pending
identity_status: pending-qc
inventory_status: pending-qc
consistency_route: pending preflight
claim_status: pending
distinctness_status: pending
text_status: pending
remaining_limitations: pending
""",
    }
    for path, content in templates.items():
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
