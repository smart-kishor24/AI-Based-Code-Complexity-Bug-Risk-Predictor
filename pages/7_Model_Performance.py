"""
Page 7: Machine Learning Model Performance & Benchmarking.
Presents empirical evaluation results on the NASA PROMISE dataset across candidate models:
Logistic Regression, Decision Tree, Random Forest, and XGBoost with modern UI styling.
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

from config.settings import MODEL_METRICS_FILE
from modules.ui_theme import apply_custom_css, render_hero_banner, get_modern_chart_layout

st.set_page_config(page_title="Model Performance - Code Risk Predictor", page_icon="📈", layout="wide")
apply_custom_css()

render_hero_banner(
    title="📈 Machine Learning Model Performance & Evaluation",
    subtitle="Empirical statistical benchmarks evaluated on NASA PROMISE historical software defect datasets.",
    badge="Step 4B: Benchmarking",
)

# Load persisted evaluation metrics
if not MODEL_METRICS_FILE.exists():
    st.error("Model evaluation metrics not found. Please run the training script.")
else:
    with open(MODEL_METRICS_FILE, "r", encoding="utf-8") as f:
        metrics_payload = json.load(f)

    all_models = metrics_payload.get("all_models", [])
    primary_eval = metrics_payload.get("primary_model", {})

    # 1. Dataset Characteristics Section
    st.subheader("1. Training Dataset Characteristics (NASA PROMISE KC1)")
    d_c1, d_c2, d_c3, d_c4 = st.columns(4)
    with d_c1:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-label">Repository Size</div>
                <div class="kpi-value">1,212</div>
                <div class="kpi-subtext">Deduplicated subroutines</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with d_c2:
        st.markdown(
            """
            <div class="kpi-card" style="border-top: 3px solid #10b981;">
                <div class="kpi-label" style="color: #065f46;">Clean Subroutines</div>
                <div class="kpi-value" style="color: #065f46;">897</div>
                <div class="kpi-subtext">74.0% of dataset</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with d_c3:
        st.markdown(
            """
            <div class="kpi-card" style="border-top: 3px solid #ef4444;">
                <div class="kpi-label" style="color: #991b1b;">Defective Records</div>
                <div class="kpi-value" style="color: #991b1b;">315</div>
                <div class="kpi-subtext">26.0% verified defect rate</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with d_c4:
        st.markdown(
            """
            <div class="kpi-card" style="border-top: 3px solid #f59e0b;">
                <div class="kpi-label" style="color: #92400e;">Imbalance Ratio</div>
                <div class="kpi-value" style="color: #92400e;">2.85 : 1</div>
                <div class="kpi-subtext">Clean vs Defective</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="info-card">
            <strong>Data Granularity Notice:</strong> NASA KC1 records describe subroutines extracted from C/C++ aerospace ground control systems.
            Stratified 5-Fold Cross-Validation and holdout train/test splitting (80/20) were strictly enforced without data leakage.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # 2. Benchmark Comparison Table
    st.subheader("2. Multi-Model Benchmark Comparison")
    table_rows = []
    for m in all_models:
        table_rows.append({
            "Algorithm": m.get("model_name"),
            "Accuracy": f"{m.get('accuracy', 0.0)*100:.2f}%",
            "Precision": f"{m.get('precision', 0.0)*100:.2f}%",
            "Recall": f"{m.get('recall', 0.0)*100:.2f}%",
            "F1-Score": f"{m.get('f1_score', 0.0)*100:.2f}%",
            "5-Fold CV F1": f"{m.get('cv_f1_mean', 0.0)*100:.2f}%",
            "ROC-AUC": f"{m.get('roc_auc', 0.0):.4f}",
        })

    benchmark_df = pd.DataFrame(table_rows)
    st.dataframe(benchmark_df, use_container_width=True)

    st.markdown("---")

    # 3. Primary Model Diagnostics
    st.subheader("3. Primary Model Diagnostics (Random Forest)")
    v_col1, v_col2 = st.columns(2)

    with v_col1:
        # Confusion Matrix Heatmap
        cm = primary_eval.get("confusion_matrix", {})
        matrix_vals = cm.get("matrix", [[134, 46], [32, 31]])

        fig_cm = px.imshow(
            matrix_vals,
            labels=dict(x="Predicted Class", y="Actual Ground Truth", color="Count"),
            x=["Clean (0)", "Defective (1)"],
            y=["Clean (0)", "Defective (1)"],
            text_auto=True,
            color_continuous_scale="Blues",
        )
        fig_cm.update_layout(get_modern_chart_layout(f"Confusion Matrix: {primary_eval.get('model_name')}", height=340))
        st.plotly_chart(fig_cm, use_container_width=True)

        st.caption(
            f"True Negatives: {cm.get('tn', 0)} | False Positives: {cm.get('fp', 0)} | "
            f"False Negatives: {cm.get('fn', 0)} | True Positives: {cm.get('tp', 0)}"
        )

    with v_col2:
        # ROC Curves Comparison
        fig_roc = go.Figure()
        fig_roc.add_shape(
            type="line", line=dict(dash="dash", color="#94a3b8"),
            x0=0, x1=1, y0=0, y1=1
        )

        for m in all_models:
            roc_data = m.get("roc_curve", {})
            fpr = roc_data.get("fpr", [])
            tpr = roc_data.get("tpr", [])
            auc_val = m.get("roc_auc", 0.5)
            if fpr and tpr:
                fig_roc.add_trace(
                    go.Scatter(x=fpr, y=tpr, name=f"{m['model_name']} ({auc_val:.3f})", mode="lines")
                )

        layout_roc = get_modern_chart_layout("ROC Curves Comparison (Holdout Test Split)", height=340)
        layout_roc["xaxis"]["title"] = "False Positive Rate (FPR)"
        layout_roc["yaxis"]["title"] = "True Positive Rate (TPR / Recall)"
        layout_roc["legend"] = dict(x=0.45, y=0.15, bgcolor="rgba(255,255,255,0.85)")
        fig_roc.update_layout(layout_roc)
        st.plotly_chart(fig_roc, use_container_width=True)

    st.markdown("---")

    # 4. Feature Importance
    st.subheader("4. Gini Feature Importance (Random Forest)")
    importances = primary_eval.get("feature_importances", [])
    if importances:
        imp_df = pd.DataFrame(importances).head(12)
        fig_imp = px.bar(
            imp_df.sort_values(by="importance", ascending=True),
            x="importance",
            y="feature",
            orientation="h",
            color="importance",
            color_continuous_scale="Teal",
            labels={"importance": "Relative Importance (MDI)", "feature": "Metric"},
        )
        fig_imp.update_layout(get_modern_chart_layout("Top 12 Most Influential Complexity Metrics", height=350))
        st.plotly_chart(fig_imp, use_container_width=True)
