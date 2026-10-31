# ui/config/presets.py
"""Demo persona definitions and session state initialization for instant testing."""
import streamlit as st

PRESETS = {
    "ramesh": {
        "label_en": "Ramesh Patil — Small Farmer",
        "label_mr": "रमेश पाटील — अल्पभूधारक शेतकरी",
        "note_en":  "Age 45 | Male | OBC | Income Rs. 90,000 | Land 1.5 Ha | Farmer",
        "note_mr":  "वय ४५ | पुरुष | ओबीसी | उत्पन्न रु. ९०,००० | जमीन १.५ हेक्टर | शेतकरी",
        "expected_en": "Eligible: PM-KISAN, Namo Shetkari",
        "expected_mr": "पात्र: पीएम-किसान, नमो शेतकरी",
        "data": dict(name="Ramesh Patil", age=45, gender="male", annual_income=90000.0,
                     caste_category="obc", land_holding_hectares=1.5, occupation="farmer",
                     has_bank_account=True, has_aadhaar=True, owns_pucca_house=False),
    },
    "sunita": {
        "label_en": "Sunita Kamble — Rural Woman",
        "label_mr": "सुनीता कांबळे — ग्रामीण महिला",
        "note_en":  "Age 35 | Female | SC | Income Rs. 2,40,000 | Land 0 Ha | Laborer",
        "note_mr":  "वय ३५ | महिला | SC | उत्पन्न रु. २,४०,००० | जमीन ० हेक्टर | मजूर",
        "expected_en": "Eligible: Ladki Bahin, PMAY-G | Almost: Sanjay Gandhi",
        "expected_mr": "पात्र: लाडकी बहीण, पीएम आवास | जवळपास: संजय गांधी",
        "data": dict(name="Sunita Kamble", age=35, gender="female", annual_income=240000.0,
                     caste_category="sc", land_holding_hectares=0.0, occupation="laborer",
                     has_bank_account=True, has_aadhaar=True, owns_pucca_house=False),
    },
    "vikram": {
        "label_en": "Vikram Joshi — Urban Salaried",
        "label_mr": "विक्रम जोशी — शहरी नोकरदार",
        "note_en":  "Age 30 | Male | General | Income Rs. 6,00,000 | Land 0 Ha | Salaried | Pucca House",
        "note_mr":  "वय ३० | पुरुष | सर्वसाधारण | उत्पन्न रु. ६,००,००० | जमीन ० हेक्टर | नोकरदार | पक्के घर",
        "expected_en": "Edge Case — Mostly Ineligible",
        "expected_mr": "उच्च उत्पन्न — बहुतांश अपात्र",
        "data": dict(name="Vikram Joshi", age=30, gender="male", annual_income=600000.0,
                     caste_category="general", land_holding_hectares=0.0, occupation="salaried",
                     has_bank_account=True, has_aadhaar=True, owns_pucca_house=True),
    },
}

DEFAULT_FORM_DATA = PRESETS["ramesh"]["data"].copy()


def init_form_state():
    """Ensure form_data exists in session_state."""
    if "form_data" not in st.session_state:
        st.session_state["form_data"] = DEFAULT_FORM_DATA.copy()
    return st.session_state["form_data"]
