"""
models.py — ALL Pydantic data shapes for the entire application
================================================================
Defines every piece of data that flows through the system.
Every other file imports from here. No logic lives here — only structure.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


# ─────────────────────────────────────────────────────────────────────────────
# 1. USER PROFILE
# ─────────────────────────────────────────────────────────────────────────────

class UserProfile(BaseModel):
    age: int = Field(..., ge=18, le=70, description="Current age of the user")
    monthly_income: float = Field(..., gt=0, description="Gross monthly income in ₹")
    monthly_expenses: Optional[float] = Field(
        None, ge=0, description="Monthly expenses in ₹ — defaults to 60% of income"
    )
    existing_savings: Optional[float] = Field(
        0.0, ge=0, description="Existing savings / investment corpus in ₹"
    )
    goal_amount: float = Field(..., gt=0, description="Target corpus amount in ₹")
    goal_age: int = Field(..., ge=19, le=80, description="Age by which goal must be met")


# ─────────────────────────────────────────────────────────────────────────────
# 2. DECISION PARAMS
# ─────────────────────────────────────────────────────────────────────────────

class DecisionParams(BaseModel):
    type: str = Field(
        ..., description="LOAN | SIP | DELAY | LUMPSUM | HOME_LOAN"
    )
    amount: Optional[float] = Field(None, ge=0, description="Loan or lump-sum amount in ₹")
    interest_rate: Optional[float] = Field(None, ge=0, description="Annual interest rate %")
    tenure_months: Optional[int] = Field(None, ge=1, description="Loan tenure in months")
    monthly_emi: Optional[float] = Field(None, ge=0, description="Pre-calculated EMI in ₹")
    cash_flow_reduction: Optional[float] = Field(
        None, ge=0, description="Monthly cash-flow reduction in ₹"
    )
    monthly_sip: Optional[float] = Field(None, ge=0, description="Monthly SIP amount in ₹")
    delay_years: Optional[int] = Field(None, ge=0, description="Years of delay for DELAY type")
    instrument: Optional[str] = Field(
        "equity", description="Investment instrument: equity | fd"
    )


# ─────────────────────────────────────────────────────────────────────────────
# 3. SIMULATION RESULT (FORWARD)
# ─────────────────────────────────────────────────────────────────────────────

class SimulationResult(BaseModel):
    labels: List[int] = Field(..., description="Year / age labels for the X-axis")
    best_case: List[float] = Field(..., description="P90 corpus curve (yearly)")
    expected_case: List[float] = Field(..., description="P50 corpus curve (yearly)")
    worst_case: List[float] = Field(..., description="P10 corpus curve (yearly)")
    without_decision: List[float] = Field(
        ..., description="Ghost line — corpus without the decision"
    )
    best_final: float = Field(..., description="Final corpus at goal age — best case (₹)")
    expected_final: float = Field(..., description="Final corpus at goal age — expected (₹)")
    worst_final: float = Field(..., description="Final corpus at goal age — worst case (₹)")
    goal_achieved: bool = Field(..., description="True if expected_final ≥ goal_amount")
    shortfall: float = Field(..., description="₹ gap between expected final and goal (0 if achieved)")
    post_tax_expected_final: float = Field(
        ..., description="Expected final corpus after LTCG tax (₹)"
    )
    ltcg_tax_paid: float = Field(..., description="LTCG tax deducted (₹)")
    story: str = Field(..., description="AI-generated 3-sentence narrative from Ollama")


# ─────────────────────────────────────────────────────────────────────────────
# 4. REVERSE RESULT
# ─────────────────────────────────────────────────────────────────────────────

class ReverseResult(BaseModel):
    required_monthly_sip: float = Field(
        ..., description="Monthly SIP needed starting today (₹)"
    )
    if_delayed_2_years: float = Field(
        ..., description="Monthly SIP if starting 2 years later (₹)"
    )
    if_delayed_5_years: float = Field(
        ..., description="Monthly SIP if starting 5 years later (₹)"
    )
    existing_savings_growth: float = Field(
        ..., description="Value of existing savings at goal date (₹)"
    )
    total_contribution: float = Field(
        ..., description="Total SIP contributions over the horizon (₹)"
    )
    total_returns: float = Field(
        ..., description="Investment gains beyond contributions (₹)"
    )
    story: str = Field(..., description="AI-generated 3-sentence narrative from Ollama")


# ─────────────────────────────────────────────────────────────────────────────
# 5. PROFILE RESPONSE
# ─────────────────────────────────────────────────────────────────────────────

class ProfileResponse(BaseModel):
    post_tax_monthly_income: float = Field(
        ..., description="Take-home income after income tax (₹/month)"
    )
    monthly_tax: float = Field(..., description="Monthly income tax deduction (₹)")
    investable_amount: float = Field(
        ..., description="Net monthly surplus available for investment (₹)"
    )
    profile_confirmed: bool = Field(default=True)


# ─────────────────────────────────────────────────────────────────────────────
# 6. ORCHESTRATION REQUEST / RESPONSE
# ─────────────────────────────────────────────────────────────────────────────

class OrchestrationRequest(BaseModel):
    message: str = Field(..., description="Free-text message from the user")
    profile: Optional[UserProfile] = Field(
        None, description="User profile if already collected"
    )


class OrchestrationResponse(BaseModel):
    route: str = Field(..., description="FORWARD | REVERSE | CLARIFY")
    decision_type: Optional[str] = Field(
        None, description="LOAN | SIP | LUMPSUM | DELAY — only for FORWARD route"
    )
    question: Optional[str] = Field(
        None, description="Clarifying question to ask user — only for CLARIFY route"
    )
