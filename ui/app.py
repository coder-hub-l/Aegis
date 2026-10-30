# ui/app.py
import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path so core and data can be imported cleanly
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.models import CitizenProfile
from core.app_logic import run_eligibility_pipeline
from ui.components.results_view import render_results
from ui.components.sidebar import render_sidebar_summary
from data.constants import CASTE_CATEGORIES, OCCUPATIONS, GENDERS

# ── Page Configuration ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Maharashtra Welfare Scheme Navigator",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Language Toggle & Localization Dictionary ───────────────────────────
lang = st.sidebar.radio("🌐 Language / भाषा", ["English", "मराठी"])

LABELS = {
    "English": {
        "title": "🏛️ Maharashtra Welfare Scheme Navigator",
        "subtitle": "Deterministic eligibility assessment backed by statutory Maharashtra Government gazette rules.",
        "badge": "Zero Hallucination · Official Gazette Rules · GenAI Explanations",
        "preset_header": "⚡ Load a Demo Persona",
        "manual_option": "-- Fill form manually --",
        "form_header": "Enter Citizen Applicant Details",
        "name": "Applicant Name (optional)",
        "age": "Age (years)",
        "gender": "Gender",
        "income": "Annual Household Income (₹)",
        "caste": "Caste Category",
        "land": "Agricultural Land Holding (hectares)",
        "occupation": "Occupation",
        "bank": "Has Aadhaar-linked Bank Account",
        "aadhaar": "Has Aadhaar Card",
        "house": "Owns a Pucca House",
        "submit": "🔍 Check Scheme Eligibility",
        "running": "Evaluating eligibility against verified Maharashtra gazette rules...",
    },
    "मराठी": {
        "title": "🏛️ महाराष्ट्र कल्याण योजना मार्गदर्शक",
        "subtitle": "महाराष्ट्र शासनाच्या अधिकृत राजपत्रातील नियमांवर आधारित अचूक पात्रता तपासणी.",
        "badge": "शून्य भ्रम (Zero Hallucination) · अधिकृत नियम · सोप्या भाषेत स्पष्टीकरण",
        "preset_header": "⚡ डेमो प्रोफाईल निवडा",
        "manual_option": "-- स्वतः माहिती भरा --",
        "form_header": "अर्जदाराची माहिती प्रविष्ट करा",
        "name": "अर्जदाराचे नाव (ऐच्छिक)",
        "age": "वय (वर्षे)",
        "gender": "लिंग",
        "income": "वार्षिक कौटुंबिक उत्पन्न (₹)",
        "caste": "जात प्रवर्ग",
        "land": "शेतीजमीन धारणा (हेक्टर)",
        "occupation": "व्यवसाय",
        "bank": "आधार लिंक असलेले बँक खाते आहे",
        "aadhaar": "आधार कार्ड आहे",
        "house": "स्वतःचे पक्के घर आहे",
        "submit": "🔍 माझी योजना पात्रता तपासा",
        "running": "अधिकृत सरकारी नियमांच्या आधारे पडताळणी सुरू आहे...",
    }
}
L = LABELS[lang]

# ── Preset Personas for Flawless Live Demo ──────────────────────────────
PRESETS = {
    "👨‍🌾 Ramesh Patil — Small Farmer (Eligible: PM-KISAN, Namo Shetkari)": {
        "name": "Ramesh Patil", "age": 45, "gender": "male",
        "annual_income": 90000.0, "caste_category": "obc",
        "land_holding_hectares": 1.5, "occupation": "farmer",
        "has_bank_account": True, "has_aadhaar": True, "owns_pucca_house": False
    },
    "👩 Sunita Kamble — Rural Woman (Eligible: Ladki Bahin | Almost: PMAY-G)": {
        "name": "Sunita Kamble", "age": 35, "gender": "female",
        "annual_income": 135000.0, "caste_category": "sc",
        "land_holding_hectares": 0.0, "occupation": "laborer",
        "has_bank_account": True, "has_aadhaar": True, "owns_pucca_house": False
    },
    "👔 Vikram Joshi — Urban Salaried (Demonstrating Edge Cases & Exclusions)": {
        "name": "Vikram Joshi", "age": 30, "gender": "male",
        "annual_income": 650000.0, "caste_category": "general",
        "land_holding_hectares": 0.0, "occupation": "salaried",
        "has_bank_account": True, "has_aadhaar": True, "owns_pucca_house": True
    }
}

# ── Main Header ─────────────────────────────────────────────────────────
st.title(L["title"])
st.caption(f"**{L['badge']}** — {L['subtitle']}")

# ── Preset Profile Picker ───────────────────────────────────────────────
preset_choice = st.selectbox(
    L["preset_header"],
    [L["manual_option"]] + list(PRESETS.keys()),
    index=0
)

defaults = PRESETS.get(preset_choice, {})

# ── Citizen Intake Form ─────────────────────────────────────────────────
st.markdown(f"#### {L['form_header']}")
with st.form("citizen_intake_form"):
    col1, col2 = st.columns(2)

    with col1:
        name_val = defaults.get("name", "")
        age_val = int(defaults.get("age", 30))
        gender_val = defaults.get("gender", "male")
        income_val = float(defaults.get("annual_income", 100000.0))
        caste_val = defaults.get("caste_category", "general")

        name = st.text_input(L["name"], value=name_val)
        age = st.number_input(L["age"], min_value=0, max_value=120, value=age_val, step=1)
        gender = st.selectbox(L["gender"], GENDERS, index=GENDERS.index(gender_val) if gender_val in GENDERS else 0)
        income = st.number_input(L["income"], min_value=0.0, step=5000.0, value=income_val, format="%.0f")
        caste = st.selectbox(L["caste"], CASTE_CATEGORIES, index=CASTE_CATEGORIES.index(caste_val) if caste_val in CASTE_CATEGORIES else 0)

    with col2:
        land_val = float(defaults.get("land_holding_hectares", 0.0))
        occ_val = defaults.get("occupation", "farmer")
        bank_val = bool(defaults.get("has_bank_account", True))
        aadhaar_val = bool(defaults.get("has_aadhaar", True))
        house_val = bool(defaults.get("owns_pucca_house", False))

        land = st.number_input(L["land"], min_value=0.0, step=0.1, value=land_val, format="%.2f")
        occupation = st.selectbox(L["occupation"], OCCUPATIONS, index=OCCUPATIONS.index(occ_val) if occ_val in OCCUPATIONS else 0)
        bank = st.checkbox(L["bank"], value=bank_val)
        aadhaar = st.checkbox(L["aadhaar"], value=aadhaar_val)
        house = st.checkbox(L["house"], value=house_val)

    submitted = st.form_submit_button(L["submit"], use_container_width=True, type="primary")

# ── Evaluation Trigger ──────────────────────────────────────────────────
if submitted:
    profile = CitizenProfile(
        name=name or "Applicant",
        age=age,
        gender=gender,
        annual_income=income,
        caste_category=caste,
        land_holding_hectares=land,
        occupation=occupation,
        has_bank_account=bank,
        has_aadhaar=aadhaar,
        owns_pucca_house=house
    )

    # Render profile in sidebar
    render_sidebar_summary(profile, lang)

    # Run pipeline
    with st.spinner(L["running"]):
        results = run_eligibility_pipeline(profile)

    # Display results
    render_results(results, lang)
