# ui/sections/intake_form.py
"""Renders the Step 2 citizen eligibility intake form and returns validated inputs."""
import streamlit as st
from core.models import CitizenProfile
from ui.config.strings import t, GENDER_LABELS, OCCUPATION_LABELS
from data.constants import CASTE_CATEGORIES, OCCUPATIONS, GENDERS


def render_intake_form(is_marathi: bool):
    """
    Render the 3-section form (personal, economic, doc status).
    Returns (submitted: bool, profile: Optional[CitizenProfile]).
    """
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
                <div style="font-size:15px;font-weight:700;color:#1B3A6B;">{t('form_heading', is_marathi)}</div>
            </div>
            <p style="font-size:12px;color:#6B7280;margin:0;">{t('form_caption', is_marathi)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    fd = st.session_state.get("form_data", {})

    with st.form("citizen_intake_form"):
        # ── Personal Details ────────────────────────────────────────────
        st.markdown(
            f"<div class='form-section-label'>{t('personal', is_marathi)}</div>",
            unsafe_allow_html=True
        )
        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            name_val = st.text_input(t("name", is_marathi), value=fd.get("name", ""), placeholder="e.g. Ramesh Patil")
        with r1c2:
            age_val = st.number_input(t("age", is_marathi), min_value=0, max_value=120, value=int(fd.get("age", 30)), step=1)
        with r1c3:
            cur_g = fd.get("gender", "male")
            cur_g_idx = GENDERS.index(cur_g) if cur_g in GENDERS else 0
            gender_val = st.selectbox(
                t("gender", is_marathi), GENDERS, index=cur_g_idx,
                format_func=lambda x: GENDER_LABELS.get(x, (x, x))[0]
            )

        # ── Economic & Agricultural Details ────────────────────────────
        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='form-section-label'>{t('economic', is_marathi)}</div>",
            unsafe_allow_html=True
        )
        r2c1, r2c2, r2c3, r2c4 = st.columns(4)
        with r2c1:
            income_val = st.number_input(
                t("income", is_marathi), min_value=0.0, step=5000.0,
                value=float(fd.get("annual_income", 100000.0)), format="%.0f",
                help="Total annual household income from all sources"
            )
            lakh = income_val / 100000.0
            st.caption(f"Rs. {income_val:,.0f}  ({lakh:.2f} Lakh / yr)")
        with r2c2:
            cur_c = fd.get("caste_category", "general")
            cur_c_idx = CASTE_CATEGORIES.index(cur_c) if cur_c in CASTE_CATEGORIES else 0
            caste_val = st.selectbox(
                t("caste", is_marathi), CASTE_CATEGORIES, index=cur_c_idx,
                format_func=lambda x: x.upper()
            )
        with r2c3:
            land_val = st.number_input(
                t("land", is_marathi), min_value=0.0, step=0.1,
                value=float(fd.get("land_holding_hectares", 0.0)), format="%.2f",
                help="Agricultural land owned. 1 Ha = 2.47 Acres."
            )
            acres = land_val * 2.47105
            land_cat = "Small/Marginal (<= 2 Ha)" if land_val <= 2.0 else "Large Holder (> 2 Ha)"
            st.caption(f"{land_val:.2f} Ha = {acres:.2f} Acres — {land_cat}")
        with r2c4:
            cur_o = fd.get("occupation", "farmer")
            cur_o_idx = OCCUPATIONS.index(cur_o) if cur_o in OCCUPATIONS else 0
            occupation_val = st.selectbox(
                t("occupation", is_marathi), OCCUPATIONS, index=cur_o_idx,
                format_func=lambda x: OCCUPATION_LABELS.get(x, (x, x))[0]
            )

        # ── Documentation & Asset Status ───────────────────────────────
        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='form-section-label'>{t('doc_status', is_marathi)}</div>",
            unsafe_allow_html=True
        )
        d1, d2, d3 = st.columns(3)
        with d1:
            bank_val = st.checkbox(t("bank", is_marathi), value=bool(fd.get("has_bank_account", True)))
        with d2:
            aadhaar_val = st.checkbox(t("aadhaar", is_marathi), value=bool(fd.get("has_aadhaar", True)))
        with d3:
            house_val = st.checkbox(t("house", is_marathi), value=bool(fd.get("owns_pucca_house", False)))

        # ── Submit ──────────────────────────────────────────────────────
        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button(t("submit", is_marathi), use_container_width=True, type="primary")

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
        return True, profile
    return False, None
