# ui/sections/topbar.py
"""Renders the official Government of Maharashtra header topbar."""
import streamlit as st
from ui.config.strings import t


def render_topbar(is_marathi: bool):
    """Render the top government navigation bar."""
    st.markdown(
        f"""
        <div class="gov-topbar">
            <div style="display:flex; align-items:center; gap:14px;">
                <div style="width:36px;height:36px;background:#FFFFFF;border-radius:50%;
                            display:flex;align-items:center;justify-content:center;font-size:18px;">
                    &#127963;
                </div>
                <div>
                    <div class="gov-portal-name">{t('portal_name', is_marathi)}</div>
                    <div class="gov-portal-sub">{t('portal_sub', is_marathi)}</div>
                </div>
            </div>
            <div style="display:flex;gap:8px;">
                <span class="gov-badge">Deterministic Engine</span>
                <span class="gov-badge">Official Gazette Data</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
