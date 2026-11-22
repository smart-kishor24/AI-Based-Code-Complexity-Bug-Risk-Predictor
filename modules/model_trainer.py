"""
Model Trainer module.
Trains, tunes, compares, and serializes multiple Machine Learning algorithms
(Logistic Regression, Decision Tree, Random Forest, XGBoost) on software defect datasets.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from config.settings import (
    PRIMARY_MODEL_FILE,
    SCALER_FILE,
    METRIC_COLUMNS_FILE,
    MODEL_METRICS_FILE,
)
from modules.model_evaluator import ModelEvaluator

# Check for XGBoost availability
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


class DefectModelTrainer:
    """Trains and benchmarks defect risk estimation models."""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.trained_models: Dict[str, Any] = {}
        self.evaluation_results: List[Dict[str, Any]] = []
        self.best_model_name: str = "Random Forest"
        self.feature_names: List[str] = []

    def train_and_evaluate_all(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.20,
    ) -> Tuple[Any, Dict[str, Any], List[Dict[str, Any]]]:
        """
        Executes full training pipeline:
        - Stratified train/test split to prevent leakage
        - Feature scaling on train set
        - Training Logistic Regression, Decision Tree, Random Forest, and XGBoost
        - Stratified K-Fold Cross-Validation
        - Evaluation on holdout test set
        - Persistence of primary model, scaler, and evaluation metrics
        """
        self.feature_names = list(X.columns)

        # 1. Stratified split (prevents test data leakage)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )

        # 2. Fit Scaler ONLY on training data
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Calculate imbalance weight
        pos_count = int(y_train.sum())
        neg_count = len(y_train) - pos_count
        scale_pos_weight = float(neg_count / max(1, pos_count))

        # 3. Define candidate models
        models = {
            "Logistic Regression (Baseline)": LogisticRegression(
                class_weight="balanced",
                max_iter=1000,
                random_state=self.random_state,
            ),
            "Decision Tree": DecisionTreeClassifier(
                class_weight="balanced",
                max_depth=6,
                min_samples_split=10,
                random_state=self.random_state,
            ),
            "Random Forest (Primary)": RandomForestClassifier(
                n_estimators=120,
                max_depth=10,
                min_samples_split=5,
                class_weight="balanced",
                random_state=self.random_state,
                n_jobs=-1,
            ),
        }

        if XGBOOST_AVAILABLE:
            models["XGBoost Classifier"] = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.08,
                scale_pos_weight=scale_pos_weight,
                random_state=self.random_state,
                eval_metric="logloss",
                use_label_encoder=False,
            )

        self.evaluation_results = []
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)

        # 4. Train and evaluate each model
        for name, clf in models.items():
            # Cross-validation F1 score on training split
            cv_scores = cross_val_score(clf, X_train_scaled, y_train, cv=cv, scoring="f1")
            cv_f1_mean = float(np.mean(cv_scores))

            # Train on entire training set
            clf.fit(X_train_scaled, y_train)
            self.trained_models[name] = clf

            # Predict on holdout test set
            y_pred = clf.predict(X_test_scaled)
            if hasattr(clf, "predict_proba"):
                y_prob = clf.predict_proba(X_test_scaled)[:, 1]
            else:
                y_prob = None

            eval_res = ModelEvaluator.evaluate(
                y_true=y_test.to_numpy(),
                y_pred=y_pred,
                y_prob=y_prob,
                model_name=name,
            )
            eval_res["cv_f1_mean"] = round(cv_f1_mean, 4)
            self.evaluation_results.append(eval_res)

        # 5. Select primary model (Random Forest as per architecture specification)
        primary_key = "Random Forest (Primary)"
        primary_model = self.trained_models[primary_key]
        primary_eval = next(res for res in self.evaluation_results if res["model_name"] == primary_key)

        # Feature importances from Random Forest
        importances = primary_model.feature_importances_
        feature_importance_list = [
            {"feature": f_name, "importance": round(float(imp), 4)}
            for f_name, imp in sorted(zip(self.feature_names, importances), key=lambda x: x[1], reverse=True)
        ]
        primary_eval["feature_importances"] = feature_importance_list

        # 6. Save model artifacts using Joblib
        self._save_artifacts(primary_model, primary_eval)

        return primary_model, primary_eval, self.evaluation_results

    def _save_artifacts(self, model: Any, evaluation: Dict[str, Any]) -> None:
        """Serializes trained model, scaler, and evaluation metrics."""
        PRIMARY_MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, PRIMARY_MODEL_FILE)
        joblib.dump(self.scaler, SCALER_FILE)
        joblib.dump(self.feature_names, METRIC_COLUMNS_FILE)

        # Save evaluation metrics to JSON
        with open(MODEL_METRICS_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "primary_model": evaluation,
                "all_models": self.evaluation_results,
            }, f, indent=2)
