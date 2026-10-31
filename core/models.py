# core/models.py
from pydantic import BaseModel, Field
from typing import Optional, List


class CitizenProfile(BaseModel):
    """
    Represents the structured profile of a citizen applicant.
    All fields match what the frontend UI produces.
    """
    name: Optional[str] = "Applicant"
    age: int = Field(..., ge=0, le=120, description="Age in years")
    gender: str = Field(..., description="'male', 'female', or 'other'")
    annual_income: float = Field(..., ge=0, description="Annual household income in INR")
    caste_category: str = Field(..., description="'general', 'obc', 'sc', 'st', 'nt', 'vjnt'")
    land_holding_hectares: float = Field(default=0.0, ge=0, description="Agricultural land in hectares")
    occupation: str = Field(..., description="'farmer', 'laborer', 'salaried', 'self_employed', 'unemployed'")
    state: str = Field(default="Maharashtra")
    has_bank_account: bool = Field(default=True)
    has_aadhaar: bool = Field(default=True)
    owns_pucca_house: bool = Field(default=False)


class SchemeResult(BaseModel):
    """
    Result of evaluating one scheme against one CitizenProfile.
    This is what gets passed to the UI for rendering.
    """
    scheme_id: str
    name: str
    department: str
    status: str  # MUST BE: "eligible" | "almost" | "ineligible"
    matched_rules: List[str] = []   # Human-readable list of passing conditions
    failed_rules: List[str] = []    # Human-readable list of failing conditions
    hints: List[str] = []           # "Almost" guidance from schemes.json hints
    exclusions: List[str] = []      # Statutory exclusions from schemes.json (Babu Shield)
    explanation: str = ""           # AI-generated verdict explanation (filled by explainer.py)
    almost_advice: str = ""         # AI-generated remediation steps (only for "almost")
    source_url: str = ""            # Official government URL
    last_fetched: str = ""          # ISO timestamp - proves no mock data
    description: str = ""           # Scheme benefit description
