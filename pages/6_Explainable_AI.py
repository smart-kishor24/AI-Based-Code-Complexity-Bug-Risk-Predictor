"""
Page 6: Explainable AI (XAI).
Presents SHAP (SHapley Additive exPlanations) for both global model feature importances
and local, function-specific risk drivers with natural language explanations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

from config.settings import PRIMARY_MODEL_FILE, SCALER_FILE, METRIC_COLUMNS_FILE
from modules.explainability import ModelExplainabilityEngine
from modules.defect_predictor import DefectRiskPredictor
from modules.ui_theme import apply_custom_css, render_hero_banner, get_modern_chart_layout

st.set_page_config(page_title="Explainable AI - Code Risk Predictor", page_icon="💡", layout="wide")
apply_custom_css()

render_hero_banner(
    title="💡 Explainable AI (SHAP Interpretability)",
    subtitle="Decomposing black-box predictions into transparent, quantifiable feature attributions and natural language narratives.",
    badge="Step 4A: XAI",
)

predictions = st.session_state.get("predictions", [])
metrics_df = st.session_state.get("metrics_df", pd.DataFrame())

if metrics_df.empty or not predictions:
    st.warning("No analysis results found. Please upload and analyze a Python script on the **Code Upload** page.")
else:
    # Load ML Model for SHAP
    model = None
    scaler = None
    feature_names = []

    if PRIMARY_MODEL_FILE.exists() and SCALER_FILE.exists() and METRIC_COLUMNS_FILE.exists():
        try:
            model = joblib.load(PRIMARY_MODEL_FILE)
            scaler = joblib.load(SCALER_FILE)
            feature_names = joblib.load(METRIC_COLUMNS_FILE)
        except Exception as e:
            st.error(f"Error loading model artifacts: {e}")

    engine = ModelExplainabilityEngine(model=model, feature_names=feature_names)
    predictor = DefectRiskPredictor()

    # 1. Global Feature Importance Section
    st.subheader("1. Global Model Feature Importance")
    st.markdown("Relative influence of software complexity metrics across the entire training repository:")

    global_importances = engine.explain_global_importance()
    if global_importances:
        g_df = pd.DataFrame(global_importances).head(10)
        fig_global = px.bar(
            g_df.sort_values(by="shap_importance", ascending=True),
            x="shap_importance",
            y="feature",
            orientation="h",
            color="shap_importance",
            color_continuous_scale="Blues",
            labels={"shap_importance": "Relative Weight / Mean |SHAP|", "feature": "Metric"},
        )
        fig_global.update_layout(get_modern_chart_layout("Top 10 Global Predictive Features", height=340))
        st.plotly_chart(fig_global, use_container_width=True)
    else:
        st.info("Global model importance unavailable.")

    st.markdown("---")

    # 2. Local Function-Level Explanation Section
    st.subheader("2. Local Prediction Attribution (Function-Specific Drivers)")
    st.markdown("Select an individual function to inspect the exact structural metrics driving its defect probability up or down:")

    func_names = metrics_df["function_name"].tolist()
    selected_func_name = st.selectbox("Select Function to Explain:", func_names)

    func_row = metrics_df[metrics_df["function_name"] == selected_func_name].iloc[0]
    matched_pred = next((p for p in predictions if p.get("function_name") == selected_func_name), {})
    prob = matched_pred.get("defect_probability", 0.5)

    # Use aligned feature matrix
    if predictor.is_model_ready():
        single_df = pd.DataFrame([func_row])
        feature_matrix = predictor.prepare_feature_matrix(single_df)
        scaled_vector = predictor.scaler.transform(feature_matrix)
    else:
        scaled_vector = np.zeros((1, len(feature_names)))

    explanation = engine.explain_local_prediction(
        function_feature_row=func_row,
        scaled_feature_vector=scaled_vector,
        function_name=selected_func_name,
        defect_probability=prob,
    )

    # Narrative Card
    st.markdown(
        f"""
        <div style="background-color: #f1f5f9; border-left: 5px solid #3b82f6; padding: 16px 20px; border-radius: 8px; margin: 16px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <div style="font-weight: 700; font-size: 15px; color: #0f172a; margin-bottom: 6px;">🧠 Natural Language Risk Attribution</div>
            <div style="font-size: 14px; color: #334155; line-height: 1.6;">{explanation['narrative_explanation']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Attribution Bar Chart
    inc_items = explanation.get("features_increasing_risk", [])
    dec_items = explanation.get("features_decreasing_risk", [])

    waterfall_rows = []
    for item in inc_items:
        waterfall_rows.append({
            "Feature": f"{item['feature']} ({item['actual_value']})",
            "Impact": item["impact"],
            "Direction": "Increased Risk (+)",
        })
    for item in dec_items:
        waterfall_rows.append({
            "Feature": f"{item['feature']} ({item['actual_value']})",
            "Impact": item["impact"],
            "Direction": "Decreased Risk (-)",
        })

    if waterfall_rows:
        wf_df = pd.DataFrame(waterfall_rows)
        fig_local = px.bar(
            wf_df.sort_values(by="Impact", ascending=True),
            x="Impact",
            y="Feature",
            orientation="h",
            color="Direction",
            color_discrete_map={"Increased Risk (+)": "#ef4444", "Decreased Risk (-)": "#10b981"},
            labels={"Impact": "SHAP Attribution Value (Log-Odds / Risk Delta)"},
        )
        fig_local.update_layout(get_modern_chart_layout(f"Feature Contributions for '{selected_func_name}'", height=340))
        st.plotly_chart(fig_local, use_container_width=True)

    # Methodological Disclaimer
    st.caption(f"ℹ️ {explanation.get('disclaimer', '')}")
