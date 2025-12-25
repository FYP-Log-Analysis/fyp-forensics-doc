import os
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view
from pathlib import Path

# Get absolute paths relative to this script's location
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# Where we keep the raw .evtx files that need processing
RAW_DIR = PROJECT_ROOT / "data" / "raw_logs"

# Where we'll dump the converted XML files for the next step
OUT_DIR = PROJECT_ROOT / "data" / "processed" / "xml"


def ingest():
    """
    Takes all the .evtx files we've collected and converts them to XML.
    
    This makes them way easier to work with in the next steps - the XML
    is much more readable than the binary .evtx format, and our parser
    can handle it without needing special Windows event log libraries.
    """
    
    # Create directories if they don't exist
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if raw directory exists and has files
    if not RAW_DIR.exists():
        print(f"Error: Raw logs directory not found: {RAW_DIR}")
        return False
    
    # Grab all the .evtx files we need to process
    evtx_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".evtx")]
    
    if not evtx_files:
        print(f"No .evtx files found in {RAW_DIR}")
        print("Available files:", list(os.listdir(RAW_DIR)) if RAW_DIR.exists() else "Directory not found")
        return False

    print(f"Found {len(evtx_files)} .evtx files to process")

    for filename in evtx_files:
        input_path = RAW_DIR / filename
        output_path = OUT_DIR / filename.replace(".evtx", ".xml")

        try:
            # Open the evtx file and stream it out as XML
            with Evtx(str(input_path)) as evtx_log:
                with open(output_path, "w", encoding='utf-8') as xml_output:
                    xml_output.write('<?xml version="1.0" encoding="utf-8"?>\n<Events>\n')
                    
                    for xml_event, _ in evtx_file_xml_view(evtx_log):
                        xml_output.write(xml_event + "\n")
                    
                    xml_output.write('</Events>\n')

            print(f"Finished converting {filename} → {output_path}")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            return False
    
    return True


if __name__ == "__main__":
    success = ingest()
    if not success:
        print("Ingestion failed!")
        exit(1)
    else:
        print("Ingestion completed successfully!")
