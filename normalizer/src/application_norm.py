# =============================================================================
# Application Channel Event Normalizer
# =============================================================================
# Handles normalization of Windows Application event logs.
#
# Application logs contain:
#   - Software application errors and warnings
#   - Application lifecycle events (start, stop, crash)
#   - Custom application-specific messages
#
# Normalization steps:
#   1. Convert event_id from string to integer
#   2. Clean event_data by removing XML namespaces
#   3. Extract string values from XML tags
# =============================================================================

from .utils import clean_event_data


def normalize_application_event(event):
    """
    Normalize an Application channel event.
    
    Args:
        event: Raw event dictionary with string event_id and messy event_data
    
    Returns:
        Normalized event with integer event_id and cleaned event_data
    """
    # Convert event ID to integer for easier querying and filtering
    event["event_id"] = int(event["event_id"])
    
    # Clean up the event_data dictionary:
    # - Remove XML namespace prefixes from keys
    # - Extract values from <string> tags
    event["event_data"] = clean_event_data(event.get("event_data", {}))
    
    return event
