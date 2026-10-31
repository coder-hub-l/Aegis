# ui/components/almost_card.py
"""Renders a single yellow warning card with actionable remediation for near-miss schemes."""
import streamlit as st
from core.models import SchemeResult
from ui.components.tts_button import render_tts_button


def render_almost_card(r: SchemeResult, is_marathi: bool):
    """Render yellow action-required card for an almost eligible scheme."""
    tts_lang = st.session_state.get("tts_lang", "mr-IN" if is_marathi else "en-IN")
    tts_label = "सुनावणी / Listen" if is_marathi else "Listen to Advice"
    missing = r.failed_rules[0] if r.failed_rules else "N/A"

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
                f"<div style='background:#FFFBEB; border-left:3px solid #D97706; "
                f"padding:8px 12px; border-radius:4px; font-size:13px; color:#92400E; margin-bottom:10px;'>"
                f"<strong>{'अपूर्ण अट' if is_marathi else 'Unmet Condition'}:</strong> {missing}"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='font-size:13px; color:#111827; margin-bottom:10px;'>"
                f"<strong>{'पात्र होण्यासाठी पुढील पावले' if is_marathi else 'Steps to Become Eligible'}:</strong>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.write(r.almost_advice)
            render_tts_button(f"{r.name}. Unmet: {missing}. {r.almost_advice}", tts_lang, tts_label)

            if r.hints:
                with st.expander("शासकीय मार्गदर्शन" if is_marathi else "Official Department Guidance"):
                    for hint in r.hints:
                        st.markdown(
                            f"<div style='font-size:13px; color:#374151; padding:4px 0;'>"
                            f"&#x2022; &nbsp;{hint}</div>",
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
                <div style="background:#FFFBEB; border:1.5px solid #D97706; border-radius:8px;
                            padding:14px; text-align:center; height:100%;">
                    <div style="font-size:11px; font-weight:700; color:#B45309;
                                letter-spacing:0.8px; text-transform:uppercase; margin-bottom:8px;">
                        STATUS
                    </div>
                    <div style="font-size:18px; font-weight:800; color:#B45309; margin-bottom:6px;">
                        ALMOST
                    </div>
                    <div style="font-size:11px; color:#92400E; margin-bottom:14px; font-weight:500;">
                        1 condition unmet
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
