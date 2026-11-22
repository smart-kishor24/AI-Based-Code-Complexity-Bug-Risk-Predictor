"""
End-to-end integration test verifying the entire analytical pipeline:
AST parsing -> Feature Extraction -> Static Analysis -> ML Prediction -> SHAP -> PDF -> DB.
"""

from pathlib import Path
import pytest
from modules.code_parser import ASTCodeAnalyzer
from modules.feature_extractor import FeatureExtractor
from modules.static_analyzer import StaticCodeAnalyzer
from modules.defect_predictor import DefectRiskPredictor
from modules.explainability import ModelExplainabilityEngine
from modules.recommendation_engine import RecommendationEngine
from modules.report_generator import ReportGenerator
from modules.history_db import HistoryDatabase
from config.settings import SAMPLE_CODE_DIR


def test_full_pipeline_complex_example():
    sample_file = SAMPLE_CODE_DIR / "complex_example.py"
    assert sample_file.exists()
    source_code = sample_file.read_text(encoding="utf-8")

    # 1. Parse AST
    analyzer = ASTCodeAnalyzer(source_code)
    parse_res = analyzer.parse()
    assert parse_res.is_valid is True
    assert len(parse_res.functions) >= 1
    func = parse_res.functions[0]
    assert func.name == "process_complex_transactions"

    # 2. Extract Features
    metrics_df = FeatureExtractor.extract_all_features(parse_res)
    assert not metrics_df.empty
    assert metrics_df["cyclomatic_complexity"].iloc[0] > 10

    # 3. Static Analysis
    static_issues = StaticCodeAnalyzer.analyze_code(source_code)
    assert isinstance(static_issues, list)

    # 4. Defect Risk Prediction
    predictor = DefectRiskPredictor()
    assert predictor.is_model_ready() is True
    predictions = predictor.predict_function_risk(metrics_df)
    assert len(predictions) == len(metrics_df)
    pred_0 = predictions[0]
    assert pred_0["defect_probability"] > 0.0
    assert pred_0["risk_category"] in ["Low Risk", "Medium Risk", "High Risk"]

    # 5. Explainable AI
    engine = ModelExplainabilityEngine(
        model=predictor.model,
        feature_names=predictor.feature_names,
    )
    feature_matrix = predictor.prepare_feature_matrix(metrics_df)
    scaled_vec = predictor.scaler.transform(feature_matrix)
    explanation = engine.explain_local_prediction(
        function_feature_row=metrics_df.iloc[0],
        scaled_feature_vector=scaled_vec,
        function_name=pred_0["function_name"],
        defect_probability=pred_0["defect_probability"],
    )
    assert len(explanation["narrative_explanation"]) > 20

    # 6. Recommendation Engine
    recs = RecommendationEngine.generate_all_recommendations(
        metrics_df=metrics_df,
        static_warnings=static_issues,
        predicted_risks=predictions,
    )
    assert len(recs) > 0

    # 7. PDF Report Generation
    pdf_bytes = ReportGenerator.generate_pdf_report(
        filename="complex_example.py",
        metrics_df=metrics_df,
        predictions=predictions,
        static_issues=static_issues,
        recommendations=recs,
    )
    assert pdf_bytes.startswith(b"%PDF")

    # 8. CSV Export
    csv_str = ReportGenerator.export_csv(metrics_df, predictions)
    assert "process_complex_transactions" in csv_str

    # 9. Database Persistence
    row_id = HistoryDatabase.save_analysis(
        filename="complex_example.py",
        function_count=len(metrics_df),
        low_risk_count=sum(1 for p in predictions if p["risk_category"] == "Low Risk"),
        medium_risk_count=sum(1 for p in predictions if p["risk_category"] == "Medium Risk"),
        high_risk_count=sum(1 for p in predictions if p["risk_category"] == "High Risk"),
        avg_cyclomatic_complexity=float(metrics_df["cyclomatic_complexity"].mean()),
        total_loc=int(metrics_df["loc"].sum()),
        static_issues_count=len(static_issues),
        summary="E2E Pipeline Integration Test Run",
    )
    assert row_id > 0
