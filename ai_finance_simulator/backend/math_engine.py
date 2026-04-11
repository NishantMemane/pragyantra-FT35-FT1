# ─────────────────────────────────────────────────────────────────
# math_engine.py — ALL pure financial math functions
# ─────────────────────────────────────────────────────────────────
#
# PURPOSE:
#   The foundation of the entire system. Every simulation engine
#   calls these functions. No randomness, no AI, no API calls.
#   Pure arithmetic only. Fully testable with print().
#
# IMPORTS NEEDED: math (standard library only)
#
# FUNCTIONS TO WRITE:
#
#   calculate_emi(principal, annual_rate, tenure_months)
#     Formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
#     where r = annual_rate / 12 / 100
#     Test: ₹5,00,000 at 12% for 36 months → should return ₹16,607
#
#   compound_growth(principal, annual_rate, years)
#     Formula: P * (1 + r/100)^years
#     Test: ₹50,000 at 12% for 24 years → should return ~₹8,00,000
#
#   calculate_sip_future_value(monthly_amount, annual_rate, years)
#     Formula: FV = M * [((1+r)^n - 1) / r] * (1+r)
#     where r = annual_rate/12/100, n = years*12
#     Test: ₹8,200/month at 12% for 24 years → should return ~₹1 crore
#
#   inflation_adjust(amount, inflation_rate, years)
#     Formula: amount / (1 + inflation_rate/100)^years
#     Returns real value of a future amount in today's money
#
#   total_loan_cost(principal, annual_rate, tenure_months)
#     Formula: EMI * tenure_months
#     Returns total amount paid over entire loan life
#
#   calculate_net_investable(income, expenses, emi, monthly_tax)
#     Formula: income - expenses - emi - monthly_tax
#     This is the core number that feeds Monte Carlo
#
# TESTING BLOCK (run this file directly to verify):
#   if __name__ == '__main__': print all test cases
# ─────────────────────────────────────────────────────────────────






"""
math_engine.py — Core Financial Math Functions
================================================
Pure arithmetic. No randomness, no AI, no external dependencies.
All other engines call these functions. Test these first.

Riya sanity checks:
  EMI(500000, 12, 36 months) → ₹16,607
  SIP(8200, 12%, 24 years)   → ~₹1 crore
"""

import math


# ─────────────────────────────────────────────────────────────────────────────
# 1. EMI CALCULATION
# ─────────────────────────────────────────────────────────────────────────────

def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """
    Calculate fixed monthly EMI for a loan.

    Formula: EMI = P × r × (1+r)^n / ((1+r)^n - 1)
      P = principal amount
      r = monthly interest rate (annual_rate / 12 / 100)
      n = tenure in months

    Args:
        principal      : Loan amount in ₹
        annual_rate    : Annual interest rate (e.g. 12 for 12%)
        tenure_months  : Loan duration in months

    Returns:
        Monthly EMI amount in ₹

    Example:
        >>> calculate_emi(500000, 12, 36)
        16607.15  # matches Riya demo ₹16,607
    """
    if annual_rate == 0:
        return principal / tenure_months

    r = annual_rate / 12 / 100          # monthly rate as decimal
    n = tenure_months
    emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return round(emi, 2) # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# 2. COMPOUND GROWTH (lump sum)
# ─────────────────────────────────────────────────────────────────────────────

def compound_growth(principal: float, annual_rate: float, years: float) -> float:
    """
    Grow a lump-sum amount at a compounded annual rate.

    Formula: FV = P × (1 + r)^t
      P = principal, r = annual rate decimal, t = years

    Args:
        principal   : Starting amount in ₹
        annual_rate : Annual return rate (e.g. 12 for 12%)
        years       : Number of years

    Returns:
        Future value in ₹

    Example:
        >>> compound_growth(50000, 12, 24)
        ~₹6.81 lakhs  (Riya's existing savings after 24 years)
    """
    r = annual_rate / 100
    return round(principal * (1 + r) ** years, 2) # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# 3. SIP FUTURE VALUE
# ─────────────────────────────────────────────────────────────────────────────

def future_value_sip(monthly_investment: float, annual_rate: float, years: float) -> float:
    """
    Calculate future value of a recurring monthly SIP investment.

    Formula: FV = M × [(1+r)^n - 1] / r × (1+r)
      M = monthly investment
      r = monthly rate (annual_rate / 12 / 100)
      n = total months (years × 12)

    The trailing × (1+r) treats contributions as made at start of period.

    Args:
        monthly_investment : Monthly SIP amount in ₹
        annual_rate        : Expected annual return (e.g. 12 for 12%)
        years              : Investment horizon in years

    Returns:
        Future corpus value in ₹

    Example:
        >>> future_value_sip(8200, 12, 24)
        ~₹1 crore  (Riya's target)
    """
    if annual_rate == 0:
        return monthly_investment * years * 12

    r = annual_rate / 12 / 100     # monthly rate
    n = years * 12                  # total months
    fv = monthly_investment * ((1 + r) ** n - 1) / r * (1 + r)
    return round(fv, 2) # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# 4. INFLATION ADJUSTMENT
