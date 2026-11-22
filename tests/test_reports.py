"""
Unit tests for Report Generator and SQLite Database modules.
Tests:
11. PDF generation
12. CSV export
13. SQLite database persistence and clearing
"""

import pytest
import pandas as pd
from modules.report_generator import ReportGenerator, REPORTLAB_AVAILABLE
from modules.history_db import HistoryDatabase


def test_csv_export():
    df = pd.DataFrame([
        {"function_name": "fn1", "loc": 20, "cyclomatic_complexity": 4},
        {"function_name": "fn2", "loc": 45, "cyclomatic_complexity": 9},
    ])
    preds = [
        {"function_name": "fn1", "defect_probability": 0.15, "risk_category": "Low Risk", "predicted_class": 0},
        {"function_name": "fn2", "defect_probability": 0.65, "risk_category": "Medium Risk", "predicted_class": 1},
    ]
    csv_str = ReportGenerator.export_csv(df, preds)
    assert "function_name" in csv_str
    assert "defect_probability" in csv_str
    assert "fn1" in csv_str
    assert "fn2" in csv_str


def test_pdf_generation():
    if not REPORTLAB_AVAILABLE:
        pytest.skip("ReportLab not installed")

    df = pd.DataFrame([
        {
            "function_name": "process_order",
            "start_line": 10,
            "end_line": 35,
            "loc": 26,
            "cyclomatic_complexity": 5,
            "max_nesting_depth": 2,
            "param_count": 3,
        }
    ])
    preds = [{
        "function_name": "process_order",
        "defect_probability": 0.35,
        "predicted_class": 0,
        "risk_category": "Medium Risk",
    }]
    static_issues = [{
        "line": 12,
        "column": 5,
        "rule_id": "W0611",
        "severity": "Warning",
        "message": "Unused import",
        "suggestion": "Remove import",
    }]
    recs = [{
        "severity": "Medium",
        "category": "Complexity",
        "target": "Function 'process_order'",
        "message": "Moderate complexity",
        "action": "Maintain tests",
    }]

    pdf_bytes = ReportGenerator.generate_pdf_report(
        filename="test_order.py",
        metrics_df=df,
        predictions=preds,
        static_issues=static_issues,
        recommendations=recs,
    )
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")


def test_sqlite_history_lifecycle():
    HistoryDatabase.init_db()

    # Save record
    row_id = HistoryDatabase.save_analysis(
        filename="test_lifecycle.py",
        function_count=5,
        low_risk_count=3,
        medium_risk_count=1,
        high_risk_count=1,
        avg_cyclomatic_complexity=4.2,
        total_loc=150,
        static_issues_count=2,
        summary="Test analysis summary",
    )
    assert row_id > 0

    # Retrieve record
    records = HistoryDatabase.get_all_analyses(limit=5)
    assert len(records) > 0
    assert any(r["filename"] == "test_lifecycle.py" for r in records)

    # Summary stats
    stats = HistoryDatabase.get_summary_stats()
    assert stats["total_files"] >= 1
    assert stats["total_functions"] >= 5

    # Clear history
    HistoryDatabase.clear_history()
    records_after = HistoryDatabase.get_all_analyses()
    assert len(records_after) == 0
