"""
Main Streamlit Application Entrypoint.
Configures page themes, shared session state, global navigation, and executive routing.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import json

from config.settings import (
    DEFAULT_LOW_RISK_THRESHOLD,
    DEFAULT_HIGH_RISK_THRESHOLD,
    PRIMARY_MODEL_FILE,
    MODEL_METRICS_FILE,
)
from modules.history_db import HistoryDatabase
from modules.ui_theme import apply_custom_css, render_hero_banner

# Page setup
st.set_page_config(
    page_title="AI Code Complexity & Defect Risk Predictor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply unified CSS
apply_custom_css()

# Initialize Session State
if "source_code" not in st.session_state:
    st.session_state["source_code"] = ""
if "filename" not in st.session_state:
    st.session_state["filename"] = "unnamed_script.py"
if "parse_result" not in st.session_state:
    st.session_state["parse_result"] = None
if "metrics_df" not in st.session_state:
    st.session_state["metrics_df"] = pd.DataFrame()
if "static_issues" not in st.session_state:
    st.session_state["static_issues"] = []
if "predictions" not in st.session_state:
    st.session_state["predictions"] = []
if "recommendations" not in st.session_state:
    st.session_state["recommendations"] = []
if "analysis_id" not in st.session_state:
    st.session_state["analysis_id"] = None
if "low_threshold" not in st.session_state:
    st.session_state["low_threshold"] = DEFAULT_LOW_RISK_THRESHOLD
if "high_threshold" not in st.session_state:
    st.session_state["high_threshold"] = DEFAULT_HIGH_RISK_THRESHOLD

# Initialize database
HistoryDatabase.init_db()

# Sidebar Global Controls & System Diagnostics
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span style="font-size: 24px;">🛡️</span>
            <div>
                <div style="font-weight: 700; font-size: 16px; color: #0f172a;">Code Risk Predictor</div>
                <div style="font-size: 11.5px; color: #64748b;">AI-Based Software Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.subheader("⚙️ Risk Threshold Bands")
    st.caption("Customize probabilistic defect risk boundaries:")

    low_val = st.slider(
        "Low Risk Upper Bound (<)",
        min_value=0.10,
        max_value=0.50,
        value=float(st.session_state["low_threshold"]),
        step=0.05,
        help="Probabilities strictly below this value are classified as Low Risk (Green).",
    )
    high_val = st.slider(
        "High Risk Lower Bound (>)",
        min_value=0.50,
        max_value=0.90,
        value=float(st.session_state["high_threshold"]),
        step=0.05,
        help="Probabilities strictly above this value are classified as High Risk (Red).",
    )
    st.session_state["low_threshold"] = low_val
    st.session_state["high_threshold"] = high_val

    st.markdown("---")
    st.subheader("📊 System Diagnostics")
    model_exists = PRIMARY_MODEL_FILE.exists()
    status_color = "#10b981" if model_exists else "#f59e0b"
    status_text = "Trained & Serialized (Random Forest)" if model_exists else "Untrained"
    
    st.markdown(
        f"""
        <div style="background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
            <div style="font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Active ML Model</div>
            <div style="font-size: 13.5px; font-weight: 600; color: #f8fafc; display: flex; align-items: center; gap: 6px; margin: 4px 0;">
                <span style="height: 8px; width: 8px; border-radius: 50%; background-color: {status_color}; display: inline-block;"></span>
                {status_text}
            </div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 8px; font-weight: 600; text-transform: uppercase;">Dataset Benchmark</div>
            <div style="font-size: 13px; font-weight: 500; color: #cbd5e1;">NASA PROMISE KC1 (1,212 instances)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state["metrics_df"] is not None and not st.session_state["metrics_df"].empty:
        st.markdown(
            f"""
            <div style="background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 10px; font-size: 12px; color: #e2e8f0;">
                📁 <strong>Active File:</strong> <code style="color: #60a5fa;">{st.session_state['filename']}</code><br>
                🔢 <strong>Functions:</strong> {len(st.session_state['metrics_df'])} analyzed
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    if st.button("🔄 Reset Analysis State", use_container_width=True):
        st.session_state["source_code"] = ""
        st.session_state["filename"] = "unnamed_script.py"
        st.session_state["parse_result"] = None
        st.session_state["metrics_df"] = pd.DataFrame()
        st.session_state["static_issues"] = []
        st.session_state["predictions"] = []
        st.session_state["recommendations"] = []
        st.session_state["analysis_id"] = None
        st.rerun()

# Hero Header Banner
render_hero_banner(
    title="🛡️ AI-Based Code Complexity & Bug Risk Predictor",
    subtitle="Hybrid static analysis, quantitative software metrics (McCabe & Halstead), and supervised ML defect risk prediction with Explainable AI.",
    badge="Production Academic Edition",
)

# Academic & Methodological Disclaimer Banner
st.markdown(
    """
    <div class="info-card">
        <strong>Academic & Methodological Transparency:</strong>
        High cyclomatic complexity indicates testability friction and cognitive strain, but does <em>not</em> guarantee an active runtime defect.
        This platform strictly isolates objective structural metrics, static lint warnings, and ML-predicted defect probabilities.
    </div>
    """,
    unsafe_allow_html=True,
)

# Pipeline Step Cards
st.subheader("🚀 Guided Analysis Workflow")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        <div class="feature-card">
            <div style="font-size: 20px; margin-bottom: 8px;">📤</div>
            <div style="font-size: 11px; font-weight: 700; color: #3b82f6; text-transform: uppercase;">Step 1</div>
            <h4 style="margin: 4px 0 8px 0; color: #0f172a; font-size: 16px;">Source Ingestion</h4>
            <p style="font-size: 13px; color: #64748b; line-height: 1.4; margin: 0 0 14px 0;">
                Upload a <code>.py</code> file or paste directly. Performs non-executing AST validation and token bounds checking.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Upload ➡️", key="btn_nav_upload", use_container_width=True):
        st.switch_page("pages/2_Code_Upload.py")

with c2:
    st.markdown(
        """
        <div class="feature-card">
            <div style="font-size: 20px; margin-bottom: 8px;">⚙️</div>
            <div style="font-size: 11px; font-weight: 700; color: #3b82f6; text-transform: uppercase;">Step 2</div>
            <h4 style="margin: 4px 0 8px 0; color: #0f172a; font-size: 16px;">Complexity Metrics</h4>
            <p style="font-size: 13px; color: #64748b; line-height: 1.4; margin: 0 0 14px 0;">
                Extract McCabe cyclomatic complexity, Halstead volume/effort, nesting depth, and static code smells via Ruff.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Complexity ➡️", key="btn_nav_comp", use_container_width=True):
        st.switch_page("pages/3_Complexity_Analysis.py")

with c3:
    st.markdown(
        """
        <div class="feature-card">
            <div style="font-size: 20px; margin-bottom: 8px;">🎯</div>
            <div style="font-size: 11px; font-weight: 700; color: #3b82f6; text-transform: uppercase;">Step 3</div>
            <h4 style="margin: 4px 0 8px 0; color: #0f172a; font-size: 16px;">Risk Prediction</h4>
            <p style="font-size: 13px; color: #64748b; line-height: 1.4; margin: 0 0 14px 0;">
                Evaluate function defect probabilities using models trained on verified NASA PROMISE historical defect records.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Predictions ➡️", key="btn_nav_pred", use_container_width=True):
        st.switch_page("pages/5_Risk_Prediction.py")

with c4:
    st.markdown(
        """
        <div class="feature-card">
            <div style="font-size: 20px; margin-bottom: 8px;">📑</div>
            <div style="font-size: 11px; font-weight: 700; color: #3b82f6; text-transform: uppercase;">Step 4</div>
            <h4 style="margin: 4px 0 8px 0; color: #0f172a; font-size: 16px;">XAI & Reports</h4>
            <p style="font-size: 13px; color: #64748b; line-height: 1.4; margin: 0 0 14px 0;">
                Inspect SHAP feature attributions and download comprehensive PDF technical reports and CSV metrics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Reports ➡️", key="btn_nav_reports", use_container_width=True):
        st.switch_page("pages/8_Reports.py")

st.markdown("---")

# Architecture Overview Accordion
with st.expander("🔍 Click to inspect complete Architecture & Analytical Pipeline", expanded=False):
    st.markdown(
        """
        ### Multi-Tier Analytical Pipeline
        1. **Safe Parsing Layer:** Python `ast.parse()` extracts the code hierarchy without executing any code.
        2. **Feature Engineering Engine:** Radon and AST visitors calculate McCabe Cyclomatic Complexity, Halstead Volume, Difficulty, Effort, Nesting Depth, and AST counts.
        3. **Static Rule Linter:** Identifies anti-patterns including mutable default arguments, bare `except:` blocks, and unhandled branches.
        4. **Supervised ML Classification:** Balanced Random Forest Classifier predicts calibrated defect probabilities based on NASA PROMISE KC1 ground truth.
        5. **Explainability Engine:** SHAP TreeExplainer delivers local and global attributions with natural language explanations.
        6. **Report Generator:** ReportLab Platypus compiles publication-grade PDF documentation.
        """
    )
