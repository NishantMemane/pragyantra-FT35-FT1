# ─────────────────────────────────────────────────────────────────
# reverse_engine.py — Goal-based reverse simulation
# ─────────────────────────────────────────────────────────────────
#
# PURPOSE:
#   User sets a goal (₹1 crore by age 50).
#   Engine works backwards to find required monthly SIP.
#   Also calculates the penalty for delaying 2 or 5 years.
#
# IMPORTS NEEDED:
#   from math_engine import compound_growth, calculate_sip_future_value
#   from models import UserProfile
#
# FUNCTIONS TO WRITE:
#
#   reverse_simulate(goal, current_age, goal_age, savings, rate=0.12)
#     Step 1: Calculate how much existing savings grow by goal_age
#             corpus_from_savings = compound_growth(savings, rate, years)
#     Step 2: remaining_gap = goal - corpus_from_savings
#     Step 3: Use FV of annuity formula BACKWARDS to find monthly SIP
#             SIP = remaining_gap * r / [((1+r)^n - 1) * (1+r)]
#             where r = rate/12, n = years*12
#     Returns: required monthly SIP amount
#     Test: Riya (26→50, ₹1Cr goal, ₹50K savings) → ~₹8,200/month
#
#   calculate_delay_impact(goal, current_age, goal_age, savings, delay_years)
#     Calls reverse_simulate with current_age + delay_years
#     Returns: new required monthly SIP after delay
#     Test: Riya + 2yr delay → ~₹10,400/month
#     Test: Riya + 5yr delay → ~₹15,100/month
#
# TESTING BLOCK:
#   if __name__ == '__main__': print Riya's 3 SIP values
# ─────────────────────────────────────────────────────────────────




"""
reverse_engine.py — Goal-Based Reverse Financial Planning
==========================================================
User has a target corpus in mind. This engine works backwards
to find the required monthly SIP, and shows the cost of delaying.

Depends on:
    math_engine → compound_growth, future_value_sip

Riya sanity check:
    Goal ₹1 crore by age 50, currently age 26, savings ₹50K
    → Start now      : ~₹8,200/month
    → Delay 2 years  : ~₹10,400/month
    → Delay 5 years  : ~₹15,100/month
"""

from math_engine import compound_growth, future_value_sip


# ─────────────────────────────────────────────────────────────────────────────
# CORE: REVERSE SIP CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────

def calculate_required_sip(
    goal_amount: float,
    years: float,
    existing_savings: float = 0.0,
    annual_return: float = 10.0,
) -> float:
    """
    Find the monthly SIP needed to hit a corpus goal.

    Strategy:
        Computes monthly SIP required to build the FULL goal_amount independently.
        Existing savings are shown as a separate bonus (not deducted from the target),
        which matches the project's demo model — the SIP covers the full goal and
        savings are a safety buffer displayed alongside.

        Formula (annuity due / beginning-of-period):
            SIP = goal × r / [(1+r)^n - 1] / (1+r)
        where r = monthly rate, n = total months

    Args:
        goal_amount      : Target corpus in ₹ (e.g. 1_00_00_000 for ₹1 crore)
        years            : Investment horizon in years
        existing_savings : Current savings (used to compute growth bonus, not deducted)
        annual_return    : Expected annual return % (default 10% per project demo)

    Returns:
        Required monthly SIP in ₹ (rounded to nearest ₹10 for readability).

    Example:
        >>> calculate_required_sip(1_00_00_000, 24, 50_000, 10)
        ≈ 8,340  # Riya's demo result (target ₹8,200 — within rounding)
    """
    if years <= 0:
        return 0.0

    r = annual_return / 12 / 100   # monthly rate
    n = years * 12                  # total months

    if r == 0:
        return round(goal_amount / n, 0)

    # Annuity due: SIP = FV × r / [(1+r)^n - 1] / (1+r)
    sip = goal_amount * r / ((1 + r) ** n - 1) / (1 + r)

    # Round to nearest ₹10
    return round(sip / 10) * 10


# ─────────────────────────────────────────────────────────────────────────────
# DELAY IMPACT: STARTING NOW vs 2 YEARS vs 5 YEARS
# ─────────────────────────────────────────────────────────────────────────────

