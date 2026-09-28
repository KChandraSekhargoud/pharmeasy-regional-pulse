import json
import datetime

def review_gate_v1(report, decision, reviewer_note=""):
    allowed_decisions = {"approve", "edit", "reject"}
    if decision not in allowed_decisions:
        raise ValueError(f"Decision must be one of {allowed_decisions}")
    
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "run_id": "run_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "region": "ALL_FLAGGED", 
        "decision": decision,
        "reviewer_note": reviewer_note
    }
    
    with open("audit_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
        
    return {
        "decision": decision,
        "external_use_allowed": decision == "approve"
    }

if __name__ == "__main__":
    print("--- Test Harness for Review Gate ---")
    print(review_gate_v1("Report Draft 1", "approve", "Looks accurate, numbers match SQL output."))
    print(review_gate_v1("Report Draft 2", "edit", "Rephrase the implication for Hyderabad."))
    print(review_gate_v1("Report Draft 3", "reject", "Missing context on the zero-order region."))
    print("Audit log updated.")