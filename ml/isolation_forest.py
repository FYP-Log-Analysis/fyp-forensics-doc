import json
from pathlib import Path
from sklearn.ensemble import IsolationForest

# Set up file paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_FILE = PROJECT_ROOT / "data" / "features" / "baseline_features.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "detection_results" / "isolation_forest_scores.json"

# Make sure output directory exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_features(file_path):
    # Load features from JSON file
    with open(file_path, "r") as file:
        return json.load(file)

def build_feature_matrix(feature_rows):
    # Convert features to matrix for machine learning
    matrix = []
    for row in feature_rows:
        vector = [
            row["event_count"],
            row["process_event_count"],
            row["unique_process_count"],
            row["unique_user_count"],
            row["system32_exec_count"],
            row["non_system32_exec_count"],
            row["registry_event_count"]
        ]
        matrix.append(vector)
    return matrix

def run_isolation_forest(feature_matrix):
    # Run anomaly detection
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(feature_matrix)
    scores = model.decision_function(feature_matrix)
    labels = model.predict(feature_matrix)
    return scores, labels

def save_results(windows, scores, labels, output_path):
    # Save results to file
    results = []
    for i in range(len(windows)):
        results.append({
            "window_start": windows[i]["window_start"],
            "window_end": windows[i]["window_end"],
            "anomaly_score": float(scores[i]),
            "is_anomalous": True if labels[i] == -1 else False
        })
    with open(output_path, "w") as file:
        json.dump(results, file, indent=2)

def main():
    if not INPUT_FILE.exists():
        print("Error: Input file not found.")
        return
    print("Loading features...")
    feature_rows = load_features(INPUT_FILE)
    print("Building feature matrix...")
    feature_matrix = build_feature_matrix(feature_rows)
    print("Running isolation forest...")
    scores, labels = run_isolation_forest(feature_matrix)
    print("Saving results...")
    save_results(feature_rows, scores, labels, OUTPUT_FILE)
    print(f"Done! Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()