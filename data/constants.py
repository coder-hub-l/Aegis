# data/constants.py
"""
Canonical constants, ground-truth legal categories, and authoritative portal references 
for the Maharashtra Welfare Scheme Navigator.
Used across core/models.py, core/engine.py, and ui/app.py.
"""

# Demographic & Categorical Constants
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

# State definition (providing both variable names to guarantee backward compatibility)
STATE = "Maharashtra"
DEFAULT_STATE = "Maharashtra"

# Official Citizen Support Portals (Verified on 2026-10-31)
PORTAL_URLS = {
    "aaple_sarkar": "https://aaplesarkar.mahaonline.gov.in",      # Income & Caste Certificates / Domicile
    "ladki_bahin": "https://ladakibahin.maharashtra.gov.in",       # Dedicated Ladki Bahin Portal
    "pmkisan": "https://pmkisan.gov.in",                           # PM-KISAN Portal
    "namo_shetkari": "https://namoshetkari.mahadbt.maharashtra.gov.in", # Namo Shetkari DBT Portal
    "pmayg": "https://pmayg.nic.in",                               # Rural Housing Portal
    "jan_dhan": "https://pmjdy.gov.in",                            # Zero-balance bank accounts
    "uidai_csc": "https://appointments.uidai.gov.in",              # Aadhaar Enrollment / CSC
    "atal_pension": "https://npscra.nsdl.co.in",                   # APY / PFRDA
    "pm_ujjwala": "https://pmuy.gov.in",                           # PMUY 2.0
    "karjmukti": "https://mjpsky.maharashtra.gov.in"               # MJPSKY Portal
}

# Direct shortcuts for UI tooltips
INCOME_CERTIFICATE_URL = PORTAL_URLS["aaple_sarkar"]
AADHAAR_ENROLLMENT_URL = PORTAL_URLS["uidai_csc"]
JAN_DHAN_URL = PORTAL_URLS["jan_dhan"]
