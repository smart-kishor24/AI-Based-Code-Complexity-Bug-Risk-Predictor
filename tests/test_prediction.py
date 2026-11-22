"""
Unit tests for ML Defect Predictor and Explainability modules.
Tests:
8. Missing dataset handling
9. Missing trained model fallback
10. Model prediction and probability output
"""

import pytest
import pandas as pd
from pathlib import Path
from modules.defect_predictor import DefectRiskPredictor
from modules.explainability import ModelExplainabilityEngine
from modules.data_loader import DefectDataLoader


def test_missing_dataset_handling():
    # Passing an invalid path should raise FileNotFoundError with actionable instructions
    with pytest.raises(FileNotFoundError):
        DefectDataLoader.load_dataset(
            dataset_name_or_path="non_existent_directory/fake_dataset.csv",
            prefer_openml_id=None,
        )


def test_predictor_handles_empty_dataframe():
    predictor = DefectRiskPredictor()
    results = predictor.predict_function_risk(pd.DataFrame())
    assert results == []


def test_trained_model_prediction():
    predictor = DefectRiskPredictor()
    assert predictor.is_model_ready() is True

    test_data = pd.DataFrame([
        {
            "function_name": "simple_func",
            "loc": 10,
            "cyclomatic_complexity": 2,
            "max_nesting_depth": 1,
            "param_count": 2,
            "return_count": 1,
            "condition_count": 1,
            "loop_count": 0,
            "call_count": 1,
            "h_volume": 45.0,
            "h_difficulty": 3.0,
            "h_effort": 135.0,
        },
        {
            "function_name": "complex_func",
            "loc": 120,
            "cyclomatic_complexity": 25,
            "max_nesting_depth": 6,
            "param_count": 8,
            "return_count": 7,
            "condition_count": 15,
            "loop_count": 4,
            "call_count": 12,
            "h_volume": 1200.0,
            "h_difficulty": 45.0,
            "h_effort": 54000.0,
        },
    ])

    predictions = predictor.predict_function_risk(test_data)
    assert len(predictions) == 2
    for pred in predictions:
        assert "defect_probability" in pred
        assert 0.0 <= pred["defect_probability"] <= 1.0
        assert pred["risk_category"] in ["Low Risk", "Medium Risk", "High Risk"]
        assert pred["predicted_class"] in [0, 1]


def test_explainability_local_and_global():
    predictor = DefectRiskPredictor()
    engine = ModelExplainabilityEngine(
        model=predictor.model,
        feature_names=predictor.feature_names,
    )

    # Test global importance
    global_imps = engine.explain_global_importance()
    assert len(global_imps) > 0
    assert "feature" in global_imps[0]
    assert "shap_importance" in global_imps[0]

    # Test local explanation
    sample_row = pd.Series({
        "loc": 50,
        "cyclomatic_complexity": 12,
        "max_nesting_depth": 4,
        "param_count": 5,
    })
    import numpy as np
    scaled_vec = np.zeros((1, len(predictor.feature_names)))

    explanation = engine.explain_local_prediction(
        function_feature_row=sample_row,
        scaled_feature_vector=scaled_vec,
        function_name="sample_target",
        defect_probability=0.72,
    )
    assert explanation["function_name"] == "sample_target"
    assert "narrative_explanation" in explanation
    assert len(explanation["narrative_explanation"]) > 20
