# core/explainer.py
"""Plain-language AI explainability and actionable remediation engine powered by Gemini.

Translates deterministic rule results into simple, spoken English tailored for rural citizens and TTS narration.
"""
import os
from dotenv import load_dotenv
from core.models import SchemeResult

load_dotenv()


# ── API Key: supports both Streamlit Cloud secrets and local .env ─────────
def _get_api_key() -> str:
    """Read GEMINI_API_KEY from st.secrets (Cloud) or .env (local)."""
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "")


# Safely import Gemini — falls back to deterministic messages if package missing
try:
    import google.generativeai as genai
    _initial_key = _get_api_key()
    if _initial_key:
        genai.configure(api_key=_initial_key)
    _GENAI_AVAILABLE = True
except Exception:
    genai = None  # type: ignore
    _GENAI_AVAILABLE = False


def get_model():
    """Lazily initialize and return the generative model if configured."""
    if not _GENAI_AVAILABLE:
        return None
    api_key = _get_api_key()
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        return None


def generate_explanation(result: SchemeResult) -> str:
    """
    Generate a plain-spoken explanation of WHY the citizen got this result.
    Tailored for rural citizens and speech-synthesized audio narration (Class 10 reading level).
    """
    model = get_model()

    if result.status == "eligible":
        rules_text = "\n".join(f"- {r}" for r in result.matched_rules)
        if not model:
            return f"Good news! You qualify for {result.name}. Your details match all government rules for this scheme."

        prompt = f"""You are a friendly government welfare helper explaining a result to a rural citizen.

The citizen qualifies for {result.name}.

Conditions they met:
{rules_text}

Write 2 short, simple sentences in plain spoken English that a person with Class 10 education can easily understand when it is read aloud to them.
Use simple, everyday words. No legal terms. No jargon.
Start with: "Good news! You qualify for {result.name}."
Keep each sentence under 20 words."""

    elif result.status == "almost":
        failed_text = "\n".join(f"- {r}" for r in result.failed_rules)
        matched_text = "\n".join(f"- {r}" for r in result.matched_rules)
        if not model:
            missed_summary = ", ".join(result.failed_rules) if result.failed_rules else "one document condition"
            return f"You are very close to qualifying for {result.name}! You only need to complete: {missed_summary}."

        prompt = f"""You are a friendly government welfare helper talking to a rural citizen.

They almost qualify for {result.name}.
Conditions they met:
{matched_text}

Conditions they missed:
{failed_text}

Write 2 short, simple sentences in plain spoken English encouraging them. 
Tell them they are very close and clearly mention what condition is pending.
No legal terms. Under 20 words per sentence."""

    else:  # ineligible
        failed_text = "\n".join(f"- {r}" for r in result.failed_rules)
        if not model:
            reasons = "; ".join(result.failed_rules) if result.failed_rules else "official rule criteria"
            return f"You do not qualify for {result.name} at this time because: {reasons}."

        prompt = f"""You are a friendly government welfare helper.

The citizen does not qualify for {result.name}.
Reasons:
{failed_text}

Write exactly 1 simple sentence in plain spoken English explaining why.
No legal terms. Under 20 words. Be kind, honest, and factual."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        if result.status == "eligible":
            return f"Good news! You qualify for {result.name}. Your details match all government rules."
        elif result.status == "almost":
            missed_summary = ", ".join(result.failed_rules) if result.failed_rules else "pending condition"
            return f"You are very close to qualifying for {result.name}! The only pending item is: {missed_summary}."
        else:
            return f"You do not qualify for {result.name} based on current official guidelines."


def generate_almost_advice(result: SchemeResult) -> str:
    """
    For "almost" results: generate practical, high-empathy remediation steps.
    Highlights the financial maximizer, shows all unmet conditions, and provides low-friction local action.
    """
    if result.status != "almost":
        return ""

    failed_text = "\n".join(f"- {r}" for r in result.failed_rules)
    hints_text = "\n".join(f"- {h}" for h in result.hints) if result.hints else "Visit your nearest Gram Panchayat or CSC center."
    model = get_model()

    if not model:
        all_hints = " ".join(result.hints) if result.hints else "Ask your local Gram Sevak or visit the nearest Aaple Sarkar Seva Kendra."
        return f"You are very close to this benefit! Here is what to do: {all_hints} It is free of cost — do not pay any agents."

    prompt = f"""You are an empathetic, practical rural welfare counselor in Maharashtra talking to a citizen.

Scheme: {result.name}
Benefit: {result.description}

All conditions they currently miss:
{failed_text}

Official department guidance & shortcuts:
{hints_text}

Write 2 to 3 very simple sentences in plain spoken English telling them exactly what to do.
Guidelines:
1. Speak warmly like you are talking in person. No legal jargon.
2. Clearly mention what they need to resolve so there are no surprises.
3. Tell them the easiest local place to go (e.g. Gram Panchayat, Gram Sevak, or Aaple Sarkar Seva Kendra).
4. Mention that government enrollment is free and advise them not to pay brokers or touts.
5. Keep the total response under 50 words so it sounds natural when read aloud."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        if result.hints:
            return " ".join(result.hints) + " Visit your local Gram Panchayat office; this service is free."
        return f"Please resolve the pending requirement with your local Gram Sevak: {', '.join(result.failed_rules)}."
