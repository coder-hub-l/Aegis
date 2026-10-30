# ui/app.py
import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.models import CitizenProfile
from core.app_logic import run_eligibility_pipeline
from ui.components.sidebar import render_sidebar
from ui.components.results_view import render_results

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Scheme Eligibility Navigator — Government of Maharashtra",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — layout & structure only.
# ALL colors for text, inputs, and backgrounds are handled by .streamlit/config.toml
# (light theme, primaryColor=#1B3A6B, textColor=#111827, backgroundColor=#FFFFFF)
# We only override structural things here — padding, border-radius, flex layout.
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base font ──────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
}

/* ── Remove excess top padding from main block ──────────────────────── */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
}

/* ── Top Government Header Bar ─────────────────────────────────────── */
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

/* ── Field sub-section labels (PERSONAL / ECONOMIC / DOCUMENTATION) ── */
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

/* ── Metric Cards ───────────────────────────────────────────────────── */
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

/* ── Tabs ───────────────────────────────────────────────────────────── */
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

/* ── Primary buttons ────────────────────────────────────────────────── */
/* Preset load buttons */
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

/* ── Sidebar border ─────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    border-right: 1px solid #D1D5DB;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE TOGGLE  — rendered inside sidebar, above all content
# ─────────────────────────────────────────────────────────────────────────────
lang = st.sidebar.radio("Language / भाषा", ["English", "मराठी"], index=0)
is_marathi = (lang == "मराठी")

# ─────────────────────────────────────────────────────────────────────────────
# STRING DICTIONARY
# ─────────────────────────────────────────────────────────────────────────────
T = {
    "portal_name":    ("Scheme Eligibility Navigator",          "योजना पात्रता तपासणी प्रणाली"),
    "portal_sub":     ("Government of Maharashtra",             "महाराष्ट्र शासन"),
    "demo_heading":   ("Step 1 — Select a Demo Profile (Optional)", "पाऊल १ — डेमो प्रोफाईल निवडा (ऐच्छिक)"),
    "demo_caption":   ("Load a pre-configured citizen profile to see instant results, or fill the form manually below.",
                       "तयार नागरिक प्रोफाईल लोड करा किंवा खाली स्वतः माहिती भरा."),
    "form_heading":   ("Step 2 — Citizen Eligibility Assessment Form", "पाऊल २ — नागरिक पात्रता तपासणी अर्ज"),
    "form_caption":   ("All fields marked with * are required for accurate eligibility verification.",
                       "* असलेली सर्व माहिती अचूक पात्रता तपासणीसाठी आवश्यक आहे."),
    "personal":       ("Personal Details",                      "वैयक्तिक माहिती"),
    "economic":       ("Economic & Agricultural Details",       "आर्थिक व शेती माहिती"),
    "doc_status":     ("Documentation & Asset Status",          "कागदपत्रे व मालमत्ता स्थिती"),
    "name":           ("Full Name",                             "पूर्ण नाव"),
    "age":            ("Age *",                                 "वय *"),
    "gender":         ("Gender *",                              "लिंग *"),
    "income":         ("Annual Household Income (INR) *",       "वार्षिक कौटुंबिक उत्पन्न (रुपये) *"),
    "caste":          ("Caste Category *",                      "जात प्रवर्ग *"),
    "land":           ("Agricultural Land Holding (Ha)",        "शेतजमीन धारणा (हेक्टर)"),
    "occupation":     ("Primary Occupation *",                  "मुख्य व्यवसाय *"),
    "bank":           ("Has active Aadhaar-linked bank account (DBT enabled) *",
                       "आधार जोडलेले सक्रिय बँक खाते उपलब्ध आहे (DBT) *"),
    "aadhaar":        ("Holds valid Aadhaar card *",            "वैध आधार कार्ड आहे *"),
    "house":          ("Owns a permanent pucca (concrete) house *",
                       "स्वतःचे पक्के (काँक्रीट) घर आहे *"),
    "submit":         ("Verify Eligibility Against Official Schemes",
                       "अधिकृत योजनांनुसार पात्रता तपासा"),
    "reset":          ("Clear Form",                            "माहिती पूर्ववत करा"),
    "spinner":        ("Verifying against official Maharashtra gazette rules…",
                       "शासकीय नियमांनुसार पडताळणी सुरु आहे…"),
    "income_note":    ("Equivalent: Rs. {amt} ({lakh:.2f} Lakh per year)",
                       "समतुल्य: रु. {amt} ({lakh:.2f} लाख प्रतिवर्ष)"),
    "land_note":      ("{ha:.2f} Ha = {acres:.2f} Acres",      "{ha:.2f} हेक्टर = {acres:.2f} एकर"),
}

def t(key): return T[key][1] if is_marathi else T[key][0]


# ─────────────────────────────────────────────────────────────────────────────
# PRESET PROFILES
# ─────────────────────────────────────────────────────────────────────────────
PRESETS = {
    "ramesh": {
        "label_en": "Ramesh Patil — Small Farmer",
        "label_mr": "रमेश पाटील — अल्पभूधारक शेतकरी",
        "note_en":  "Age 45 | Male | OBC | Income Rs. 90,000 | Land 1.5 Ha | Farmer",
        "note_mr":  "वय ४५ | पुरुष | ओबीसी | उत्पन्न रु. ९०,००० | जमीन १.५ हेक्टर | शेतकरी",
        "expected_en": "Eligible: PM-KISAN, Namo Shetkari",
        "expected_mr": "पात्र: पीएम-किसान, नमो शेतकरी",
        "data": dict(name="Ramesh Patil", age=45, gender="male", annual_income=90000.0,
                     caste_category="obc", land_holding_hectares=1.5, occupation="farmer",
                     has_bank_account=True, has_aadhaar=True, owns_pucca_house=False),
    },
    "sunita": {
        "label_en": "Sunita Kamble — Rural Woman",
        "label_mr": "सुनीता कांबळे — ग्रामीण महिला",
        "note_en":  "Age 35 | Female | SC | Income Rs. 2,40,000 | Land 0 Ha | Laborer",
        "note_mr":  "वय ३५ | महिला | SC | उत्पन्न रु. २,४०,००० | जमीन ० हेक्टर | मजूर",
        "expected_en": "Eligible: Ladki Bahin, PMAY-G | Almost: Sanjay Gandhi",
        "expected_mr": "पात्र: लाडकी बहीण, पीएम आवास | जवळपास: संजय गांधी",
        "data": dict(name="Sunita Kamble", age=35, gender="female", annual_income=240000.0,
                     caste_category="sc", land_holding_hectares=0.0, occupation="laborer",
                     has_bank_account=True, has_aadhaar=True, owns_pucca_house=False),
    },
    "vikram": {
        "label_en": "Vikram Joshi — Urban Salaried",
        "label_mr": "विक्रम जोशी — शहरी नोकरदार",
        "note_en":  "Age 30 | Male | General | Income Rs. 6,00,000 | Land 0 Ha | Salaried | Pucca House",
        "note_mr":  "वय ३० | पुरुष | सर्वसाधारण | उत्पन्न रु. ६,००,००० | जमीन ० हेक्टर | नोकरदार | पक्के घर",
        "expected_en": "Edge Case — Mostly Ineligible",
        "expected_mr": "उच्च उत्पन्न — बहुतांश अपात्र",
        "data": dict(name="Vikram Joshi", age=30, gender="male", annual_income=600000.0,
                     caste_category="general", land_holding_hectares=0.0, occupation="salaried",
                     has_bank_account=True, has_aadhaar=True, owns_pucca_house=True),
    },
}

if "form_data" not in st.session_state:
    st.session_state["form_data"] = PRESETS["ramesh"]["data"].copy()

fd = st.session_state["form_data"]

# ─────────────────────────────────────────────────────────────────────────────
# GOVERNMENT TOP NAVIGATION BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="gov-topbar">
        <div style="display:flex; align-items:center; gap:14px;">
            <div style="width:36px;height:36px;background:#FFFFFF;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;font-size:18px;">
                &#127963;
            </div>
            <div>
                <div class="gov-portal-name">{t('portal_name')}</div>
                <div class="gov-portal-sub">{t('portal_sub')}</div>
            </div>
        </div>
        <div style="display:flex;gap:8px;">
            <span class="gov-badge">Deterministic Engine</span>
            <span class="gov-badge">Official Gazette Data</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN PAGE CONTENT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)

# ─── SECTION 1: DEMO PROFILES ────────────────────────────────────────────────
st.markdown(
    f"""
    <div style="background-color:#FFFFFF; border:1px solid #D1D5DB; border-radius:8px;
                padding:20px 24px; margin-bottom:16px;">
        <div style="display:flex; align-items:center; gap:10px;
                    border-bottom:1px solid #E5E7EB; padding-bottom:12px; margin-bottom:12px;">
            <div style="width:26px;height:26px;background:#1B3A6B;color:#FFFFFF;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;">
                1
            </div>
            <div style="font-size:15px;font-weight:700;color:#1B3A6B;">{t('demo_heading')}</div>
        </div>
        <p style="font-size:13px;color:#374151;margin:0;">{t('demo_caption')}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Render persona buttons OUTSIDE the HTML block (Streamlit widgets)
with st.container():
    pc1, pc2, pc3, pc4 = st.columns([2, 2, 2, 1])
    with pc1:
        p = PRESETS["ramesh"]
        lbl = p["label_mr"] if is_marathi else p["label_en"]
        note = p["note_mr"] if is_marathi else p["note_en"]
        exp  = p["expected_mr"] if is_marathi else p["expected_en"]
        if st.button(lbl, use_container_width=True, help=f"{note}\nExpected: {exp}"):
            st.session_state["form_data"] = p["data"].copy()
            st.rerun()
        st.caption(f"{note}")
        st.caption(f"Expected — {exp}")

    with pc2:
        p = PRESETS["sunita"]
        lbl = p["label_mr"] if is_marathi else p["label_en"]
        note = p["note_mr"] if is_marathi else p["note_en"]
        exp  = p["expected_mr"] if is_marathi else p["expected_en"]
        if st.button(lbl, use_container_width=True, help=f"{note}\nExpected: {exp}"):
            st.session_state["form_data"] = p["data"].copy()
            st.rerun()
        st.caption(f"{note}")
        st.caption(f"Expected — {exp}")

    with pc3:
        p = PRESETS["vikram"]
        lbl = p["label_mr"] if is_marathi else p["label_en"]
        note = p["note_mr"] if is_marathi else p["note_en"]
        exp  = p["expected_mr"] if is_marathi else p["expected_en"]
        if st.button(lbl, use_container_width=True, help=f"{note}\nExpected: {exp}"):
            st.session_state["form_data"] = p["data"].copy()
            st.rerun()
        st.caption(f"{note}")
        st.caption(f"Expected — {exp}")

    with pc4:
        st.write("")
        if st.button(t("reset"), use_container_width=True):
            st.session_state["form_data"] = dict(
                name="", age=30, gender="male", annual_income=100000.0,
                caste_category="general", land_holding_hectares=0.0,
                occupation="farmer", has_bank_account=True, has_aadhaar=True,
                owns_pucca_house=False
            )
            st.rerun()

# ─── SECTION 2: INTAKE FORM ──────────────────────────────────────────────────
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="background-color:#FFFFFF; border:1px solid #D1D5DB; border-radius:8px;
                padding:20px 24px 8px 24px; margin-bottom:4px;">
        <div style="display:flex; align-items:center; gap:10px;
                    border-bottom:1px solid #E5E7EB; padding-bottom:12px; margin-bottom:12px;">
            <div style="width:26px;height:26px;background:#1B3A6B;color:#FFFFFF;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;">
                2
            </div>
            <div style="font-size:15px;font-weight:700;color:#1B3A6B;">{t('form_heading')}</div>
        </div>
        <p style="font-size:12px;color:#6B7280;margin:0;">{t('form_caption')}</p>
    </div>
    """,
    unsafe_allow_html=True
)

fd = st.session_state["form_data"]

with st.form("citizen_intake_form"):

    # ── Personal Details ────────────────────────────────────────────────
    st.markdown(
        f"<div style='font-size:11px;font-weight:700;color:#1B3A6B;text-transform:uppercase;"
        f"letter-spacing:0.8px;padding:6px 0 10px 0;border-bottom:1.5px solid #E5E7EB;"
        f"margin-bottom:14px;background-color:transparent;'>{t('personal')}</div>",
        unsafe_allow_html=True
    )
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        name_val = st.text_input(t("name"), value=fd.get("name", ""), placeholder="e.g. Ramesh Patil")
    with r1c2:
        age_val = st.number_input(t("age"), min_value=0, max_value=120, value=int(fd.get("age", 30)), step=1)
    with r1c3:
        g_opts = ["male", "female", "other"]
        g_labels = {"male": "Male / पुरुष", "female": "Female / महिला", "other": "Other / इतर"}
        cur_g = fd.get("gender", "male")
        gender_val = st.selectbox(t("gender"), g_opts, index=g_opts.index(cur_g),
                                  format_func=lambda x: g_labels[x])

    # ── Economic & Agricultural Details ────────────────────────────────
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:11px;font-weight:700;color:#1B3A6B;text-transform:uppercase;"
        f"letter-spacing:0.8px;padding:6px 0 10px 0;border-bottom:1.5px solid #E5E7EB;"
        f"margin-bottom:14px;background-color:transparent;'>{t('economic')}</div>",
        unsafe_allow_html=True
    )
    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    with r2c1:
        income_val = st.number_input(t("income"), min_value=0.0, step=5000.0,
                                     value=float(fd.get("annual_income", 100000.0)), format="%.0f",
                                     help="Total annual income of the household from all sources")
        lakh = income_val / 100000.0
        st.caption(f"Rs. {income_val:,.0f}  ({lakh:.2f} Lakh / yr)")
    with r2c2:
        c_opts = ["general", "obc", "sc", "st", "nt", "vjnt"]
        cur_c = fd.get("caste_category", "general")
        caste_val = st.selectbox(t("caste"), c_opts, index=c_opts.index(cur_c),
                                 format_func=lambda x: x.upper())
    with r2c3:
        land_val = st.number_input(t("land"), min_value=0.0, step=0.1,
                                   value=float(fd.get("land_holding_hectares", 0.0)), format="%.2f",
                                   help="Agricultural land owned. 1 Ha = 2.47 Acres. Small farmer ceiling: 2.0 Ha")
        acres = land_val * 2.47105
        land_cat = "Small/Marginal (<= 2 Ha)" if land_val <= 2.0 else "Large Holder (> 2 Ha)"
        st.caption(f"{land_val:.2f} Ha = {acres:.2f} Acres — {land_cat}")
    with r2c4:
        o_opts = ["farmer", "laborer", "salaried", "self_employed", "unemployed"]
        o_labels = {
            "farmer":       "Farmer / शेतकरी",
            "laborer":      "Laborer / मजूर",
            "salaried":     "Salaried / नोकरदार",
            "self_employed":"Self-Employed / व्यावसायिक",
            "unemployed":   "Unemployed / बेरोजगार",
        }
        cur_o = fd.get("occupation", "farmer")
        occupation_val = st.selectbox(t("occupation"), o_opts, index=o_opts.index(cur_o),
                                      format_func=lambda x: o_labels[x])

    # ── Documentation & Asset Status ───────────────────────────────────
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:11px;font-weight:700;color:#1B3A6B;text-transform:uppercase;"
        f"letter-spacing:0.8px;padding:6px 0 10px 0;border-bottom:1.5px solid #E5E7EB;"
        f"margin-bottom:14px;background-color:transparent;'>{t('doc_status')}</div>",
        unsafe_allow_html=True
    )
    d1, d2, d3 = st.columns(3)
    with d1:
        bank_val = st.checkbox(t("bank"), value=bool(fd.get("has_bank_account", True)))
    with d2:
        aadhaar_val = st.checkbox(t("aadhaar"), value=bool(fd.get("has_aadhaar", True)))
    with d3:
        house_val = st.checkbox(t("house"), value=bool(fd.get("owns_pucca_house", False)))

    # ── Submit ──────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button(t("submit"), use_container_width=True, type="primary")

# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE — on submit
# ─────────────────────────────────────────────────────────────────────────────
if submitted:
    profile = CitizenProfile(
        name=name_val.strip() or "Applicant",
        age=int(age_val),
        gender=gender_val,
        annual_income=float(income_val),
        caste_category=caste_val,
        land_holding_hectares=float(land_val),
        occupation=occupation_val,
        state="Maharashtra",
        has_bank_account=bank_val,
        has_aadhaar=aadhaar_val,
        owns_pucca_house=house_val
    )
    render_sidebar(profile=profile, lang=lang)
    with st.spinner(t("spinner")):
        results = run_eligibility_pipeline(profile)
    render_results(results, lang=lang, profile=profile)
else:
    render_sidebar(profile=None, lang=lang)

st.markdown("</div>", unsafe_allow_html=True)  # close .page-wrapper
