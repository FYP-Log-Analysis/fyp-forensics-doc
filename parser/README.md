# README — XML to JSON Parser (`parse_xml.py`)

## What this script does

`parse_xml.py` is the parser for this project’s Windows event log pipeline.
After the ingestion step exports `.evtx` files into XML, this script takes those XML files and converts them into clean, structured JSON that the rest of the system can actually work with.

The parser is built to handle:

* Multi-line `<Event>...</Event>` blocks
* Windows Event Log namespaces
* Very large files (hundreds of thousands of events)
* Random malformed or incomplete XML entries
* Efficient, streaming-style processing so memory usage stays low

The output from this step becomes the input for the **behavior analysis** and **detection** modules.

---

## Where the files go

### **Input (`data/processed/`)**

This folder contains the XML output from the ingestion module:

```
Application.xml
Security.xml
System.xml
PowerShell_Operational.xml
```

Each file contains a sequence of full Windows Event Log `<Event>` blocks.

### **Output (`data/processed/json/`)**

This is where the script writes the converted JSON files:

```
Application.json
Security.json
System.json
PowerShell_Operational.json
```

Each JSON file is an array of event objects.

---

## How the parser works (in simple terms)

1. It reads each XML file line by line.
2. Whenever it finds `<Event ...>`, it starts collecting lines until it reaches `</Event>`.
3. It parses that full block using `ElementTree` with namespace support.
4. It extracts fields like:

   * EventID
   * Timestamp
   * Level
   * Channel
   * Computer name
   * Security User SID
5. It also reads everything inside `<EventData>` and turns those into key–value pairs.
6. It writes each event into a JSON array in a streaming way to avoid loading everything into memory at once.

Anything malformed or incomplete is simply skipped.

---

## How to run it

Inside the `parser/src` folder:

```bash
python3 parse_xml.py
```

It will automatically scan for all `.xml` files inside:

```
../../data/processed/
```

and write `.json` files into:

```
../../data/processed/json/
```

Example output:

```
Converting Security.xml...
[OK] Parsed 48,312 events → Security.json
```

---

## Example of what a parsed event looks like

```json
{
  "event_id": "4624",
  "timestamp": "2025-11-23T09:25:27.038235+00:00",
  "computer": "WIN-E0UGH20N01E",
  "channel": "Security",
  "security_user": "S-1-5-18",
  "event_data": {
    "LogonType": "3",
    "TargetUserName": "Administrator",
    "IpAddress": "192.168.1.10"
  }
}
```

This structure makes it much easier to do behavior analysis, search, filtering, and detection later on.

---

## Why this file matters

The ingestion step gives you raw XML, but XML isn’t fun to work with — especially in security logs where everything is deeply nested.
This parser turns all that into clean, usable JSON that:

* The behavior engine can analyze
* The detection module can run rules on
* The dashboard can display
* ML/LLM features can be pulled from

It converts “raw logs” into “forensic data.”