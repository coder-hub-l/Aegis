# ui/config/strings.py
"""Bilingual English and Marathi string dictionaries and localization helpers."""

STRINGS = {
    "portal_name":    ("Scheme Eligibility Navigator", "योजना पात्रता तपासणी प्रणाली"),
    "portal_sub":     ("Government of Maharashtra", "महाराष्ट्र शासन"),
    "demo_heading":   ("Step 1 — Select a Demo Profile (Optional)", "पाऊल १ — डेमो प्रोफाईल निवडा (ऐच्छिक)"),
    "demo_caption":   ("Load a pre-configured citizen profile to see instant results, or fill the form manually below.",
                       "तयार नागरिक प्रोफाईल लोड करा किंवा खाली स्वतः माहिती भरा."),
    "form_heading":   ("Step 2 — Citizen Eligibility Assessment Form", "पाऊल २ — नागरिक पात्रता तपासणी अर्ज"),
    "form_caption":   ("All fields marked with * are required for accurate eligibility verification.",
                       "* असलेली सर्व माहिती अचूक पात्रता तपासणीसाठी आवश्यक आहे."),
    "personal":       ("Personal Details", "वैयक्तिक माहिती"),
    "economic":       ("Economic & Agricultural Details", "आर्थिक व शेती माहिती"),
    "doc_status":     ("Documentation & Asset Status", "कागदपत्रे व मालमत्ता स्थिती"),
    "name":           ("Full Name", "पूर्ण नाव"),
    "age":            ("Age *", "वय *"),
    "gender":         ("Gender *", "लिंग *"),
    "income":         ("Annual Household Income (INR) *", "वार्षिक कौटुंबिक उत्पन्न (रुपये) *"),
    "caste":          ("Caste Category *", "जात प्रवर्ग *"),
    "land":           ("Agricultural Land Holding (Ha)", "शेतजमीन धारणा (हेक्टर)"),
    "occupation":     ("Primary Occupation *", "मुख्य व्यवसाय *"),
    "bank":           ("Has active Aadhaar-linked bank account (DBT enabled) *",
                       "आधार जोडलेले सक्रिय बँक खाते उपलब्ध आहे (DBT) *"),
    "aadhaar":        ("Holds valid Aadhaar card *", "वैध आधार कार्ड आहे *"),
    "house":          ("Owns a permanent pucca (concrete) house *", "स्वतःचे पक्के (काँक्रीट) घर आहे *"),
    "submit":         ("Verify Eligibility Against Official Schemes", "अधिकृत योजनांनुसार पात्रता तपासा"),
    "reset":          ("Clear Form", "माहिती पूर्ववत करा"),
    "spinner":        ("Verifying against official Maharashtra gazette rules…", "शासकीय नियमांनुसार पडताळणी सुरु आहे…"),
}

GENDER_LABELS = {
    "male": ("Male / पुरुष", "पुरुष"),
    "female": ("Female / महिला", "महिला"),
    "other": ("Other / इतर", "इतर"),
}

OCCUPATION_LABELS = {
    "farmer": ("Farmer / शेतकरी", "शेतकरी"),
    "laborer": ("Laborer / मजूर", "मजूर"),
    "salaried": ("Salaried / नोकरदार", "नोकरदार"),
    "self_employed": ("Self-Employed / व्यावसायिक", "व्यावसायिक"),
    "unemployed": ("Unemployed / बेरोजगार", "बेरोजगार"),
}


def t(key: str, is_marathi: bool) -> str:
    """Return the localized string for the specified key."""
    pair = STRINGS.get(key, (key, key))
    return pair[1] if is_marathi else pair[0]
