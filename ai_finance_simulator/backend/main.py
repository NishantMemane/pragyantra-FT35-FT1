# ─────────────────────────────────────────────────────────────────
# main.py — FastAPI application, all routes wired together
# ─────────────────────────────────────────────────────────────────
# PURPOSE:
#   Entry point for the entire backend. Creates the FastAPI app,
#   sets up CORS, defines all 4 routes, and calls the right
#   engines in the right order for each route.
#
# RUN COMMAND:
#   uvicorn main:app --reload --port 8000   (run from backend/ dir)
#   Docs available at: http://localhost:8000/docs
# ─────────────────────────────────────────────────────────────────

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models import (
    UserProfile,
    DecisionParams,
    SimulationResult,
    ReverseResult,
    ProfileResponse,
    OrchestrationRequest,
    OrchestrationResponse,
)
from tax_engine import (
    calculate_income_tax,
    calculate_ltcg_tax,
    calculate_home_loan_benefit,
)
from math_engine import (
    calculate_emi,
    calculate_net_investable,
)
from monte_carlo import (
    run_monte_carlo,
    run_without_decision,
)
from reverse_engine import reverse_simulate
from ollama_engine import get_story
from orchestrator import smart_orchestrate


# ─────────────────────────────────────────────────────────────────
#  Composite request bodies for simulation routes
# ─────────────────────────────────────────────────────────────────

class ForwardSimulationRequest(BaseModel):
    profile: UserProfile
    decision: DecisionParams


class ReverseSimulationRequest(BaseModel):
    profile: UserProfile


# ─────────────────────────────────────────────────────────────────
#  App + CORS
# ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="AI Finance Simulator",
    version="1.0",
    description="Monte Carlo financial simulation engine with Indian tax rules and AI storytelling.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────────
#  Shared helpers
# ─────────────────────────────────────────────────────────────────

def resolve_expenses(profile: UserProfile) -> float:
    """Default monthly_expenses to 60 % of income when not provided."""
    if profile.monthly_expenses is None:
        return profile.monthly_income * 0.6
    return profile.monthly_expenses


def profile_to_dict(profile: UserProfile) -> dict:
    """Convert Pydantic UserProfile → plain dict for simulation engines."""
    return {
        "age":              profile.age,
        "monthly_income":   profile.monthly_income,
        "monthly_expenses": resolve_expenses(profile),
        "existing_savings": profile.existing_savings or 0.0,
        "goal_amount":      profile.goal_amount,
        "goal_age":         profile.goal_age,
    }


def decision_to_dict(decision: DecisionParams) -> dict:
    """Convert Pydantic DecisionParams → plain dict for simulation engines."""
    return {
        "type":                decision.type,
        "amount":              decision.amount or 0.0,
        "interest_rate":       decision.interest_rate or 0.0,
        "tenure_months":       decision.tenure_months or 0,
        "monthly_emi":         decision.monthly_emi or 0.0,
        "cash_flow_reduction": decision.cash_flow_reduction or 0.0,
        "monthly_sip":         decision.monthly_sip or 0.0,
        "delay_years":         decision.delay_years or 0,
        "instrument":          decision.instrument or "equity",
    }


def pad_or_trim(curve: list, length: int) -> list:
    """Ensure a corpus curve is exactly `length` elements."""
    if len(curve) >= length:
        return curve[:length]
    last = curve[-1] if curve else 0.0
    return curve + [last] * (length - len(curve))


# ─────────────────────────────────────────────────────────────────
#  Route 1 — POST /api/profile
# ─────────────────────────────────────────────────────────────────

