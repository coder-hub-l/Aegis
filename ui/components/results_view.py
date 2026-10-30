# ui/components/results_view.py
import streamlit as st
from typing import List
from core.models import SchemeResult


def render_results(results: List[SchemeResult], lang: str = "English"):
    """Render the three-section eligibility results dashboard."""

    eligible = [r for r in results if r.status == "eligible"]
    almost = [r for r in results if r.status == "almost"]
    ineligible = [r for r in results if r.status == "ineligible"]

    # Section 1: Eligible
    st.divider()
    if lang == "मराठी":
        st.subheader(f"✅ पात्र योजना ({len(eligible)})")
    else:
        st.subheader(f"✅ Fully Eligible Schemes ({len(eligible)})")

    if eligible:
        for r in eligible:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {r.name}")
                    st.caption(f"🏛️ {r.department}")
                    st.info(r.description)
                    st.markdown(f"**{'पात्रतेचे कारण' if lang == 'मराठी' else 'Why you qualify'}:** {r.explanation}")
                    with st.expander("पडताळणी केलेल्या अटी" if lang == "मराठी" else "Verified passing conditions"):
                        for rule in r.matched_rules:
                            st.markdown(f"- ✓ {rule}")
                with col2:
                    st.success("ELIGIBLE / पात्र")
                    if r.source_url:
                        st.markdown(f"[अधिकृत पोर्टल ↗]({r.source_url})" if lang == "मराठी" else f"[Official Portal ↗]({r.source_url})")
                    st.caption(f"Verified: {r.last_fetched[:10] if r.last_fetched else 'Active'}")
    else:
        st.info("या प्रोफाईलसाठी सर्व अटी पूर्ण करणारी कोणतीही योजना आढळली नाही." if lang == "मराठी" else "No schemes matched 100% of the statutory criteria for this profile.")

    # Section 2: Almost Eligible
    st.divider()
    if lang == "मराठी":
        st.subheader(f"🟡 जवळपास पात्र — कृती आवश्यक ({len(almost)})")
    else:
        st.subheader(f"🟡 Almost Eligible — Action Required ({len(almost)})")

    if almost:
        for r in almost:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {r.name}")
                    st.caption(f"🏛️ {r.department}")
                    st.warning(f"**{'एक अट अपूर्ण' if lang == 'मराठी' else 'Missing one condition'}:** {r.failed_rules[0] if r.failed_rules else ''}")
                    if r.almost_advice:
                        st.markdown(f"**{'पात्र होण्यासाठी काय करावे' if lang == 'मराठी' else 'What to do to qualify'}:** {r.almost_advice}")
                    if r.hints:
                        with st.expander("शासकीय मार्गदर्शन" if lang == "मराठी" else "Official Guidance & Remedy"):
                            for hint in r.hints:
                                st.markdown(f"- 💡 {hint}")
                with col2:
                    st.warning("ALMOST / जवळपास")
                    if r.source_url:
                        st.markdown(f"[अधिकृत पोर्टल ↗]({r.source_url})" if lang == "मराठी" else f"[Official Portal ↗]({r.source_url})")
                    st.caption(f"Verified: {r.last_fetched[:10] if r.last_fetched else 'Active'}")
    else:
        st.info("या प्रोफाईलसाठी कोणतीही जवळपास पात्र योजना नाही." if lang == "मराठी" else "No near-miss schemes found for this profile.")

    # Section 3: Ineligible
    st.divider()
    ineligible_label = f"❌ अपात्र योजना ({len(ineligible)}) — पाहण्यासाठी क्लिक करा" if lang == "मराठी" else f"❌ Ineligible Schemes ({len(ineligible)}) — Click to Expand"
    with st.expander(ineligible_label):
        for r in ineligible:
            with st.container(border=True):
                st.markdown(f"**{r.name}**")
                st.caption(f"🏛️ {r.department}")
                st.markdown(f"*{r.explanation}*")
                for rule in r.failed_rules:
                    st.markdown(f"  - ✗ {rule}")
