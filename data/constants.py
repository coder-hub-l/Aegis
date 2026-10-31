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

# Official Marathi Ground-Truth Translations for All 8 Schemes
SCHEME_TRANSLATIONS = {
    "pm_kisan": {
        "name_mr": "पीएम-किसान सन्मान निधी",
        "dept_mr": "कृषी व शेतकरी कल्याण मंत्रालय, भारत सरकार",
        "desc_mr": "पात्र शेतकरी कुटुंबांना दरवर्षी ₹६,००० चा थेट आर्थिक लाभ तीन समान हप्त्यांमध्ये दिला जातो.",
        "eligible_reason": "तुम्ही पीएम-किसान योजनेच्या सर्व अटी (शेतकरी व्यवसाय, आधार आणि सक्रिय बँक खाते) पूर्ण करता.",
        "almost_advice": "तुमचे बँक खाते आधारशी लिंक (DBT सक्षम) असल्याची खात्री करा किंवा जवळच्या सीएससी केंद्रात जाऊन ई-केवायसी पूर्ण करा."
    },
    "ladki_bahin": {
        "name_mr": "मुख्यमंत्री माझी लाडकी बहीण योजना",
        "dept_mr": "महिला व बालविकास विभाग, महाराष्ट्र शासन",
        "desc_mr": "महाराष्ट्रातील २१ ते ६५ वयोगटातील पात्र महिलांना दरमहा ₹१,५०० थेट बँक खात्यात दिले जातात.",
        "eligible_reason": "तुम्ही माझी लाडकी बहीण योजनेच्या सर्व निकषांची (वय, उत्पन्न, महिला लिंग व महाराष्ट्र रहिवासी) पूर्तता करता.",
        "almost_advice": "आपले सरकार पोर्टलवरून वार्षिक उत्पन्न प्रमाणपत्र मिळवा (किंवा पिवळे/केशरी रेशन कार्ड जोडा) आणि आधार लिंक बँक खाते सादर करा."
    },
    "pmay_gramin": {
        "name_mr": "प्रधानमंत्री आवास योजना - ग्रामीण",
        "dept_mr": "ग्रामविकास मंत्रालय / ग्रामविकास विभाग महाराष्ट्र",
        "desc_mr": "ग्रामीण भागातील बेघर व कच्च्या घरात राहणाऱ्या कुटुंबांना पक्के घर बांधण्यासाठी ₹१.२० लाख ते ₹१.३० लाखांचे अनुदान.",
        "eligible_reason": "पक्के घर नसणे, आधार आणि बँक खाते या सर्व मूलभूत ग्रामीण गृहनिर्माण निकषांची पूर्तता झाली आहे.",
        "almost_advice": "तुमच्या ग्रामपंचायतीशी संपर्क साधा आणि तुमचे नाव आवास+ २०२४ (Awaas+ 2024) सर्वेक्षण यादीत समाविष्ट असल्याची खात्री करा."
    },
    "namo_shetkari": {
        "name_mr": "नमो शेतकरी महासन्मान निधी",
        "dept_mr": "कृषी विभाग, महाराष्ट्र शासन",
        "desc_mr": "महाराष्ट्र शासनाकडून पात्र शेतकऱ्यांना दरवर्षी अतिरिक्त ₹६,००० थेट खात्यात (पीएम-किसान सोबत एकूण ₹१२,०००).",
        "eligible_reason": "महाराष्ट्र राज्यातील शेतकरी म्हणून तुम्ही राज्य शासनाच्या नमो शेतकरी सन्मान निधीसाठी पूर्णपणे पात्र आहात.",
        "almost_advice": "तुमची जमीन नोंदणी (७/१२ उतारा) अद्ययावत ठेवा आणि पीएम-किसान पोर्टलवर नोंदणी सक्रिय असल्याची खात्री करा."
    },
    "sanjay_gandhi_niradhar": {
        "name_mr": "संजय गांधी निराधार अनुदान योजना",
        "dept_mr": "सामाजिक न्याय व विशेष सहाय्य विभाग, महाराष्ट्र शासन",
        "desc_mr": "निराधार व्यक्ती, विधवा, दिव्यांग व संकटग्रस्त नागरिकांना दरमहा ₹१,५०० आर्थिक सहाय्य.",
        "eligible_reason": "तुम्ही संजय गांधी निराधार योजनेच्या उत्पन्न व सामाजिक निकषांची पूर्तता करता.",
        "almost_advice": "तहसीलदार कार्यालयाकडून ₹२१,००० च्या आतील कौटुंबिक वार्षिक उत्पन्नाचा दाखला आणि रहिवासी दाखला सादर करा."
    },
    "atal_pension": {
        "name_mr": "अटल पेन्शन योजना",
        "dept_mr": "वित्तीय सेवा विभाग, भारत सरकार / PFRDA",
        "desc_mr": "१८ ते ४० वयोगटातील नागरिकांसाठी वयाच्या ६० वर्षांनंतर दरमहा ₹१,००० ते ₹५,००० ची निश्चित पेन्शन.",
        "eligible_reason": "तुम्ही वयोमर्यादा (१८-४० वर्षे) व असंघटित क्षेत्र निकषांनुसार अटल पेन्शन योजनेसाठी पात्र आहात.",
        "almost_advice": "तुमच्या राष्ट्रीयकृत बँक किंवा पोस्ट ऑफिस शाखेत जाऊन ऑटो-डेबिट सुविधेसह अटल पेन्शन अर्ज भरा."
    },
    "pm_ujjwala": {
        "name_mr": "प्रधानमंत्री उज्ज्वला योजना २.०",
        "dept_mr": "पेट्रोलियम व नैसर्गिक वायू मंत्रालय, भारत सरकार",
        "desc_mr": "गरीब कुटुंबातील प्रौढ महिलांना विनामूल्य एलपीजी गॅस जोडणी, पहिला सिलिंडर आणि शेगडी मोफत.",
        "eligible_reason": "तुम्ही उज्ज्वला २.० योजनेच्या महिला कुटुंबप्रमुख व आर्थिक निकषांची पूर्तता करता.",
        "almost_advice": "रेशन कार्ड, आधार कार्ड आणि बँक पासबुकसह जवळच्या गॅस वितरकाकडे (Indane/BharatGas/HP) ई-केवायसी अर्ज जमा करा."
    },
    "karjmukti_yojana": {
        "name_mr": "महात्मा ज्योतिराव फुले शेतकरी कर्जमुक्ती योजना",
        "dept_mr": "सहकार व पणन विभाग, महाराष्ट्र शासन",
        "desc_mr": "थकबाकीदार शेतकऱ्यांसाठी ₹२ लाखांपर्यंत कर्जमाफी आणि नियमित कर्जफेड करणाऱ्या शेतकऱ्यांना ₹५०,००० प्रोत्साहनपर लाभ.",
        "eligible_reason": "तुम्ही शेतकरी कर्जमुक्ती योजनेच्या शेतकरी व पीक कर्ज निकषांची पूर्तता करता.",
        "almost_advice": "तुमच्या बँक शाखेत जाऊन आधार प्रमाणीकरण (Biometric Aadhaar Authentication) पूर्ण करा."
    }
}
