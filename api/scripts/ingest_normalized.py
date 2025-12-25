import json
import glob
import sys
import os
from datetime import datetime
from pathlib import Path

# Add the API directory to Python path
api_dir = Path(__file__).parent.parent
sys.path.append(str(api_dir))

try:
    from main import SessionLocal
    from models.normalized_log import NormalizedLog
except ImportError:
    # If we can't import from main, skip database operations
    print("Warning: Database not available, skipping database ingestion")
    SessionLocal = None
    NormalizedLog = None


def load_logs():
    if SessionLocal is None or NormalizedLog is None:
        print("Skipping database ingestion - database not available")
        return True
    
    db = SessionLocal()

    # Use relative path from project root
    project_root = Path(__file__).parent.parent.parent
    normalized_dir = project_root / "data" / "processed" / "normalized"
    
    files = list(normalized_dir.glob("*.json"))

    print(f"Found {len(files)} files to load.")

    if not files:
        print("No normalized files found to load")
        return True

    for file in files:
        print(f"Loading {file}...")
        with open(file, "r") as f:
            logs = json.load(f)

        for log in logs:
            ts_string = log.get("timestamp")
            if not ts_string:
                continue

            timestamp = datetime.fromisoformat(ts_string.replace("Z", "+00:00"))

            db_entry = NormalizedLog(
                timestamp=timestamp,
                event_id=log.get("event_id"),
                source=log.get("source"),
                user_name=log.get("user"),
                computer=log.get("computer"),
                process_path=log.get("process_path"),
                command_line=log.get("command_line"),
                category=log.get("category"),
                summary=log.get("summary"),
                raw=log
            )

            db.add(db_entry)

        db.commit()

    db.close()
    print("Uploaded all logs.")
    return True

if __name__ == "__main__":
    success = load_logs()
    if not success:
        exit(1)
