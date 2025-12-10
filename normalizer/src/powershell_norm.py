def normalize_powershell_event(event):
    # Convert event_id from string to integer
    event["event_id"] = int(event["event_id"])

    # Ensure event_data exists, since PowerShell logs may have empty fields
    if "event_data" not in event:
        event["event_data"] = {}

    # Return the normalized PowerShell event
    return event