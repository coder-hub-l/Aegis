# ui/components/whatsapp_sender.py
"""Builds and renders the WhatsApp Seva Pass deep-link button."""
import urllib.parse
from datetime import datetime
from typing import List, Optional
import streamlit as st
from core.models import SchemeResult, CitizenProfile


def build_whatsapp_message(
    results: List[SchemeResult],
    profile: Optional[CitizenProfile] = None,
    is_marathi: bool = False
) -> str:
    """Generate concise text payload for WhatsApp sharing."""
    applicant_name = profile.name if profile and profile.name else ("नागरिक" if is_marathi else "Citizen")
    today = datetime.now().strftime("%d-%m-%Y")

    eligible = [r for r in results if r.status == "eligible"]
    almost = [r for r in results if r.status == "almost"]

    if is_marathi:
        lines = [
            "*महाराष्ट्र शासन कल्याणकारी योजना - अहवाल (Aegis)*",
            f"अर्जदार: {applicant_name}",
            f"दिनांक: {today}",
            "--------------------------------",
        ]
        if eligible:
            lines.append(f"\n*पात्र योजना ({len(eligible)})*:")
            for idx, r in enumerate(eligible, 1):
                lines.append(f"{idx}. *{r.name}*")
                lines.append(f"   विभाग: {r.department}")
                lines.append(f"   अधिकृत पोर्टल: {r.source_url}")
        if almost:
            lines.append(f"\n*जवळपास पात्र योजना ({len(almost)})*:")
            for idx, r in enumerate(almost, 1):
                missing = r.failed_rules[0] if r.failed_rules else "आवश्यक कागदपत्र"
                lines.append(f"{idx}. *{r.name}*")
                lines.append(f"   अपूर्ण अट: {missing}")
                if r.almost_advice:
                    lines.append(f"   पुढील पाऊल: {r.almost_advice[:120]}...")
        lines.append("\n_Aegis Maharashtra Welfare Navigator द्वारे जनरेट केलेले_")
    else:
        lines = [
            "*Govt of Maharashtra Welfare Eligibility - Aegis Seva Pass*",
            f"Applicant: {applicant_name}",
            f"Date: {today}",
            "--------------------------------",
        ]
        if eligible:
            lines.append(f"\n*Eligible Schemes ({len(eligible)})*:")
            for idx, r in enumerate(eligible, 1):
                lines.append(f"{idx}. *{r.name}*")
                lines.append(f"   Department: {r.department}")
                lines.append(f"   Official Portal: {r.source_url}")
        if almost:
            lines.append(f"\n*Almost Eligible Schemes ({len(almost)})*:")
            for idx, r in enumerate(almost, 1):
                missing = r.failed_rules[0] if r.failed_rules else "Pending Verification"
                lines.append(f"{idx}. *{r.name}*")
                lines.append(f"   Pending: {missing}")
                if r.almost_advice:
                    lines.append(f"   Next Step: {r.almost_advice[:120]}...")
        lines.append("\n_Generated via Aegis Maharashtra Welfare Navigator_")

    return "\n".join(lines)


def get_whatsapp_share_url(
    results: List[SchemeResult],
    profile: Optional[CitizenProfile] = None,
    is_marathi: bool = False
) -> str:
    """Encode message into wa.me sharing URL."""
    raw_msg = build_whatsapp_message(results, profile, is_marathi)
    encoded = urllib.parse.quote(raw_msg)
    return f"https://wa.me/?text={encoded}"


def render_whatsapp_button(
    results: List[SchemeResult],
    profile: Optional[CitizenProfile] = None,
    is_marathi: bool = False
) -> None:
    """Render WhatsApp deep-link button using st.link_button."""
    url = get_whatsapp_share_url(results, profile, is_marathi)
    label = "व्हॉट्सॲपवर पाठवा" if is_marathi else "Share via WhatsApp"
    st.link_button(label=label, url=url, use_container_width=True)
