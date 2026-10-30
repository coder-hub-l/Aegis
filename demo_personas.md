# Demo Personas & Presentation Ground-Truth (Vinit's Pitch Sheet)
**Updated & Verified:** October 31, 2026 (03:00 AM)  
**Status:** 100% Aligned with Verified `schemes.json`

Give these exact input parameters and narrative cues to Srijan for the Streamlit UI presets.

---

### Persona A: "Ramesh Patil" (Small Marginal Farmer from Vidarbha)
* **Demo Goal:** Showcase dual Central + State synergy (PM-KISAN + Namo Shetkari) and prove that all landholding farmers qualify without artificial land caps.
* **Demographics & Form Inputs:**
  - **Name:** Ramesh Patil
  - **Age:** 46
  - **Gender:** Male (`male`)
  - **Annual Income:** ₹85,000
  - **Caste:** OBC (`obc`)
  - **Land Holding:** 1.4 Hectares
  - **Occupation:** Farmer (`farmer`)
  - **Bank Account:** Yes (`True`)
  - **Aadhaar:** Yes (`True`)
  - **Owns Pucca House:** No (`False`)
* **Expected Live Engine Outputs:**
  - ✅ **Eligible:**
    1. **PM-KISAN Samman Nidhi:** Direct ₹6,000/yr (Passed: Farmer, Aadhaar eKYC, Bank account).
    2. **Namo Shetkari Mahasanman Nidhi:** Direct ₹6,000/yr state top-up (Total ₹12,000 combined annual benefit!).
    3. **Mahatma Jyotirao Phule Shetkari Karjmukti Yojana:** Automated crop loan relief / regular repayment incentive.
  - 🟡 **Almost Eligible / Action Required:**
    1. **PMAY-Gramin:** Qualifies on housing (no pucca house) & banking; needs verification of household inclusion in the Gram Panchayat's **Awaas+ 2024 survey**.
  - ❌ **Ineligible:**
    1. **Mukhyamantri Majhi Ladki Bahin:** Ineligible (Gender: Male; scheme is exclusively for women).
    2. **PM Ujjwala 2.0:** Ineligible (Exclusively issued in the name of an adult female).

---

### Persona B: "Sunita Kamble" (Rural Female Daily Wage Laborer)
* **Demo Goal:** Showcase Maharashtra's marquee women's welfare initiative (*Ladki Bahin*) + highlight the **AI "Almost Eligible" Remediation Guidance**.
* **Demographics & Form Inputs:**
  - **Name:** Sunita Kamble
  - **Age:** 36
  - **Gender:** Female (`female`)
  - **Annual Income:** ₹2,40,000 (Qualifies under the ₹2.5 Lakh Ladki Bahin ceiling)
  - **Caste:** SC (`sc`)
  - **Land Holding:** 0.0 Hectares (Landless)
  - **Occupation:** Laborer (`laborer`)
  - **Bank Account:** Yes (`True`)
  - **Aadhaar:** Yes (`True`)
  - **Owns Pucca House:** No (`False`)
* **Expected Live Engine Outputs:**
  - ✅ **Eligible:**
    1. **Mukhyamantri Majhi Ladki Bahin Yojana:** ₹1,500/month (Passed: Female, age 36 within [21–65], income ₹2.4L < ₹2.5L limit, Maharashtra resident).
    2. **Atal Pension Yojana (APY):** Qualifies for voluntary unorganized sector guaranteed pension (Age 36 within [18–40]).
    3. **Pradhan Mantri Ujjwala Yojana 2.0:** Qualifies for deposit-free LPG connection + ₹300/cylinder DBT subsidy as an adult woman from a vulnerable/SC household.
  - 🟡 **Almost Eligible / Action Required:**
    1. **PMAY-Gramin:** Income and housing pass; AI guides her to submit an Awaas+ 2024 survey form via her Gram Sevak.
  - ❌ **Ineligible:**
    1. **PM-KISAN / Namo Shetkari:** Ineligible (Occupation: Laborer, no agricultural land record).

---

### Persona C: "Vikram Joshi" (Urban Salaried Private Employee)
* **Demo Goal:** Prove that the system **does not hallucinate** and strictly rejects applicants who fail legal welfare criteria.
* **Demographics & Form Inputs:**
  - **Name:** Vikram Joshi
  - **Age:** 32
  - **Gender:** Male (`male`)
  - **Annual Income:** ₹6,50,000
  - **Caste:** General (`general`)
  - **Land Holding:** 0.0 Hectares
  - **Occupation:** Salaried (`salaried`)
  - **Bank Account:** Yes (`True`)
  - **Aadhaar:** Yes (`True`)
  - **Owns Pucca House:** Yes (`True`)
* **Expected Live Engine Outputs:**
  - ✅ **Eligible:**
    1. **Atal Pension Yojana (APY):** Eligible *only if* he is not an active income-tax filer.
  - ❌ **Ineligible (Rejected across the board):**
    - **PM-KISAN / Namo Shetkari:** Rejected (Not a farmer).
    - **Ladki Bahin:** Rejected (Male; Income ₹6.5L > ₹2.5L).
    - **PMAY-G:** Rejected (Already owns a pucca house).
    - **Sanjay Gandhi Niradhar:** Rejected (Not destitute, income ₹6.5L >> ₹21,000 ceiling).
    - **PM Ujjwala 2.0:** Rejected (Gender: Male).
