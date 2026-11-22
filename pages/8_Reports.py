"""
Page 8: Reports and Historical Export.
Generates downloadable, publication-grade PDF and CSV reports,
displays actionable recommendations, and manages analysis history database records with modern UI polish.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from modules.report_generator import ReportGenerator, REPORTLAB_AVAILABLE
from modules.history_db import HistoryDatabase
from modules.ui_theme import apply_custom_css, render_hero_banner

st.set_page_config(page_title="Reports & Export - Code Risk Predictor", page_icon="📑", layout="wide")
apply_custom_css()

render_hero_banner(
    title="📑 Reports, Refactoring Actions & Export",
    subtitle="Generate publication-grade PDF technical reports, download raw metric CSV datasets, and manage historical inspection logs.",
    badge="Step 4C: Deliverables",
)

metrics_df = st.session_state.get("metrics_df", pd.DataFrame())
predictions = st.session_state.get("predictions", [])
static_issues = st.session_state.get("static_issues", [])
recommendations = st.session_state.get("recommendations", [])
filename = st.session_state.get("filename", "unnamed_script.py")

tab_report, tab_recs, tab_history = st.tabs(["📄 Export PDF & CSV Reports", "💡 Actionable Refactoring Guidance", "🗄️ Database Inspection Logs"])

with tab_report:
    st.subheader(f"Download Deliverables for: `{filename}`")

    if metrics_df.empty:
        st.warning("No analysis data available in current session. Please upload and analyze a Python script first.")
    else:
        col_pdf, col_csv = st.columns(2)

        # PDF Report Generation Card
        with col_pdf:
            st.markdown(
                """
                <div class="feature-card">
                    <span style="font-size: 24px;">📑</span>
                    <h4 style="margin: 6px 0 4px 0; color: #0f172a;">PDF Technical Report</h4>
                    <p style="font-size: 13px; color: #64748b; margin-bottom: 16px;">
                        Publication-grade multi-page document compiling executive summaries, function complexity matrices, static lint findings, and XAI insights.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if not REPORTLAB_AVAILABLE:
                st.error("ReportLab is not installed. PDF generation disabled.")
            else:
                try:
                    pdf_bytes = ReportGenerator.generate_pdf_report(
                        filename=filename,
                        metrics_df=metrics_df,
                        predictions=predictions,
                        static_issues=static_issues,
                        recommendations=recommendations,
                    )
                    st.download_button(
                        label="📥 Download PDF Technical Report",
                        data=pdf_bytes,
                        file_name=f"Code_Risk_Report_{Path(filename).stem}.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Error compiling PDF: {e}")

        # CSV Export Card
        with col_csv:
            st.markdown(
                """
                <div class="feature-card">
                    <span style="font-size: 24px;">📊</span>
                    <h4 style="margin: 6px 0 4px 0; color: #0f172a;">Raw Metrics CSV Export</h4>
                    <p style="font-size: 13px; color: #64748b; margin-bottom: 16px;">
                        Structured tabular dataset with function-wise McCabe CC, Halstead attributes, line boundaries, and predicted defect probabilities.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            csv_data = ReportGenerator.export_csv(metrics_df, predictions)
            st.download_button(
                label="📥 Download Raw Metrics CSV",
                data=csv_data,
                file_name=f"metrics_{Path(filename).stem}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("---")

        # Master Project Documentation Downloads
        st.subheader("📚 Master Project Academic Documentation (Pin-to-Pin)")
        st.markdown("Download the complete, publication-grade academic documentation containing theoretical foundations, mathematical derivations, empirical benchmark outputs, test matrices, and architecture:")

        doc_c1, doc_c2 = st.columns(2)
        pdf_doc_path = Path(__file__).resolve().parent.parent / "docs" / "AI_Code_Complexity_Bug_Risk_Predictor_Documentation.pdf"
        docx_doc_path = Path(__file__).resolve().parent.parent / "docs" / "AI_Code_Complexity_Bug_Risk_Predictor_Documentation.docx"

        with doc_c1:
            if pdf_doc_path.exists():
                with open(pdf_doc_path, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button(
                    label="📕 Download Master Documentation (PDF)",
                    data=pdf_bytes,
                    file_name="AI_Code_Complexity_Bug_Risk_Predictor_Documentation.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

        with doc_c2:
            if docx_doc_path.exists():
                with open(docx_doc_path, "rb") as f:
                    docx_bytes = f.read()
                st.download_button(
                    label="📘 Download Master Documentation (Word / DOCX)",
                    data=docx_bytes,
                    file_name="AI_Code_Complexity_Bug_Risk_Predictor_Documentation.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )

        st.markdown("---")

        # Executive Summary Preview
        st.subheader("📋 Executive Summary Preview")
        total_f = len(metrics_df)
        high_r = sum(1 for p in predictions if p.get("risk_category") == "High Risk")
        med_r = sum(1 for p in predictions if p.get("risk_category") == "Medium Risk")
        low_r = sum(1 for p in predictions if p.get("risk_category") == "Low Risk")
        avg_cc = round(metrics_df["cyclomatic_complexity"].mean(), 2) if "cyclomatic_complexity" in metrics_df.columns else 0

        st.markdown(
            f"""
            <div class="kpi-card">
                <div style="font-weight: 700; font-size: 15px; color: #0f172a; margin-bottom: 8px;">Analysis Snapshot: <code>{filename}</code></div>
                <div style="font-size: 13.5px; color: #334155; line-height: 1.8;">
                    • <strong>Evaluated Functions:</strong> {total_f} isolated routines<br>
                    • <strong>Average Cyclomatic Complexity:</strong> {avg_cc}<br>
                    • <strong>Defect Risk Breakdown:</strong> 
                        <span class="risk-pill risk-high">{high_r} High</span> 
                        <span class="risk-pill risk-med">{med_r} Medium</span> 
                        <span class="risk-pill risk-low">{low_r} Low</span><br>
                    • <strong>Static Code Warnings:</strong> {len(static_issues)} issues detected<br>
                    • <strong>Predictive Model:</strong> Random Forest Classifier (Trained on NASA PROMISE KC1)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_recs:
    st.subheader("🛠️ Prioritized Code Quality & Refactoring Guidance")
    if not recommendations:
        st.info("No urgent code recommendations for the current script.")
    else:
        for idx, rec in enumerate(recommendations, 1):
            sev = rec.get("severity", "Medium")
            border_color = (
                "#ef4444" if sev == "Critical"
                else ("#ea580c" if sev == "High"
                else ("#f59e0b" if sev == "Warning" else "#3b82f6"))
            )
            badge_class = (
                "risk-high" if sev in ["Critical", "High"]
                else ("risk-med" if sev == "Warning" else "risk-low")
            )
            st.markdown(
                f"""
                <div style="border: 1px solid #1f2937; border-left: 5px solid {border_color}; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; background-color: #111827; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 700; font-size: 14.5px; color: #f8fafc;">#{idx} &bull; {rec.get('target')}</span>
                        <span class="risk-pill {badge_class}">{sev} &bull; {rec.get('category')}</span>
                    </div>
                    <div style="font-size: 13.5px; color: #cbd5e1; margin-bottom: 8px;">
                        <strong>Observation:</strong> {rec.get('message')}
                    </div>
                    <div style="font-size: 13px; color: #e2e8f0; background: #1e293b; border: 1px solid #334155; padding: 8px 12px; border-radius: 6px;">
                        👉 <strong>Remediation:</strong> {rec.get('action')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab_history:
    st.subheader("🗄️ SQLite Analysis History Database")
    history_records = HistoryDatabase.get_all_analyses(limit=50)

    if history_records:
        h_df = pd.DataFrame(history_records)
        st.dataframe(h_df, use_container_width=True)

        st.markdown("---")
        if st.button("🗑️ Clear Analysis History Database", type="secondary"):
            HistoryDatabase.clear_history()
            st.success("Analysis history database cleared successfully.")
            st.rerun()
    else:
        st.info("No prior analyses recorded in SQLite database.")
