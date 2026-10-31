# ui/components/eligible_card.py
"""Renders a single green success card for an eligible welfare scheme."""
import streamlit as st
from core.models import SchemeResult
from ui.components.tts_button import render_tts_button


def render_eligible_card(r: SchemeResult, is_marathi: bool):
    """Render green result card for an eligible scheme."""
    tts_lang = "mr-IN" if is_marathi else "en-US"
    tts_label = "सुनावणी / Listen" if is_marathi else "Listen to Verdict"

    with st.container(border=True):
        c_left, c_right = st.columns([4, 1])

        with c_left:
            st.markdown(
                f"<div style='font-size:16px; font-weight:700; color:#1B3A6B; margin-bottom:2px;'>"
                f"{r.name}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='font-size:12px; color:#6B7280; margin-bottom:10px;'>"
                f"{r.department}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='background:#EFF6FF; border-left:3px solid #2563EB; "
                f"padding:8px 12px; border-radius:4px; font-size:13px; color:#1E40AF; margin-bottom:10px;'>"
                f"<strong>{'योजनेचा लाभ' if is_marathi else 'Scheme Benefit'}:</strong> {r.description}"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='font-size:13px; color:#111827; margin-bottom:10px;'>"
                f"<strong>{'पात्रतेचे कारण' if is_marathi else 'Eligibility Reason'}:</strong> {r.explanation}"
                f"</div>",
                unsafe_allow_html=True
            )
            render_tts_button(f"{r.name}. {r.explanation}", tts_lang, tts_label)

            with st.expander("पडताळलेले पात्र नियम" if is_marathi else "Verified Passing Conditions"):
                for rule in r.matched_rules:
                    st.markdown(
                        f"<div style='font-size:13px; color:#166534; padding:3px 0;'>"
                        f"&#10003; &nbsp;{rule}</div>",
                        unsafe_allow_html=True
                    )

        with c_right:
            st.markdown(
                f"""
                <div style="background:#F0FDF4; border:1.5px solid #16A34A; border-radius:8px;
                            padding:14px; text-align:center; height:100%;">
                    <div style="font-size:11px; font-weight:700; color:#15803D;
                                letter-spacing:0.8px; text-transform:uppercase; margin-bottom:8px;">
                        STATUS
                    </div>
                    <div style="font-size:18px; font-weight:800; color:#15803D; margin-bottom:14px;">
                        ELIGIBLE
                    </div>
                    <a href="{r.source_url}" target="_blank"
                       style="font-size:12px; color:#2563EB; font-weight:600; text-decoration:none;">
                        Official Portal &#8599;
                    </a><br>
                    <div style="font-size:11px; color:#9CA3AF; margin-top:8px;">
                        Data verified<br>{r.last_fetched[:10] if r.last_fetched else '2026-10-31'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
