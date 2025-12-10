from .utils import convert_hex

def normalize_security_event(event):
    # Convert event_id from string to integer
    event["event_id"] = int(event["event_id"])

    # Prepare a new dictionary for cleaned event_data
    new_data = {}

    # Loop through all key-value pairs in the event_data section
    for key, value in event.get("event_data", {}).items():
        # Convert hex-formatted values (e.g., "0x12") into integers
        new_data[key] = convert_hex(value)

    # Replace original event_data with the cleaned data
    event["event_data"] = new_data

    # Return the normalized Security event
    return event
