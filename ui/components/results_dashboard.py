# ui/components/results_dashboard.py
"""Orchestrates the eligibility results view: metrics, filter, tabs, and cards."""
import streamlit as st
from typing import List, Optional
from core.models import SchemeResult, CitizenProfile
from ui.components.eligible_card import render_eligible_card
from ui.components.almost_card import render_almost_card
from ui.components.ineligible_card import render_ineligible_card
from ui.components.report_builder import build_text_report
from ui.components.whatsapp_sender import render_whatsapp_button


def render_results(results: List[SchemeResult], lang: str = "English", profile: Optional[CitizenProfile] = None):
    """Render the complete eligibility results dashboard."""
    is_marathi = (lang == "मराठी")

    eligible = [r for r in results if r.status == "eligible"]
    almost = [r for r in results if r.status == "almost"]
    ineligible = [r for r in results if r.status == "ineligible"]

    # ── Summary Metrics Bar ───────────────────────────────────────────────
    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Evaluated" if not is_marathi else "एकूण तपासलेल्या योजना", len(results))
    with m2:
        st.metric("Eligible Schemes" if not is_marathi else "पात्र योजना", len(eligible))
    with m3:
        st.metric("Almost Eligible" if not is_marathi else "जवळपास पात्र", len(almost),
                  delta="Near-Miss" if almost else None)
    with m4:
        st.metric("Ineligible" if not is_marathi else "अपात्र योजना", len(ineligible))

    # ── Search & Report Actions ───────────────────────────────────────────
    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    da, db, dc = st.columns([2.2, 1.2, 1.2])
    with da:
        search_q = st.text_input(
            "Filter by scheme name or department keyword",
            placeholder="e.g. kisan, bahin, awas, pension…",
            key="results_search"
        ).strip().lower()
    with db:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        report_txt = build_text_report(results, profile)
        st.download_button(
            label="Download Report" if not is_marathi else "अहवाल डाउनलोड करा",
            data=report_txt,
            file_name="maharashtra_eligibility_report.txt",
            mime="text/plain",
            use_container_width=True
        )
    with dc:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        render_whatsapp_button(results, profile, is_marathi)

    def matches_search(r):
        return not search_q or search_q in r.name.lower() or search_q in r.department.lower()

    f_elig = [r for r in eligible if matches_search(r)]
    f_alm = [r for r in almost if matches_search(r)]
    f_inel = [r for r in ineligible if matches_search(r)]

    # ── Categorized Tabs ──────────────────────────────────────────────────
    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs([
        f"Eligible ({len(f_elig)})" if not is_marathi else f"पात्र ({len(f_elig)})",
        f"Almost Eligible ({len(f_alm)})" if not is_marathi else f"जवळपास पात्र ({len(f_alm)})",
        f"Ineligible ({len(f_inel)})" if not is_marathi else f"अपात्र ({len(f_inel)})",
        "All Schemes" if not is_marathi else "सर्व योजना",
    ])

    with tab1:
        if f_elig:
            for r in f_elig:
                render_eligible_card(r, is_marathi)
        else:
            st.info("No eligible schemes for this profile.")

    with tab2:
        if f_alm:
            banner_text = (
                "<strong>Action Required —</strong> You are exactly 1 condition away from qualifying. Follow official steps below."
                if not is_marathi else
                "<strong>कृती आवश्यक —</strong> या योजनांसाठी फक्त एक अट अपूर्ण आहे. खालील सूचनांचे पालन करा."
            )
            st.markdown(
                f"<div style='background:#FFFBEB; border:1px solid #FDE68A; border-radius:6px; "
                f"padding:10px 14px; font-size:13px; color:#92400E; margin-bottom:16px;'>"
                f"{banner_text}</div>",
                unsafe_allow_html=True
            )
            for r in f_alm:
                render_almost_card(r, is_marathi)
        else:
            st.info("No near-miss schemes for this profile.")

    with tab3:
        if f_inel:
            st.caption("These schemes failed legal criteria." if not is_marathi
                       else "या योजनांसाठी शासकीय अटी पूर्ण झालेल्या नाहीत.")
            for r in f_inel:
                render_ineligible_card(r, is_marathi)
        else:
            st.info("No ineligible schemes.")

    with tab4:
        for r in results:
            if not matches_search(r):
                continue
            colour = {"eligible": "#15803D", "almost": "#B45309", "ineligible": "#991B1B"}[r.status]
            st.markdown(
                f"<div style='border:1px solid #E5E7EB; border-radius:6px; padding:12px 16px; "
                f"margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;'>"
                f"<div>"
                f"<div style='font-size:14px; font-weight:700; color:#1B3A6B;'>{r.name}</div>"
                f"<div style='font-size:12px; color:#6B7280;'>{r.department}</div>"
                f"<div style='font-size:12px; color:#374151; margin-top:4px;'>{r.description}</div>"
                f"</div>"
                f"<div style='text-align:right; min-width:100px;'>"
                f"<span style='background:{colour}22; color:{colour}; border:1px solid {colour}44; "
                f"padding:3px 10px; border-radius:12px; font-size:11px; font-weight:700; "
                f"text-transform:uppercase;'>{r.status}</span>"
                f"</div></div>",
                unsafe_allow_html=True
            )