@app.post("/api/profile", response_model=ProfileResponse)
def profile_route(profile: UserProfile):
    """
    Accept a user profile, return post-tax income and investable surplus.
    """
    try:
        expenses = resolve_expenses(profile)

        tax_info    = calculate_income_tax(profile.monthly_income * 12)
        monthly_tax = tax_info["monthly_tax"]

        post_tax_income = profile.monthly_income - monthly_tax
        investable = calculate_net_investable(
            profile.monthly_income, expenses,
            monthly_emi=0.0, monthly_tax=monthly_tax,
        )

        return ProfileResponse(
            post_tax_monthly_income=round(post_tax_income, 2),
            monthly_tax=round(monthly_tax, 2),
            investable_amount=round(investable, 2),
            profile_confirmed=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────
#  Route 2 — POST /api/orchestrate
# ─────────────────────────────────────────────────────────────────

@app.post("/api/orchestrate", response_model=OrchestrationResponse)
def orchestrate_route(request: OrchestrationRequest):
    """
    Route a free-text user message to FORWARD / REVERSE / CLARIFY.
    Uses keyword matching first, falls back to Ollama for unclear cases.
    """
    try:
        profile_dict = profile_to_dict(request.profile) if request.profile else None
        result = smart_orchestrate(request.message, profile_dict)

        return OrchestrationResponse(
            route=result["route"],
            decision_type=result.get("decision_type"),
            question=result.get("question"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────
#  Route 3 — POST /api/simulate/forward
# ─────────────────────────────────────────────────────────────────

@app.post("/api/simulate/forward", response_model=SimulationResult)
def simulate_forward(request: ForwardSimulationRequest):
    """
    Run 500 Monte Carlo paths WITH and WITHOUT the decision.
    Applies Indian tax engine. Returns corpus curves + AI story.
    """
    try:
        profile  = request.profile
        decision = request.decision
        expenses = resolve_expenses(profile)

        # ── Step 1: Income tax ───────────────────────────────────
        tax_info    = calculate_income_tax(profile.monthly_income * 12)
        monthly_tax = tax_info["monthly_tax"]

        # ── Step 2: EMI calculation for LOAN decisions ───────────
        emi = 0.0
        if decision.type == "LOAN":
            if decision.monthly_emi and decision.monthly_emi > 0:
                emi = decision.monthly_emi
            elif decision.amount and decision.interest_rate and decision.tenure_months:
                emi = calculate_emi(
                    decision.amount,
                    decision.interest_rate,
                    decision.tenure_months,
                )
            # Write back so simulation engines see the computed EMI
            decision.monthly_emi = emi
            decision.cash_flow_reduction = emi

        # ── Step 3: Home loan tax benefit (old regime — logged only)
        if decision.type in ("LOAN", "HOME_LOAN") and decision.interest_rate and decision.amount:
            annual_interest = decision.amount * (decision.interest_rate / 100)
            _benefit = calculate_home_loan_benefit(
                annual_interest, profile.monthly_income * 12
            )
            # Not deducted under new regime — kept for audit trail.

        # ── Step 4: Build plain dicts for simulation engines ─────
        profile_dict  = profile_to_dict(profile)
        decision_dict = decision_to_dict(decision)

        years  = profile.goal_age - profile.age
        labels = list(range(profile.age, profile.goal_age + 1))

        # ── Step 5: 500 simulations WITH decision ────────────────
        mc_with = run_monte_carlo(profile_dict, decision_dict, simulations=500)

        # ── Step 6: 500 simulations WITHOUT decision (ghost) ─────
        mc_without = run_without_decision(profile_dict, simulations=500)

        # ── Step 7: Extract yearly corpus curves ─────────────────
        best_curve     = pad_or_trim(mc_with["best_case"],       len(labels))
        expected_curve = pad_or_trim(mc_with["expected_case"],   len(labels))
        worst_curve    = pad_or_trim(mc_with["worst_case"],      len(labels))
        ghost_curve    = pad_or_trim(mc_without["expected_case"], len(labels))

        best_final     = mc_with["best_final"]
        expected_final = mc_with["expected_final"]
        worst_final    = mc_with["worst_final"]
        goal_achieved  = mc_with["goal_achieved"]
        shortfall      = mc_with["shortfall"]

        # ── Step 8: Apply LTCG tax on expected final corpus ──────
        net_monthly   = calculate_net_investable(
            profile.monthly_income, expenses, emi, monthly_tax
        )
        total_invested = (profile.existing_savings or 0.0) + net_monthly * 12 * years
        gains          = max(0.0, expected_final - total_invested)
        ltcg_info      = calculate_ltcg_tax(gains)
        ltcg_tax       = ltcg_info["ltcg_tax"]
        post_tax_final = expected_final - ltcg_tax

        # ── Step 9: AI narrative from Ollama ─────────────────────
        result_dict = {
            "best_final":     best_final,
            "expected_final": expected_final,
            "worst_final":    worst_final,
            "goal_achieved":  goal_achieved,
            "shortfall":      shortfall,
        }
        story = get_story(
            profile_dict, result_dict,
            decision=decision_dict, mode="forward",
        )

        return SimulationResult(
            labels=labels,
            best_case=[float(v) for v in best_curve],
            expected_case=[float(v) for v in expected_curve],
            worst_case=[float(v) for v in worst_curve],
            without_decision=[float(v) for v in ghost_curve],
            best_final=float(best_final),
            expected_final=float(expected_final),
            worst_final=float(worst_final),
            goal_achieved=goal_achieved,
            shortfall=float(shortfall),
            post_tax_expected_final=round(float(post_tax_final), 2),
            ltcg_tax_paid=round(float(ltcg_tax), 2),
            story=story,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────
#  Route 4 — POST /api/simulate/reverse
# ─────────────────────────────────────────────────────────────────

@app.post("/api/simulate/reverse", response_model=ReverseResult)
def simulate_reverse(request: ReverseSimulationRequest):
    """
    Work backwards from the goal to compute required monthly SIP.
    Shows penalty for delaying 2 or 5 years. Returns AI story.
    """
    try:
        profile      = request.profile
        profile_dict = profile_to_dict(profile)

        # ── Reverse simulation ────────────────────────────────────
        result = reverse_simulate(
            goal_amount=profile.goal_amount,
            current_age=profile.age,
            goal_age=profile.goal_age,
            existing_savings=profile.existing_savings or 0.0,
        )

        # ── AI narrative ──────────────────────────────────────────
        story = get_story(
            profile_dict, result,
            decision=None, mode="reverse",
        )

        return ReverseResult(
            required_monthly_sip=round(float(result["required_monthly_sip"]), 0),
            if_delayed_2_years=round(float(result["if_delayed_2_years"]), 0),
            if_delayed_5_years=round(float(result["if_delayed_5_years"]), 0),
            existing_savings_growth=round(float(result["existing_savings_growth"]), 0),
            total_contribution=round(float(result["total_contribution"]), 0),
            total_returns=round(float(result["total_returns"]), 0),
            story=story,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)