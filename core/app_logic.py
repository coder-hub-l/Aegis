# core/app_logic.py
from typing import List
from core.models import CitizenProfile, SchemeResult
from core.engine import run_engine
from core.explainer import generate_explanation, generate_almost_advice


def run_eligibility_pipeline(profile: CitizenProfile) -> List[SchemeResult]:
    """
    Full pipeline:
    1. Deterministic evaluation (zero AI hallucination).
    2. AI enrichment (plain language explanation + almost-eligible advice).
    3. Return sorted results (eligible -> almost -> ineligible).
    """
    # Step 1: Pure deterministic rule evaluation
    results = run_engine(profile)

    # Step 2: AI explains the findings
    for result in results:
        result.explanation = generate_explanation(result)
        if result.status == "almost":
            result.almost_advice = generate_almost_advice(result)

    return results
