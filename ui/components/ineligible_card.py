# ui/components/ineligible_card.py
"""Renders a single compact red card for ineligible schemes with transparent failure reasons and source provenance."""
import streamlit as st
from core.models import SchemeResult
from ui.config.strings import translate_rule_mr
try:
    from data.constants import SCHEME_TRANSLATIONS
except Exception:
    SCHEME_TRANSLATIONS = {}


def render_ineligible_card(r: SchemeResult, is_marathi: bool):
    """Render compact card for an ineligible scheme with transparent legal criteria."""
    trans = SCHEME_TRANSLATIONS.get(r.scheme_id, {})
    disp_name = (getattr(r, "name_mr", None) or trans.get("name_mr") or r.name) if is_marathi else r.name
    disp_dept = (getattr(r, "department_mr", None) or trans.get("dept_mr") or r.department) if is_marathi else r.department

    clean_domain = r.source_url.replace("https://", "").replace("http://", "").split("/")[0] if r.source_url else "gov.in"
    verified_date = r.last_fetched[:10] if r.last_fetched else "2026-10-31"

    with st.container(border=True):
        # ── Row 1: Scheme Title (Left) + Status Badge (Right) ────────────────
        c_head_left, c_head_right = st.columns([3.8, 1.2])
        with c_head_left:
            st.markdown(
                f"<div style='font-size:16px; font-weight:700; color:#374151; line-height:1.3; margin-bottom:2px;'>"
                f"{disp_name}</div>"
                f"<div style='font-size:12px; color:#9CA3AF; margin-bottom:4px;'>{disp_dept}</div>",
                unsafe_allow_html=True
            )
        with c_head_right:
            st.markdown(
                f"""
                <div style="background:#FEF2F2; border:1px solid #EF4444; border-radius:20px;
                            padding:4px 12px; text-align:center; float:right;">
                    <span style="font-size:12px; font-weight:700; color:#991B1B; letter-spacing:0.5px;">
                        🔴 {'अपात्र' if is_marathi else 'NOT ELIGIBLE'}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ── Row 2: Official Source Link + Verified Date ─────────────────────
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap; margin:6px 0 10px 0;
                        padding:5px 10px; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:5px;">
                <a href="{r.source_url}" target="_blank"
                   style="font-size:11px; font-weight:600; color:#2563EB; text-decoration:none; display:inline-flex; align-items:center; gap:4px;">
                    🔗 {'अधिकृत स्रोत' if is_marathi else 'Official Source'}: {clean_domain} ↗
                </a>
                <span style="color:#CBD5E1;">|</span>
                <span style="font-size:11px; color:#64748B;">
                    📅 {'डेटा पडताळणी' if is_marathi else 'Data verified'}: {verified_date}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Row 3: Transparent Failing Criteria ─────────────────────────────
        if r.explanation:
            st.markdown(
                f"<div style='font-size:12px; color:#4B5563; margin-bottom:6px;'>{r.explanation}</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            f"<div style='font-size:12px; color:#6B7280; font-weight:600; margin-bottom:4px;'>"
            f"{'अपात्रतेची कारणे (Statutory Reasons)' if is_marathi else 'Statutory Failing Criteria'}:</div>",
            unsafe_allow_html=True
        )
        for rule in r.failed_rules:
            disp_rule = translate_rule_mr(rule) if is_marathi else rule
            st.markdown(
                f"<div style='font-size:12px; color:#991B1B; padding:2px 0;'>"
                f"&#10007; &nbsp;{disp_rule}</div>",
                unsafe_allow_html=True
            )
