# ui/components/sidebar.py
"""Left sidebar: govt logo, controls, profile inspector, portals, architecture note."""
import streamlit as st
from pathlib import Path
from typing import Optional
from core.models import CitizenProfile
from data.constants import INCOME_CERTIFICATE_URL, AADHAAR_ENROLLMENT_URL, JAN_DHAN_URL

# Resolve logo relative to project root
_LOGO_PATH = Path(__file__).resolve().parent.parent.parent / "logo_MH.png"

# Voice language options — selected value stored in st.session_state["tts_lang"]
TTS_LANG_OPTIONS = {
    "English (en-IN)": "en-IN",
    "हिंदी (hi-IN)":   "hi-IN",
    "मराठी (mr-IN)":   "mr-IN",
}


def render_sidebar(profile: Optional[CitizenProfile] = None, lang: str = "English"):
    is_marathi = (lang == "मराठी")

    with st.sidebar:
        # ── Government Logo (always pinned top) ─────────────────────────
        if _LOGO_PATH.exists():
            st.image(str(_LOGO_PATH), width=80)
        st.markdown(
            """
            <div style="padding:6px 0 18px 0;
                        border-bottom:2px solid #E5E7EB; margin-bottom:16px;">
                <div style="font-size:15px; font-weight:800; color:#1B3A6B; line-height:1.3;">
                    महाराष्ट्र शासन
                </div>
                <div style="font-size:11px; color:#6B7280; font-weight:500; margin-top:2px;">
                    Government of Maharashtra
                </div>
                <div style="font-size:11px; color:#6B7280;">
                    Scheme Eligibility Navigator
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Voice Language Selector ──────────────────────────────────────
        st.markdown(
            f"<div style='font-size:11px; font-weight:700; color:#6B7280; "
            f"text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;'>"
            f"{'आवाज भाषा' if is_marathi else 'Voice Language'}</div>",
            unsafe_allow_html=True,
        )
        selected_label = st.selectbox(
            "Voice Language",
            options=list(TTS_LANG_OPTIONS.keys()),
            index=0,
            label_visibility="collapsed",
            key="tts_lang_label",
        )
        st.session_state["tts_lang"] = TTS_LANG_OPTIONS[selected_label]

        st.markdown(
            "<hr style='border:none; border-top:1px solid #E5E7EB; margin:14px 0;'>",
            unsafe_allow_html=True,
        )

        # ── Active Applicant Profile ─────────────────────────────────────
        if profile:
            st.markdown(
                f"<div style='font-size:11px; font-weight:700; color:#6B7280; "
                f"text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px;'>"
                f"{'सादर केलेले अर्जदार प्रोफाईल' if is_marathi else 'Active Applicant Profile'}"
                f"</div>",
                unsafe_allow_html=True,
            )
            rows = [
                ("Name"       if not is_marathi else "नाव",             profile.name),
                ("Age"        if not is_marathi else "वय",              f"{profile.age} years"),
                ("Gender"     if not is_marathi else "लिंग",            profile.gender.capitalize()),
                ("Income"     if not is_marathi else "वार्षिक उत्पन्न", f"Rs. {profile.annual_income:,.0f}"),
                ("Caste"      if not is_marathi else "जात",             profile.caste_category.upper()),
                ("Land"       if not is_marathi else "जमीन",            f"{profile.land_holding_hectares} Ha"),
                ("Occupation" if not is_marathi else "व्यवसाय",
                 profile.occupation.replace("_", " ").capitalize()),
            ]
            table_rows = "".join(
                f"<tr>"
                f"<td style='font-size:12px; color:#6B7280; font-weight:600; "
                f"padding:5px 8px 5px 0; white-space:nowrap;'>{k}</td>"
                f"<td style='font-size:12px; color:#111827; padding:5px 0;'>{v}</td>"
                f"</tr>"
                for k, v in rows
            )
            st.markdown(
                f"<table style='border-collapse:collapse; width:100%;'>{table_rows}</table>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<hr style='border:none; border-top:1px solid #E5E7EB; margin:14px 0;'>",
                unsafe_allow_html=True,
            )

        # ── Official Portals ─────────────────────────────────────────────
        st.markdown(
            f"<div style='font-size:11px; font-weight:700; color:#6B7280; "
            f"text-transform:uppercase; letter-spacing:0.8px; margin-bottom:10px;'>"
            f"{'अधिकृत सरकारी पोर्टल्स' if is_marathi else 'Official Government Portals'}"
            f"</div>",
            unsafe_allow_html=True,
        )
        portals = [
            ("MahaDBT — Scheme Applications", "https://mahadbt.maharashtra.gov.in"),
            ("Aaple Sarkar — Certificates",   INCOME_CERTIFICATE_URL),
            ("UIDAI — Aadhaar Enrolment",     AADHAAR_ENROLLMENT_URL),
            ("PM Jan Dhan — Bank Accounts",   JAN_DHAN_URL),
            ("PM-KISAN Official Portal",      "https://pmkisan.gov.in"),
        ]
        for label, url in portals:
            st.markdown(
                f"<div style='padding:6px 0; border-bottom:1px solid #F3F4F6;'>"
                f"<a href='{url}' target='_blank' style='font-size:12px; color:#2563EB; "
                f"font-weight:600; text-decoration:none;'>{label} &#8599;</a>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<hr style='border:none; border-top:1px solid #E5E7EB; margin:14px 0;'>",
            unsafe_allow_html=True,
        )

        # ── Technical Architecture Note ──────────────────────────────────
        with st.expander("System Architecture" if not is_marathi else "प्रणाली रचना"):
            st.markdown(
                """
                <div style="font-size:12px; color:#374151; line-height:1.7;">
                    <strong style="color:#1B3A6B;">Deterministic Rule Engine</strong><br>
                    All eligibility decisions are executed in pure Python based on
                    verified Maharashtra gazette conditions.
                    <br><br>
                    <strong style="color:#1B3A6B;">Zero LLM Hallucination</strong><br>
                    The AI model never decides eligibility. It only translates the
                    engine's binary verdict into plain-language explanations and
                    actionable remediation advice.
                </div>
                """,
                unsafe_allow_html=True,
            )
