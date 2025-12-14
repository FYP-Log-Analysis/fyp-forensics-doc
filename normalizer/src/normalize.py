import json
import os
from pathlib import Path

# Import event-type-specific normalizers
from .application_norm import normalize_application_event
from .system_norm import normalize_system_event
from .security_norm import normalize_security_event
from .powershell_norm import normalize_powershell_event

# Figure out where we are in the project structure
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Where the parser dumped the raw JSON files
INPUT_DIR = BASE_DIR / "data" / "processed" / "json"

# Where we'll save the cleaned up versions
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "normalized"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_json(path):
    # Just a simple wrapper to read JSON files
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    # Write JSON with nice formatting so it's readable
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def normalize_file(input_path, output_path, normalizer):
    # Load up all the events from the file
    events = load_json(input_path)

    # Run each event through the normalizer to clean it up
    normalized = [normalizer(event) for event in events]

    # Write out the cleaned events
    save_json(output_path, normalized)

def main():
    # Process each log type with its specific normalizer
    normalize_file(
        INPUT_DIR / "Application.json",
        OUTPUT_DIR / "Application_normalized.json",
        normalize_application_event,
    )

    normalize_file(
        INPUT_DIR / "System.json",
        OUTPUT_DIR / "System_normalized.json",
        normalize_system_event,
    )

    normalize_file(
        INPUT_DIR / "Security.json",
        OUTPUT_DIR / "Security_normalized.json",
        normalize_security_event,
    )

    normalize_file(
        INPUT_DIR / "PowerShell_Operational.json",
        OUTPUT_DIR / "PowerShell_Operational_normalized.json",
        normalize_powershell_event,
    )

    # Let them know we're done
    print("Normalization complete. Files saved to /data/processed/normalized/")

if __name__ == "__main__":
    # Fire up the normalization process
    main()
