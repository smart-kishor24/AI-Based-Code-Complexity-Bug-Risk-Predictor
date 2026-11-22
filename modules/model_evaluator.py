"""
Model Evaluation module.
Calculates rigorous evaluation metrics for software defect prediction models,
including Confusion Matrix, ROC-AUC, Precision, Recall, F1-Score, and curves for Plotly visualization.
"""

from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve,
)


class ModelEvaluator:
    """Computes and visualizes model performance metrics."""

    @classmethod
    def evaluate(
        cls,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: Optional[np.ndarray] = None,
        model_name: str = "Model",
    ) -> Dict[str, Any]:
        """
        Computes standard classification evaluation metrics.
        """
        acc = float(accuracy_score(y_true, y_pred))
        prec = float(precision_score(y_true, y_pred, zero_division=0))
        rec = float(recall_score(y_true, y_pred, zero_division=0))
        f1 = float(f1_score(y_true, y_pred, zero_division=0))

        roc_auc = 0.5
        if y_prob is not None:
            try:
                roc_auc = float(roc_auc_score(y_true, y_prob))
            except Exception:
                roc_auc = 0.5

        cm = confusion_matrix(y_true, y_pred).tolist()
        tn, fp, fn, tp = (
            int(cm[0][0]),
            int(cm[0][1]),
            int(cm[1][0]),
            int(cm[1][1]),
        ) if len(cm) == 2 and len(cm[0]) == 2 else (0, 0, 0, 0)

        # ROC Curve Points
        roc_data = {}
        if y_prob is not None:
            try:
                fpr, tpr, roc_thresh = roc_curve(y_true, y_prob)
                roc_data = {
                    "fpr": fpr.tolist(),
                    "tpr": tpr.tolist(),
                    "thresholds": roc_thresh.tolist(),
                }
            except Exception:
                roc_data = {"fpr": [0.0, 1.0], "tpr": [0.0, 1.0], "thresholds": [1.0, 0.0]}

        # Precision-Recall Curve Points
        pr_data = {}
        if y_prob is not None:
            try:
                prec_arr, rec_arr, pr_thresh = precision_recall_curve(y_true, y_prob)
                pr_data = {
                    "precision": prec_arr.tolist(),
                    "recall": rec_arr.tolist(),
                    "thresholds": pr_thresh.tolist(),
                }
            except Exception:
                pr_data = {"precision": [prec, prec], "recall": [1.0, 0.0], "thresholds": [0.5]}

        report_dict = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

        return {
            "model_name": model_name,
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "confusion_matrix": {
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tp": tp,
                "matrix": cm,
            },
            "roc_curve": roc_data,
            "pr_curve": pr_data,
            "classification_report": report_dict,
        }

    @classmethod
    def compare_models(cls, evaluation_results: List[Dict[str, Any]]) -> pd.DataFrame:
        """Constructs a side-by-side comparison DataFrame of multiple evaluated models."""
        rows = []
        for res in evaluation_results:
            rows.append({
                "Model": res.get("model_name", "Unknown"),
                "Accuracy": f"{res.get('accuracy', 0.0) * 100:.2f}%",
                "Precision": f"{res.get('precision', 0.0) * 100:.2f}%",
                "Recall": f"{res.get('recall', 0.0) * 100:.2f}%",
                "F1-Score": f"{res.get('f1_score', 0.0) * 100:.2f}%",
                "ROC-AUC": f"{res.get('roc_auc', 0.0):.4f}",
            })
        return pd.DataFrame(rows)
