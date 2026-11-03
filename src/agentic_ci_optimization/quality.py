"""Advisory classification, never test retirement or oracle authority."""


def review_controls(doc):
    if not isinstance(doc, dict) or doc.get("schema") != "aco.control-review.v1":
        raise ValueError("unsupported control review")
    rows = doc.get("controls")
    if not isinstance(rows, list):
        raise ValueError("missing controls")
    reviewed = []
    seen = set()
    for item in rows:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("invalid control")
        cid = item["id"]
        if not cid or cid in seen:
            raise ValueError("missing/duplicate control ID")
        seen.add(cid)
        required = ("contract_ref", "oracle_ref", "fault_ref", "legal_neighbor_ref",
                    "demand_ref", "source_ref")
        missing = [k for k in required if not isinstance(item.get(k), str) or not item[k]]
        if missing:
            recommendation = "evidence_gap"
        elif item.get("replacement_proposal"):
            recommendation = "candidate_for_independent_consolidation_review"
        elif item.get("high_cost") is True:
            recommendation = "candidate_for_performance_refactor"
        else:
            recommendation = "retain_or_review_demand"
        reviewed.append({"id": cid, "recommendation": recommendation,
                         "missing": missing, "owner_decision_required": True,
                         "may_delete": False})
    return {"schema": "aco.control-review-result.v1", "controls": reviewed,
            "authority": "advisory_only_original_owner_retains_selection"}
