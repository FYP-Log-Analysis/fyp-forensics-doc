
# This script filters Windows process creation events from a normalized log file.
# It saves only the important fields for later analysis.

import json
from pathlib import Path

# Set up file paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "normalized" / "Security_normalized.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "intermediate" / "process_execution_events.json"

# Only keep events with this ID (process creation)
PROCESS_EVENT_ID = 4688

# Make sure the output folder exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_events(file_path):
    """Load all events from the input file."""
    with open(file_path, "r") as f:
        return json.load(f)

def filter_process_events(events):
    """Keep only process creation events with the needed fields."""
    filtered = []
    for event in events:
        if event.get("event_id") != PROCESS_EVENT_ID:
            continue
        if event.get("channel") != "Security":
            continue
        event_data = event.get("event_data", {})
        process_name = event_data.get("NewProcessName")
        timestamp = event.get("timestamp")
        if not process_name or not timestamp:
            continue
        filtered.append({
            "timestamp": timestamp,
            "computer": event.get("computer"),
            "user_sid": event_data.get("SubjectUserSid"),
            "process": process_name,
            "parent_process": event_data.get("ParentProcessName")
        })
    return filtered

def save_filtered_events(filtered, file_path):
    """Save the filtered events to a file."""
    with open(file_path, "w") as f:
        json.dump(filtered, f, indent=2)

def main():
    # Check if the input file exists
    if not INPUT_FILE.exists():
        print("Error: Input file not found.")
        return
    events = load_events(INPUT_FILE)
    print(f"Loaded {len(events)} events.")
    filtered = filter_process_events(events)
    print(f"Filtered {len(filtered)} process creation events.")
    save_filtered_events(filtered, OUTPUT_FILE)
    print(f"Saved filtered events to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
