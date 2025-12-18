import subprocess
import sys
import os


def run_pipeline():

    # Get the root directory of the project

    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    # List of pipeline scripts in the order they must run
    steps = [
        "analysis/preprocessing/event_filter.py",
        "analysis/preprocessing/window_aggregation.py",
        "analysis/feature_engineering/feature_extraction.py",
        "analysis/detection/isolation_forest.py"
    ]

    # Run each step one by one
    for step in steps:
        script_path = os.path.join(project_root, step)

        print("Running:", script_path)

        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True
        )

        # If a step fails, stop the pipeline
        if result.returncode != 0:
            return {
                "status": "failed",
                "failed_step": step,
                "error_message": result.stderr
            }

    # If all steps run 
    return {
        "status": "success",
        "message": "200"
    }
