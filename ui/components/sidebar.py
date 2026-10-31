# ui/components/sidebar.py
"""Left sidebar: govt logo pinned at top, unified language, dark mode, portals, profile."""
import streamlit as st
from pathlib import Path
from typing import Optional, Tuple, Any
from core.models import CitizenProfile
from data.constants import INCOME_CERTIFICATE_URL, AADHAAR_ENROLLMENT_URL, JAN_DHAN_URL

# Resolve official Maharashtra seal logo relative to project root
_LOGO_PATH = Path(__file__).resolve().parent.parent.parent / "logo_MH.png"


def _safe_get(obj: Any, key: str, default: Any = "") -> Any:
    """Safely extract field from either a Pydantic model or a dictionary."""
    if hasattr(obj, key):
        val = getattr(obj, key)
        return val if val is not None else default
    elif isinstance(obj, dict):
        return obj.get(key, default)
    return default


def render_sidebar(profile: Optional[CitizenProfile] = None) -> Tuple[str, bool, bool]:
    """
    Renders the unified left sidebar in strict authoritative order:
    1. Maharashtra Government Seal
    2. Header Title
    3. Single Unified Language Selector (controls page text AND voice language)
    4. Dark Mode Toggle
    5. Active Applicant Profile (when available)
    6. Official Portals
    7. System Architecture Note
    
    Returns:
        (lang, is_marathi, dark_mode)
    """
    # Safe fallback defaults
    lang = st.session_state.get("unified_app_lang", "English")
    is_marathi = (lang == "मराठी")
    dark_mode = st.session_state.get("unified_dark_mode", False)

    with st.sidebar:
        # ── 1. Government Seal Logo (Pinned at top) ──────────────────────
        if _LOGO_PATH.exists():
            st.image(str(_LOGO_PATH), width=75)

        # ── 2. Header Title ──────────────────────────────────────────────
        st.markdown(
            """
            <div style="padding:4px 0 14px 0; border-bottom:2px solid #E5E7EB; margin-bottom:14px;">
                <div style="font-size:15px; font-weight:800; color:#1B3A6B; line-height:1.3;">
                    महाराष्ट्र शासन
                </div>
                <div style="font-size:11px; color:#6B7280; font-weight:600; margin-top:2px;">
                    Government of Maharashtra
                </div>
                <div style="font-size:11px; color:#6B7280;">
                    Scheme Eligibility Navigator
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── 3. Unified Language Selector (Page + Voice) ──────────────────
        lang = st.radio(
            "Language / भाषा",
            ["English", "मराठी"],
            index=0,
            key="unified_app_lang"
        )
        is_marathi = (lang == "मराठी")

        # ── 4. Dark Mode Toggle ──────────────────────────────────────────
        dark_mode = st.toggle(
            "Dark Mode" if not is_marathi else "डार्क मोड",
            value=False,
            key="unified_dark_mode"
        )

        st.markdown(
            "<hr style='border:none; border-top:1px solid #E5E7EB; margin:14px 0;'>",
            unsafe_allow_html=True,
        )

        # ── 5. Active Applicant Profile (Rendered when submitted) ────────
        if profile:
            st.markdown(
                f"<div style='font-size:11px; font-weight:700; color:#6B7280; "
                f"text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px;'>"
                f"{'सादर केलेले अर्जदार प्रोफाईल' if is_marathi else 'Active Applicant Profile'}"
                f"</div>",
                unsafe_allow_html=True,
            )
            p_name = _safe_get(profile, "name", "Applicant")
            p_age = _safe_get(profile, "age", 30)
            p_gender = str(_safe_get(profile, "gender", "other")).capitalize()
            p_income = _safe_get(profile, "annual_income", 0)
            p_caste = str(_safe_get(profile, "caste_category", "general")).upper()
            p_land = _safe_get(profile, "land_holding_hectares", 0.0)
            p_occ = str(_safe_get(profile, "occupation", "farmer")).replace("_", " ").capitalize()

            rows = [
                ("Name"       if not is_marathi else "नाव",             p_name),
                ("Age"        if not is_marathi else "वय",              f"{p_age} years" if not is_marathi else f"{p_age} वर्षे"),
                ("Gender"     if not is_marathi else "लिंग",            p_gender),
                ("Income"     if not is_marathi else "वार्षिक उत्पन्न", f"Rs. {float(p_income):,.0f}"),
                ("Caste"      if not is_marathi else "जात",             p_caste),
                ("Land"       if not is_marathi else "जमीन",            f"{p_land} Ha"),
                ("Occupation" if not is_marathi else "व्यवसाय",         p_occ),
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

        # ── 6. Official Portals ──────────────────────────────────────────
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

        # ── 7. Technical Architecture Note ───────────────────────────────
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

    return (lang, is_marathi, dark_mode)
