# ui/config/strings.py
"""Bilingual English and Marathi string dictionaries and localization helpers."""

STRINGS = {
    "portal_name":    ("Scheme Eligibility Navigator", "योजना पात्रता तपासणी प्रणाली"),
    "portal_sub":     ("Government of Maharashtra", "महाराष्ट्र शासन"),
    "demo_heading":   ("Select a Demo Profile (Optional)", "नमुना नागरिक प्रोफाईल (ऐच्छिक)"),
    "demo_caption":   ("Load a pre-configured citizen profile to see instant results, or fill the form manually below.",
                       "तयार नागरिक प्रोफाईल लोड करा किंवा खाली स्वतः माहिती भरा."),
    "form_heading":   ("Citizen Eligibility Assessment Form", "नागरिक पात्रता तपासणी अर्ज"),
    "form_caption":   ("All fields marked with * are required for accurate eligibility verification.",
                       "* चिन्हांकित केलेली सर्व माहिती अचूक पात्रता तपासणीसाठी आवश्यक आहे."),
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
                       "आधार जोडलेले सक्रिय बँक खाते उपलब्ध आहे (थेट बँक खात्यात / DBT) *"),
    "aadhaar":        ("Holds valid Aadhaar card *", "वैध आधार कार्ड आहे *"),
    "house":          ("Owns a permanent pucca (concrete) house *", "स्वतःचे पक्के (काँक्रीट) घर आहे *"),
    "submit":         ("Verify Eligibility Against Official Schemes", "अधिकृत योजनांनुसार पात्रता तपासा"),
    "reset":          ("Clear Form", "माहिती पूर्ववत करा"),
    "spinner":        ("Verifying against official Maharashtra gazette rules…", "शासकीय नियमांनुसार पडताळणी सुरु आहे…"),
}

GENDER_LABELS = {
    "male": ("Male", "पुरुष"),
    "female": ("Female", "महिला"),
    "other": ("Other", "इतर"),
}

OCCUPATION_LABELS = {
    "farmer": ("Farmer", "शेतकरी"),
    "laborer": ("Laborer", "मजूर"),
    "salaried": ("Salaried", "नोकरदार / वेतनधारक"),
    "self_employed": ("Self-Employed", "स्वयंरोजगार / व्यावसायिक"),
    "unemployed": ("Unemployed", "बेरोजगार"),
}

CASTE_LABELS = {
    "general": ("General", "खुला प्रवर्ग (General)"),
    "obc": ("OBC", "इतर मागास वर्ग (OBC)"),
    "sc": ("SC", "अनुसूचित जाती (SC)"),
    "st": ("ST", "अनुसूचित जमाती (ST)"),
    "nt": ("NT", "भटक्या जमाती (NT)"),
    "vjnt": ("VJNT", "विमुक्त जाती व भटक्या जमाती (VJNT)"),
}


def t(key: str, is_marathi: bool) -> str:
    """Return the localized string for the specified key."""
    pair = STRINGS.get(key, (key, key))
    return pair[1] if is_marathi else pair[0]


def translate_rule_mr(rule_text: str) -> str:
    """Translate engine-generated condition strings into clean Marathi."""
    r = rule_text.strip()

    # Gender
    if "Gender (" in r and "matches required" in r:
        return "लिंग निकष पात्र (महिला/पुरुष अट पूर्ण)"
    if "Gender must be" in r:
        if "female" in r.lower():
            return "ही योजना केवळ महिला अर्जदारांसाठी आहे"
        return "लिंग निकष अपूर्ण आहे"

    # Age
    if "Age" in r and "is within required range" in r:
        return r.replace("Age", "वय").replace("is within required range", "अधिकृत वयोगटात आहे:")
    if "Age must be between" in r:
        return r.replace("Age must be between", "वय आवश्यक मर्यादेत असावे:").replace("applicant is", "सध्याचे वय:")

    # Income
    if "Income" in r and "is within ceiling" in r:
        return r.replace("Income", "वार्षिक उत्पन्न").replace("is within ceiling", "अधिकृत मर्यादेत आहे:")
    if "Income" in r and "exceeds ceiling of" in r:
        return r.replace("Income", "वार्षिक उत्पन्न").replace("exceeds ceiling of", "अधिकृत मर्यादेपेक्षा जास्त आहे (मर्यादा):")

    # Land
    if "Land" in r and "within range" in r:
        return r.replace("Land", "शेतजमीन धारणा").replace("within range", "मर्यादेत आहे:")
    if "is below minimum" in r:
        return r.replace("Land", "शेतजमीन").replace("is below minimum", "किमान मर्यादेपेक्षा कमी आहे:")
    if "exceeds limit of" in r:
        return r.replace("Land", "शेतजमीन").replace("exceeds limit of", "कमाल मर्यादेपेक्षा जास्त आहे:")

    # Occupation
    if "Occupation (" in r and "matches required" in r:
        return "व्यवसाय निकष पात्र (आवश्यक व्यवसाय जुळतो)"
    if "Occupation must be one of" in r:
        return "व्यवसाय निकष अपूर्ण (केवळ विहित व्यवसायातील नागरिकांसाठी)"

    # Caste
    if "Caste category" in r and "is eligible" in r:
        return "जात प्रवर्ग निकष पात्र"
    if "Caste must be one of" in r:
        return "जात प्रवर्ग निकष अपूर्ण"

    # State
    if "State domicile" in r and "matches required" in r:
        return "महाराष्ट्र राज्य अधिवास (डोमिसाईल) पात्र"
    if "State must be" in r:
        return "महाराष्ट्र राज्याचा अधिवास (डोमिसाईल) असणे आवश्यक आहे"

    # Booleans
    if "Has Bank Account: [OK]" in r:
        return "सक्रिय बँक खाते: उपलब्ध [पूर्ण]"
    if "Has Bank Account must be True" in r:
        return "आधार जोडलेले बँक खाते असणे आवश्यक आहे"

    if "Has Aadhaar: [OK]" in r:
        return "वैध आधार कार्ड: उपलब्ध [पूर्ण]"
    if "Has Aadhaar must be True" in r:
        return "वैध आधार कार्ड असणे आवश्यक आहे"

    if "Owns Pucca House: [OK]" in r:
        return "स्वतःचे पक्के घर नाही: निकष पात्र [पूर्ण]"
    if "Owns Pucca House must be False" in r:
        return "स्वतःचे पक्के (काँक्रीट) घर नसावे (केवळ कच्च्या घरातील नागरिकांसाठी)"

    return r
