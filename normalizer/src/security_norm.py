import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

try:
    from utils import convert_hex
except ImportError:
    from .utils import convert_hex

def normalize_security_event(event):
    # Fix the event ID to be a proper integer
    event["event_id"] = int(event["event_id"])

    # Build a clean version of the event data
    new_data = {}

    # Go through each field and clean it up
    for key, value in event.get("event_data", {}).items():
        # Security logs love hex values - convert them to proper numbers
        new_data[key] = convert_hex(value)

    # Swap out the old messy data with our clean version
    event["event_data"] = new_data

    return event
