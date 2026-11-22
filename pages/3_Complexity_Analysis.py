"""
Page 3: Code Complexity Analysis.
Displays function-wise software complexity metrics (McCabe, Halstead, AST features)
and interactive Plotly visualization charts with modern styling.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.settings import METRIC_THRESHOLDS
from modules.ui_theme import apply_custom_css, render_hero_banner, get_modern_chart_layout

st.set_page_config(page_title="Complexity Analysis - Code Risk Predictor", page_icon="⚙️", layout="wide")
apply_custom_css()

render_hero_banner(
    title="⚙️ Software Complexity Metrics Analysis",
    subtitle="Quantitative decomposition of control flow paths, McCabe Cyclomatic Complexity, nesting hierarchies, and Halstead metrics.",
    badge="Step 2: Metrics",
)

metrics_df = st.session_state.get("metrics_df", pd.DataFrame())

if metrics_df.empty:
    st.warning("No code analysis data found in session. Please upload and analyze a Python script on the **Code Upload** page.")
else:
    fname = st.session_state.get("filename", "unnamed.py")

    # Top-Level Summary Metrics Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Functions</div>
                <div class="kpi-value">{len(metrics_df)}</div>
                <div class="kpi-subtext">Isolated subroutines</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        total_loc = int(metrics_df["loc"].sum()) if "loc" in metrics_df.columns else 0
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Total LOC</div>
                <div class="kpi-value">{total_loc}</div>
                <div class="kpi-subtext">Cumulative lines</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        avg_cc = round(metrics_df["cyclomatic_complexity"].mean(), 2) if "cyclomatic_complexity" in metrics_df.columns else 0
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Average CC</div>
                <div class="kpi-value">{avg_cc}</div>
                <div class="kpi-subtext">Industry standard: &le; 10</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        max_cc = int(metrics_df["cyclomatic_complexity"].max()) if "cyclomatic_complexity" in metrics_df.columns else 0
        cc_color = "#991b1b" if max_cc > 15 else ("#92400e" if max_cc > 8 else "#065f46")
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Max Function CC</div>
                <div class="kpi-value" style="color: {cc_color};">{max_cc}</div>
                <div class="kpi-subtext">Peak complexity node</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c5:
        max_depth = int(metrics_df["max_nesting_depth"].max()) if "max_nesting_depth" in metrics_df.columns else 0
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Max Nesting</div>
                <div class="kpi-value">{max_depth}</div>
                <div class="kpi-subtext">Control flow depth</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Interactive Complexity Visualizations
    st.subheader("📊 Interactive Complexity Charts")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        # Bar Chart: Cyclomatic Complexity per Function
        fig_cc = px.bar(
            metrics_df,
            x="function_name",
            y="cyclomatic_complexity",
            color="cyclomatic_complexity",
            color_continuous_scale="Reds",
            labels={"function_name": "Function Name", "cyclomatic_complexity": "McCabe CC"},
        )
        fig_cc.add_hline(
            y=METRIC_THRESHOLDS["cyclomatic_complexity"]["warning"],
            line_dash="dash",
            line_color="#f59e0b",
            annotation_text="Warning Threshold (8)",
        )
        fig_cc.add_hline(
            y=METRIC_THRESHOLDS["cyclomatic_complexity"]["critical"],
            line_dash="dot",
            line_color="#ef4444",
            annotation_text="Critical Threshold (15)",
        )
        fig_cc.update_layout(get_modern_chart_layout("Cyclomatic Complexity by Function", height=350))
        st.plotly_chart(fig_cc, use_container_width=True)

    with col_chart2:
        # Scatter Plot: LOC vs Cyclomatic Complexity
        fig_scatter = px.scatter(
            metrics_df,
            x="loc",
            y="cyclomatic_complexity",
            size="max_nesting_depth",
            color="cyclomatic_complexity",
            hover_name="function_name",
            hover_data=["param_count", "loop_count", "condition_count"],
            labels={"loc": "Lines of Code (LOC)", "cyclomatic_complexity": "Cyclomatic Complexity"},
            color_continuous_scale="Viridis",
        )
        fig_scatter.update_layout(get_modern_chart_layout("LOC vs. Complexity (Sized by Nesting Depth)", height=350))
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # Function Metrics Table
    st.subheader("📋 Function-Level Metrics Table")

    display_cols = [
        "function_name",
        "class_name",
        "start_line",
        "end_line",
        "loc",
        "cyclomatic_complexity",
        "max_nesting_depth",
        "param_count",
        "return_count",
        "loop_count",
        "condition_count",
        "call_count",
        "exception_count",
    ]
    available_cols = [c for c in display_cols if c in metrics_df.columns]

    st.dataframe(
        metrics_df[available_cols].sort_values(by="cyclomatic_complexity", ascending=False),
        use_container_width=True,
    )

    st.markdown("---")

    # Halstead Software Science Metrics
    st.subheader("📐 Halstead Software Science Metrics")
    halstead_cols = [
        "function_name",
        "h_length",
        "h_vocabulary",
        "h_volume",
        "h_difficulty",
        "h_effort",
        "h_time",
        "h_bugs",
    ]
    avail_halstead = [c for c in halstead_cols if c in metrics_df.columns]
    if len(avail_halstead) > 1:
        st.dataframe(metrics_df[avail_halstead], use_container_width=True)

    # Function Inspector Drawer
    st.markdown("---")
    st.subheader("🔍 Function Code & Metrics Inspector")
    func_names = metrics_df["function_name"].tolist()
    selected_func_name = st.selectbox("Select Function to Inspect:", func_names)

    parse_result = st.session_state.get("parse_result")
    if parse_result:
        matched = next((f for f in parse_result.functions if f.name == selected_func_name), None)
        if matched:
            fi_col1, fi_col2 = st.columns([1.2, 0.8])
            with fi_col1:
                st.markdown(f"**Function Code:** `{matched.name}` (Lines {matched.start_line}-{matched.end_line})")
                st.code(matched.raw_code, language="python")
            with fi_col2:
                func_row = metrics_df[metrics_df["function_name"] == selected_func_name].iloc[0]
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <h4 style="margin: 0 0 10px 0; color: #f8fafc;">Metric Blueprint</h4>
                        <div style="font-size: 13.5px; color: #cbd5e1; line-height: 1.8;">
                            • <strong>Lines of Code (LOC):</strong> {func_row.get('loc')}<br>
                            • <strong>Cyclomatic Complexity:</strong> {func_row.get('cyclomatic_complexity')}<br>
                            • <strong>Max Nesting Depth:</strong> {func_row.get('max_nesting_depth')}<br>
                            • <strong>Arguments:</strong> {func_row.get('param_count')}<br>
                            • <strong>Return Points:</strong> {func_row.get('return_count')}<br>
                            • <strong>Conditionals:</strong> {func_row.get('condition_count')}<br>
                            • <strong>Loop Iterations:</strong> {func_row.get('loop_count')}<br>
                            • <strong>Calls Out:</strong> {func_row.get('call_count')}<br>
                            • <strong>Halstead Volume:</strong> {func_row.get('h_volume', 'N/A')}<br>
                            • <strong>Halstead Difficulty:</strong> {func_row.get('h_difficulty', 'N/A')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
