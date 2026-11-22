"""
Page 4: Static Code Analysis.
Presents static linting issues, code smells, style warnings, and anti-patterns
detected via Ruff and AST inspection with modern UI styling.
"""

import streamlit as st
import pandas as pd
from modules.ui_theme import apply_custom_css, render_hero_banner

st.set_page_config(page_title="Static Analysis - Code Risk Predictor", page_icon="🔍", layout="wide")
apply_custom_css()

render_hero_banner(
    title="🔍 Static Code Analysis & Anti-Pattern Detection",
    subtitle="Automated inspection identifying dangerous anti-patterns, style violations, mutable defaults, and bare exceptions.",
    badge="Step 2B: Linting",
)

st.markdown(
    """
    <div class="warning-card">
        <strong>Notice on Static Linting:</strong> Static analysis findings indicate coding standard infractions,
        potential anti-patterns, or maintainability debt. They are strictly differentiated from confirmed runtime bugs and ML defect predictions.
    </div>
    """,
    unsafe_allow_html=True,
)

static_issues = st.session_state.get("static_issues", [])

if not static_issues:
    if st.session_state.get("source_code"):
        st.markdown(
            """
            <div class="notice-card">
                🎉 <strong>Clean Static Scan:</strong> No static analysis warnings or anti-patterns detected in the active code.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("No code analyzed yet. Please upload and analyze a Python script on the **Code Upload** page.")
else:
    fname = st.session_state.get("filename", "unnamed.py")

    # Severity Breakdown Cards
    issue_df = pd.DataFrame(static_issues)
    sev_counts = issue_df["severity"].value_counts().to_dict()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Findings</div>
                <div class="kpi-value">{len(static_issues)}</div>
                <div class="kpi-subtext">Across active file</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-top: 3px solid #ef4444;">
                <div class="kpi-label" style="color: #991b1b;">Errors</div>
                <div class="kpi-value" style="color: #991b1b;">{sev_counts.get('Error', 0)}</div>
                <div class="kpi-subtext">Immediate fixes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-top: 3px solid #f59e0b;">
                <div class="kpi-label" style="color: #92400e;">Warnings</div>
                <div class="kpi-value" style="color: #92400e;">{sev_counts.get('Warning', 0)}</div>
                <div class="kpi-subtext">Anti-patterns</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-top: 3px solid #3b82f6;">
                <div class="kpi-label" style="color: #1e40af;">Refactors</div>
                <div class="kpi-value" style="color: #1e40af;">{sev_counts.get('Refactor', 0)}</div>
                <div class="kpi-subtext">Length / params</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col5:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-top: 3px solid #10b981;">
                <div class="kpi-label" style="color: #065f46;">Conventions</div>
                <div class="kpi-value" style="color: #065f46;">{sev_counts.get('Convention', 0)}</div>
                <div class="kpi-subtext">Docstrings / style</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Filter by Severity
    severities = ["All Severities"] + sorted(list(issue_df["severity"].unique()))
    selected_sev = st.selectbox("Filter Findings by Category:", severities)

    filtered_df = issue_df if selected_sev == "All Severities" else issue_df[issue_df["severity"] == selected_sev]

    st.subheader(f"Findings Log ({len(filtered_df)})")

    # Display Structured Table
    display_cols = ["line", "column", "rule_id", "severity", "message", "suggestion"]
    st.dataframe(
        filtered_df[display_cols].sort_values(by=["line", "column"]),
        use_container_width=True,
    )

    st.markdown("---")

    # Detailed Cards for Top Issues
    st.subheader("💡 Highlighted Anti-Patterns & Remediations")
    for _, item in filtered_df.head(6).iterrows():
        sev = item["severity"]
        badge_color = "#ef4444" if sev == "Error" else ("#f59e0b" if sev == "Warning" else "#3b82f6")
        st.markdown(
            f"""
            <div style="border: 1px solid #1f2937; border-left: 4px solid {badge_color}; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; background-color: #111827; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; font-size: 14px; color: #f8fafc;">Line {item['line']}, Column {item['column']}</span>
                    <span style="background-color: {badge_color}25; color: {badge_color}; padding: 3px 10px; border-radius: 12px; font-weight: 600; font-size: 12px;">{item['rule_id']} &bull; {item['severity']}</span>
                </div>
                <div style="font-size: 13.5px; color: #cbd5e1; margin-bottom: 8px;"><strong>Description:</strong> {item['message']}</div>
                <div style="font-size: 13px; color: #e2e8f0; background: #1e293b; border: 1px solid #334155; padding: 8px 12px; border-radius: 6px;">
                    👉 <strong>Suggested Action:</strong> {item['suggestion']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
