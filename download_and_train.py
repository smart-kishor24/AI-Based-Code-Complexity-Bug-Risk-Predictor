"""
Download and Train script.
Fetches legitimate NASA PROMISE defect datasets (KC1 / JM1) from OpenML / public repositories,
caches them locally in dataset/, and runs the full ML training & evaluation pipeline.
"""

import sys
from pathlib import Path
import pandas as pd
from sklearn.datasets import fetch_openml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config.settings import DATASET_DIR
from modules.data_loader import DefectDataLoader
from modules.model_trainer import DefectModelTrainer


def main():
    print("=== Step 1: Downloading legitimate NASA PROMISE Dataset ===")
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    kc1_path = DATASET_DIR / "kc1.csv"

    if not kc1_path.exists():
        print("Fetching NASA KC1 dataset from OpenML (Data ID: 1067)...")
        try:
            kc1_openml = fetch_openml(data_id=1067, as_frame=True, parser="auto")
            df_kc1 = kc1_openml.frame
            df_kc1.to_csv(kc1_path, index=False)
            print(f"Successfully saved NASA KC1 dataset: {len(df_kc1)} records to {kc1_path}")
        except Exception as e:
            print(f"Failed to fetch KC1 from OpenML: {e}")
            print("Attempting to fetch JM1 (OpenML ID: 1039)...")
            try:
                jm1_openml = fetch_openml(data_id=1039, as_frame=True, parser="auto")
                df_jm1 = jm1_openml.frame
                df_jm1.to_csv(DATASET_DIR / "jm1.csv", index=False)
                print(f"Successfully saved NASA JM1 dataset: {len(df_jm1)} records.")
            except Exception as e2:
                print(f"Failed to fetch JM1: {e2}")

    print("\n=== Step 2: Loading & Cleaning Dataset ===")
    X, y, feature_names, metadata = DefectDataLoader.load_dataset()
    print("Dataset Metadata Summary:")
    for k, v in metadata.items():
        if k != "feature_names":
            print(f"  {k}: {v}")

    print("\n=== Step 3: Training & Evaluating ML Models ===")
    trainer = DefectModelTrainer(random_state=42)
    primary_model, primary_eval, all_evals = trainer.train_and_evaluate_all(X, y)

    print("\n=== Model Benchmark Results ===")
    for res in all_evals:
        print(f"\nModel: {res['model_name']}")
        print(f"  Accuracy:  {res['accuracy']*100:.2f}%")
        print(f"  Precision: {res['precision']*100:.2f}%")
        print(f"  Recall:    {res['recall']*100:.2f}%")
        print(f"  F1-Score:  {res['f1_score']*100:.2f}%")
        print(f"  ROC-AUC:   {res['roc_auc']:.4f}")
        print(f"  5-Fold CV F1: {res.get('cv_f1_mean', 0.0)*100:.2f}%")
        cm = res['confusion_matrix']
        print(f"  Confusion Matrix: TN={cm['tn']}, FP={cm['fp']}, FN={cm['fn']}, TP={cm['tp']}")

    print("\nTop 5 Feature Importances (Random Forest):")
    for imp in primary_eval.get("feature_importances", [])[:5]:
        print(f"  {imp['feature']}: {imp['importance']:.4f}")

    print("\nArtifacts saved successfully.")


if __name__ == "__main__":
    main()
