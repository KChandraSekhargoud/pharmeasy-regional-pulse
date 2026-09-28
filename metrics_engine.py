import json
import os

def compute_percentage_change_v1(current, previous):
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100

def flag_significant_regions_v1(changes, threshold=8):
    return {region: change for region, change in changes.items() if abs(change) > threshold}

def save_state_v1(month_summary, path):
    with open(path, 'w') as f:
        json.dump(month_summary, f)

def load_previous_state_v1(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    demo_changes = {"Guntur": 122.19, "Nellore": 3.2, "Hyderabad": 14.5}
    print("Flagged:", flag_significant_regions_v1(demo_changes))