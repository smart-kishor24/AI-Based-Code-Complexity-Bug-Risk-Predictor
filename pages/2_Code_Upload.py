"""
Page 2: Code Upload and Direct Input.
Validates input, handles files and raw text, executes the end-to-end analysis pipeline,
and updates shared session state with modern UI polish.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

from config.settings import (
    MAX_FILE_SIZE_BYTES,
    MAX_SOURCE_LINES,
    SAMPLE_CODE_DIR,
)
from modules.code_parser import ASTCodeAnalyzer
from modules.feature_extractor import FeatureExtractor
from modules.static_analyzer import StaticCodeAnalyzer
from modules.defect_predictor import DefectRiskPredictor
from modules.recommendation_engine import RecommendationEngine
from modules.history_db import HistoryDatabase
from modules.ui_theme import apply_custom_css, render_hero_banner

st.set_page_config(page_title="Code Upload - Code Risk Predictor", page_icon="📤", layout="wide")
apply_custom_css()

render_hero_banner(
    title="📤 Source Code Ingestion & AST Parsing",
    subtitle="Submit Python source code via file upload, direct editor input, or load preconfigured benchmark samples.",
    badge="Step 1: Input",
)

# Input Mode Tabs
tab_upload, tab_paste, tab_samples = st.tabs(["📁 File Uploader", "✍️ Interactive Code Editor", "🧪 Preloaded Benchmark Samples"])

source_code_input = ""
selected_filename = "custom_code.py"

with tab_upload:
    st.markdown("Upload any standard Python (`.py`) script for non-executing AST compilation:")
    uploaded_file = st.file_uploader(
        "Choose a Python file",
        type=["py"],
        help="Upload standard Python files up to 2MB. Code is inspected purely via AST and never executed.",
    )
    if uploaded_file is not None:
        if uploaded_file.size > MAX_FILE_SIZE_BYTES:
            st.error(f"File size exceeds maximum allowed limit ({MAX_FILE_SIZE_BYTES // (1024*1024)} MB).")
        else:
            try:
                source_code_input = uploaded_file.getvalue().decode("utf-8")
                selected_filename = uploaded_file.name
                st.success(f"Loaded `{uploaded_file.name}` ({len(source_code_input.splitlines())} lines).")
            except UnicodeDecodeError:
                st.error("Encoding Error: File must be valid UTF-8 formatted text.")

with tab_paste:
    st.markdown("Paste raw Python code directly into the syntax box below:")
    pasted_code = st.text_area(
        "Python Code:",
        height=320,
        placeholder="def calculate_total(items, discount):\n    total = 0\n    for item in items:\n        total += item['price']\n    return total * (1 - discount)",
        key="pasted_code_area",
    )
    if pasted_code.strip():
        source_code_input = pasted_code
        selected_filename = "pasted_script.py"

with tab_samples:
    st.markdown("Select a representative software engineering benchmark to test complexity detection:")
    sample_col1, sample_col2, sample_col3 = st.columns(3)
    
    with sample_col1:
        st.markdown(
            """
            <div class="feature-card">
                <span class="risk-pill risk-low">Clean Utility</span>
                <h4 style="margin: 8px 0 4px 0; font-size: 15px;">Simple Example</h4>
                <p style="font-size: 12.5px; color: #64748b; line-height: 1.4;">
                    Modular, PEP-8 compliant arithmetic utilities with minimal branching and low complexity.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("📗 Load Clean Sample", key="load_simple", use_container_width=True):
            p = SAMPLE_CODE_DIR / "simple_example.py"
            if p.exists():
                source_code_input = p.read_text(encoding="utf-8")
                selected_filename = "simple_example.py"
                st.session_state["source_code"] = source_code_input
                st.session_state["filename"] = selected_filename
                st.rerun()

    with sample_col2:
        st.markdown(
            """
            <div class="feature-card">
                <span class="risk-pill risk-med">Financial Core</span>
                <h4 style="margin: 8px 0 4px 0; font-size: 15px;">Complex Example</h4>
                <p style="font-size: 12.5px; color: #64748b; line-height: 1.4;">
                    Multi-tier transaction processor with 9 parameters, multiple loops, and CC &gt; 15.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("📙 Load Complex Sample", key="load_complex", use_container_width=True):
            p = SAMPLE_CODE_DIR / "complex_example.py"
            if p.exists():
                source_code_input = p.read_text(encoding="utf-8")
                selected_filename = "complex_example.py"
                st.session_state["source_code"] = source_code_input
                st.session_state["filename"] = selected_filename
                st.rerun()

    with sample_col3:
        st.markdown(
            """
            <div class="feature-card">
                <span class="risk-pill risk-high">Anti-Patterns</span>
                <h4 style="margin: 8px 0 4px 0; font-size: 15px;">Nested Conditions</h4>
                <p style="font-size: 12.5px; color: #64748b; line-height: 1.4;">
                    Deep control-flow nesting depth (4+ levels), mutable default argument, and bare except.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("📕 Load Nested Sample", key="load_nested", use_container_width=True):
            p = SAMPLE_CODE_DIR / "nested_conditions.py"
            if p.exists():
                source_code_input = p.read_text(encoding="utf-8")
                selected_filename = "nested_conditions.py"
                st.session_state["source_code"] = source_code_input
                st.session_state["filename"] = selected_filename
                st.rerun()

# If session state already holds source code
if not source_code_input and st.session_state.get("source_code"):
    source_code_input = st.session_state["source_code"]
    selected_filename = st.session_state.get("filename", "unnamed.py")

# Preview & Execution Section
st.markdown("---")
if source_code_input.strip():
    lines_count = len(source_code_input.splitlines())
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h3 style="margin: 0; font-size: 17px; color: #0f172a;">Active Source: <code>{selected_filename}</code></h3>
            <span style="font-size: 13px; color: #64748b;"><strong>{lines_count}</strong> lines</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Click to view full source code snippet", expanded=False):
        st.code(source_code_input, language="python", line_numbers=True)

    if lines_count > MAX_SOURCE_LINES:
        st.warning(f"File has {lines_count} lines, exceeding the recommended limit of {MAX_SOURCE_LINES} lines.")

    # Execution Trigger Button
    if st.button("🚀 Run Full Analytical Pipeline", type="primary", use_container_width=True):
        with st.spinner("Compiling AST, extracting McCabe & Halstead features, and estimating ML defect risk..."):
            # 1. Parse AST
            analyzer = ASTCodeAnalyzer(source_code_input)
            parse_result = analyzer.parse()

            if not parse_result.is_valid:
                st.error(f"AST Parsing Error: {parse_result.error_message}")
                if parse_result.error_line:
                    st.error(f"Location: Line {parse_result.error_line}, Column {parse_result.error_column}")
            else:
                # 2. Extract Features
                metrics_df = FeatureExtractor.extract_all_features(parse_result)

                # 3. Static Analysis
                static_issues = StaticCodeAnalyzer.analyze_code(source_code_input)

                # 4. ML Defect Risk Prediction
                predictor = DefectRiskPredictor(
                    low_risk_threshold=st.session_state["low_threshold"],
                    high_risk_threshold=st.session_state["high_threshold"],
                )
                predictions = predictor.predict_function_risk(metrics_df)

                # 5. Recommendations
                recommendations = RecommendationEngine.generate_all_recommendations(
                    metrics_df=metrics_df,
                    static_warnings=static_issues,
                    predicted_risks=predictions,
                )

                # 6. Save to SQLite History
                low_cnt = sum(1 for p in predictions if p.get("risk_category") == "Low Risk")
                med_cnt = sum(1 for p in predictions if p.get("risk_category") == "Medium Risk")
                high_cnt = sum(1 for p in predictions if p.get("risk_category") == "High Risk")
                avg_cc = float(metrics_df["cyclomatic_complexity"].mean()) if not metrics_df.empty else 0.0
                total_loc = int(metrics_df["loc"].sum()) if not metrics_df.empty else 0

                summary_text = (
                    f"Analyzed {len(metrics_df)} functions with {len(static_issues)} static warnings. "
                    f"Defect risk distribution: {high_cnt} High, {med_cnt} Medium, {low_cnt} Low."
                )

                analysis_id = HistoryDatabase.save_analysis(
                    filename=selected_filename,
                    function_count=len(metrics_df),
                    low_risk_count=low_cnt,
                    medium_risk_count=med_cnt,
                    high_risk_count=high_cnt,
                    avg_cyclomatic_complexity=round(avg_cc, 2),
                    total_loc=total_loc,
                    static_issues_count=len(static_issues),
                    summary=summary_text,
                )

                # 7. Update Session State
                st.session_state["source_code"] = source_code_input
                st.session_state["filename"] = selected_filename
                st.session_state["parse_result"] = parse_result
                st.session_state["metrics_df"] = metrics_df
                st.session_state["static_issues"] = static_issues
                st.session_state["predictions"] = predictions
                st.session_state["recommendations"] = recommendations
                st.session_state["analysis_id"] = analysis_id

                st.success(f"Analysis completed successfully! {len(metrics_df)} functions parsed from `{selected_filename}`.")
                st.info("Navigate to **Complexity Analysis** or **Risk Prediction** in the sidebar to inspect the results.")
else:
    st.markdown(
        """
        <div class="info-card">
            Please upload a Python file, paste source code, or click one of the benchmark samples above to begin analysis.
        </div>
        """,
        unsafe_allow_html=True,
    )
