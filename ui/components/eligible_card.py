# ui/components/eligible_card.py
"""Renders a single green success card for an eligible welfare scheme with prominent official source and status."""
import streamlit as st
from core.models import SchemeResult
from ui.components.tts_button import render_tts_button
from ui.config.strings import translate_rule_mr
try:
    from data.constants import SCHEME_TRANSLATIONS
except Exception:
    SCHEME_TRANSLATIONS = {}


def render_eligible_card(r: SchemeResult, is_marathi: bool):
    """Render green result card for an eligible scheme with optimal eye-flow."""
    tts_lang = "mr-IN" if is_marathi else "en-IN"
    tts_label = "सुनावणी" if is_marathi else "Listen"

    trans = SCHEME_TRANSLATIONS.get(r.scheme_id, {})
    disp_name = (getattr(r, "name_mr", None) or trans.get("name_mr") or r.name) if is_marathi else r.name
    disp_dept = (getattr(r, "department_mr", None) or trans.get("dept_mr") or r.department) if is_marathi else r.department
    disp_desc = (getattr(r, "description_mr", None) or trans.get("desc_mr") or r.description) if is_marathi else r.description
    disp_expl = (getattr(r, "explanation_mr", None) or trans.get("eligible_reason") or r.explanation) if is_marathi else (r.explanation or f"You meet all statutory requirements for {r.name}.")

    clean_domain = r.source_url.replace("https://", "").replace("http://", "").split("/")[0] if r.source_url else "gov.in"
    verified_date = r.last_fetched[:10] if r.last_fetched else "2026-10-31"

    with st.container(border=True):
        # ── Row 1: Scheme Title (Left) + Status Badge (Right) ────────────────
        c_head_left, c_head_right = st.columns([3.8, 1.2])
        with c_head_left:
            st.markdown(
                f"<div style='font-size:18px; font-weight:700; color:#1B3A6B; line-height:1.3; margin-bottom:2px;'>"
                f"{disp_name}</div>"
                f"<div style='font-size:12px; color:#6B7280; margin-bottom:4px;'>{disp_dept}</div>",
                unsafe_allow_html=True
            )
        with c_head_right:
            st.markdown(
                f"""
                <div style="background:#F0FDF4; border:1.5px solid #16A34A; border-radius:20px;
                            padding:6px 14px; text-align:center; float:right;">
                    <span style="font-size:13px; font-weight:800; color:#15803D; letter-spacing:0.5px;">
                        🟢 {'पात्र' if is_marathi else 'ELIGIBLE'}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ── Row 2: Official Source Link + Verified Date ─────────────────────
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap; margin:6px 0 12px 0;
                        padding:7px 12px; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:6px;">
                <a href="{r.source_url}" target="_blank"
                   style="font-size:12px; font-weight:700; color:#1D4ED8; text-decoration:none; display:inline-flex; align-items:center; gap:5px;">
                    🔗 {'अधिकृत स्रोत' if is_marathi else 'Official Source'}: {clean_domain} ↗
                </a>
                <span style="color:#CBD5E1;">|</span>
                <span style="font-size:12px; color:#64748B;">
                    📅 {'डेटा पडताळणी' if is_marathi else 'Data verified'}: {verified_date}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Row 3: Benefit Description ──────────────────────────────────────
        st.markdown(
            f"<div style='background:#EFF6FF; border-left:3.5px solid #2563EB; "
            f"padding:10px 14px; border-radius:4px; font-size:13px; color:#1E40AF; margin-bottom:12px;'>"
            f"<strong>{'योजनेचा लाभ' if is_marathi else 'Scheme Benefit'}:</strong> {disp_desc}"
            f"</div>",
            unsafe_allow_html=True
        )

        # ── Row 4: Reason & Voice Player ────────────────────────────────────
        st.markdown(
            f"<div style='font-size:13px; color:#111827; margin-bottom:12px; line-height:1.5;'>"
            f"<strong>{'पात्रतेचे कारण' if is_marathi else 'Why You Qualify'}:</strong> {disp_expl}"
            f"</div>",
            unsafe_allow_html=True
        )
        render_tts_button(f"{disp_name}. {disp_expl}", tts_lang, tts_label)

        # ── Row 5: Expanders ────────────────────────────────────────────────
        with st.expander("पडताळलेले पात्र नियम" if is_marathi else "Verified Passing Conditions"):
            for rule in r.matched_rules:
                disp_rule = translate_rule_mr(rule) if is_marathi else rule
                st.markdown(
                    f"<div style='font-size:13px; color:#166534; padding:3px 0;'>"
                    f"&#10003; &nbsp;{disp_rule}</div>",
                    unsafe_allow_html=True
                )

        if r.exclusions:
            with st.expander("बाबू शील्ड — शासकीय अपवाद संरक्षण" if is_marathi else "Babu Shield — Statutory Immunity Checklist"):
                st.markdown(
                    f"<div style='font-size:12px; color:#4B5563; margin-bottom:6px;'>"
                    f"{'शासकीय नियमांनुसार अधिकारी खालील अपवाद नसताना तुमचा अर्ज नाकारू शकत नाहीत:' if is_marathi else 'Verifying officers cannot reject your application unless you fall under one of these official exclusions:'}"
                    f"</div>",
                    unsafe_allow_html=True
                )
                for exc in r.exclusions:
                    st.markdown(
                        f"<div style='font-size:12px; color:#374151; padding:2px 0;'>"
                        f"&bull; &nbsp;{exc}</div>",
                        unsafe_allow_html=True
                    )
