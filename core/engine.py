# core/engine.py
import json
from pathlib import Path
from typing import List, Dict, Any
from core.models import CitizenProfile, SchemeResult


def load_schemes() -> List[Dict[str, Any]]:
    """Load schemes from data/schemes.json."""
    path = Path(__file__).parent.parent / "data" / "schemes.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_scheme(profile: CitizenProfile, scheme: Dict[str, Any]) -> SchemeResult:
    """
    Deterministically evaluate a single scheme against a citizen profile.
    Returns a SchemeResult with status: "eligible", "almost", or "ineligible".
    AI explanation fields are left empty here — explainer.py fills them later.
    """
    rules = scheme.get("rules", {})
    hints_data = scheme.get("almost_eligible_hints", {})
    matched = []
    failed = []
    hints = []

    # ── Rule: gender ──────────────────────────────────────────────
    if "gender" in rules:
        allowed = [g.lower() for g in rules["gender"]]
        if profile.gender.lower() in allowed:
            matched.append(f"Gender ({profile.gender}) matches required: {rules['gender']}")
        else:
            failed.append(f"Gender must be {rules['gender']}, applicant is: {profile.gender}")
            if "gender" in hints_data:
                hints.append(hints_data["gender"])

    # ── Rule: age range ───────────────────────────────────────────
    if "age" in rules:
        min_age = rules["age"].get("min", 0)
        max_age = rules["age"].get("max", 200)
        if min_age <= profile.age <= max_age:
            matched.append(f"Age {profile.age} is within required range {min_age}–{max_age}")
        else:
            failed.append(f"Age must be between {min_age} and {max_age}; applicant is {profile.age}")
            if "age" in hints_data:
                hints.append(hints_data["age"])

    # ── Rule: annual income ceiling ────────────────────────────────
    income_hard_disqualified = False
    if "annual_income" in rules:
        max_inc = rules["annual_income"].get("max")
        if max_inc is not None:
            if profile.annual_income <= max_inc:
                matched.append(f"Income ₹{profile.annual_income:,.0f} is within ceiling ₹{max_inc:,.0f}")
            else:
                failed.append(f"Income ₹{profile.annual_income:,.0f} exceeds ceiling of ₹{max_inc:,.0f}")
                # If income exceeds ceiling by more than 25%, it is a hard disqualifier (not a near-miss)
                if profile.annual_income > max_inc * 1.25:
                    income_hard_disqualified = True
                elif "annual_income" in hints_data:
                    hints.append(hints_data["annual_income"])

    # ── Rule: land holding ceiling and floor ───────────────────────
    if "land_holding_hectares" in rules:
        min_land = rules["land_holding_hectares"].get("min", 0.0)
        max_land = rules["land_holding_hectares"].get("max")
        if profile.land_holding_hectares < min_land:
            failed.append(f"Land {profile.land_holding_hectares} Ha is below minimum {min_land} Ha")
            if "land_holding_hectares" in hints_data:
                hints.append(hints_data["land_holding_hectares"])
        elif max_land is not None and profile.land_holding_hectares > max_land:
            failed.append(f"Land {profile.land_holding_hectares} Ha exceeds limit of {max_land} Ha")
            if "land_holding_hectares" in hints_data:
                hints.append(hints_data["land_holding_hectares"])
        else:
            matched.append(f"Land {profile.land_holding_hectares} Ha within range ({min_land}–{max_land} Ha)")

    # ── Rule: occupation ──────────────────────────────────────────
    if "occupation" in rules:
        allowed = [o.lower() for o in rules["occupation"]]
        if profile.occupation.lower() in allowed:
            matched.append(f"Occupation ({profile.occupation}) matches required: {rules['occupation']}")
        else:
            failed.append(f"Occupation must be one of {rules['occupation']}; applicant is: {profile.occupation}")
            if "occupation" in hints_data:
                hints.append(hints_data["occupation"])

    # ── Rule: caste category ───────────────────────────────────────
    if "caste_category" in rules:
        allowed = [c.lower() for c in rules["caste_category"]]
        if profile.caste_category.lower() in allowed:
            matched.append(f"Caste category ({profile.caste_category}) is eligible")
        else:
            failed.append(f"Caste must be one of {rules['caste_category']}; applicant is: {profile.caste_category}")
            if "caste_category" in hints_data:
                hints.append(hints_data["caste_category"])

    # ── Rule: state domicile ───────────────────────────────────────
    if "state" in rules:
        allowed = [s.lower() for s in rules["state"]]
        if profile.state.lower() in allowed:
            matched.append(f"State domicile ({profile.state}) matches required: {rules['state']}")
        else:
            failed.append(f"State must be {rules['state']}; applicant is: {profile.state}")
            if "state" in hints_data:
                hints.append(hints_data["state"])

    # ── Rule: boolean fields ───────────────────────────────────────
    for field_name in ["has_bank_account", "has_aadhaar", "owns_pucca_house"]:
        if field_name in rules:
            expected = rules[field_name]
            actual = getattr(profile, field_name)
            label = field_name.replace("_", " ").title()
            if actual == expected:
                matched.append(f"{label}: [OK] ({actual})")
            else:
                failed.append(f"{label} must be {expected}; applicant has: {actual}")
                if field_name in hints_data:
                    hints.append(hints_data[field_name])

    # ── Determine final status ─────────────────────────────────────
    # Hard statutory disqualifiers that can never be "almost" eligible:
    gender_failed = any("Gender must be" in f for f in failed)
    occupation_failed = any("Occupation must be" in f for f in failed)
    pucca_failed = any("Owns Pucca House must be False" in f for f in failed)

    is_hard_disqualified = gender_failed or occupation_failed or pucca_failed or income_hard_disqualified

    if len(failed) == 0:
        status = "eligible"
    elif len(failed) == 1 and not is_hard_disqualified:
        status = "almost"
    else:
        status = "ineligible"

    return SchemeResult(
        scheme_id=scheme["scheme_id"],
        name=scheme["name"],
        department=scheme.get("department", "Government of Maharashtra"),
        status=status,
        matched_rules=matched,
        failed_rules=failed,
        hints=hints,
        exclusions=scheme.get("exclusions", []),
        explanation="",       # Will be filled by explainer.py
        almost_advice="",     # Will be filled by explainer.py
        source_url=scheme.get("source_url", ""),
        last_fetched=scheme.get("last_fetched", ""),
        description=scheme.get("description", "")
    )


def run_engine(profile: CitizenProfile) -> List[SchemeResult]:
    """
    Run all schemes against the given profile.
    Returns results sorted: eligible first, almost second, ineligible last.
    """
    schemes = load_schemes()
    results = [evaluate_scheme(profile, scheme) for scheme in schemes]

    order = {"eligible": 0, "almost": 1, "ineligible": 2}
    return sorted(results, key=lambda r: order[r.status])
