from .utils import clean_event_data


def normalize_application_event(event):
    """
    Clean up Application channel events so they're easier to work with.
    
    Takes the messy raw event and fixes the event_id (string -> int) and
    cleans up all the XML namespace junk in the event_data.
    """
    # Make the event ID a proper integer so we can filter on it easily
    event["event_id"] = int(event["event_id"])
    
    # Strip out all the XML namespace cruft and extract the actual values
    event["event_data"] = clean_event_data(event.get("event_data", {}))
    
    return event
