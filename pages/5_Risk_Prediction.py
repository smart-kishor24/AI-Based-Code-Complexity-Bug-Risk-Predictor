"""
Page 5: Machine Learning Defect Risk Prediction.
Presents model-predicted defect probabilities, risk tier categorizations,
and function-level risk indicators with modern UI styling.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from config.settings import DEFAULT_LOW_RISK_THRESHOLD, DEFAULT_HIGH_RISK_THRESHOLD
from modules.ui_theme import apply_custom_css, render_hero_banner, get_modern_chart_layout

st.set_page_config(page_title="Risk Prediction - Code Risk Predictor", page_icon="🎯", layout="wide")
apply_custom_css()

render_hero_banner(
    title="🎯 Machine Learning Defect Risk Prediction",
    subtitle="Probabilistic defect susceptibility estimation powered by ensemble models trained on NASA PROMISE repositories.",
    badge="Step 3: Predictions",
)

predictions = st.session_state.get("predictions", [])
metrics_df = st.session_state.get("metrics_df", pd.DataFrame())

if not predictions:
    st.warning("No defect risk predictions available. Please upload and analyze a Python script on the **Code Upload** page.")
else:
    pred_df = pd.DataFrame(predictions)
    fname = st.session_state.get("filename", "unnamed.py")

    low_th = st.session_state.get("low_threshold", DEFAULT_LOW_RISK_THRESHOLD)
    high_th = st.session_state.get("high_threshold", DEFAULT_HIGH_RISK_THRESHOLD)

    st.markdown(
        f"""
        <div class="info-card">
            <strong>Active Probability Calibration Bands:</strong> &nbsp;
            <span class="risk-pill risk-low">Low Risk: &lt; {low_th*100:.0f}%</span> &nbsp;
            <span class="risk-pill risk-med">Medium Risk: {low_th*100:.0f}% - {high_th*100:.0f}%</span> &nbsp;
            <span class="risk-pill risk-high">High Risk: &gt; {high_th*100:.0f}%</span> &nbsp;
            <span style="font-size: 12px; color: #64748b;">(Adjustable via sidebar sliders)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Risk Distribution KPI Metrics
    high_funcs = pred_df[pred_df["risk_category"] == "High Risk"]
    med_funcs = pred_df[pred_df["risk_category"] == "Medium Risk"]
    low_funcs = pred_df[pred_df["risk_category"] == "Low Risk"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Analyzed Functions</div>
                <div class="kpi-value">{len(pred_df)}</div>
                <div class="kpi-subtext">Total evaluated</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-top: 3px solid #ef4444;">
                <div class="kpi-label" style="color: #991b1b;">High Risk</div>
                <div class="kpi-value" style="color: #991b1b;">{len(high_funcs)}</div>
                <div class="kpi-subtext">Urgent review</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-top: 3px solid #f59e0b;">
                <div class="kpi-label" style="color: #92400e;">Medium Risk</div>
                <div class="kpi-value" style="color: #92400e;">{len(med_funcs)}</div>
                <div class="kpi-subtext">Monitor metrics</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-top: 3px solid #10b981;">
                <div class="kpi-label" style="color: #065f46;">Low Risk</div>
                <div class="kpi-value" style="color: #065f46;">{len(low_funcs)}</div>
                <div class="kpi-subtext">Baseline compliant</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Interactive Risk Charts
    col_v1, col_v2 = st.columns(2)

    with col_v1:
        # Donut Chart
        cat_counts = pred_df["risk_category"].value_counts().reset_index()
        cat_counts.columns = ["Risk Tier", "Count"]
        color_map = {"Low Risk": "#10b981", "Medium Risk": "#f59e0b", "High Risk": "#ef4444"}
        fig_donut = px.pie(
            cat_counts,
            names="Risk Tier",
            values="Count",
            hole=0.55,
            color="Risk Tier",
            color_discrete_map=color_map,
        )
        fig_donut.update_layout(get_modern_chart_layout("Defect Risk Tier Distribution", height=340))
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_v2:
        # Horizontal Probability Chart
        pred_sorted = pred_df.sort_values(by="defect_probability", ascending=True)
        fig_bar = px.bar(
            pred_sorted,
            x="defect_probability",
            y="function_name",
            orientation="h",
            color="risk_category",
            color_discrete_map=color_map,
            labels={"defect_probability": "Defect Probability", "function_name": "Function"},
        )
        fig_bar.add_vline(x=low_th, line_dash="dash", line_color="#10b981", annotation_text=f"Low ({low_th:.2f})")
        fig_bar.add_vline(x=high_th, line_dash="dash", line_color="#ef4444", annotation_text=f"High ({high_th:.2f})")
        fig_bar.update_layout(get_modern_chart_layout("Estimated Defect Probability per Function", height=340))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # High-Risk Alert Banner if present
    if not high_funcs.empty:
        st.subheader("🚨 High Defect Risk Function Alerts")
        for _, h_row in high_funcs.iterrows():
            prob_pct = h_row['defect_probability'] * 100
            st.markdown(
                f"""
                <div style="border: 1px solid rgba(239, 68, 68, 0.4); border-left: 5px solid #ef4444; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; background: rgba(239, 68, 68, 0.12);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 700; font-size: 15px; color: #fca5a5;">Function: <code>{h_row['function_name']}</code> (Lines {h_row['start_line']}-{h_row['end_line']})</span>
                        <span class="risk-pill risk-high">{prob_pct:.1f}% Probability</span>
                    </div>
                    <div style="font-size: 13.5px; color: #cbd5e1;">
                        Cyclomatic Complexity: <strong>{h_row['cyclomatic_complexity']}</strong> &nbsp;|&nbsp; 
                        Length: <strong>{h_row['loc']} LOC</strong> &nbsp;|&nbsp; 
                        Classification: <strong>Defect-Prone (Class 1)</strong> &nbsp;|&nbsp;
                        Model: <strong>{h_row.get('model_used', 'Random Forest')}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Complete Prediction Table
    st.subheader("📋 Function Risk Assessment Table")
    display_df = pred_df[[
        "function_name",
        "class_name",
        "start_line",
        "end_line",
        "loc",
        "cyclomatic_complexity",
        "defect_probability",
        "predicted_class",
        "risk_category",
        "model_used",
    ]].copy()

    display_df["defect_probability"] = display_df["defect_probability"].apply(lambda p: f"{p*100:.1f}%")
    display_df["predicted_class"] = display_df["predicted_class"].apply(lambda c: "Defective (1)" if c == 1 else "Clean (0)")

    st.dataframe(display_df, use_container_width=True)
