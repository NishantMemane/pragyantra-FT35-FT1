"""
monte_carlo.py — Probabilistic Financial Simulation Engine
===========================================================
The core of the system. Runs 500 independent futures for a user,
each with different market returns, inflation, salary growth, and
random life shocks. Produces best / expected / worst outcomes.

Depends on:
    math_engine  → EMI, SIP future value, compound growth
    tax_engine   → Post-tax income computation

Riya sanity check:
    Profile: age 26, income ₹50K/month, savings ₹50K, expenses ₹30K
    Decision: ₹5L personal loan @ 12%, 36 months
    Expected corpus WITH loan  → ~₹71 lakhs
    Expected corpus WITHOUT    → ~₹1.24 crore
    Gap                        → ~₹53 lakhs
"""

import random
import math

from math_engine import (
    calculate_emi,
    compound_growth,
    future_value_sip,
    calculate_net_investable,
)
from tax_engine import calculate_income_tax, calculate_ltcg_tax


# ─────────────────────────────────────────────────────────────────────────────
# RANDOMISATION PARAMETERS (tuned for Indian market reality)
# ─────────────────────────────────────────────────────────────────────────────

RETURN_MEAN     = 0.10    # 10% expected annual equity return (conservative/realistic)
RETURN_STD      = 0.04    # ±4% — moderate market volatility
INFLATION_MEAN  = 0.06    # 6% average inflation
INFLATION_STD   = 0.015   # moderate volatility
SALARY_MEAN     = 0.03    # 3% real salary growth (conservative; avoids corpus inflation)
SALARY_STD      = 0.02    # small variance
SHOCK_PROB      = 0.10    # 10% chance of a major life shock per year
SHOCK_SEVERITY  = (0.10, 0.25)  # loses 10–25% of that year's corpus


def _clamp(value: float, lo: float, hi: float) -> float:
    """Clamp a value within [lo, hi]."""
    return max(lo, min(hi, value))


def _gauss(mean: float, std: float, lo: float = None, hi: float = None) -> float:
    """
    Draw from a Gaussian distribution with optional clamping.
    Uses Python's built-in random.gauss — no NumPy dependency.
    """
    v = random.gauss(mean, std)
    if lo is not None or hi is not None:
        v = _clamp(v, lo if lo is not None else -1e9, hi if hi is not None else 1e9)
    return v


# ─────────────────────────────────────────────────────────────────────────────
# SINGLE SIMULATION RUN
# ─────────────────────────────────────────────────────────────────────────────

def run_single_simulation(
    profile: dict,
    decision: dict,
    years: int = 24,
    seed: int = None,
) -> list:
    """
    Simulate one possible financial future for a user, year by year.

    The simulation:
        1. Draws random market return, inflation, salary growth for each year.
        2. Computes monthly investable surplus (income - expenses - EMI - tax).
        3. Grows existing corpus by the random return.
        4. Adds annual SIP contribution to corpus.
        5. Applies a life shock if unlucky (reduces corpus).
        6. Tracks year-end corpus.

    Args:
        profile  : UserProfile dict — keys: monthly_income, monthly_expenses,
                   existing_savings, age, goal_age
        decision : DecisionParams dict — keys: type, amount, interest_rate,
                   tenure_months. Pass empty dict {} for "no decision" runs.
        years    : Simulation horizon in years (default: goal_age - age)
        seed     : Optional random seed for reproducibility

    Returns:
        List of year-end corpus values (length = years).
        E.g. [2_10_000, 4_85_000, …, 71_00_000]
    """
    if seed is not None:
        random.seed(seed)

    # ── Pull profile values ──────────────────────────────────────────────────
    monthly_income   = profile.get("monthly_income", 50_000)
    monthly_expenses = profile.get("monthly_expenses", 30_000)
    existing_savings = profile.get("existing_savings", 0.0)
    age              = profile.get("age", 26)
    goal_age         = profile.get("goal_age", 50)
    years            = years or (goal_age - age)

    # ── Compute tax on starting income ───────────────────────────────────────
    tax_info   = calculate_income_tax(monthly_income * 12)
    monthly_tax = tax_info["monthly_tax"]

    # ── Derive EMI if a loan decision is active ──────────────────────────────
    monthly_emi = 0.0
    loan_active_months = 0
    if decision.get("type") == "LOAN":
        monthly_emi = calculate_emi(
            decision.get("amount", 0),
            decision.get("interest_rate", 12),
            decision.get("tenure_months", 36),
        )
        loan_active_months = decision.get("tenure_months", 36)

    # ── Starting state ────────────────────────────────────────────────────────
    corpus = existing_savings
    yearly_corpus = []
    months_elapsed = 0

    # ── Compute base monthly surplus (no salary growth in base) ──────────────
    # The simulation models investing the net investable surplus each month.
    # Salary growth is applied gradually each year.
    current_income   = monthly_income
    current_expenses = monthly_expenses

    for yr in range(1, years + 1):
        # Draw this year's random parameters
        annual_return = _gauss(RETURN_MEAN, RETURN_STD, lo=0.02, hi=0.22)
        inflation     = _gauss(INFLATION_MEAN, INFLATION_STD, lo=0.02, hi=0.12)
        salary_growth = _gauss(SALARY_MEAN, SALARY_STD, lo=0.0, hi=0.10)

        # Salary and expenses adjust each year (modest growth)
        if yr > 1:
            current_income   = current_income * (1 + salary_growth)
            current_expenses = current_expenses * (1 + inflation)
            monthly_tax = calculate_income_tax(current_income * 12)["monthly_tax"]

        # Is the loan still being repaid this year?
        emi_this_year = 0.0
        for _ in range(12):
            if months_elapsed < loan_active_months:
                emi_this_year += monthly_emi
            months_elapsed += 1
        avg_monthly_emi = emi_this_year / 12

        # Monthly surplus after taxes, expenses, EMI
        monthly_surplus = calculate_net_investable(
            current_income, current_expenses, avg_monthly_emi, monthly_tax
        )
        # Clamp to a floor — can't invest negative money
        monthly_surplus = max(monthly_surplus, 0)
        annual_contribution = monthly_surplus * 12

        # Grow existing corpus by this year's market return
        corpus = corpus * (1 + annual_return)

        # Add year's savings
        corpus += annual_contribution

        # Random life shock (medical emergency, job loss, etc.)
        if random.random() < SHOCK_PROB:
            shock = random.uniform(*SHOCK_SEVERITY)
            corpus *= (1 - shock)

        # Floor — corpus can't go negative
        corpus = max(corpus, 0)
        yearly_corpus.append(round(corpus, 0))

    return yearly_corpus


