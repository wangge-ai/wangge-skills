import argparse
import json
import pathlib
import sys

TOP_KEYS = {
    "schema_version", "category", "business_status", "evidence_pack_refs",
    "rows", "held_claims", "missing_evidence",
}
REF_KEYS = {"pack_id", "pack_type", "version", "scope"}
INDEX_KEYS = {"schema_version", "evidence_packs"}
INDEX_PACK_KEYS = REF_KEYS | {"item_ids"}
ROW_KEYS = {
    "position_id", "segment", "title_direction", "keyword_roots",
    "user_problem", "desired_outcome", "differentiation", "main_copy",
    "secondary_copy", "composition_task", "main_image_positioning",
    "detail_page_tasks", "micro_detail_tasks", "evidence_refs",
    "held_claims", "missing_evidence",
}
PACK_TYPES = {"competitor_market", "keywords", "voc"}
STATUSES = {"success", "partial", "needs_input"}


def exact_keys(value, expected, field):
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError(f"{field} keys must be exactly: {sorted(expected)}")


def nonempty_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty text")


def text_list(value, field, allow_empty=True):
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ValueError(f"{field} must be a text list")
    for item in value:
        nonempty_text(item, field)


def validate_evidence_index(evidence_index):
    exact_keys(evidence_index, INDEX_KEYS, "evidence_index")
    if evidence_index["schema_version"] != 1:
        raise ValueError("evidence_index schema_version must be 1")
    packs = evidence_index["evidence_packs"]
    if not isinstance(packs, list):
        raise ValueError("evidence_packs must be a list")

    packs_by_id = {}
    item_owners = {}
    for index, pack in enumerate(packs):
        exact_keys(pack, INDEX_PACK_KEYS, f"evidence_packs[{index}]")
        nonempty_text(pack["pack_id"], "pack_id")
        if pack["pack_id"] in packs_by_id:
            raise ValueError("duplicate pack_id in evidence_index")
        if pack["pack_type"] not in PACK_TYPES:
            raise ValueError("unsupported pack_type")
        if type(pack["version"]) is not int or pack["version"] < 1:
            raise ValueError("version must be a positive integer")
        if pack["scope"] != "project":
            raise ValueError("all pack scopes must be project")
        text_list(pack["item_ids"], "item_ids", allow_empty=False)
        if len(set(pack["item_ids"])) != len(pack["item_ids"]):
            raise ValueError("duplicate item_id in evidence_index Pack")
        for item_id in pack["item_ids"]:
            if item_id in item_owners:
                raise ValueError("duplicate item_id across evidence_index Packs")
            item_owners[item_id] = pack["pack_id"]
        packs_by_id[pack["pack_id"]] = pack
    return packs_by_id, item_owners


