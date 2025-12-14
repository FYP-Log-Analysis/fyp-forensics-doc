from .utils import clean_event_data

def normalize_system_event(event):
    # Make the event ID a proper number
    event["event_id"] = int(event["event_id"])

    # Strip out XML junk and get the actual values
    event["event_data"] = clean_event_data(event.get("event_data", {}))

    return event