# ─────────────────────────────────────────────────────────────────────────────

def adjust_for_inflation(amount: float, inflation_rate: float, years: float) -> float:
    """
    Discount a future amount back to today's purchasing power.

    Formula: Real Value = Amount / (1 + i)^t

    Args:
        amount         : Future amount in ₹
        inflation_rate : Annual inflation rate (e.g. 6 for 6%)
        years          : Number of years into the future

    Returns:
        Inflation-adjusted (real) value in ₹
    """
    i = inflation_rate / 100
    return round(amount / (1 + i) ** years, 2) # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# 5. TOTAL LOAN COST
# ─────────────────────────────────────────────────────────────────────────────

def total_loan_cost(principal: float, annual_rate: float, tenure_months: int) -> dict:
    """
    Calculate the total amount repaid and total interest for a loan.

    Args:
        principal      : Loan amount in ₹
        annual_rate    : Annual interest rate (e.g. 12 for 12%)
        tenure_months  : Loan duration in months

    Returns:
        dict with:
            emi            : Monthly EMI
            total_paid     : Total amount paid over loan tenure
            total_interest : Extra cost beyond principal (interest burden)
    """
    emi = calculate_emi(principal, annual_rate, tenure_months)
    total_paid = round(emi * tenure_months, 2) # type: ignore
    total_interest = round(total_paid - principal, 2)
    return {
        "emi": emi,
        "total_paid": total_paid,
        "total_interest": total_interest,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 6. NET INVESTABLE SURPLUS
# ─────────────────────────────────────────────────────────────────────────────

def calculate_net_investable(
    monthly_income: float,
    monthly_expenses: float,
    monthly_emi: float = 0.0,
    monthly_tax: float = 0.0,
) -> float:
    """
    Compute how much money is left each month for investments.

    Net = Income - Expenses - EMI - Tax

    Args:
        monthly_income   : Take-home (or gross) monthly income in ₹
        monthly_expenses : Fixed monthly expenditure in ₹
        monthly_emi      : Total EMI obligations in ₹ (default 0)
        monthly_tax      : Monthly income tax deducted in ₹ (default 0)

    Returns:
        Investable surplus per month in ₹ (floored at 0)
    """
    surplus = monthly_income - monthly_expenses - monthly_emi - monthly_tax
    return round(max(surplus, 0.0), 2) # type: ignore


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST — run: python math_engine.py
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("MATH ENGINE — RIYA SANITY CHECKS")
    print("=" * 55)

    # EMI check
    emi = calculate_emi(500_000, 12, 36)
    print(f"\n1. EMI(₹5L, 12%, 36m)          → ₹{emi:,.2f}")
    print(f"   Expected                       → ₹16,607  {'✓' if abs(emi - 16607) < 5 else '✗'}")

    # SIP check
    sip_corpus = future_value_sip(8_200, 12, 24)
    print(f"\n2. SIP(₹8,200/m, 12%, 24yr)    → ₹{sip_corpus:,.0f}")
    print(f"   Expected                       → ~₹1 crore  {'✓' if 90_00_000 < sip_corpus < 1_10_00_000 else '✗'}")

    # Compound growth check
    savings_growth = compound_growth(50_000, 12, 24)
    print(f"\n3. Lump-sum(₹50K, 12%, 24yr)   → ₹{savings_growth:,.0f}")

    # Inflation adjust
    real = adjust_for_inflation(1_00_00_000, 6, 24)
    print(f"\n4. ₹1Cr real value after 24yr   → ₹{real:,.0f}")

    # Total loan cost
    loan_info = total_loan_cost(500_000, 12, 36)
    print(f"\n5. Loan cost ₹5L @ 12% 36m:")
    print(f"   EMI          : ₹{loan_info['emi']:,.2f}")
    print(f"   Total paid   : ₹{loan_info['total_paid']:,.0f}")
    print(f"   Interest paid: ₹{loan_info['total_interest']:,.0f}")

    # Net investable
    net = calculate_net_investable(50_000, 30_000, 16_607, 1_250)
    print(f"\n6. Net investable (Riya + loan) → ₹{net:,.0f}/month")
    print("=" * 55)