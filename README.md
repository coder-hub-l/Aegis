# Aegis — Maharashtra Welfare Scheme Eligibility Navigator

> **Zero-Hallucination Welfare Scheme Matching Engine with Multilingual GenAI Explanations & Actionable "Almost-Eligible" Remediation.**  
> *Built for Forge ’26 Gen AI Buildathon (48-Hour Sprint).*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Validation](https://img.shields.io/badge/Validation-Pydantic_v2-red.svg)](https://docs.pydantic.dev/)
[![LLM](https://img.shields.io/badge/AI-Google_Gemini_1.5_Flash-8E75B2.svg)](https://ai.google.dev/)
[![Bilingual](https://img.shields.io/badge/Language-English_%7C_मराठी-success.svg)](#)

---

## 💡 The Core Problem & Our USP

### The Problem with ChatGPT Wrappers
General-purpose LLMs hallucinate welfare scheme conditions. A false-positive recommendation sends a vulnerable farmer or rural citizen on a weeks-long wild goose chase to administrative tehsil offices for benefits they legally cannot receive.

### How Aegis Solves This
```
┌─────────────────────────────────────────────────────────────┐
│                       TRADITIONAL LLM                       │
│  User input ──► [ LLM Guesses Rules & Hallucinates ] ──► ???│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                            AEGIS                            │
│  User Form ──► [ Pydantic Type Check ]                      │
│                      │                                      │
│                      ▼                                      │
│           [ Deterministic Rule Engine ]                     │
│           • Evaluates statutory gazette rules               │
│           • ZERO LLM involvement in decision                │
│           • 100% mathematically reproducible                │
│                      │                                      │
│                      ▼                                      │
│           [ Gemini 1.5 Flash Explainer ]                    │
│           • Only explains the engine's verdict              │
│           • Generates actionable "Almost Eligible" remedy   │
│           • English & मराठी natural language                │
└─────────────────────────────────────────────────────────────┘
```

> **The Jury-Proof Answer:**  
> *"ChatGPT guesses. Our deterministic engine executes the actual legal conditions from the official Maharashtra scheme gazettes. The AI is only the voice — the engine is the brain."*

---

## 🌟 Key Features

1. **Deterministic Rule Engine (Zero Hallucinations):** Evaluates age, gender, caste, landholdings, annual income, pucca house ownership, and bank/Aadhaar status with 0% margin of error.
2. **Actionable "Almost Eligible" Remediation:** If a citizen misses eligibility by just **one** condition (e.g. income ceiling, missing Jan Dhan account, land records), the system flags them as *Almost Eligible* and provides exact administrative steps (which portal to visit, what certificate to request from the Tahsildar).
3. **Bilingual Support (English + मराठी):** Built-in toggle providing end-to-end interface and verdict explanations in Marathi and English.
4. **Preset Personas for Flawless Demos:** Instant 1-click loading of real-world personas (Ramesh - Small Farmer, Sunita - Rural Woman, Vikram - Urban Salaried).
5. **Zero Mock Data (Verifiable Lineage):** Every scheme is mapped to official `.gov.in` source URLs with verifiable ISO timestamps.

---

## 🏛️ Supported Schemes (Official State & Central Gazettes)

| Scheme ID | Scheme Name | Nodal Department | Official Gazette Portal | Verification |
| :--- | :--- | :--- | :--- | :--- |
| `pm_kisan` | **PM-KISAN Samman Nidhi** | Ministry of Agriculture, GoI | [pmkisan.gov.in](https://pmkisan.gov.in) | Verified Active |
| `majhi_ladki_bahin` | **Mukhyamantri Majhi Ladki Bahin Yojana** | Women & Child Development, GoM | [mahadbt.maharashtra.gov.in](https://mahadbt.maharashtra.gov.in) | Verified Active |
| `pmay_g` | **PMAY - Gramin (Housing)** | Rural Development Dept | [pmayg.nic.in](https://pmayg.nic.in) | Verified Active |
| `namo_shetkari` | **Namo Shetkari Maha Samman Nidhi** | Dept of Agriculture, GoM | [mahadbt.maharashtra.gov.in](https://mahadbt.maharashtra.gov.in) | Verified Active |
| `sanjay_gandhi_niradhar` | **Sanjay Gandhi Niradhar Anudan** | Social Justice Dept, GoM | [sjsa.maharashtra.gov.in](https://sjsa.maharashtra.gov.in) | Verified Active |
| `atal_pension` | **Atal Pension Yojana (APY)** | PFRDA / Finance Ministry | [npscra.nsdl.co.in](https://npscra.nsdl.co.in) | Verified Active |
| `pm_ujjwala` | **PM Ujjwala Yojana 2.0 (LPG)** | Ministry of Petroleum, GoI | [pmuy.gov.in](https://pmuy.gov.in) | Verified Active |
| `mahatma_phule_karjmukti` | **Mahatma Phule Shetkari Karjmukti** | Co-operation & Marketing, GoM | [mahadbt.maharashtra.gov.in](https://mahadbt.maharashtra.gov.in) | Verified Active |

---

## 📁 Repository Architecture

```text
Aegis/
├── data/
│   ├── schemes.json          # Verified statutory schemes, rule conditions & remedy hints
│   └── constants.py          # Canonical caste categories, occupations & gov URLs
├── core/
│   ├── models.py             # Type-safe Pydantic models (CitizenProfile, SchemeResult)
│   ├── engine.py             # Pure Python deterministic rule engine (Zero LLM)
│   ├── explainer.py          # Google Gemini 1.5 Flash natural language explainer
│   └── app_logic.py          # Unified pipeline (Validate -> Evaluate -> Explain)
├── ui/
│   ├── app.py                # Main Streamlit web application & bilingual state
│   └── components/
│       ├── results_view.py   # 3-tier card layout (Eligible, Almost Eligible, Ineligible)
│       └── sidebar.py        # Submitted profile inspector & payload viewer
├── tests/
│   └── test_engine.py        # Automated test suite covering edge cases and personas
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Clone & Enter Directory
```bash
cd Aegis
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and add your Gemini API Key:
```bash
# In .env:
GEMINI_API_KEY="your_actual_gemini_api_key_here"
```
*(Note: If no API key is provided, the application will automatically fall back to deterministic statutory explanation templates without crashing).*

### 5. Run Automated Tests
```bash
python tests/test_engine.py
```
Output:
```text
Running engine unit tests...
[PASS] test_load_schemes (8 schemes loaded)
[PASS] test_persona_ramesh_small_farmer
[PASS] test_persona_sunita_rural_woman
[PASS] test_persona_vikram_urban_salaried
[PASS] test_almost_eligible_remedy_hints

ALL TESTS PASSED SUCCESSFULLY!
```

### 6. Launch the Web Dashboard
```bash
streamlit run ui/app.py
```
The application will launch at `http://localhost:8501`.

---

## 👥 The Team

| Team Member | Role | Core Responsibility |
| :--- | :--- | :--- |
| **Laukik Wani** | **Tech Lead & SDE** | Backend architecture, Pydantic contracts, deterministic rule engine & AI pipeline |
| **Srijan** | **Frontend & Demo Lead** | Streamlit UI/UX, English/Marathi localization, live demo flow & pitch |
| **Vinit Patil** | **Product & Ground Truth** | Gazette rule verification, official data lineage, farmer heuristics & edge cases |
