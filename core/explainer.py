# core/explainer.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from core.models import SchemeResult

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


def get_model():
    """Lazily initialize and return the generative model if configured."""
    if not os.getenv("GEMINI_API_KEY"):
        return None
    try:
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        return None


def generate_explanation(result: SchemeResult) -> str:
    """
    Generate a plain-language explanation of WHY the citizen got this result.
    Based only on the rule outcomes — NOT on speculative knowledge.
    """
    model = get_model()

    if result.status == "eligible":
        rules_text = "\n".join(f"- {r}" for r in result.matched_rules)
        if not model:
            return f"You meet all statutory requirements for {result.name}, including occupation, documentation, and category criteria."
        prompt = f"""You are a government welfare advisor. A citizen has been found ELIGIBLE for {result.name}.

The following conditions were all met:
{rules_text}

Write exactly 2 sentences in simple English explaining why they qualify.
Be factual. Only refer to the conditions listed above. Do not add any new conditions."""

    elif result.status == "almost":
        failed_text = "\n".join(f"- {r}" for r in result.failed_rules)
        matched_text = "\n".join(f"- {r}" for r in result.matched_rules)
        if not model:
            return f"You meet almost all requirements for {result.name}, but currently miss one condition: {result.failed_rules[0] if result.failed_rules else 'Pending requirement'}."
        prompt = f"""You are a government welfare advisor. A citizen ALMOST qualifies for {result.name}.

Conditions they met:
{matched_text}

One condition they did NOT meet:
{failed_text}

Write exactly 2 sentences explaining why they almost qualify. Be factual and specific."""

    else:  # ineligible
        failed_text = "\n".join(f"- {r}" for r in result.failed_rules)
        if not model:
            return f"You do not qualify for {result.name} due to unmet statutory conditions: {', '.join(result.failed_rules)}."
        prompt = f"""You are a government welfare advisor. A citizen does NOT qualify for {result.name}.

Conditions they failed:
{failed_text}

Write exactly 1 sentence explaining why they are ineligible. Be factual. Do not suggest they appeal."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # Fallback to deterministic clean message if offline or quota reached
        if result.status == "eligible":
            return f"You meet all verified statutory requirements for {result.name}."
        elif result.status == "almost":
            return f"You qualify for most criteria but miss one specific condition: {result.failed_rules[0] if result.failed_rules else ''}."
        else:
            return f"You are currently ineligible for {result.name} based on official scheme rules."


def generate_almost_advice(result: SchemeResult) -> str:
    """
    For "almost" results only: generate concrete actionable steps to become eligible.
    """
    if result.status != "almost":
        return ""

    failed_text = "\n".join(f"- {r}" for r in result.failed_rules)
    hints_text = "\n".join(f"- {h}" for h in result.hints) if result.hints else "No specific hints available."
    model = get_model()

    if not model:
        if result.hints:
            return "Action needed: " + " ".join(result.hints)
        return f"Please resolve the following requirement: {result.failed_rules[0] if result.failed_rules else ''}."

    prompt = f"""You are a helpful government welfare officer helping a citizen become eligible for {result.name}.

The one condition they are failing:
{failed_text}

Official guidance on this condition:
{hints_text}

Write 2–3 specific, actionable steps this person can take to meet this condition.
Be practical. Mention specific document names or government offices (e.g., CSC center, Aaple Sarkar, Tahsildar) where relevant.
Do not give general advice. Focus strictly on resolving the failed condition."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        if result.hints:
            return " ".join(result.hints)
        return f"Verify your documents with the local Tahsildar or CSC center to resolve: {result.failed_rules[0] if result.failed_rules else ''}."