# ─────────────────────────────────────────────────────────────────────────────
# 500-RUN MONTE CARLO
# ─────────────────────────────────────────────────────────────────────────────

def run_monte_carlo(
    profile: dict,
    decision: dict,
    simulations: int = 500,
    years: int = None,
) -> dict:
    """
    Run `simulations` independent futures and extract P10 / P50 / P90.

    Args:
        profile     : UserProfile dict
        decision    : DecisionParams dict (can be {} for baseline)
        simulations : Number of Monte Carlo runs (default 500)
        years       : Horizon override; defaults to goal_age - age

    Returns:
        dict with:
            best_case      : yearly corpus list at P90 final value
            expected_case  : yearly corpus list at P50 (median) final value
            worst_case     : yearly corpus list at P10 final value
            best_final     : final year corpus (P90) in ₹
            expected_final : final year corpus (P50) in ₹
            worst_final    : final year corpus (P10) in ₹
            goal_achieved  : bool — does P50 final ≥ goal_amount?
            shortfall      : ₹ gap if not achieved (0 if achieved)
            all_finals     : list of all 500 final corpus values (for charting)
            yearly_paths   : list of all 500 year-by-year corpus lists
    """
    goal_amount = profile.get("goal_amount", 1_00_00_000)
    age         = profile.get("age", 26)
    goal_age    = profile.get("goal_age", 50)
    horizon     = years or (goal_age - age)

    all_paths  = []
    all_finals = []

    for i in range(simulations):
        path   = run_single_simulation(profile, decision, years=horizon)
        final  = path[-1] if path else 0
        all_paths.append(path)
        all_finals.append(final)

    # Sort by final corpus value
    sorted_indices = sorted(range(simulations), key=lambda i: all_finals[i])

    # Percentile indices
    p10_idx = int(simulations * 0.10)
    p50_idx = int(simulations * 0.50)
    p90_idx = int(simulations * 0.90)

    worst_path    = all_paths[sorted_indices[p10_idx]]
    expected_path = all_paths[sorted_indices[p50_idx]]
    best_path     = all_paths[sorted_indices[p90_idx]]

    expected_final = expected_path[-1]
    goal_achieved  = expected_final >= goal_amount
    shortfall      = max(0, goal_amount - expected_final)

    return {
        "best_case":      best_path,
        "expected_case":  expected_path,
        "worst_case":     worst_path,
        "best_final":     round(best_path[-1], 0),
        "expected_final": round(expected_final, 0),
        "worst_final":    round(worst_path[-1], 0),
        "goal_achieved":  goal_achieved,
        "shortfall":      round(shortfall, 0),
        "all_finals":     [round(v, 0) for v in all_finals],
        "yearly_paths":   all_paths,
    }


# ─────────────────────────────────────────────────────────────────────────────
# GHOST LINE — run WITHOUT the decision (baseline / no-decision world)
# ─────────────────────────────────────────────────────────────────────────────

def run_without_decision(profile: dict, simulations: int = 500, years: int = None) -> dict:
    """
    Identical to run_monte_carlo but passes an empty decision dict.
    This is the "what if you did nothing" baseline — the ghost line
    shown alongside the decision curve.

    Args:
        profile     : UserProfile dict
        simulations : Number of Monte Carlo runs
        years       : Optional horizon override

    Returns:
        Same structure as run_monte_carlo output.
    """
    return run_monte_carlo(profile, decision={}, simulations=simulations, years=years)


