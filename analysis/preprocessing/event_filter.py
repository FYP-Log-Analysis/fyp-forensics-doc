import json
from pathlib import Path

# Get absolute paths relative to this script's location
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# Paths
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "normalized" / "Security_normalized.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "intermediate" / "process_execution_events.json"

PROCESS_EVENT_ID = 4688

# Create output directory if it doesn't exist
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Check if input file exists
if not INPUT_FILE.exists():
    print(f"Error: Input file not found: {INPUT_FILE}")
    print("Available normalized files:")
    normalized_dir = PROJECT_ROOT / "data" / "processed" / "normalized"
    if normalized_dir.exists():
        for f in normalized_dir.glob("*.json"):
            print(f"  - {f.name}")
    else:
        print("  Normalized directory not found!")
    exit(1)

# Pull all the normalized security events
with open(INPUT_FILE, "r") as f:
    events = json.load(f)

print(f"Loaded {len(events)} total events")

# pick out process creation events (ID 4688)
filtered_events = []

for event in events:
    # Skip anything that's not a process creation event
    if event.get("event_id") != PROCESS_EVENT_ID:
        continue

    # Only Security channel events
    if event.get("channel") != "Security":
        continue

    # key fields for analysis
    event_data = event.get("event_data", {})
    process_name = event_data.get("NewProcessName")
    timestamp = event.get("timestamp")

    if not process_name or not timestamp:
        continue

    # Build a clean record with the required fields
    filtered_events.append({
        "timestamp": timestamp,
        "computer": event.get("computer"),
        "user_sid": event_data.get("SubjectUserSid"),
        "process": process_name,
        "parent_process": event_data.get("ParentProcessName")
    })

# Write out the filtered events for the next analysis step
with open(OUTPUT_FILE, "w") as f:
    json.dump(filtered_events, f, indent=2)

print(f"Filtered {len(filtered_events)} process creation events")
print(f"Saved to {OUTPUT_FILE}")
