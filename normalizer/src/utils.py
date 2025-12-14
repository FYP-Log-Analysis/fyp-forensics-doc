import re
import json

# Regex to strip out those annoying XML namespace prefixes
NAMESPACE_REGEX = r"\{.*?\}"

def remove_xml_namespace(key: str) -> str:
    """Strip out XML namespace junk from keys so they're actually readable."""
    # Get rid of the {http://whatever} prefix
    return re.sub(NAMESPACE_REGEX, "", key)

def extract_strings(raw_str: str):
    """Pull out the actual values from <string> tags in XML data."""
    # If it's not a string, just leave it alone
    if not isinstance(raw_str, str):
        return raw_str

    # Look for anything wrapped in <string> tags
    matches = re.findall(r"<string>(.*?)</string>", raw_str, re.DOTALL)

    # If we found exactly one, return it as a plain string
    if len(matches) == 1:
        return matches[0]

    # If there are multiple, give back a list
    return matches

def convert_hex(value: str):
    """Turn hex strings like '0x00000012' into actual numbers."""
    # See if this looks like a hex value
    if isinstance(value, str) and value.startswith("0x"):
        try:
            # Try to parse it as hex
            return int(value, 16)
        except ValueError:
            # If that fails, just leave it as-is
            return value

    # Not hex, so don't touch it
    return value

def clean_event_data(event_data: dict):
    """Clean up the messy XML event data so it's actually usable."""
    new_data = {}

    # Go through each field and fix it up
    for key, value in event_data.items():

        # Strip the XML namespace cruft from the key name
        clean_key = remove_xml_namespace(key)

        # Pull out the actual content from <string> tags
        new_data[clean_key] = extract_strings(value)

    return new_data
