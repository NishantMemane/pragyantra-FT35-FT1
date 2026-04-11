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
