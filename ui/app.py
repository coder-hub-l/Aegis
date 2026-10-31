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
from ui.config.styles import GLOBAL_CSS, DARK_CSS
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

# ── State Initialization ────────────────────────────────────────────────
init_form_state()

# ── Sidebar: Logo Pinned Top, Language, Dark Mode, Portals, Profile ─────
active_profile = st.session_state.get("submitted_profile")
lang, is_marathi, dark_mode = render_sidebar(profile=active_profile)
if dark_mode:
    st.markdown(DARK_CSS, unsafe_allow_html=True)

# ── Header & Main Form View ─────────────────────────────────────────────
render_topbar(is_marathi)

st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)

# Step 1: Demo Presets
render_preset_picker(is_marathi)

# Step 2: Intake Form
submitted, profile = render_intake_form(is_marathi)

# Step 3: Evaluation Pipeline
if submitted and profile:
    st.session_state["submitted_profile"] = profile
    with st.spinner(t("spinner", is_marathi)):
        results = run_eligibility_pipeline(profile)
        st.session_state["latest_results"] = results
    render_results(results, lang=lang, profile=profile)
elif "latest_results" in st.session_state and st.session_state.get("submitted_profile"):
    # Re-render results if user switched language or toggled dark mode without re-submitting
    render_results(st.session_state["latest_results"], lang=lang, profile=st.session_state["submitted_profile"])

st.markdown("</div>", unsafe_allow_html=True)
