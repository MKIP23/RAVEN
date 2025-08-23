import pandas as pd
import os
import re
import joblib
import time
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    confusion_matrix, f1_score, classification_report
)

def parse_gem5_stats(file_path):
    """Parse gem5 statistics file into a dictionary"""
    data = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = re.split(r'\s+', line, maxsplit=2)
            if len(parts) < 2:
                continue

            metric_name = parts[0]
            value = parts[1]

            try:
                value = float(value) if '.' in value else int(value)
                data[metric_name] = value
            except ValueError:
                continue
    return data

def load_test_data(directory):
    """Load stats files from a directory (no labels)"""
    data = []
    file_names = []
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith('.txt'):
            continue

        file_path = os.path.join(directory, filename)
        metrics = parse_gem5_stats(file_path)
        if metrics:
            data.append(metrics)
            file_names.append(filename)
    return pd.DataFrame(data), file_names

def main():
    # Load trained model
    model_path = 'spectre_rf_model.pkl'
    model = joblib.load(model_path)

    # Load and tag test data
    df_attack, files_attack = load_test_data('attack_stats_dir_test')
    df_benign, files_benign = load_test_data('benign_stats_dir_test')

    test_df = pd.concat([df_attack, df_benign], ignore_index=True)
    true_labels = [1]*len(df_attack) + [0]*len(df_benign)
    test_files = files_attack + files_benign

    # Ensure only columns seen during training are used
    expected_features = model.feature_names_in_
    test_df = test_df.reindex(columns=expected_features, fill_value=0)

    # Inference timing
    start_time = time.time()
    predictions = model.predict(test_df)
    inference_time = time.time() - start_time

    # Evaluation metrics
    acc = accuracy_score(true_labels, predictions)
    prec = precision_score(true_labels, predictions)
    rec = recall_score(true_labels, predictions)
    f1 = f1_score(true_labels, predictions)
    tn, fp, fn, tp = confusion_matrix(true_labels, predictions).ravel()

    # Model size in KB
    model_size_kb = os.path.getsize(model_path) / 1024

    # Print metrics
    print("\n--- Evaluation on Test Set ---")
    print(f"Accuracy:      {acc:.4f}")
    print(f"Precision:     {prec:.4f}")
    print(f"Recall:        {rec:.4f}")
    print(f"F1 Score:      {f1:.4f}")
    print(f"Inference Time:{inference_time:.6f} seconds")
    print(f"Model Size:    {model_size_kb:.2f} KB")

    print("\nConfusion Matrix:")
    print(f"TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}")

    print("\nClassification Report:")
    print(classification_report(true_labels, predictions, target_names=["Benign", "Attack"]))

    print("\n--- Prediction Results per File ---")
    for fname, pred in zip(test_files, predictions):
        label = "Attack" if pred == 1 else "Benign"
        print(f"{fname}: {label}")

if __name__ == "__main__":
    main()
