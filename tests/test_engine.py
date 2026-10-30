# tests/test_engine.py
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.models import CitizenProfile
from core.engine import run_engine, evaluate_scheme, load_schemes


def test_load_schemes():
    """Verify schemes.json is valid and contains expected schemes."""
    schemes = load_schemes()
    assert len(schemes) >= 5, f"Expected at least 5 schemes, found {len(schemes)}"
    scheme_ids = [s["scheme_id"] for s in schemes]
    assert "pm_kisan" in scheme_ids
    assert "majhi_ladki_bahin" in scheme_ids
    print(f"[PASS] test_load_schemes ({len(schemes)} schemes loaded)")


def test_persona_ramesh_small_farmer():
    """Ramesh should qualify for PM-KISAN and Namo Shetkari."""
    ramesh = CitizenProfile(
        name="Ramesh Patil",
        age=45,
        gender="male",
        annual_income=90000.0,
        caste_category="obc",
        land_holding_hectares=1.5,
        occupation="farmer",
        has_bank_account=True,
        has_aadhaar=True,
        owns_pucca_house=False
    )
    results = run_engine(ramesh)
    results_map = {r.scheme_id: r.status for r in results}

    assert results_map.get("pm_kisan") == "eligible", f"Expected eligible, got {results_map.get('pm_kisan')}"
    assert results_map.get("namo_shetkari") == "eligible", f"Expected eligible, got {results_map.get('namo_shetkari')}"
    assert results_map.get("majhi_ladki_bahin") == "ineligible"  # Male applicant
    print("[PASS] test_persona_ramesh_small_farmer")


def test_persona_sunita_rural_woman():
    """Sunita should qualify for Majhi Ladki Bahin."""
    sunita = CitizenProfile(
        name="Sunita Kamble",
        age=35,
        gender="female",
        annual_income=135000.0,
        caste_category="sc",
        land_holding_hectares=0.0,
        occupation="laborer",
        has_bank_account=True,
        has_aadhaar=True,
        owns_pucca_house=False
    )
    results = run_engine(sunita)
    results_map = {r.scheme_id: r.status for r in results}

    assert results_map.get("majhi_ladki_bahin") == "eligible", f"Expected eligible, got {results_map.get('majhi_ladki_bahin')}"
    # Income ₹1.35L exceeds PMAY-G ₹1.20L by one condition -> should be 'almost'
    assert results_map.get("pmay_g") == "almost", f"Expected almost, got {results_map.get('pmay_g')}"
    print("[PASS] test_persona_sunita_rural_woman")


def test_persona_vikram_urban_salaried():
    """Vikram should be ineligible for farmer and income-capped welfare schemes."""
    vikram = CitizenProfile(
        name="Vikram Joshi",
        age=30,
        gender="male",
        annual_income=650000.0,
        caste_category="general",
        land_holding_hectares=0.0,
        occupation="salaried",
        has_bank_account=True,
        has_aadhaar=True,
        owns_pucca_house=True
    )
    results = run_engine(vikram)
    results_map = {r.scheme_id: r.status for r in results}

    assert results_map.get("pm_kisan") == "ineligible"
    assert results_map.get("majhi_ladki_bahin") == "ineligible"
    assert results_map.get("pmay_g") == "ineligible"
    print("[PASS] test_persona_vikram_urban_salaried")


def test_almost_eligible_remedy_hints():
    """Verify that 'almost' status extracts actionable remedy hints."""
    applicant = CitizenProfile(
        name="Missing Bank Account Farmer",
        age=40,
        gender="male",
        annual_income=80000.0,
        caste_category="obc",
        land_holding_hectares=1.0,
        occupation="farmer",
        has_bank_account=False,  # Single failed rule
        has_aadhaar=True,
        owns_pucca_house=False
    )
    results = run_engine(applicant)
    pm_kisan = next(r for r in results if r.scheme_id == "pm_kisan")
    assert pm_kisan.status == "almost"
    assert len(pm_kisan.failed_rules) == 1
    assert len(pm_kisan.hints) > 0
    print("[PASS] test_almost_eligible_remedy_hints")


if __name__ == "__main__":
    print("Running engine unit tests...")
    test_load_schemes()
    test_persona_ramesh_small_farmer()
    test_persona_sunita_rural_woman()
    test_persona_vikram_urban_salaried()
    test_almost_eligible_remedy_hints()
    print("\nALL TESTS PASSED SUCCESSFULLY!")
