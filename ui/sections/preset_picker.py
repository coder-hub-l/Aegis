# ui/sections/preset_picker.py
"""Renders the optional demo persona quick-load buttons inside an expander with distinct blue shades."""
import streamlit as st
from ui.config.strings import t
from ui.config.presets import PRESETS, DEFAULT_FORM_DATA


def _inject_preset_styles(active_preset: str) -> None:
    """Inject 3 distinct shades of blue for the preset buttons and active indicator."""
    active_col = {"ramesh": 1, "sunita": 2, "vikram": 3}.get(active_preset, 0)

    shadow_rule = ""
    if active_col == 1:
        shadow_rule = """
        [data-testid="stExpander"] [data-testid="column"]:nth-child(1) .stButton > button {
            box-shadow: 0 0 0 3px #1E3A8A, 0 4px 14px rgba(30, 58, 138, 0.40) !important;
            background-color: #EFF6FF !important;
            font-weight: 700 !important;
        }
        """
    elif active_col == 2:
        shadow_rule = """
        [data-testid="stExpander"] [data-testid="column"]:nth-child(2) .stButton > button {
            box-shadow: 0 0 0 3px #2563EB, 0 4px 14px rgba(37, 99, 235, 0.40) !important;
            background-color: #EFF6FF !important;
            font-weight: 700 !important;
        }
        """
    elif active_col == 3:
        shadow_rule = """
        [data-testid="stExpander"] [data-testid="column"]:nth-child(3) .stButton > button {
            box-shadow: 0 0 0 3px #0284C7, 0 4px 14px rgba(2, 132, 199, 0.40) !important;
            background-color: #F0F9FF !important;
            font-weight: 700 !important;
        }
        """

    st.markdown(
        f"""<style>
        /* Preset 1: Ramesh Patil - Deep Navy Blue */
        [data-testid="stExpander"] [data-testid="column"]:nth-child(1) .stButton > button {{
            border: 2px solid #1E3A8A !important;
            color: #1E3A8A !important;
            background-color: #FFFFFF !important;
        }}
        [data-testid="stExpander"] [data-testid="column"]:nth-child(1) .stButton > button:hover {{
            background-color: #1E3A8A !important;
            color: #FFFFFF !important;
        }}

        /* Preset 2: Sunita Kamble - Vibrant Royal Blue */
        [data-testid="stExpander"] [data-testid="column"]:nth-child(2) .stButton > button {{
            border: 2px solid #2563EB !important;
            color: #2563EB !important;
            background-color: #FFFFFF !important;
        }}
        [data-testid="stExpander"] [data-testid="column"]:nth-child(2) .stButton > button:hover {{
            background-color: #2563EB !important;
            color: #FFFFFF !important;
        }}

        /* Preset 3: Vikram Joshi - Ocean / Steel Blue */
        [data-testid="stExpander"] [data-testid="column"]:nth-child(3) .stButton > button {{
            border: 2px solid #0284C7 !important;
            color: #0284C7 !important;
            background-color: #FFFFFF !important;
        }}
        [data-testid="stExpander"] [data-testid="column"]:nth-child(3) .stButton > button:hover {{
            background-color: #0284C7 !important;
            color: #FFFFFF !important;
        }}

        /* Reset Button */
        [data-testid="stExpander"] [data-testid="column"]:nth-child(4) .stButton > button {{
            border: 1.5px solid #64748B !important;
            color: #64748B !important;
        }}
        [data-testid="stExpander"] [data-testid="column"]:nth-child(4) .stButton > button:hover {{
            background-color: #64748B !important;
            color: #FFFFFF !important;
        }}

        {shadow_rule}
        </style>""",
        unsafe_allow_html=True,
    )


def render_preset_picker(is_marathi: bool):
    """Render the preset buttons inside an optional expander with 3 distinct shades of blue."""
    active = st.session_state.get("active_preset")
    _inject_preset_styles(active)

    expander_title = (
        "👤 नमुना नागरिक प्रोफाइल पहा (ऐच्छिक डेमो प्रोफाइल)"
        if is_marathi else
        "👤 Try a Sample Citizen Profile (Optional Demo Profiles)"
    )

    with st.expander(expander_title, expanded=bool(active)):
        caption_text = (
            "ही प्रात्यक्षिकासाठी उदाहरणे आहेत. आपण खालील अर्ज स्वतः देखील भरू शकता."
            if is_marathi else
            "These are example profiles for demonstration. You can also fill the form below manually."
        )
        st.caption(caption_text)

        pc1, pc2, pc3, pc4 = st.columns([2, 2, 2, 1])

        with pc1:
            p = PRESETS["ramesh"]
            lbl = p["label_mr"] if is_marathi else p["label_en"]
            note = p["note_mr"] if is_marathi else p["note_en"]
            exp = p["expected_mr"] if is_marathi else p["expected_en"]
            if st.button(lbl, use_container_width=True, help=f"{note}\nExpected: {exp}", key="preset_ramesh_btn"):
                st.session_state["form_data"] = p["data"].copy()
                st.session_state["active_preset"] = "ramesh"
                st.rerun()
            st.caption(f"**{note}**")
            st.caption(f"Expected: {exp}")

        with pc2:
            p = PRESETS["sunita"]
            lbl = p["label_mr"] if is_marathi else p["label_en"]
            note = p["note_mr"] if is_marathi else p["note_en"]
            exp = p["expected_mr"] if is_marathi else p["expected_en"]
            if st.button(lbl, use_container_width=True, help=f"{note}\nExpected: {exp}", key="preset_sunita_btn"):
                st.session_state["form_data"] = p["data"].copy()
                st.session_state["active_preset"] = "sunita"
                st.rerun()
            st.caption(f"**{note}**")
            st.caption(f"Expected: {exp}")

        with pc3:
            p = PRESETS["vikram"]
            lbl = p["label_mr"] if is_marathi else p["label_en"]
            note = p["note_mr"] if is_marathi else p["note_en"]
            exp = p["expected_mr"] if is_marathi else p["expected_en"]
            if st.button(lbl, use_container_width=True, help=f"{note}\nExpected: {exp}", key="preset_vikram_btn"):
                st.session_state["form_data"] = p["data"].copy()
                st.session_state["active_preset"] = "vikram"
                st.rerun()
            st.caption(f"**{note}**")
            st.caption(f"Expected: {exp}")

        with pc4:
            st.write("")
            if st.button(t("reset", is_marathi), use_container_width=True, key="preset_reset_btn"):
                st.session_state["form_data"] = dict(
                    name="", age=30, gender="male", annual_income=100000.0,
                    caste_category="general", land_holding_hectares=0.0,
                    occupation="farmer", has_bank_account=True, has_aadhaar=True,
                    owns_pucca_house=False
                )
                st.session_state["active_preset"] = None
                st.rerun()
