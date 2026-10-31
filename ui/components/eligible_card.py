# ui/components/eligible_card.py
"""Renders a single green success card for an eligible welfare scheme."""
import streamlit as st
from core.models import SchemeResult
from ui.components.tts_button import render_tts_button
from data.constants import SCHEME_TRANSLATIONS


def render_eligible_card(r: SchemeResult, is_marathi: bool):
    """Render green result card for an eligible scheme."""
    tts_lang = "mr-IN" if is_marathi else "en-IN"
    tts_label = "सुनावणी" if is_marathi else "Listen"

    trans = SCHEME_TRANSLATIONS.get(r.scheme_id, {})
    disp_name = (getattr(r, "name_mr", None) or trans.get("name_mr") or r.name) if is_marathi else r.name
    disp_dept = (getattr(r, "department_mr", None) or trans.get("dept_mr") or r.department) if is_marathi else r.department
    disp_desc = (getattr(r, "description_mr", None) or trans.get("desc_mr") or r.description) if is_marathi else r.description
    disp_expl = (getattr(r, "explanation_mr", None) or trans.get("eligible_reason") or r.explanation) if is_marathi else (r.explanation or f"You meet all statutory requirements for {r.name}.")

    with st.container(border=True):
        c_left, c_right = st.columns([3.8, 1.2])

        with c_left:
            st.markdown(
                f"<div style='font-size:16px; font-weight:700; color:#1B3A6B; margin-bottom:2px;'>"
                f"{disp_name}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='font-size:12px; color:#6B7280; margin-bottom:10px;'>"
                f"{disp_dept}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='background:#EFF6FF; border-left:3px solid #2563EB; "
                f"padding:8px 12px; border-radius:4px; font-size:13px; color:#1E40AF; margin-bottom:10px;'>"
                f"<strong>{'योजनेचा लाभ' if is_marathi else 'Scheme Benefit'}:</strong> {disp_desc}"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='font-size:13px; color:#111827; margin-bottom:10px;'>"
                f"<strong>{'पात्रतेचे कारण' if is_marathi else 'Eligibility Reason'}:</strong> {disp_expl}"
                f"</div>",
                unsafe_allow_html=True
            )
            render_tts_button(f"{disp_name}. {disp_expl}", tts_lang, tts_label)

            with st.expander("पडताळलेले पात्र नियम" if is_marathi else "Verified Passing Conditions"):
                for rule in r.matched_rules:
                    st.markdown(
                        f"<div style='font-size:13px; color:#166534; padding:3px 0;'>"
                        f"&#10003; &nbsp;{rule}</div>",
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

        with c_right:
            st.markdown(
                f"""
                <div style="background:#F0FDF4; border:1.5px solid #16A34A; border-radius:8px;
                            padding:14px; text-align:center; min-height:90px; margin-top:4px;">
                    <div style="font-size:11px; font-weight:700; color:#15803D;
                                letter-spacing:0.8px; text-transform:uppercase; margin-bottom:6px;">
                        STATUS
                    </div>
                    <div style="font-size:18px; font-weight:800; color:#15803D; margin-bottom:10px;">
                        {'पात्र' if is_marathi else 'ELIGIBLE'}
                    </div>
                    <a href="{r.source_url}" target="_blank"
                       style="font-size:12px; color:#2563EB; font-weight:600; text-decoration:none;">
                        {'अधिकृत पोर्टल' if is_marathi else 'Official Portal'} &#8599;
                    </a><br>
                    <div style="font-size:11px; color:#9CA3AF; margin-top:8px;">
                        {'पडताळणी दिनांक' if is_marathi else 'Data verified'}<br>{r.last_fetched[:10] if r.last_fetched else '2026-10-31'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
