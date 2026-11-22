"""
UI Theme and Modern Styling module.
Provides unified modern CSS design tokens, dark developer theme components,
and Plotly chart templates for the Streamlit dashboard.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Optional, Dict, Any


def apply_custom_css() -> None:
    """Injects high-polish, dark-theme modern software engineering UI styling."""
    st.markdown(
        """
        <style>
        /* Import clean modern typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        html, body, [class*="css"], [class*="st-"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        code, pre, [class*="stCode"] {
            font-family: 'JetBrains Mono', Consolas, monospace !important;
        }

        /* Hero & Header Banner */
        .hero-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #1e3a8a 100%);
            border-radius: 12px;
            padding: 24px 28px;
            color: #ffffff;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }
        .hero-title {
            font-size: 26px;
            font-weight: 700;
            color: #ffffff;
            margin: 0 0 6px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .hero-subtitle {
            font-size: 14.5px;
            color: #cbd5e1;
            margin: 0;
            line-height: 1.5;
        }

        /* Metric KPI Cards (Dark Slate) */
        .kpi-card {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 14px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
            transition: transform 0.15s ease, border-color 0.15s ease;
        }
        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: #3b82f6;
        }
        .kpi-label {
            font-size: 11.5px;
            font-weight: 600;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 4px;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            color: #f8fafc;
            line-height: 1.2;
        }
        .kpi-subtext {
            font-size: 12px;
            color: #64748b;
            margin-top: 4px;
        }

        /* Modern Risk Badges */
        .risk-pill {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
            text-align: center;
        }
        .risk-high {
            background-color: rgba(239, 68, 68, 0.18);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.45);
        }
        .risk-med {
            background-color: rgba(245, 158, 11, 0.18);
            color: #fcd34d;
            border: 1px solid rgba(245, 158, 11, 0.45);
        }
        .risk-low {
            background-color: rgba(16, 185, 129, 0.18);
            color: #6ee7b7;
            border: 1px solid rgba(16, 185, 129, 0.45);
        }

        /* Feature Card */
        .feature-card {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 10px;
            padding: 20px;
            height: 100%;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            transition: border-color 0.15s ease, transform 0.15s ease;
        }
        .feature-card:hover {
            border-color: #3b82f6;
            transform: translateY(-2px);
        }

        /* Dark-Theme Callout Banners */
        .notice-card {
            background: rgba(16, 185, 129, 0.12);
            border-left: 4px solid #10b981;
            padding: 12px 18px;
            border-radius: 6px;
            margin-bottom: 18px;
            font-size: 13.5px;
            color: #d1fae5;
            border-top: 1px solid rgba(16, 185, 129, 0.2);
            border-right: 1px solid rgba(16, 185, 129, 0.2);
            border-bottom: 1px solid rgba(16, 185, 129, 0.2);
        }
        .warning-card {
            background: rgba(245, 158, 11, 0.12);
            border-left: 4px solid #f59e0b;
            padding: 12px 18px;
            border-radius: 6px;
            margin-bottom: 18px;
            font-size: 13.5px;
            color: #fef3c7;
            border-top: 1px solid rgba(245, 158, 11, 0.2);
            border-right: 1px solid rgba(245, 158, 11, 0.2);
            border-bottom: 1px solid rgba(245, 158, 11, 0.2);
        }
        .info-card {
            background: rgba(2, 132, 199, 0.12);
            border-left: 4px solid #0284c7;
            padding: 12px 18px;
            border-radius: 6px;
            margin-bottom: 18px;
            font-size: 13.5px;
            color: #e0f2fe;
            border-top: 1px solid rgba(2, 132, 199, 0.2);
            border-right: 1px solid rgba(2, 132, 199, 0.2);
            border-bottom: 1px solid rgba(2, 132, 199, 0.2);
        }

        /* Sidebar Styling (Dark Cohesive) */
        section[data-testid="stSidebar"] {
            background-color: #0d131f !important;
            border-right: 1px solid #1f2937 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #e2e8f0;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {
            border-radius: 8px;
            padding: 6px 12px;
            margin: 3px 0;
            color: #cbd5e1 !important;
            transition: background-color 0.15s ease;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {
            background-color: #1e293b !important;
            color: #60a5fa !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {
            background: linear-gradient(90deg, #1e3a8a 0%, #1e293b 100%) !important;
            color: #ffffff !important;
            font-weight: 600;
            border-left: 3px solid #3b82f6;
        }

        /* Tab Navigation */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
            border-bottom: 1px solid #1f2937;
            padding-bottom: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 6px 6px 0 0;
            padding: 8px 16px;
            font-weight: 500;
            color: #94a3b8;
        }
        .stTabs [aria-selected="true"] {
            color: #60a5fa !important;
            border-bottom: 2px solid #3b82f6 !important;
        }

        /* DataFrames & Tables */
        .stDataFrame {
            border: 1px solid #1f2937;
            border-radius: 8px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero_banner(title: str, subtitle: str, badge: Optional[str] = None) -> None:
    """Renders a styled dark-slate header banner."""
    badge_html = f'<span style="background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 20px; font-size: 11.5px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">{badge}</span>' if badge else ''
    st.markdown(
        f"""
        <div class="hero-banner">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <h1 class="hero-title">{title}</h1>
                {badge_html}
            </div>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_risk_pill(risk_category: str) -> str:
    """Returns an HTML string for a colored risk pill."""
    if risk_category == "High Risk":
        return '<span class="risk-pill risk-high">High Risk</span>'
    elif risk_category == "Medium Risk":
        return '<span class="risk-pill risk-med">Medium Risk</span>'
    else:
        return '<span class="risk-pill risk-low">Low Risk</span>'


def get_modern_chart_layout(title: str, height: int = 360) -> Dict[str, Any]:
    """Returns a clean dark Plotly layout configuration."""
    return dict(
        title=dict(text=title, font=dict(family="Inter, sans-serif", size=15, color="#f8fafc")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#cbd5e1", size=12),
        margin=dict(l=40, r=30, t=50, b=40),
        height=height,
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.08)",
            linecolor="rgba(255, 255, 255, 0.15)",
            tickfont=dict(color="#94a3b8"),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.08)",
            linecolor="rgba(255, 255, 255, 0.15)",
            tickfont=dict(color="#94a3b8"),
        ),
        legend=dict(
            font=dict(family="Inter, sans-serif", size=11, color="#e2e8f0"),
            bgcolor="rgba(17, 24, 39, 0.85)",
            bordercolor="#1f2937",
            borderwidth=1,
        ),
    )
