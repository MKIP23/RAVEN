import pandas as pd
import os
import re
import time
from scipy import stats
import numpy as np
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score
import joblib

def parse_gem5_stats(file_path):
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

def load_data(directory, label):
    data = []
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith('.txt'):
            continue
        file_path = os.path.join(directory, filename)
        metrics = parse_gem5_stats(file_path)
        if metrics:
            metrics['label'] = label
            data.append(metrics)
    return pd.DataFrame(data)

def main():
    # Load and combine data
    attack_df = load_data('attack_stats_dir', label=1)
    benign_df = load_data('benign_stats_dir', label=0)
    df = pd.concat([attack_df, benign_df], ignore_index=True)

    # Drop columns with missing values
    df = df.dropna(axis=1)

    # Separate features and label
    y = df['label']
    X = df.drop('label', axis=1)

    # Mann-Whitney U test
    attack = X[y == 1]
    benign = X[y == 0]
    results = []
    for col in X.columns:
        try:
            u_stat, p_val = stats.mannwhitneyu(attack[col], benign[col])
            with np.errstate(divide='ignore', invalid='ignore'):
                benign_median = np.median(benign[col])
                effect_size = (np.median(attack[col]) - benign_median) / benign_median
                effect_size = effect_size if np.isfinite(effect_size) else 0
            results.append({'Metric': col, 'p_value': p_val, 'Effect_Size': effect_size})
        except ValueError:
            continue

    results_df = pd.DataFrame(results)
    results_df['abs_effect'] = np.abs(results_df['Effect_Size'])
    results_df = results_df.sort_values(by=['p_value', 'abs_effect'], ascending=[True, False])
    print("\nTop 10 Discriminative Metrics (Mann-Whitney + Effect Size):")
    print(results_df.head(20)[['Metric', 'p_value', 'Effect_Size']].to_string(index=False))

    # Model training
    clf = RandomForestClassifier(n_estimators=90000, random_state=90042)
    start_time = time.time()
    clf.fit(X, y)
    end_time = time.time()
    model_time = end_time - start_time

    # Save model
    model_path = 'spectre_rf_model.pkl'
    joblib.dump(clf, model_path)
    model_size_kb = os.path.getsize(model_path) / 1024

    # Predict and evaluate
    y_pred = clf.predict(X)
    acc = accuracy_score(y, y_pred)
    prec = precision_score(y, y_pred)
    rec = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    f1_macro = f1_score(y, y_pred, average='macro')
    tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()
    #     # NEW: parameter count and FLOPs
    # num_params = get_num_parameters(clf)
    # avg_flops   = estimate_flops_per_inference(clf, X, subsample=200)

    print("\n--- Training Evaluation ---")
    print(f"Accuracy:       {acc:.4f}")
    print(f"Precision:      {prec:.4f}")
    print(f"Recall:         {rec:.4f}")
    print(f"F1 Score:       {f1:.4f}")
    print(f"F1 Macro:       {f1_macro:.4f}")
    print(f"Train Time:     {model_time:.2f} seconds")
    print(f"Model Size:     {model_size_kb:.2f} KB")
    print(f"TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}")
    # if num_params is not None:
    #     print(f"Number of Parameters: {num_params:,}")
    # if avg_flops is not None:
    #     print(f"Approx. FLOPs per Inference: {avg_flops:,.0f}")

    # Feature importance
    importances = clf.feature_importances_
    importance_df = pd.DataFrame({
        'Metric': X.columns,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)

    print("\nTop 20 Features by RandomForest Importance:")
    print(importance_df.head(20).to_string(index=False))

if __name__ == "__main__":
    main()
