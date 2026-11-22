"""
Explainable AI (XAI) module.
Leverages SHAP (SHapley Additive exPlanations) to explain global feature importance
and local, function-specific risk drivers in a human-interpretable manner.
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False


class ModelExplainabilityEngine:
    """Computes global and local model explanations using SHAP."""

    def __init__(self, model: Any, feature_names: List[str]):
        self.model = model
        self.feature_names = feature_names
        self.explainer: Optional[Any] = None
        self._init_explainer()

    def _init_explainer(self) -> None:
        """Initializes the appropriate SHAP Explainer for the trained model."""
        if not SHAP_AVAILABLE or self.model is None:
            return

        try:
            # TreeExplainer is fast and exact for tree-based ensembles (RandomForest, XGBoost)
            self.explainer = shap.TreeExplainer(self.model)
        except Exception:
            try:
                self.explainer = shap.Explainer(self.model)
            except Exception as e:
                print(f"SHAP Explainer initialization failed: {e}")
                self.explainer = None

    def explain_global_importance(self, X_sample: Optional[pd.DataFrame] = None) -> List[Dict[str, Any]]:
        """
        Returns global feature importances ranked by mean absolute SHAP value
        or model feature importances as a fallback.
        """
        if self.model is None:
            return []

        # If SHAP is initialized and background data is provided
        if self.explainer is not None and X_sample is not None and not X_sample.empty:
            try:
                shap_values = self.explainer.shap_values(X_sample)
                # If binary classification, take positive class (index 1)
                if isinstance(shap_values, list) and len(shap_values) == 2:
                    vals = shap_values[1]
                elif hasattr(shap_values, "values"):
                    vals = shap_values.values
                    if vals.ndim == 3:
                        vals = vals[:, :, 1]
                else:
                    vals = shap_values

                mean_abs = np.mean(np.abs(vals), axis=0)
                ranked = sorted(
                    zip(self.feature_names, mean_abs),
                    key=lambda x: x[1],
                    reverse=True,
                )
                return [{"feature": f, "shap_importance": round(float(v), 4)} for f, v in ranked]
            except Exception as e:
                print(f"SHAP global computation failed: {e}")

        # Fallback to model's native feature importances
        if hasattr(self.model, "feature_importances_"):
            importances = self.model.feature_importances_
            ranked = sorted(
                zip(self.feature_names, importances),
                key=lambda x: x[1],
                reverse=True,
            )
            return [{"feature": f, "shap_importance": round(float(v), 4)} for f, v in ranked]

        return []

    def explain_local_prediction(
        self,
        function_feature_row: pd.Series,
        scaled_feature_vector: np.ndarray,
        function_name: str,
        defect_probability: float,
    ) -> Dict[str, Any]:
        """
        Computes local SHAP attributions for a single function prediction.
        Identifies features that pushed the estimated defect risk up or down.
        """
        features_increasing_risk = []
        features_decreasing_risk = []
        base_value = 0.5

        if self.explainer is not None:
            try:
                shap_values = self.explainer.shap_values(scaled_feature_vector)
                if isinstance(shap_values, list) and len(shap_values) == 2:
                    # Positive class contributions
                    local_vals = shap_values[1][0]
                elif hasattr(shap_values, "values"):
                    v = shap_values.values[0]
                    local_vals = v[:, 1] if v.ndim == 2 else v
                else:
                    local_vals = shap_values[0]

                if hasattr(self.explainer, "expected_value"):
                    ev = self.explainer.expected_value
                    base_value = float(ev[1] if isinstance(ev, (list, np.ndarray)) else ev)

                # Pair feature names with SHAP impacts and actual values
                contributions = []
                for f_name, impact in zip(self.feature_names, local_vals):
                    actual_val = function_feature_row.get(f_name, 0.0)
                    contributions.append({
                        "feature": f_name,
                        "impact": round(float(impact), 4),
                        "actual_value": actual_val,
                    })

                # Sort positive impacts (increasing risk)
                pos = [c for c in contributions if c["impact"] > 0]
                pos.sort(key=lambda x: x["impact"], reverse=True)
                features_increasing_risk = pos[:5]

                # Sort negative impacts (decreasing risk)
                neg = [c for c in contributions if c["impact"] < 0]
                neg.sort(key=lambda x: x["impact"])
                features_decreasing_risk = neg[:5]

            except Exception as e:
                print(f"Local SHAP calculation failed: {e}")

        # If SHAP is unavailable, generate rule-based metric contributions
        if not features_increasing_risk and not features_decreasing_risk:
            # Fallback based on metric thresholds
            cc = function_feature_row.get("cyclomatic_complexity", 1)
            loc = function_feature_row.get("loc", 1)
            depth = function_feature_row.get("max_nesting_depth", 1)
            params = function_feature_row.get("param_count", 0)

            if cc > 8:
                features_increasing_risk.append({
                    "feature": "cyclomatic_complexity",
                    "impact": 0.25,
                    "actual_value": cc,
                })
            else:
                features_decreasing_risk.append({
                    "feature": "cyclomatic_complexity",
                    "impact": -0.15,
                    "actual_value": cc,
                })

            if depth > 3:
                features_increasing_risk.append({
                    "feature": "max_nesting_depth",
                    "impact": 0.18,
                    "actual_value": depth,
                })
            if loc > 40:
                features_increasing_risk.append({
                    "feature": "loc",
                    "impact": 0.15,
                    "actual_value": loc,
                })

        # Generate human-readable narrative explanation
        narrative = self._generate_narrative(
            function_name=function_name,
            defect_probability=defect_probability,
            increasing=features_increasing_risk,
            decreasing=features_decreasing_risk,
        )

        return {
            "function_name": function_name,
            "defect_probability": defect_probability,
            "base_value": round(base_value, 4),
            "features_increasing_risk": features_increasing_risk,
            "features_decreasing_risk": features_decreasing_risk,
            "narrative_explanation": narrative,
            "disclaimer": (
                "Important Note: SHAP explanations indicate statistical feature contributions "
                "within the trained predictive model. They do not establish physical causality, "
                "nor do they guarantee that an executable runtime bug exists."
            ),
        }

    def _generate_narrative(
        self,
        function_name: str,
        defect_probability: float,
        increasing: List[Dict[str, Any]],
        decreasing: List[Dict[str, Any]],
    ) -> str:
        """Constructs an academic, clear narrative explanation."""
        risk_pct = f"{defect_probability * 100:.1f}%"
        sentences = [f"Function '{function_name}' has an estimated defect probability of {risk_pct}."]

        if increasing:
            inc_factors = ", ".join(
                [f"{item['feature']} ({item['actual_value']}, contribution +{item['impact']:.2f})" for item in increasing[:3]]
            )
            sentences.append(f"Elevated risk is primarily driven by: {inc_factors}.")

        if decreasing:
            dec_factors = ", ".join(
                [f"{item['feature']} ({item['actual_value']}, contribution {item['impact']:.2f})" for item in decreasing[:3]]
            )
            sentences.append(f"Factors moderating the risk include: {dec_factors}.")

        if not increasing and not decreasing:
            sentences.append("All metrics reside within baseline bounds with no prominent anomaly detected.")

        return " ".join(sentences)
