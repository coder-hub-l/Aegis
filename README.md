# Maharashtra Citizen Welfare Scheme Navigator
> **Forge ’26 Gen AI Buildathon — Team Aegis**  
> *A deterministic welfare scheme eligibility engine coupled with agentic plain-language explainability and remediation guidance.*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://img.shields.io/badge/frontend-Streamlit-red.svg)](https://streamlit.io/)
[![Zero Hallucination Core](https://img.shields.io/badge/decision--engine-deterministic-success.svg)](#architecture)
[![Official Data Verified](https://img.shields.io/badge/data.gov.in-verified_2026--10--31-green.svg)](data/schemes.json)

---

## Executive Summary

Every year, millions of eligible citizens miss out on government welfare schemes because eligibility rules are buried in complex legal gazettes, spread across fragmented departmental portals, and written in dense bureaucratic language. 

Generic LLM solutions (ChatGPT wrappers) hallucinate qualification conditions, misinforming vulnerable citizens and causing wasted weeks at government offices.

**The Maharashtra Welfare Scheme Navigator decouples decision logic from linguistic intelligence:**
1. **Deterministic Rule Engine:** 100% auditable, zero-hallucination code directly executing official statutory gazette rules (PM-KISAN, Ladki Bahin, PMAY-G, Namo Shetkari, APY, etc.).
2. **Agentic Remediation ("Almost Eligible"):** Identifies near-miss candidates and generates actionable legal remediation steps (e.g., land partition deeds, ration card waivers, Tahsildar destitute certificates).
3. **Official Data Provenance:** Every single recommendation links directly to verified government portals with verifiable retrieval timestamps.

---

## Architecture & Technical Separation of Concerns

```
┌────────────────────────────────────────────────────────┐
│            Streamlit User Interface (ui/app.py)        │
│   • Multi-demographic citizen intake form              │
│   • Instant demo presets (Ramesh, Sunita, Vikram)      │
│   • Marathi / English language localization toggle     │
└───────────────────────────┬────────────────────────────┘
                            │ Raw Input Dict
                            ▼
┌────────────────────────────────────────────────────────┐
│         Data Contracts & Validation (core/models.py)   │
│   • Pydantic CitizenProfile validation                 │
│   • Type enforcement, bounds, and sanitation           │
└───────────────────────────┬────────────────────────────┘
                            │ Validated CitizenProfile
                            ▼
┌────────────────────────────────────────────────────────┐
│     Deterministic Decision Engine (core/engine.py)     │
│   • Evaluates citizen profile against data/schemes.json│
│   • Quantitative bounds (income, land, age)            │
│   • Categorical inclusion (caste, occupation)          │
│   • Strict boolean prerequisites (banking, Aadhaar)    │
│   • Zero LLM involvement in eligibility determination  │
└───────────────────────────┬────────────────────────────┘
                            │ SchemeResult (eligible | almost | ineligible)
                            ▼
┌────────────────────────────────────────────────────────┐
│        AI Explainer & Remediation (core/explainer.py)  │
│   • Google Gemini API integration                      │
│   • Translates binary rule outcomes into plain prose   │
│   • Formulates actionable steps for "almost" candidates│
└───────────────────────────┬────────────────────────────┘
                            │ Enriched SchemeResult List
                            ▼
┌────────────────────────────────────────────────────────┐
│        Audit Trail & Results View (ui/results_view.py) │
│   • Eligible schemes with full benefit breakdowns      │
│   • Almost eligible with actionable remediation        │
│   • Ineligible schemes with statutory failure audit    │
│   • Verifiable portal links and timestamp badges       │
└────────────────────────────────────────────────────────┘
```

---

## Ground-Truth Scheme Database (`data/schemes.json`)

All 8 schemes in this repository were manually verified on **October 31, 2026** against official state and central portals:

| Scheme Name | Department / Ministry | Official Portal | Verification Timestamp |
| :--- | :--- | :--- | :--- |
| **PM-KISAN Samman Nidhi** | Ministry of Agriculture & Farmers Welfare, GoI | [pmkisan.gov.in](https://pmkisan.gov.in) | `2026-10-31T02:38:00Z` |
| **Mukhyamantri Majhi Ladki Bahin** | Women & Child Development Dept, GoM | [ladakibahin.maharashtra.gov.in](https://ladakibahin.maharashtra.gov.in) | `2026-10-31T02:38:00Z` |
| **PMAY - Gramin (2024–29 Extension)** | Ministry of Rural Development, GoI | [pmayg.nic.in](https://pmayg.nic.in) | `2026-10-31T02:38:00Z` |
| **Namo Shetkari Mahasanman Nidhi** | Department of Agriculture, GoM | [namoshetkari.mahadbt.maharashtra.gov.in](https://namoshetkari.mahadbt.maharashtra.gov.in) | `2026-10-31T02:38:00Z` |
| **Sanjay Gandhi Niradhar Anudan** | Social Justice & Special Assistance Dept, GoM | [sjsa.maharashtra.gov.in](https://sjsa.maharashtra.gov.in) | `2026-10-31T02:38:00Z` |
| **Atal Pension Yojana (APY)** | PFRDA / Ministry of Finance, GoI | [npscra.nsdl.co.in](https://npscra.nsdl.co.in) | `2026-10-31T02:38:00Z` |
| **PM Ujjwala Yojana 2.0** | Ministry of Petroleum & Natural Gas, GoI | [pmuy.gov.in](https://pmuy.gov.in) | `2026-10-31T02:38:00Z` |
| **Shetkari Karjmukti Yojana (MJPSKY)** | Co-operation & Marketing Dept, GoM | [mjpsky.maharashtra.gov.in](https://mjpsky.maharashtra.gov.in) | `2026-10-31T02:38:00Z` |

---

## Quickstart & Installation

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 3. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 5. Run the Application
```bash
streamlit run ui/app.py
```
Open your browser at `http://localhost:8501`.

---

## Live Demo Personas (Jury Test Cases)

Use the top dropdown in the application to pre-fill test profiles:

1. ** Ramesh Patil (Small Farmer, Vidarbha):**
   - *Tests:* Dual Central + State agricultural synergy.
   - *Expected:* Eligible for **PM-KISAN** (₹6,000/yr), **Namo Shetkari** (₹6,000/yr top-up), and **Karjmukti Yojana**. Correctly rejected for Ladki Bahin (gender mismatch).
2. ** Sunita Kamble (Rural Landless Woman):**
   - *Tests:* Women & Child social safety net + AI "Almost Eligible" guidance.
   - *Expected:* Eligible for **Ladki Bahin** (₹1,500/mo), **APY**, and **Ujjwala 2.0**. Shows "Almost Eligible" guidance for housing verification under Awaas+ 2024.
3. ** Vikram Joshi (Urban Salaried Professional):**
   - *Tests:* Zero-hallucination boundary checks.
   - *Expected:* Rejected across targeted welfare schemes due to high income and asset ownership.

---

## Team Aegis & Responsibilities

- **Vinit Patil** — *Product, Data & Validation Lead*  
  Official scheme parameter extraction, statutory cutoff verification, demo personas, and pitch presentation.
- **Laukik Wani** — *Tech Lead & Backend SDE*  
  Pydantic data modeling (`models.py`), deterministic rule evaluation engine (`engine.py`), and Gemini explainer orchestration (`explainer.py`).
- **Srijan** — *Frontend & Demo Lead*  
  Streamlit interactive dashboard (`app.py`), status badge visualization cards, audit sidebar, and demo presentation execution.

---

## Compliance with Hackathon Regulations
- **Zero Mock/Hardcoded Outcomes:** All outputs dynamically evaluated at runtime against official scheme criteria.
- **Timestamp Provenance:** Direct citations with ISO 8601 timestamps to official portals.
- **Zero Hallucination Decision Core:** Decoupled architecture ensures LLM never makes legal entitlement decisions.
