import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

try:
    from utils import clean_event_data
except ImportError:
    from .utils import clean_event_data

def normalize_system_event(event):
    # Make the event ID a proper number
    event["event_id"] = int(event["event_id"])

    # Strip out XML junk and get the actual values
    event["event_data"] = clean_event_data(event.get("event_data", {}))

    return event
