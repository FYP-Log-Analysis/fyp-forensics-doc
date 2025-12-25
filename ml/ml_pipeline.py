# This script runs the full ML pipeline: feature extraction and anomaly detection.

import subprocess
import sys
import os

# Paths to scripts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FEATURE_SCRIPT = os.path.join(SCRIPT_DIR, "feature_engineering", "feature_extraction.py")
ISOLATION_SCRIPT = os.path.join(SCRIPT_DIR, "isolation_forest.py")

# Run feature extraction
print("Step 1: Extracting features...")
result = subprocess.run([sys.executable, FEATURE_SCRIPT])
if result.returncode != 0:
    print("Feature extraction failed.")
    sys.exit(1)

# Run isolation forest
print("Step 2: Running isolation forest...")
result = subprocess.run([sys.executable, ISOLATION_SCRIPT])
if result.returncode != 0:
    print("Isolation forest failed.")
    sys.exit(1)

print("ML pipeline completed successfully.")
