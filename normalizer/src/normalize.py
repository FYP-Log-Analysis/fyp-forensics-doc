import json
import os
from pathlib import Path

# Import event-type-specific normalizers
from .application_norm import normalize_application_event
from .system_norm import normalize_system_event
from .security_norm import normalize_security_event
from .powershell_norm import normalize_powershell_event

# Base project directory (3 levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Input folder: raw JSON from the parser
INPUT_DIR = BASE_DIR / "data" / "processed" / "json"

# Output folder: cleaned / normalized JSON files
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "normalized"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_json(path):
    # Read JSON file and return Python object
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    # Write Python object to JSON file with indentation
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def normalize_file(input_path, output_path, normalizer):
    # Load events from input JSON file
    events = load_json(input_path)

    # Apply the specific normalizer function to each event
    normalized = [normalizer(event) for event in events]

    # Save the normalized events to output JSON file
    save_json(output_path, normalized)

def main():
    # Normalize Application logs
    normalize_file(
        INPUT_DIR / "Application.json",
        OUTPUT_DIR / "Application_normalized.json",
        normalize_application_event,
    )

    # Normalize System logs
    normalize_file(
        INPUT_DIR / "System.json",
        OUTPUT_DIR / "System_normalized.json",
        normalize_system_event,
    )

    # Normalize Security logs
    normalize_file(
        INPUT_DIR / "Security.json",
        OUTPUT_DIR / "Security_normalized.json",
        normalize_security_event,
    )

    # Normalize PowerShell Operational logs
    normalize_file(
        INPUT_DIR / "PowerShell_Operational.json",
        OUTPUT_DIR / "PowerShell_Operational_normalized.json",
        normalize_powershell_event,
    )

    # Notify user when processing is done
    print("Normalization complete. Files saved to /data/processed/normalized/")

if __name__ == "__main__":
    # Run the main normalization routine
    main()
