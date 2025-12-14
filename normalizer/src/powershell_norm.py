def normalize_powershell_event(event):
    # Fix the event ID format
    event["event_id"] = int(event["event_id"])

    # PowerShell events can be weird - make sure event_data exists
    if "event_data" not in event:
        event["event_data"] = {}

    return event