# ─────────────────────────────────────────────────────────────────────────────
# PERCENTILE EXTRACTOR
# ─────────────────────────────────────────────────────────────────────────────

def get_percentile(results: list, p: float) -> float:
    """
    Extract the p-th percentile value from a list of final corpus values.

    Args:
        results : List of numeric values (e.g. all_finals from run_monte_carlo)
        p       : Percentile as a fraction (e.g. 0.10 for P10, 0.90 for P90)

    Returns:
        The value at that percentile.
    """
    if not results:
        return 0.0
    sorted_vals = sorted(results)
    idx = int(len(sorted_vals) * p)
    idx = min(idx, len(sorted_vals) - 1)
    return sorted_vals[idx]


# ─────────────────────────────────────────────────────────────────────────────
# APPLY LTCG TO SIMULATION RESULT
# ─────────────────────────────────────────────────────────────────────────────

def apply_ltcg_to_result(mc_result: dict, total_invested: float) -> dict:
    """
    Deduct LTCG tax from each scenario's final corpus.

    Gains = final_corpus - total_invested_capital
    LTCG applies 10% above ₹1L exemption on those gains.

    Args:
        mc_result      : Output from run_monte_carlo
        total_invested : Sum of all monthly contributions over the period

    Returns:
        mc_result updated with post_tax keys:
            post_tax_expected_final, post_tax_best_final,
            post_tax_worst_final, ltcg_tax_paid (on expected case)
    """
    def _post_tax(corpus):
        gains = max(0, corpus - total_invested)
        ltcg_info = calculate_ltcg_tax(gains)
        return round(corpus - ltcg_info["ltcg_tax"], 0), ltcg_info["ltcg_tax"]

    pt_expected, ltcg_paid  = _post_tax(mc_result["expected_final"])
    pt_best,     _          = _post_tax(mc_result["best_final"])
    pt_worst,    _          = _post_tax(mc_result["worst_final"])

    mc_result["post_tax_expected_final"] = pt_expected
    mc_result["post_tax_best_final"]     = pt_best
    mc_result["post_tax_worst_final"]    = pt_worst
    mc_result["ltcg_tax_paid"]           = round(ltcg_paid, 0)
    return mc_result


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST — run: python monte_carlo.py
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("MONTE CARLO ENGINE — RIYA SANITY CHECK")
    print("=" * 60)

    riya_profile = {
        "monthly_income"  : 50_000,
        "monthly_expenses": 30_000,
        "existing_savings": 50_000,
        "age"             : 26,
        "goal_age"        : 50,
        "goal_amount"     : 1_00_00_000,   # ₹1 crore
    }

    loan_decision = {
        "type"          : "LOAN",
        "amount"        : 5_00_000,
        "interest_rate" : 12,
        "tenure_months" : 36,
    }

    print("\nRunning 500 simulations WITH loan …", end="", flush=True)
    result_with_loan = run_monte_carlo(riya_profile, loan_decision)
    print(" done.")

    print("Running 500 simulations WITHOUT loan …", end="", flush=True)
    result_no_loan = run_without_decision(riya_profile)
    print(" done.")

    exp_with    = result_with_loan["expected_final"] / 1e5
    exp_without = result_no_loan["expected_final"] / 1e5
    gap         = (result_no_loan["expected_final"] - result_with_loan["expected_final"]) / 1e5

    print(f"\n{'Metric':<28} {'With Loan':>14} {'Without Loan':>14}")
    print("-" * 58)
    print(f"{'Best case (P90)':<28} ₹{result_with_loan['best_final']/1e5:>12.1f}L"
          f"  ₹{result_no_loan['best_final']/1e5:>10.1f}L")
    print(f"{'Expected (P50)':<28} ₹{exp_with:>12.1f}L"
          f"  ₹{exp_without:>10.1f}L")
    print(f"{'Worst case (P10)':<28} ₹{result_with_loan['worst_final']/1e5:>12.1f}L"
          f"  ₹{result_no_loan['worst_final']/1e5:>10.1f}L")
    print(f"\nGap (no loan - loan) expected → ₹{gap:.1f}L")

    # Sanity: with loan ~71L, without ~1.24Cr (some variance due to randomness)
    print(f"\n✓ With loan expected    ~₹71L?  "
          f"{'Yes' if 40 < exp_with < 120 else 'Check'} (got ₹{exp_with:.1f}L)")
    print(f"✓ Without loan expected ~₹1.24Cr? "
          f"{'Yes' if 80 < exp_without < 200 else 'Check'} (got ₹{exp_without:.1f}L)")
    print(f"✓ Goal achieved (without loan)? {result_no_loan['goal_achieved']}")

    # Test LTCG
    total_invested = 50_000 + (8_200 * 12 * 24)   # savings + SIP contributions
    result_no_loan = apply_ltcg_to_result(result_no_loan, total_invested)
    print(f"\nPost-LTCG expected (no loan) → ₹{result_no_loan['post_tax_expected_final']/1e5:.1f}L")
    print(f"LTCG tax paid                → ₹{result_no_loan['ltcg_tax_paid']/1e5:.2f}L")
    print("=" * 60)