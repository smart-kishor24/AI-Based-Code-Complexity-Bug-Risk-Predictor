"""
Defect Risk Predictor module.
Loads the trained ML model and predicts defect probabilities and risk categories
for extracted functions based on software complexity and structural metrics.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import joblib

from config.settings import (
    PRIMARY_MODEL_FILE,
    SCALER_FILE,
    METRIC_COLUMNS_FILE,
    MODEL_METRICS_FILE,
    DEFAULT_LOW_RISK_THRESHOLD,
    DEFAULT_HIGH_RISK_THRESHOLD,
)


class DefectRiskPredictor:
    """Predicts defect probability and classifies functions into risk tiers."""

    def __init__(
        self,
        low_risk_threshold: float = DEFAULT_LOW_RISK_THRESHOLD,
        high_risk_threshold: float = DEFAULT_HIGH_RISK_THRESHOLD,
    ):
        self.low_threshold = low_risk_threshold
        self.high_threshold = high_risk_threshold
        self.model: Optional[Any] = None
        self.scaler: Optional[Any] = None
        self.feature_names: List[str] = []
        self._load_model_artifacts()

    def _load_model_artifacts(self) -> bool:
        """Loads serialized model, scaler, and feature schema from disk."""
        if PRIMARY_MODEL_FILE.exists() and SCALER_FILE.exists() and METRIC_COLUMNS_FILE.exists():
            try:
                self.model = joblib.load(PRIMARY_MODEL_FILE)
                self.scaler = joblib.load(SCALER_FILE)
                self.feature_names = joblib.load(METRIC_COLUMNS_FILE)
                return True
            except Exception as e:
                print(f"Error loading model artifacts: {e}")
                self.model = None
                return False
        return False

    def is_model_ready(self) -> bool:
        """Checks if a trained model is ready for inference."""
        return self.model is not None and self.scaler is not None and len(self.feature_names) > 0

    def prepare_feature_matrix(self, function_df: pd.DataFrame) -> pd.DataFrame:
        """
        Maps extracted function metrics into model input features aligned with training schema.
        """
        X_input = pd.DataFrame(index=function_df.index)

        for col in self.feature_names:
            if col in function_df.columns:
                X_input[col] = function_df[col]
            elif col == "cyclomatic_complexity" and "cyclomatic_complexity" in function_df.columns:
                X_input[col] = function_df["cyclomatic_complexity"]
            elif col == "branch_count" and "condition_count" in function_df.columns:
                X_input[col] = function_df["condition_count"] + function_df.get("loop_count", 0)
            elif col == "essential_complexity" and "max_nesting_depth" in function_df.columns:
                X_input[col] = np.maximum(1, function_df["max_nesting_depth"])
            elif col == "design_complexity" and "call_count" in function_df.columns:
                X_input[col] = np.maximum(1, function_df["call_count"] + 1)
            elif col == "loc_code" and "loc" in function_df.columns:
                X_input[col] = function_df["loc"]
            elif col == "loc_comment":
                X_input[col] = 0.0
            elif col == "loc_blank":
                X_input[col] = 0.0
            elif col == "loc_code_comment":
                X_input[col] = 0.0
            else:
                X_input[col] = 0.0

        return X_input.fillna(0.0).astype(float)

    def predict_function_risk(self, function_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Calculates defect risk probabilities for each function in the DataFrame.
        Maps extracted function metrics into model input features.
        """
        if function_df.empty:
            return []

        if not self.is_model_ready():
            # If no trained model yet, return heuristic baseline with clear disclosure
            return self._heuristic_fallback_predictions(function_df)

        # Build feature matrix matching model training columns
        X_input = self.prepare_feature_matrix(function_df)

        # Scale features
        try:
            X_scaled = self.scaler.transform(X_input)
        except Exception:
            # In case of feature shape mismatch, re-align
            X_scaled = np.zeros((len(X_input), len(self.feature_names)))

        # Get probabilities
        try:
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(X_scaled)[:, 1]
            else:
                probs = self.model.predict(X_scaled).astype(float)
        except Exception as e:
            print(f"Prediction failed: {e}")
            return self._heuristic_fallback_predictions(function_df)

        results = []
        for i, row in function_df.iterrows():
            prob = float(probs[i])
            category, color = self._classify_probability(prob)
            results.append({
                "function_name": str(row.get("function_name", f"func_{i}")),
                "class_name": str(row.get("class_name", "(Global)")),
                "start_line": int(row.get("start_line", 1)),
                "end_line": int(row.get("end_line", 1)),
                "loc": int(row.get("loc", 1)),
                "cyclomatic_complexity": int(row.get("cyclomatic_complexity", 1)),
                "defect_probability": round(prob, 4),
                "predicted_class": 1 if prob >= 0.50 else 0,
                "risk_category": category,
                "risk_color": color,
                "model_used": type(self.model).__name__,
                "is_ml_prediction": True,
            })

        return results

    def _classify_probability(self, probability: float) -> Tuple[str, str]:
        """Maps probability to risk tier and badge color."""
        if probability < self.low_threshold:
            return "Low Risk", "#28a745"  # Green
        elif probability <= self.high_threshold:
            return "Medium Risk", "#ffc107"  # Yellow
        else:
            return "High Risk", "#dc3545"  # Red

    def _heuristic_fallback_predictions(self, function_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Defensible rule-based scoring when ML model has not yet been trained,
        clearly labeled as heuristic demonstration.
        """
        results = []
        for i, row in function_df.iterrows():
            cc = float(row.get("cyclomatic_complexity", 1))
            loc = float(row.get("loc", 1))
            depth = float(row.get("max_nesting_depth", 1))

            # Heuristic normalized risk score [0, 1]
            score = min(1.0, (cc / 20.0) * 0.5 + (loc / 80.0) * 0.3 + (depth / 6.0) * 0.2)
            prob = round(score, 4)
            category, color = self._classify_probability(prob)

            results.append({
                "function_name": str(row.get("function_name", f"func_{i}")),
                "class_name": str(row.get("class_name", "(Global)")),
                "start_line": int(row.get("start_line", 1)),
                "end_line": int(row.get("end_line", 1)),
                "loc": int(loc),
                "cyclomatic_complexity": int(cc),
                "defect_probability": prob,
                "predicted_class": 1 if prob >= 0.50 else 0,
                "risk_category": category,
                "risk_color": color,
                "model_used": "Heuristic Rule-Based Engine (ML Model Not Yet Loaded)",
                "is_ml_prediction": False,
            })
        return results
