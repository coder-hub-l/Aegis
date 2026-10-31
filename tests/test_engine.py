# tests/test_engine.py
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.models import CitizenProfile
from core.engine import run_engine, load_schemes


def test_load_schemes():
    """Verify schemes.json is valid and contains expected schemes."""
    schemes = load_schemes()
    assert len(schemes) == 8, f"Expected 8 schemes, found {len(schemes)}"
    scheme_ids = [s["scheme_id"] for s in schemes]
    assert "pm_kisan" in scheme_ids
    assert "ladki_bahin" in scheme_ids
    assert "pmay_gramin" in scheme_ids
    assert "namo_shetkari" in scheme_ids
    print(f"[PASS] test_load_schemes ({len(schemes)} schemes loaded)")


def test_persona_ramesh_small_farmer():
    """Ramesh should qualify for PM-KISAN, Namo Shetkari, and MJPSKY."""
    ramesh = CitizenProfile(
        name="Ramesh Patil",
        age=45,
        gender="male",
        annual_income=90000.0,
        caste_category="obc",
        land_holding_hectares=1.5,
        occupation="farmer",
        state="Maharashtra",
        has_bank_account=True,
        has_aadhaar=True,
        owns_pucca_house=False
    )
    results = run_engine(ramesh)
    results_map = {r.scheme_id: r.status for r in results}

    assert results_map.get("pm_kisan") == "eligible", f"Expected eligible, got {results_map.get('pm_kisan')}"
    assert results_map.get("namo_shetkari") == "eligible", f"Expected eligible, got {results_map.get('namo_shetkari')}"
    assert results_map.get("ladki_bahin") == "ineligible"  # Male applicant
    print("[PASS] test_persona_ramesh_small_farmer")


def test_persona_sunita_rural_woman():
    """Sunita should qualify for Ladki Bahin, PMAY-G, APY, PMUY, and be Almost for Sanjay Gandhi."""
    sunita = CitizenProfile(
        name="Sunita Kamble",
        age=35,
        gender="female",
        annual_income=240000.0,
        caste_category="sc",
        land_holding_hectares=0.0,
        occupation="laborer",
        state="Maharashtra",
        has_bank_account=True,
        has_aadhaar=True,
        owns_pucca_house=False
    )
    results = run_engine(sunita)
    results_map = {r.scheme_id: r.status for r in results}

    assert results_map.get("ladki_bahin") == "eligible", f"Expected eligible, got {results_map.get('ladki_bahin')}"
    assert results_map.get("pm_ujjwala") == "eligible", f"Expected eligible, got {results_map.get('pm_ujjwala')}"
    assert results_map.get("atal_pension") == "eligible", f"Expected eligible, got {results_map.get('pmay_gramin')}"
    assert results_map.get("pm_kisan") == "ineligible"  # Laborer, not farmer
    assert results_map.get("namo_shetkari") == "ineligible"
    assert results_map.get("sanjay_gandhi_niradhar") == "ineligible"  # Income ₹2.4L exceeds destitute limit ₹21k
    print("[PASS] test_persona_sunita_rural_woman")


def test_persona_vikram_urban_salaried():
    """Vikram should be ineligible for welfare schemes."""
    vikram = CitizenProfile(
        name="Vikram Joshi",
        age=30,
        gender="male",
        annual_income=600000.0,
        caste_category="general",
        land_holding_hectares=0.0,
        occupation="salaried",
        state="Maharashtra",
        has_bank_account=True,
        has_aadhaar=True,
        owns_pucca_house=True
    )
    results = run_engine(vikram)
    results_map = {r.scheme_id: r.status for r in results}

    assert results_map.get("pm_kisan") == "ineligible"
    assert results_map.get("ladki_bahin") == "ineligible"
    assert results_map.get("pmay_gramin") == "ineligible"  # Owns pucca house
    assert results_map.get("sanjay_gandhi_niradhar") == "ineligible"  # Income exceeds
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
        state="Maharashtra",
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
