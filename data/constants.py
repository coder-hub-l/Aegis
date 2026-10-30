# data/constants.py
"""
Constants and ground-truth legal categories for Maharashtra Welfare Scheme Navigator.
Used by Srijan for UI dropdowns and Laukik for Pydantic schema validation.
"""

CASTE_CATEGORIES = [
    "general",
    "obc",
    "sc",
    "st",
    "nt",
    "vjnt"
]

OCCUPATIONS = [
    "farmer",
    "laborer",
    "salaried",
    "self_employed",
    "unemployed"
]

GENDERS = [
    "male",
    "female",
    "other"
]

DEFAULT_STATE = "Maharashtra"

# Official Citizen Support Portals (Used for UI links and citations)
PORTAL_URLS = {
    "aaple_sarkar": "https://aaplesarkar.mahaonline.gov.in",     # Income & Caste Certificates
    "mahadbt": "https://mahadbt.maharashtra.gov.in",               # Direct Benefit Transfer Portal
    "pmkisan": "https://pmkisan.gov.in",                           # PM-KISAN Portal
    "pmayg": "https://pmayg.nic.in",                               # Rural Housing
    "jan_dhan": "https://pmjdy.gov.in",                            # Zero-balance bank accounts
    "uidai_csc": "https://appointments.uidai.gov.in"               # Aadhaar Enrollment / CSC
}
