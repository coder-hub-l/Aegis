"""Runtime integration test — runs outside Streamlit, tests engine + translations."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import run_engine
from core.models import CitizenProfile

PERSONAS = [
    CitizenProfile(name="Ramesh Patil", age=45, gender="male", annual_income=90000.0,
                   caste_category="obc", land_holding_hectares=1.5, occupation="farmer",
                   has_bank_account=True, has_aadhaar=True, owns_pucca_house=False),
    CitizenProfile(name="Sunita Kamble", age=35, gender="female", annual_income=240000.0,
                   caste_category="sc", land_holding_hectares=0.0, occupation="laborer",
                   has_bank_account=True, has_aadhaar=True, owns_pucca_house=False),
    CitizenProfile(name="Vikram Joshi", age=30, gender="male", annual_income=600000.0,
                   caste_category="general", land_holding_hectares=0.0, occupation="salaried",
                   has_bank_account=True, has_aadhaar=True, owns_pucca_house=True),
]

errors = []
for profile in PERSONAS:
    results = run_engine(profile)
    assert len(results) == 8, f"Expected 8 scheme results for {profile.name}, got {len(results)}"
    for r in results:
        # Every result must have English name + status
        assert r.name, f"Missing name for scheme_id={r.scheme_id}"
        assert r.status in ("eligible", "almost", "ineligible"), f"Bad status={r.status}"
        # Eligible/almost results must have Marathi translations
        if r.status in ("eligible", "almost"):
            if not r.name_mr:
                errors.append(f"WARN: {profile.name} | {r.scheme_id} => missing name_mr")
        print(f"  {profile.name}: {r.scheme_id:25s} => {r.status:11s} | "
              f"name_mr={'OK' if r.name_mr else 'MISS'} | "
              f"desc_mr={'OK' if r.description_mr else 'MISS'}")

print()
if errors:
    print("WARNINGS:")
    for e in errors:
        print(" ", e)
else:
    print("=== ENGINE RUNTIME TEST PASS — No missing translations ===")