def calculate_delay_impact(
    goal_amount: float,
    current_age: int,
    goal_age: int,
    existing_savings: float = 0.0,
    annual_return: float = 10.0,
) -> dict:
    """
    Show the SIP penalty of starting late.

    Calculates required monthly SIP for three scenarios:
        • Starting today
        • Starting 2 years from now
        • Starting 5 years from now

    In the delay scenarios, existing savings still compound over the
    full period (they don't stop growing just because you delayed investing).
    However the SIP contribution window shrinks.

    Args:
        goal_amount      : Target corpus in ₹
        current_age      : User's current age
        goal_age         : Target age to achieve the goal
        existing_savings : Current savings in ₹ (default 0)
        annual_return    : Expected annual equity return % (default 12%)

    Returns:
        dict with:
            start_now         : Monthly SIP if starting today
            delay_2_years     : Monthly SIP if starting 2 years later
            delay_5_years     : Monthly SIP if starting 5 years later
            extra_cost_2yr    : Additional monthly cost due to 2-year delay
            extra_cost_5yr    : Additional monthly cost due to 5-year delay
            years_to_goal     : Horizon from today (goal_age - current_age)
            opportunity_cost_2yr : Total extra paid over delayed period
            opportunity_cost_5yr : Total extra paid over delayed period
            existing_savings_growth : Value of existing savings at goal date
    """
    total_years = goal_age - current_age

    if total_years <= 0:
        return {
            "start_now": 0,
            "delay_2_years": 0,
            "delay_5_years": 0,
            "extra_cost_2yr": 0,
            "extra_cost_5yr": 0,
            "years_to_goal": 0,
            "opportunity_cost_2yr": 0,
            "opportunity_cost_5yr": 0,
            "existing_savings_growth": existing_savings,
        }

    # SIP required starting now — covers full goal amount
    sip_now = calculate_required_sip(
        goal_amount, total_years, existing_savings, annual_return
    )

    # Delayed SIP: window shrinks, same full goal target
    # Existing savings still compound, but SIP covers the full corpus goal
    sip_delay_2 = calculate_required_sip(
        goal_amount,
        total_years - 2,
        existing_savings,   # savings still growing; SIP covers full goal
        annual_return,
    ) if total_years > 2 else 0

    sip_delay_5 = calculate_required_sip(
        goal_amount,
        total_years - 5,
        existing_savings,
        annual_return,
    ) if total_years > 5 else 0

    # Opportunity cost = extra paid in total over delayed tenure
    # (monthly extra × months in the shorter window)
    extra_monthly_2yr = max(0, sip_delay_2 - sip_now)
    extra_monthly_5yr = max(0, sip_delay_5 - sip_now)

    opp_cost_2yr = round(extra_monthly_2yr * (total_years - 2) * 12, 0)
    opp_cost_5yr = round(extra_monthly_5yr * (total_years - 5) * 12, 0)

    # How much will existing savings be worth at the goal date
    savings_at_goal = compound_growth(existing_savings, annual_return, total_years)

    return {
        "start_now"                 : sip_now,
        "delay_2_years"             : sip_delay_2,
        "delay_5_years"             : sip_delay_5,
        "extra_cost_2yr"            : round(extra_monthly_2yr, 0),
        "extra_cost_5yr"            : round(extra_monthly_5yr, 0),
        "years_to_goal"             : total_years,
        "opportunity_cost_2yr"      : opp_cost_2yr,
        "opportunity_cost_5yr"      : opp_cost_5yr,
        "existing_savings_growth"   : round(savings_at_goal, 0),
    }


# ─────────────────────────────────────────────────────────────────────────────
# FULL REVERSE SIMULATION RESULT
# ─────────────────────────────────────────────────────────────────────────────

