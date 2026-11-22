"""
Report Generation module.
Generates downloadable, publication-grade PDF and CSV reports containing
executive summaries, function complexity metrics, static analysis warnings,
ML defect risk predictions, and actionable improvement recommendations.
"""

import io
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

from config.settings import REPORTS_DIR

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        KeepTogether,
        HRFlowable,
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class ReportGenerator:
    """Generates PDF and CSV reports for code analysis sessions."""

    @classmethod
    def export_csv(
        cls,
        metrics_df: pd.DataFrame,
        predictions: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Merges metrics and ML predictions into a clean CSV string."""
        if metrics_df.empty:
            return ""

        merged = metrics_df.copy()
        if predictions:
            pred_df = pd.DataFrame(predictions)
            keep_cols = ["function_name", "defect_probability", "predicted_class", "risk_category"]
            pred_df = pred_df[[c for c in keep_cols if c in pred_df.columns]]
            merged = pd.merge(merged, pred_df, on="function_name", how="left")

        return merged.to_csv(index=False)

    @classmethod
    def generate_pdf_report(
        cls,
        filename: str,
        metrics_df: pd.DataFrame,
        predictions: List[Dict[str, Any]],
        static_issues: List[Dict[str, Any]],
        recommendations: List[Dict[str, str]],
        output_filename: Optional[str] = None,
    ) -> bytes:
        """
        Creates a PDF report conforming to academic and professional standards.
        Returns the PDF as raw bytes.
        """
        if not REPORTLAB_AVAILABLE:
            raise ImportError(
                "ReportLab is not installed or available. Please install 'reportlab' to enable PDF export."
            )

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()

        # Custom typography styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#1A365D"),
            spaceAfter=6,
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#4A5568"),
            spaceAfter=12,
        )
        heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#2B6CB0"),
            spaceBefore=12,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "BodyDark",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#2D3748"),
        )
        body_bold = ParagraphStyle(
            "BodyDarkBold",
            parent=body_style,
            fontName="Helvetica-Bold",
        )
        table_cell_style = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=colors.HexColor("#1A202C"),
        )
        table_header_style = ParagraphStyle(
            "TableHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white,
        )

        story = []

        # 1. Header Banner
        story.append(Paragraph("AI-Based Code Complexity & Bug Risk Predictor", title_style))
        analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        story.append(
            Paragraph(
                f"<b>Target File:</b> {filename} &nbsp;|&nbsp; <b>Analysis Date:</b> {analysis_time} &nbsp;|&nbsp; <b>Architecture:</b> Hybrid AST & ML",
                subtitle_style,
            )
        )
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=10))

        # 2. Executive Summary Metrics
        total_funcs = len(metrics_df) if not metrics_df.empty else 0
        total_loc = int(metrics_df["loc"].sum()) if not metrics_df.empty and "loc" in metrics_df.columns else 0
        avg_cc = round(float(metrics_df["cyclomatic_complexity"].mean()), 2) if not metrics_df.empty and "cyclomatic_complexity" in metrics_df.columns else 0.0

        high_risk_count = sum(1 for p in predictions if p.get("risk_category") == "High Risk")
        med_risk_count = sum(1 for p in predictions if p.get("risk_category") == "Medium Risk")
        low_risk_count = sum(1 for p in predictions if p.get("risk_category") == "Low Risk")

        summary_data = [
            [
                Paragraph("<b>Metric</b>", table_header_style),
                Paragraph("<b>Value</b>", table_header_style),
                Paragraph("<b>Metric</b>", table_header_style),
                Paragraph("<b>Value</b>", table_header_style),
            ],
            [
                Paragraph("Total Functions", table_cell_style),
                Paragraph(str(total_funcs), table_cell_style),
                Paragraph("High Risk Functions", table_cell_style),
                Paragraph(f"<font color='#C53030'><b>{high_risk_count}</b></font>", table_cell_style),
            ],
            [
                Paragraph("Total Code Lines (LOC)", table_cell_style),
                Paragraph(str(total_loc), table_cell_style),
                Paragraph("Medium Risk Functions", table_cell_style),
                Paragraph(f"<font color='#D69E2E'><b>{med_risk_count}</b></font>", table_cell_style),
            ],
            [
                Paragraph("Average Cyclomatic Complexity", table_cell_style),
                Paragraph(str(avg_cc), table_cell_style),
                Paragraph("Low Risk Functions", table_cell_style),
                Paragraph(f"<font color='#38A169'><b>{low_risk_count}</b></font>", table_cell_style),
            ],
            [
                Paragraph("Static Analysis Issues", table_cell_style),
                Paragraph(str(len(static_issues)), table_cell_style),
                Paragraph("Actionable Recommendations", table_cell_style),
                Paragraph(str(len(recommendations)), table_cell_style),
            ],
        ]

        summary_table = Table(summary_data, colWidths=[140, 110, 140, 110])
        summary_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
        )
        story.append(summary_table)
        story.append(Spacer(1, 10))

        # 3. Function Complexity & ML Defect Risk Table
        story.append(Paragraph("1. Function-Level Complexity & Defect Risk Analysis", heading_style))

        if not metrics_df.empty:
            func_headers = [
                Paragraph("<b>Function</b>", table_header_style),
                Paragraph("<b>Lines</b>", table_header_style),
                Paragraph("<b>LOC</b>", table_header_style),
                Paragraph("<b>CC</b>", table_header_style),
                Paragraph("<b>Depth</b>", table_header_style),
                Paragraph("<b>Params</b>", table_header_style),
                Paragraph("<b>ML Prob</b>", table_header_style),
                Paragraph("<b>Risk Band</b>", table_header_style),
            ]
            func_rows = [func_headers]

            pred_map = {p.get("function_name"): p for p in predictions}

            for _, row in metrics_df.iterrows():
                fname = str(row.get("function_name", "unknown"))
                p_info = pred_map.get(fname, {})
                prob_str = f"{p_info.get('defect_probability', 0.0)*100:.1f}%"
                risk_cat = p_info.get("risk_category", "N/A")

                color_hex = "#2D3748"
                if risk_cat == "High Risk":
                    color_hex = "#C53030"
                elif risk_cat == "Medium Risk":
                    color_hex = "#D69E2E"
                elif risk_cat == "Low Risk":
                    color_hex = "#38A169"

                func_rows.append([
                    Paragraph(f"<b>{fname}</b>", table_cell_style),
                    Paragraph(f"{row.get('start_line', 1)}-{row.get('end_line', 1)}", table_cell_style),
                    Paragraph(str(row.get("loc", 1)), table_cell_style),
                    Paragraph(str(row.get("cyclomatic_complexity", 1)), table_cell_style),
                    Paragraph(str(row.get("max_nesting_depth", 0)), table_cell_style),
                    Paragraph(str(row.get("param_count", 0)), table_cell_style),
                    Paragraph(prob_str, table_cell_style),
                    Paragraph(f"<font color='{color_hex}'><b>{risk_cat}</b></font>", table_cell_style),
                ])

            func_table = Table(func_rows, colWidths=[120, 50, 40, 35, 45, 45, 65, 80])
            func_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2D3748")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ])
            )
            story.append(func_table)
        else:
            story.append(Paragraph("No function-level metrics detected.", body_style))

        story.append(Spacer(1, 10))

        # 4. Static Code Analysis Warnings
        story.append(Paragraph("2. Static Code Analysis Findings", heading_style))
        if static_issues:
            static_headers = [
                Paragraph("<b>Line:Col</b>", table_header_style),
                Paragraph("<b>Code</b>", table_header_style),
                Paragraph("<b>Severity</b>", table_header_style),
                Paragraph("<b>Description</b>", table_header_style),
                Paragraph("<b>Suggested Remediation</b>", table_header_style),
            ]
            static_rows = [static_headers]
            for issue in static_issues[:15]:  # Limit top 15 in summary to prevent pagination overflow
                static_rows.append([
                    Paragraph(f"{issue.get('line', 1)}:{issue.get('column', 1)}", table_cell_style),
                    Paragraph(str(issue.get("rule_id", "WARN")), table_cell_style),
                    Paragraph(str(issue.get("severity", "Warning")), table_cell_style),
                    Paragraph(str(issue.get("message", "")), table_cell_style),
                    Paragraph(str(issue.get("suggestion", "")), table_cell_style),
                ])

            static_table = Table(static_rows, colWidths=[50, 45, 55, 175, 175])
            static_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4A5568")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ])
            )
            story.append(static_table)
        else:
            story.append(Paragraph("No static analysis warnings found. Clean static inspection.", body_style))

        story.append(Spacer(1, 10))

        # 5. Improvement Recommendations
        story.append(Paragraph("3. Actionable Code Improvement Recommendations", heading_style))
        if recommendations:
            for rec in recommendations[:8]:
                sev = rec.get("severity", "Medium")
                target = rec.get("target", "")
                msg = rec.get("message", "")
                act = rec.get("action", "")
                story.append(
                    Paragraph(
                        f"• <b>[{sev}] {target}:</b> {msg} <i>Remediation: {act}</i>",
                        body_style,
                    )
                )
                story.append(Spacer(1, 3))
        else:
            story.append(Paragraph("No urgent structural refactorings required.", body_style))

        story.append(Spacer(1, 10))

        # 6. Methodological Limitations & Academic Disclaimer
        story.append(Paragraph("4. Methodological Notice and Academic Limitations", heading_style))
        disclaimer_text = (
            "<b>Disclaimer:</b> High cyclomatic complexity or code length does not automatically guarantee "
            "the existence of an executable software defect. Defect probabilities are statistical estimates "
            "generated by Machine Learning algorithms trained on historical NASA PROMISE repository defect records. "
            "Explainable AI (SHAP) attributions illustrate mathematical correlations rather than physical causality. "
            "This automated report is designed as an advisory decision-support tool for code review prioritization."
        )
        story.append(Paragraph(disclaimer_text, body_style))

        # Build Document
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        # Save to disk if requested
        if output_filename:
            out_path = REPORTS_DIR / output_filename
            with open(out_path, "wb") as f:
                f.write(pdf_bytes)

        return pdf_bytes
