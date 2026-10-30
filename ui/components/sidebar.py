# ui/components/sidebar.py
import streamlit as st
from core.models import CitizenProfile


def render_sidebar_summary(profile: CitizenProfile, lang: str):
    """Render the submitted citizen profile and live metadata in the sidebar."""
    with st.sidebar:
        st.divider()
        if lang == "मराठी":
            st.subheader("📋 अर्जदाराची प्रोफाइल")
            st.markdown(f"**नाव:** {profile.name}")
            st.markdown(f"**वय:** {profile.age} वर्षे")
            st.markdown(f"**लिंग:** {profile.gender}")
            st.markdown(f"**उत्पन्न:** ₹{profile.annual_income:,.0f}/वर्ष")
            st.markdown(f"**जात प्रवर्ग:** {profile.caste_category.upper()}")
            st.markdown(f"**जमीन:** {profile.land_holding_hectares} हेक्टर")
            st.markdown(f"**व्यवसाय:** {profile.occupation}")
        else:
            st.subheader("📋 Submitted Profile")
            st.markdown(f"**Name:** {profile.name}")
            st.markdown(f"**Age:** {profile.age} years")
            st.markdown(f"**Gender:** {profile.gender.title()}")
            st.markdown(f"**Annual Income:** ₹{profile.annual_income:,.0f}")
            st.markdown(f"**Caste Category:** {profile.caste_category.upper()}")
            st.markdown(f"**Land Holding:** {profile.land_holding_hectares} Ha")
            st.markdown(f"**Occupation:** {profile.occupation.replace('_', ' ').title()}")

        with st.expander("Raw Profile JSON"):
            st.json(profile.model_dump())
