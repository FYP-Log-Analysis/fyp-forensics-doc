import os
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view

# Where we keep the raw .evtx files that need processing
RAW_DIR = "../../data/raw_logs/"

# Where we'll dump the converted XML files for the next step
OUT_DIR = "../../data/processed/"


def ingest():
    """
    Takes all the .evtx files we've collected and converts them to XML.
    
    This makes them way easier to work with in the next steps - the XML
    is much more readable than the binary .evtx format, and our parser
    can handle it without needing special Windows event log libraries.
    """

    # Grab all the .evtx files we need to process
    evtx_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".evtx")]

    for filename in evtx_files:
        input_path = os.path.join(RAW_DIR, filename)
        output_path = os.path.join(OUT_DIR, filename.replace(".evtx", ".xml"))

        # Open the evtx file and stream it out as XML
        with Evtx(input_path) as evtx_log:
            with open(output_path, "w") as xml_output:
                for xml_event, _ in evtx_file_xml_view(evtx_log):
                    xml_output.write(xml_event + "\n")

        print(f"Finished converting {filename} → {output_path}")


if __name__ == "__main__":
    ingest()
