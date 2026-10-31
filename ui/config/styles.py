# ui/config/styles.py
"""Global CSS layout and component styling for the Aegis Streamlit application.

Exports:
    GLOBAL_CSS  – always injected (light mode base)
    DARK_CSS    – injected only when dark mode toggle is on
"""

GLOBAL_CSS = """
<style>
/* Base typography */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
}

/* Remove default whitespace */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
}

/* Top Government Header Bar */
.gov-topbar {
    background-color: #1B3A6B;
    padding: 0 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 54px;
    margin-bottom: 8px;
}
.gov-portal-name {
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 700;
}
.gov-portal-sub {
    color: #BAD4F7;
    font-size: 11px;
    margin-top: 1px;
}
.gov-badge {
    background-color: rgba(255,255,255,0.15);
    color: #DBEAFE;
    border: 1px solid rgba(255,255,255,0.3);
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Field Sub-section Header Labels */
.form-section-label {
    font-size: 11px;
    font-weight: 700;
    color: #1B3A6B;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 6px 0 10px 0;
    border-bottom: 1.5px solid #E5E7EB;
    margin-bottom: 14px;
}

/* Metric Containers */
div[data-testid="metric-container"] {
    border: 1px solid #D1D5DB;
    border-radius: 8px;
    padding: 14px 18px;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #1B3A6B !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 2px solid #E5E7EB;
}
.stTabs [data-baseweb="tab"] {
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #1B3A6B !important;
    border-bottom: 2px solid #1B3A6B !important;
}

/* Button Defaults */
.stButton > button {
    border: 1.5px solid #1B3A6B !important;
    color: #1B3A6B !important;
    background-color: #FFFFFF !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
}
.stButton > button:hover {
    background-color: #1B3A6B !important;
    color: #FFFFFF !important;
}

/* Sidebar divider styling */
[data-testid="stSidebar"] {
    border-right: 1px solid #D1D5DB;
}
</style>
"""

DARK_CSS = """
<style>
/* ── Dark Mode Overrides ─────────────────────────────────────────────── */

/* App & page background */
.stApp, html, body, [class*="css"],
.block-container, [data-testid="stAppViewContainer"] {
    background-color: #0F172A !important;
    color: #F1F5F9 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1E293B !important;
    border-right: 1px solid #334155 !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {
    color: #CBD5E1 !important;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #93C5FD !important;
}
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #0F172A !important;
    border-bottom: 2px solid #334155 !important;
}
.stTabs [data-baseweb="tab"] {
    background-color: #0F172A !important;
    color: #94A3B8 !important;
}
.stTabs [aria-selected="true"] {
    color: #93C5FD !important;
    border-bottom: 2px solid #93C5FD !important;
}

/* Buttons */
.stButton > button {
    background-color: #1E293B !important;
    border: 1.5px solid #334155 !important;
    color: #93C5FD !important;
}
.stButton > button:hover {
    background-color: #1B3A6B !important;
    color: #FFFFFF !important;
}

/* Text inputs, selects, number inputs */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background-color: #1E293B !important;
    color: #F1F5F9 !important;
    border-color: #334155 !important;
}

/* Markdown text & captions */
.stMarkdown p, .stMarkdown div, .stMarkdown li,
p, label, span {
    color: #CBD5E1 !important;
}
.stCaption p { color: #64748B !important; }

/* Download button */
[data-testid="stDownloadButton"] > button {
    background-color: #1E293B !important;
    border: 1.5px solid #334155 !important;
    color: #93C5FD !important;
}
</style>
"""
