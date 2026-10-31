# ui/sections/topbar.py
"""Renders the official Government of Maharashtra header topbar."""
import streamlit as st
from ui.config.strings import t


def render_topbar(is_marathi: bool):
    """Render the top government navigation bar."""
    st.markdown(
        f"""
        <div class="gov-topbar">
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="width:34px;height:34px;background:#FFFFFF;border-radius:50%;
                            display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="#1B3A6B">
                        <path d="M12 2L2 7V9H22V7L12 2ZM4 11V19H7V11H4ZM10 11V19H14V11H10ZM17 11V19H20V11H17ZM2 20V22H22V20H2Z"/>
                    </svg>
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
