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
