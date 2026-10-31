# ui/sections/preset_picker.py
"""Renders the Step 1 demo persona quick-load buttons and form reset."""
import streamlit as st
from ui.config.strings import t
from ui.config.presets import PRESETS, DEFAULT_FORM_DATA


def _inject_active_shadow(active_preset: str) -> None:
    """Inject a blue+grey box-shadow on whichever preset column is active."""
    col_index = {"ramesh": 1, "sunita": 2, "vikram": 3}.get(active_preset, 0)
    if not col_index:
        return
    st.markdown(
        f"""<style>
        [data-testid="stHorizontalBlock"]:first-of-type
        [data-testid="column"]:nth-child({col_index})
        .stButton > button {{
            box-shadow: 0 0 0 3px #1B3A6B,
                        0 4px 14px rgba(100, 116, 139, 0.40) !important;
        }}
        </style>""",
        unsafe_allow_html=True,
    )


def render_preset_picker(is_marathi: bool):
    """Render the preset buttons banner and click handlers."""
    active = st.session_state.get("active_preset")
    _inject_active_shadow(active)

    st.markdown(
        f"""
        <div style="background-color:#FFFFFF; border:1px solid #D1D5DB; border-radius:8px;
                    padding:20px 24px; margin-bottom:16px;">
            <div style="display:flex; align-items:center; gap:10px;
                        border-bottom:1px solid #E5E7EB; padding-bottom:12px; margin-bottom:12px;">
                <div style="width:26px;height:26px;background:#1B3A6B;color:#FFFFFF;border-radius:50%;
                            display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;">
                    1
                </div>
                <div style="font-size:15px;font-weight:700;color:#1B3A6B;">{t('demo_heading', is_marathi)}</div>
            </div>
            <p style="font-size:13px;color:#374151;margin:0;">{t('demo_caption', is_marathi)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pc1, pc2, pc3, pc4 = st.columns([2, 2, 2, 1])

    with pc1:
        p = PRESETS["ramesh"]
        lbl = p["label_mr"] if is_marathi else p["label_en"]
        note = p["note_mr"] if is_marathi else p["note_en"]
        exp = p["expected_mr"] if is_marathi else p["expected_en"]
        if st.button(lbl, use_container_width=True, help=f"{note}\nExpected: {exp}"):
            st.session_state["form_data"] = p["data"].copy()
            st.session_state["active_preset"] = "ramesh"
            st.rerun()
        st.caption(f"{note}")
        st.caption(f"Expected — {exp}")

    with pc2:
        p = PRESETS["sunita"]
        lbl = p["label_mr"] if is_marathi else p["label_en"]
        note = p["note_mr"] if is_marathi else p["note_en"]
        exp = p["expected_mr"] if is_marathi else p["expected_en"]
        if st.button(lbl, use_container_width=True, help=f"{note}\nExpected: {exp}"):
            st.session_state["form_data"] = p["data"].copy()
            st.session_state["active_preset"] = "sunita"
            st.rerun()
        st.caption(f"{note}")
        st.caption(f"Expected — {exp}")

    with pc3:
        p = PRESETS["vikram"]
        lbl = p["label_mr"] if is_marathi else p["label_en"]
        note = p["note_mr"] if is_marathi else p["note_en"]
        exp = p["expected_mr"] if is_marathi else p["expected_en"]
        if st.button(lbl, use_container_width=True, help=f"{note}\nExpected: {exp}"):
            st.session_state["form_data"] = p["data"].copy()
            st.session_state["active_preset"] = "vikram"
            st.rerun()
        st.caption(f"{note}")
        st.caption(f"Expected — {exp}")

    with pc4:
        st.write("")
        if st.button(t("reset", is_marathi), use_container_width=True):
            st.session_state["form_data"] = dict(
                name="", age=30, gender="male", annual_income=100000.0,
                caste_category="general", land_holding_hectares=0.0,
                occupation="farmer", has_bank_account=True, has_aadhaar=True,
                owns_pucca_house=False
            )
            st.session_state["active_preset"] = None
            st.rerun()