def validate(payload, evidence_index):
    exact_keys(payload, TOP_KEYS, "output")
    if payload["schema_version"] != 1:
        raise ValueError("schema_version must be 1")
    nonempty_text(payload["category"], "category")
    if payload["business_status"] not in STATUSES:
        raise ValueError("unsupported business_status")
    text_list(payload["held_claims"], "held_claims")
    text_list(payload["missing_evidence"], "missing_evidence")

    refs = payload["evidence_pack_refs"]
    if not isinstance(refs, list):
        raise ValueError("evidence_pack_refs must be a list")
    pack_types = set()
    pack_ids = set()
    output_packs = {}
    for index, ref in enumerate(refs):
        exact_keys(ref, REF_KEYS, f"evidence_pack_refs[{index}]")
        nonempty_text(ref["pack_id"], "pack_id")
        if ref["pack_id"] in output_packs:
            raise ValueError("duplicate pack_id in evidence_pack_refs")
        if ref["pack_type"] not in PACK_TYPES:
            raise ValueError("unsupported pack_type")
        if type(ref["version"]) is not int or ref["version"] < 1:
            raise ValueError("version must be a positive integer")
        if ref["scope"] != "project":
            raise ValueError("all pack scopes must be project")
        pack_types.add(ref["pack_type"])
        pack_ids.add(ref["pack_id"])
        output_packs[ref["pack_id"]] = ref

    indexed_packs, item_owners = validate_evidence_index(evidence_index)
    if set(output_packs) != set(indexed_packs):
        raise ValueError("Pack identities must match exactly")
    for pack_id, ref in output_packs.items():
        indexed = indexed_packs[pack_id]
        if any(indexed[key] != ref[key] for key in REF_KEYS):
            raise ValueError(f"Pack identity mismatch for {pack_id}")

    rows = payload["rows"]
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    required_packs_present = {"competitor_market", "keywords"}.issubset(pack_types)
    if payload["business_status"] == "needs_input":
        if required_packs_present:
            raise ValueError("needs_input requires a missing required Pack")
        if rows:
            raise ValueError("needs_input must not contain rows")
        if not payload["held_claims"] or not payload["missing_evidence"]:
            raise ValueError("needs_input requires held_claims and missing_evidence")
        return payload
    if not required_packs_present:
        raise ValueError("missing required Pack requires needs_input")
    if not rows:
        raise ValueError("formal output requires rows")
    if "voc" not in pack_types and payload["business_status"] != "partial":
        raise ValueError("missing voc requires partial")
    if "voc" not in pack_types and (
        not payload["held_claims"] or not payload["missing_evidence"]
    ):
        raise ValueError("missing voc requires top-level held_claims and missing_evidence")
    if payload["business_status"] == "success" and payload["missing_evidence"]:
        raise ValueError("success cannot contain missing_evidence")
    if payload["business_status"] == "success" and payload["held_claims"]:
        raise ValueError("success cannot contain held_claims")

    positions = set()
    for index, row in enumerate(rows):
        exact_keys(row, ROW_KEYS, f"rows[{index}]")
        for field in (
            "position_id", "segment", "title_direction", "user_problem",
            "desired_outcome", "differentiation", "main_copy",
            "secondary_copy", "composition_task", "main_image_positioning",
        ):
            nonempty_text(row[field], f"rows[{index}].{field}")
        if row["position_id"] in positions:
            raise ValueError("duplicate position_id")
        positions.add(row["position_id"])
        text_list(row["keyword_roots"], "keyword_roots", allow_empty=False)
        text_list(row["detail_page_tasks"], "detail_page_tasks", allow_empty=False)
        text_list(row["micro_detail_tasks"], "micro_detail_tasks", allow_empty=False)
        if len(row["micro_detail_tasks"]) != 5:
            raise ValueError("micro_detail_tasks must contain exactly 5 tasks")
        text_list(row["evidence_refs"], "evidence_refs", allow_empty=False)
        text_list(row["held_claims"], "row held_claims")
        text_list(row["missing_evidence"], "row missing_evidence")
        if payload["business_status"] == "success" and row["missing_evidence"]:
            raise ValueError("success cannot contain missing_evidence")
        if payload["business_status"] == "success" and row["held_claims"]:
            raise ValueError("success cannot contain held_claims")
        if "voc" not in pack_types and (
            not row["held_claims"] or not row["missing_evidence"]
        ):
            raise ValueError("missing voc requires row held_claims and missing_evidence")
        row_pack_types = set()
        for evidence_ref in row["evidence_refs"]:
            raw_pack_id, separator, raw_item_id = evidence_ref.partition(":")
            if (
                evidence_ref != evidence_ref.strip()
                or raw_pack_id != raw_pack_id.strip()
                or raw_item_id != raw_item_id.strip()
                or not separator
                or not raw_pack_id
                or not raw_item_id
                or ":" in raw_item_id
            ):
                raise ValueError("invalid evidence_ref")
            pack_id = raw_pack_id
            item_id = raw_item_id
            if pack_id not in pack_ids:
                raise ValueError("evidence_ref references undeclared pack_id")
            if item_id not in item_owners:
                raise ValueError("evidence_ref item_id is not declared")
            if item_owners[item_id] != pack_id:
                raise ValueError("evidence_ref item_id is owned by wrong pack")
            row_pack_types.add(output_packs[pack_id]["pack_type"])
        for required_type in ("competitor_market", "keywords"):
            if required_type not in row_pack_types:
                raise ValueError(f"row requires {required_type} evidence")
        if "voc" in pack_types and "voc" not in row_pack_types:
            raise ValueError("row requires voc evidence")
    return payload


def main():
    parser = argparse.ArgumentParser(description="Validate a category-link positioning output")
    parser.add_argument("--input", required=True)
    parser.add_argument("--evidence-index", required=True)
    args = parser.parse_args()
    payload = json.loads(pathlib.Path(args.input).read_text(encoding="utf-8-sig"))
    evidence_index = json.loads(
        pathlib.Path(args.evidence_index).read_text(encoding="utf-8-sig")
    )
    validate(payload, evidence_index)
    print(json.dumps({
        "status": "valid",
        "business_status": payload["business_status"],
        "rows": len(payload["rows"]),
    }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
