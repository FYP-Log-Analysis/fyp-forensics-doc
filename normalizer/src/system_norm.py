from .utils import clean_event_data

def normalize_system_event(event):
    # Convert event_id from string to integer
    event["event_id"] = int(event["event_id"])

    # Clean XML namespaces and extract <string> content from event_data
    event["event_data"] = clean_event_data(event.get("event_data", {}))

    # Return the normalized System event
    return event
