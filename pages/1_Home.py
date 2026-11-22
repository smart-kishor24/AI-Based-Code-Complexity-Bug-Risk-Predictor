"""
Page 1: Home Dashboard.
Displays high-level analysis metrics, aggregated statistics from past runs,
and executive summary cards with modern UI styling.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.history_db import HistoryDatabase
from modules.ui_theme import apply_custom_css, render_hero_banner, get_modern_chart_layout

st.set_page_config(page_title="Home Dashboard - Code Risk Predictor", page_icon="🏠", layout="wide")
apply_custom_css()

render_hero_banner(
    title="🏠 Executive Home Dashboard",
    subtitle="High-level repository health, aggregated defect risk metrics, and historical inspection trends.",
    badge="Analytics Overview",
)

# Aggregate statistics from SQLite history
stats = HistoryDatabase.get_summary_stats()
recent_records = HistoryDatabase.get_all_analyses(limit=10)

# Top KPI Metric Cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Analyzed Files</div>
            <div class="kpi-value">{stats['total_files']}</div>
            <div class="kpi-subtext">Across past runs</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Evaluated Functions</div>
            <div class="kpi-value">{stats['total_functions']}</div>
            <div class="kpi-subtext">AST subroutines</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top: 3px solid #ef4444;">
            <div class="kpi-label" style="color: #991b1b;">High Risk Alerts</div>
            <div class="kpi-value" style="color: #991b1b;">{stats['total_high_risk']}</div>
            <div class="kpi-subtext">Prob &gt; 70%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top: 3px solid #f59e0b;">
            <div class="kpi-label" style="color: #92400e;">Medium Risk</div>
            <div class="kpi-value" style="color: #92400e;">{stats['total_medium_risk']}</div>
            <div class="kpi-subtext">Prob 30% - 70%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col5:
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top: 3px solid #10b981;">
            <div class="kpi-label" style="color: #065f46;">Low Risk</div>
            <div class="kpi-value" style="color: #065f46;">{stats['total_low_risk']}</div>
            <div class="kpi-subtext">Prob &lt; 30%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Active Session Snapshot
st.subheader("Current Session Snapshot")
if st.session_state.get("metrics_df") is not None and not st.session_state["metrics_df"].empty:
    m_df = st.session_state["metrics_df"]
    preds = st.session_state.get("predictions", [])
    fname = st.session_state.get("filename", "unnamed.py")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Current File</div>
                <div style="font-weight: 700; font-size: 16px; color: #0f172a; word-break: break-all;">{fname}</div>
                <div class="kpi-subtext">{len(m_df)} functions detected</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        avg_cc = round(m_df["cyclomatic_complexity"].mean(), 2) if "cyclomatic_complexity" in m_df.columns else 0
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Mean Cyclomatic CC</div>
                <div class="kpi-value">{avg_cc}</div>
                <div class="kpi-subtext">Target: &le; 10</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        total_loc = int(m_df["loc"].sum()) if "loc" in m_df.columns else 0
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Code Lines</div>
                <div class="kpi-value">{total_loc}</div>
                <div class="kpi-subtext">Active lines of code</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        high_cnt = sum(1 for p in preds if p.get("risk_category") == "High Risk")
        st.markdown(
            f"""
            <div class="kpi-card" style="border-left: 4px solid {'#ef4444' if high_cnt > 0 else '#10b981'};">
                <div class="kpi-label">High Risk Functions</div>
                <div class="kpi-value" style="color: {'#991b1b' if high_cnt > 0 else '#065f46'};">{high_cnt}</div>
                <div class="kpi-subtext">Priority for testing</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Risk Distribution Donut Chart & Maintainability Gauge
    chart_c1, chart_c2 = st.columns(2)

    with chart_c1:
        if preds:
            pred_df = pd.DataFrame(preds)
            cat_counts = pred_df["risk_category"].value_counts().reset_index()
            cat_counts.columns = ["Risk Category", "Count"]

            color_map = {"Low Risk": "#10b981", "Medium Risk": "#f59e0b", "High Risk": "#ef4444"}
            fig = px.pie(
                cat_counts,
                names="Risk Category",
                values="Count",
                hole=0.55,
                color="Risk Category",
                color_discrete_map=color_map,
            )
            fig.update_layout(get_modern_chart_layout(f"Defect Risk Distribution: {fname}", height=320))
            st.plotly_chart(fig, use_container_width=True)

    with chart_c2:
        # Software Quality & Maintainability Index Gauge
        if not m_df.empty:
            avg_cc = float(m_df["cyclomatic_complexity"].mean()) if "cyclomatic_complexity" in m_df.columns else 1.0
            # Heuristic Codebase Maintainability Index (0-100)
            health_score = max(0, min(100, int(100 - (avg_cc * 3.5) - (high_cnt * 12))))
            gauge_color = "#10b981" if health_score >= 70 else ("#f59e0b" if health_score >= 45 else "#ef4444")

            fig_gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=health_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Code Maintainability Index", 'font': {'size': 15, 'family': 'Inter, sans-serif'}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
                        'bar': {'color': gauge_color},
                        'bgcolor': "white",
                        'borderwidth': 1,
                        'bordercolor': "#e2e8f0",
                        'steps': [
                            {'range': [0, 45], 'color': 'rgba(239, 68, 68, 0.15)'},
                            {'range': [45, 70], 'color': 'rgba(245, 158, 11, 0.15)'},
                            {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.15)'},
                        ],
                    },
                )
            )
            fig_gauge.update_layout(get_modern_chart_layout("", height=320))
            st.plotly_chart(fig_gauge, use_container_width=True)
else:
    st.markdown(
        """
        <div class="notice-card">
            💡 <strong>Ready to start:</strong> No code file has been loaded in the current session.
            Go to <strong>Code Upload</strong> via the sidebar to analyze a Python file or test preloaded benchmark samples.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Historical Analyses Table
st.subheader("📜 Recent Analysis History")
if recent_records:
    history_df = pd.DataFrame(recent_records)
    display_cols = [
        "id",
        "filename",
        "timestamp",
        "function_count",
        "high_risk_count",
        "medium_risk_count",
        "low_risk_count",
        "avg_cyclomatic_complexity",
        "total_loc",
    ]
    st.dataframe(
        history_df[[c for c in display_cols if c in history_df.columns]],
        use_container_width=True,
    )
else:
    st.info("No prior analysis history stored in the SQLite database.")
