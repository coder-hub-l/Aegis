# ui/components/ineligible_card.py
"""Renders a single compact red card for ineligible schemes with transparent failure reasons."""
import streamlit as st
from core.models import SchemeResult
try:
    from data.constants import SCHEME_TRANSLATIONS
except Exception:
    SCHEME_TRANSLATIONS = {}


def render_ineligible_card(r: SchemeResult, is_marathi: bool):
    """Render compact card for an ineligible scheme."""
    trans = SCHEME_TRANSLATIONS.get(r.scheme_id, {})
    disp_name = (getattr(r, "name_mr", None) or trans.get("name_mr") or r.name) if is_marathi else r.name
    disp_dept = (getattr(r, "department_mr", None) or trans.get("dept_mr") or r.department) if is_marathi else r.department

    with st.container(border=True):
        c_left, c_right = st.columns([3.8, 1.2])

        with c_left:
            st.markdown(
                f"<div style='font-size:14px; font-weight:700; color:#374151; margin-bottom:4px;'>"
                f"{disp_name}</div>"
                f"<div style='font-size:12px; color:#9CA3AF; margin-bottom:8px;'>{disp_dept}</div>",
                unsafe_allow_html=True
            )
            if r.explanation:
                st.caption(r.explanation)
            st.markdown(
                f"<div style='font-size:12px; color:#6B7280; font-weight:600; margin-bottom:4px;'>"
                f"{'अपात्रतेची कारणे' if is_marathi else 'Failing Criteria'}:</div>",
                unsafe_allow_html=True
            )
            for rule in r.failed_rules:
                st.markdown(
                    f"<div style='font-size:12px; color:#991B1B; padding:2px 0;'>"
                    f"&#10007; &nbsp;{rule}</div>",
                    unsafe_allow_html=True
                )

        with c_right:
            st.markdown(
                f"""
                <div style="background:#FEF2F2; border:1px solid #EF4444; border-radius:6px;
                            padding:8px 10px; text-align:center; min-height:40px; margin-top:4px;">
                    <div style="font-size:10px; font-weight:700; color:#991B1B; text-transform:uppercase;">
                        {'अपात्र' if is_marathi else 'INELIGIBLE'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
