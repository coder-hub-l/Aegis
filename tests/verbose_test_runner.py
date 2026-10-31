import json
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from core.models import CitizenProfile
from core.engine import run_engine, load_schemes

def run_verbose_audit():
    print("================================================================================")
    print("                    AEGIS DETERMINISTIC ENGINE TEST AUDIT LOGS                  ")
    print("================================================================================")

    # -------------------------------------------------------------------------
    # TEST 1: SCHEME DATABASE INTEGRITY
    # -------------------------------------------------------------------------
    print("\n[TEST 1] SCHEMES DATABASE INTEGRITY & METADATA VERIFICATION")
    print("-" * 80)
    schemes = load_schemes()
    print(f"Total Statutory Schemes Loaded: {len(schemes)}")
    for i, s in enumerate(schemes, 1):
        print(f"  {i}. ID: {s['scheme_id']:<24} | Department: {s['department'][:35]}...")
        print(f"     Source URL : {s.get('source_url', 'N/A')}")
        print(f"     Last Sync  : {s.get('last_fetched', 'N/A')}")
        print(f"     Rules Keys : {list(s.get('rules', {}).keys())}")

    # -------------------------------------------------------------------------
    # TEST 2: PERSONA RAMESH PATIL (Small Marginal Farmer)
    # -------------------------------------------------------------------------
    print("\n[TEST 2] PERSONA A: RAMESH PATIL (Small Marginal Farmer - Vidarbha)")
    print("-" * 80)
    ramesh = CitizenProfile(
        name="Ramesh Patil", age=45, gender="male", annual_income=90000.0,
        caste_category="obc", land_holding_hectares=1.5, occupation="farmer",
        state="Maharashtra", has_bank_account=True, has_aadhaar=True, owns_pucca_house=False
    )
    print("Input Profile:")
    print("  Age=45, Gender=Male, Income=Rs.90,000, Land=1.5 Ha, Caste=OBC, Occ=Farmer, Bank=True, Aadhaar=True, Pucca=False")
    print("\nEngine Evaluation Verdicts:")
    results_ramesh = run_engine(ramesh)
    for r in results_ramesh:
        badge = f"[{r.status.upper()}]"
        print(f"  {badge:<12} {r.name}")
        for p in r.matched_rules:
            print(f"       + Passed: {p}")
        for f in r.failed_rules:
            print(f"       - Failed: {f}")

    # -------------------------------------------------------------------------
    # TEST 3: PERSONA SUNITA KAMBLE (Rural Woman Laborer)
    # -------------------------------------------------------------------------
    print("\n[TEST 3] PERSONA B: SUNITA KAMBLE (Rural Female Laborer - Marathwada)")
    print("-" * 80)
    sunita = CitizenProfile(
        name="Sunita Kamble", age=35, gender="female", annual_income=240000.0,
        caste_category="sc", land_holding_hectares=0.0, occupation="laborer",
        state="Maharashtra", has_bank_account=True, has_aadhaar=True, owns_pucca_house=False
    )
    print("Input Profile:")
    print("  Age=35, Gender=Female, Income=Rs.2,40,000, Land=0.0 Ha, Caste=SC, Occ=Laborer, Bank=True, Aadhaar=True, Pucca=False")
    print("\nEngine Evaluation Verdicts:")
    results_sunita = run_engine(sunita)
    for r in results_sunita:
        badge = f"[{r.status.upper()}]"
        print(f"  {badge:<12} {r.name}")
        for p in r.matched_rules:
            print(f"       + Passed: {p}")
        for f in r.failed_rules:
            print(f"       - Failed: {f}")

    # -------------------------------------------------------------------------
    # TEST 4: PERSONA VIKRAM JOSHI (Urban Salaried - Edge-Case Boundary)
    # -------------------------------------------------------------------------
    print("\n[TEST 4] PERSONA C: VIKRAM JOSHI (Urban Salaried - Edge-Case Negative)")
    print("-" * 80)
    vikram = CitizenProfile(
        name="Vikram Joshi", age=30, gender="male", annual_income=600000.0,
        caste_category="general", land_holding_hectares=0.0, occupation="salaried",
        state="Maharashtra", has_bank_account=True, has_aadhaar=True, owns_pucca_house=True
    )
    print("Input Profile:")
    print("  Age=30, Gender=Male, Income=Rs.6,00,000, Land=0.0 Ha, Caste=General, Occ=Salaried, Bank=True, Aadhaar=True, Pucca=True")
    print("\nEngine Evaluation Verdicts:")
    results_vikram = run_engine(vikram)
    for r in results_vikram:
        badge = f"[{r.status.upper()}]"
        print(f"  {badge:<12} {r.name}")
        for p in r.matched_rules:
            print(f"       + Passed: {p}")
        for f in r.failed_rules:
            print(f"       - Failed: {f}")

    # -------------------------------------------------------------------------
    # TEST 5: ALMOST-ELIGIBLE ACTIONABLE REMEDIATION HINTS
    # -------------------------------------------------------------------------
    print("\n[TEST 5] NEAR-MISS REMEDIATION (Farmer Missing Bank Account)")
    print("-" * 80)
    applicant = CitizenProfile(
        name="Santosh Gaikwad", age=40, gender="male", annual_income=80000.0,
        caste_category="obc", land_holding_hectares=1.0, occupation="farmer",
        state="Maharashtra", has_bank_account=False, has_aadhaar=True, owns_pucca_house=False
    )
    print("Input Profile: Farmer meeting all criteria EXCEPT has_bank_account=False")
    results_applicant = run_engine(applicant)
    pm_kisan = next(r for r in results_applicant if r.scheme_id == "pm_kisan")
    print(f"  PM-KISAN Status : [{pm_kisan.status.upper()}]")
    print(f"  Failed Rules    : {pm_kisan.failed_rules}")
    print("  Actionable Hints Extracted for Citizen:")
    for h in pm_kisan.hints:
        print(f"    -> {h}")

    print("\n================================================================================")
    print("                        END OF TEST SUITE AUDIT REPORT                          ")
    print("================================================================================")

if __name__ == "__main__":
    run_verbose_audit()
