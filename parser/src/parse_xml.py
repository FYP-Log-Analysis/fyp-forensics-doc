import os
import json
import xml.etree.ElementTree as ET

INPUT_DIRECTORY = "../../data/processed/"
OUTPUT_DIRECTORY = "../../data/processed/json/"

os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# Microsoft's XML namespace for event logs - we need this to find anything
NS = {"e": "http://schemas.microsoft.com/win/2004/08/events/event"}


def parse_event(xml_string):
    """Take a chunk of XML and extract all the useful event data from it."""

    try:
        root = ET.fromstring(xml_string)

        system = root.find("e:System", NS)
        if system is None:
            return None

        event_data = root.find("e:EventData", NS)

        record = {
            "event_id": system.findtext("e:EventID", None, NS),
            "version": system.findtext("e:Version", None, NS),
            "level": system.findtext("e:Level", None, NS),
            "task": system.findtext("e:Task", None, NS),
            "opcode": system.findtext("e:Opcode", None, NS),
            "keywords": system.findtext("e:Keywords", None, NS),
            "timestamp": (
                system.find("e:TimeCreated", NS).attrib.get("SystemTime")
                if system.find("e:TimeCreated", NS) is not None else None
            ),
            "record_id": system.findtext("e:EventRecordID", None, NS),
            "computer": system.findtext("e:Computer", None, NS),
            "channel": system.findtext("e:Channel", None, NS),
            "security_user": (
                system.find("e:Security", NS).attrib.get("UserID")
                if system.find("e:Security", NS) is not None else None
            ),
            "event_data": {}
        }

        # Pull out the actual event details if they exist
        if event_data is not None:
            for child in event_data:
                name = child.attrib.get("Name", child.tag)
                record["event_data"][name] = child.text

        return record

    except Exception:
        return None


def convert_file(filename):
    """Read an XML log file and turn it into a nice JSON array of events."""

    input_path = os.path.join(INPUT_DIRECTORY, filename)
    output_path = os.path.join(OUTPUT_DIRECTORY, filename.replace(".xml", ".json"))

    print(f"Converting {filename}...")

    inside_event = False
    buffer = []
    count = 0

    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        outfile.write("[\n")
        first = True

        for line in infile:
            stripped = line.strip()

            # Found the start of a new event - start collecting lines
            if stripped.startswith("<Event "):
                inside_event = True
                buffer = [line]
                continue

            # Keep adding lines while we're inside an event
            if inside_event:
                buffer.append(line)

            # Hit the end - time to process this event
            if stripped == "</Event>":
                inside_event = False

                xml_block = "".join(buffer)
                event = parse_event(xml_block)

                if event:
                    if not first:
                        outfile.write(",\n")
                    outfile.write(json.dumps(event))
                    first = False
                    count += 1

        outfile.write("\n]\n")

    print(f"[OK] Parsed {count} events → {output_path}")


def main():
    xml_files = [f for f in os.listdir(INPUT_DIRECTORY) if f.endswith(".xml")]
    for xml in xml_files:
        convert_file(xml)


if __name__ == "__main__":
    main()
