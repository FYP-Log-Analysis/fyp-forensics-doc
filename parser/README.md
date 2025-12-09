# Parser Service

This service handles parsing Windows Event Log (.evtx) files into structured JSON format.

## Overview

The parser service is responsible for:
- Processing .evtx files from the raw_logs directory
- Converting binary event logs to structured JSON format
- Storing parsed output in the data/processed directory
- Handling various Windows event log formats

## Structure

- `src/` - Source code for the parser service