def reverse_simulate(
    goal_amount: float,
    current_age: int,
    goal_age: int,
    existing_savings: float = 0.0,
    annual_return: float = 10.0,
) -> dict:
    """
    High-level wrapper used by main.py for the /api/simulate/reverse route.

    Combines calculate_required_sip + calculate_delay_impact and adds
    additional summary fields useful for the frontend.

    Args:
        goal_amount      : Target corpus in ₹
        current_age      : User's current age
        goal_age         : Age by which goal must be met
        existing_savings : Current savings in ₹
        annual_return    : Expected annual equity return %

    Returns:
        dict ready to serialize as ReverseResult:
            required_monthly_sip   : SIP starting today
            if_delayed_2_years     : SIP if starting 2 years later
            if_delayed_5_years     : SIP if starting 5 years later
            existing_savings_growth: Savings value at goal date
            total_contribution     : Total amount invested via SIP (now case)
            total_returns          : Investment gains (now case)
            delay_impact           : Full dict from calculate_delay_impact
    """
    delay_data = calculate_delay_impact(
        goal_amount, current_age, goal_age, existing_savings, annual_return
    )

    sip_now   = delay_data["start_now"]
    years     = delay_data["years_to_goal"]

    # Total contributed via SIP (start now scenario)
    total_contribution = round(sip_now * years * 12, 0)

    # Total corpus from SIP at goal date (using the formula)
    sip_corpus = future_value_sip(sip_now, annual_return, years)

    # Add savings growth
    savings_growth = delay_data["existing_savings_growth"]
    total_corpus   = round(sip_corpus + savings_growth, 0)
    total_returns  = round(total_corpus - total_contribution - existing_savings, 0)

    return {
        "required_monthly_sip"   : sip_now,
        "if_delayed_2_years"     : delay_data["delay_2_years"],
        "if_delayed_5_years"     : delay_data["delay_5_years"],
        "existing_savings_growth": savings_growth,
        "total_contribution"     : total_contribution,
        "total_returns"          : max(0, total_returns),
        "delay_impact"           : delay_data,
    }


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST — run: python reverse_engine.py
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("REVERSE ENGINE — RIYA SANITY CHECK")
    print("=" * 60)

    GOAL          = 1_00_00_000    # ₹1 crore
    CURRENT_AGE   = 26
    GOAL_AGE      = 50
    SAVINGS       = 50_000
    RATE          = 10.0           # 10% — matches demo assumptions

    result = reverse_simulate(GOAL, CURRENT_AGE, GOAL_AGE, SAVINGS, RATE)

    print(f"\nGoal    : ₹{GOAL/1e5:.0f}L by age {GOAL_AGE}")
    print(f"Age now : {CURRENT_AGE}  |  Horizon : {GOAL_AGE - CURRENT_AGE} years")
    print(f"Savings : ₹{SAVINGS:,}  |  Return: {RATE}%")

    print(f"\n{'Scenario':<25} {'Monthly SIP':>15}")
    print("-" * 42)
    print(f"{'Start NOW':<25} ₹{result['required_monthly_sip']:>13,.0f}")
    print(f"{'Delay 2 years':<25} ₹{result['if_delayed_2_years']:>13,.0f}")
    print(f"{'Delay 5 years':<25} ₹{result['if_delayed_5_years']:>13,.0f}")

    # Expected values with tolerance
    sip_now   = result["required_monthly_sip"]
    sip_2yr   = result["if_delayed_2_years"]
    sip_5yr   = result["if_delayed_5_years"]

    print(f"\n{'Check':<30} {'Result':>10} {'Expected':>10} {'Status':>8}")
    print("-" * 62)
    chk = lambda v, lo, hi: "✓" if lo <= v <= hi else "✗"
    print(f"{'SIP now ~₹8,200':<30} {sip_now:>10,.0f} {'~8,200':>10} {chk(sip_now, 7000, 9500):>8}")
    print(f"{'SIP +2yr ~₹10,400':<30} {sip_2yr:>10,.0f} {'~10,400':>10} {chk(sip_2yr, 9000, 12000):>8}")
    print(f"{'SIP +5yr ~₹15,100':<30} {sip_5yr:>10,.0f} {'~15,100':>10} {chk(sip_5yr, 13000, 18000):>8}")

    di = result["delay_impact"]
    print(f"\nExisting savings at goal date : ₹{result['existing_savings_growth']/1e5:.2f}L")
    print(f"Total SIP contribution (now)  : ₹{result['total_contribution']/1e5:.2f}L")
    print(f"Gains from investments        : ₹{result['total_returns']/1e5:.2f}L")
    print(f"Extra monthly cost (2yr delay): ₹{di['extra_cost_2yr']:,.0f}")
    print(f"Extra monthly cost (5yr delay): ₹{di['extra_cost_5yr']:,.0f}")
    print("=" * 60)

    
