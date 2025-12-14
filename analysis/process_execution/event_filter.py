import json
from pathlib import Path

# Configuration
INPUT_FILE = Path("../../data/processed/normalized/security_normalized.json")
OUTPUT_FILE = Path("process_execution_events.json")

PROCESS_EVENT_ID = 4688

# Load normalized logs
with open(INPUT_FILE, "r") as f:
    events = json.load(f)

print(f"Loaded {len(events)} total events")

# Filter process creation events
filtered_events = []

for event in events:
    # 1. Event ID check
    if event.get("event_id") != PROCESS_EVENT_ID:
        continue

    # 2. Channel check
    if event.get("channel") != "Security":
        continue

    # 3. Required fields
    event_data = event.get("event_data", {})
    process_name = event_data.get("NewProcessName")
    timestamp = event.get("timestamp")

    if not process_name or not timestamp:
        continue

    # 4. Store ML-ready record
    filtered_events.append({
        "timestamp": timestamp,
        "computer": event.get("computer"),
        "user_sid": event_data.get("SubjectUserSid"),
        "process": process_name,
        "parent_process": event_data.get("ParentProcessName")
    })

# Save filtered output
with open(OUTPUT_FILE, "w") as f:
    json.dump(filtered_events, f, indent=2)

print(f"Filtered {len(filtered_events)} process creation events")
print(f"Saved to {OUTPUT_FILE}")
