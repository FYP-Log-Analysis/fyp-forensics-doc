import re
import json

# Pattern to match XML namespaces like {http://...}
NAMESPACE_REGEX = r"\{.*?\}"

def remove_xml_namespace(key: str) -> str:
    """Remove the XML namespace from keys."""
    # Strip XML namespace prefix from the key
    return re.sub(NAMESPACE_REGEX, "", key)

def extract_strings(raw_str: str):
    """Extract <string>...</string> values from XML-like data."""
    # If not a string, return the value unchanged
    if not isinstance(raw_str, str):
        return raw_str

    # Find all <string>...</string> occurrences
    matches = re.findall(r"<string>(.*?)</string>", raw_str, re.DOTALL)

    # If only one string value found, return it directly
    if len(matches) == 1:
        return matches[0]

    # If multiple strings found, return as a list
    return matches

def convert_hex(value: str):
    """Convert hex strings like '0x00000012' to integers."""
    # Check if the value is hex-format
    if isinstance(value, str) and value.startswith("0x"):
        try:
            # Convert hex string to integer
            return int(value, 16)
        except ValueError:
            # If conversion fails, return original value
            return value

    # Return unchanged if not hex
    return value

def clean_event_data(event_data: dict):
    """Clean all keys and extract string values for Application/System logs."""
    new_data = {}

    # Process each key-value pair in event_data
    for key, value in event_data.items():

        # Remove XML namespace from the key
        clean_key = remove_xml_namespace(key)

        # Extract <string> content or return original value
        new_data[clean_key] = extract_strings(value)

    # Return cleaned dictionary
    return new_data
