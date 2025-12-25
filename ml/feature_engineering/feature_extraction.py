import json
from pathlib import Path
from collections import Counter

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "intermediate" / "execution_windows.json"
OUTPUT_FILE = BASE_DIR / "data" / "features" / "baseline_features.json"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def get_process_name(path):
    """Extract executable name from full path."""
    if path is None:
        return None
    return path.split("\\")[-1].lower()


def extract_features_from_window(window):
    events = window.get("events", [])

    process_names = []
    users = []
    registry_events = 0
    system32_execs = 0
    non_system32_execs = 0

    for event in events:
        process_path = event.get("process")
        user = event.get("user_sid")

        if user:
            users.append(user)

        # Registry events
        if process_path == "Registry":
            registry_events += 1
            continue

        process_name = get_process_name(process_path)
        if process_name:
            process_names.append(process_name)

        if process_path and "\\windows\\system32\\" in process_path.lower():
            system32_execs += 1
        else:
            non_system32_execs += 1

    process_counter = Counter(process_names)

    features = {
        "window_start": window.get("window_start"),
        "window_end": window.get("window_end"),
        "event_count": len(events),
        "process_event_count": sum(process_counter.values()),
        "unique_process_count": len(process_counter),
        "unique_user_count": len(set(users)),
        "registry_event_count": registry_events,
        "system32_exec_count": system32_execs,
        "non_system32_exec_count": non_system32_execs
    }

    return features


def main():
    if not INPUT_FILE.exists():
        print("Input file not found:", INPUT_FILE)
        return

    print("Loading execution windows...")
    with open(INPUT_FILE, "r") as f:
        windows = json.load(f)

    print("Extracting features...")
    all_features = []

    for window in windows:
        features = extract_features_from_window(window)
        all_features.append(features)

    print("Saving features...")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_features, f, indent=2)

    print("Feature extraction completed")
    print("Total windows processed:", len(all_features))


if __name__ == "__main__":
    main()
