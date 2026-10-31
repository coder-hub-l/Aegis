# ui/app.py
"""Main application entry point for the Maharashtra Scheme Eligibility Navigator."""
import sys
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.app_logic import run_eligibility_pipeline
from ui.config.styles import GLOBAL_CSS
from ui.config.strings import t
from ui.config.presets import init_form_state
from ui.sections.topbar import render_topbar
from ui.sections.preset_picker import render_preset_picker
from ui.sections.intake_form import render_intake_form
from ui.components.results_dashboard import render_results
from ui.components.sidebar import render_sidebar

# ── Page Configuration ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Scheme Eligibility Navigator — Government of Maharashtra",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS Injection ────────────────────────────────────────────────
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Language Toggle (Sidebar top) ───────────────────────────────────────
lang = st.sidebar.radio("Language / भाषा", ["English", "मराठी"], index=0)
is_marathi = (lang == "मराठी")

# ── State Initialization ────────────────────────────────────────────────
init_form_state()

# ── Header & Main Form View ─────────────────────────────────────────────
render_topbar(is_marathi)

st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)

# Step 1: Demo Presets
render_preset_picker(is_marathi)

# Step 2: Intake Form
submitted, profile = render_intake_form(is_marathi)

# Step 3: Evaluation Pipeline
if submitted and profile:
    render_sidebar(profile=profile, lang=lang)
    with st.spinner(t("spinner", is_marathi)):
        results = run_eligibility_pipeline(profile)
    render_results(results, lang=lang, profile=profile)
else:
    render_sidebar(profile=None, lang=lang)

st.markdown("</div>", unsafe_allow_html=True)
