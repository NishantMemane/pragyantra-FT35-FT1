# ─────────────────────────────────────────────────────────────────
# monte_carlo.py — 500-run forward simulation engine
# ─────────────────────────────────────────────────────────────────
#
# PURPOSE:
#   Run 500 different versions of the user's financial future.
#   Each run has randomized market returns, inflation, salary
#   growth, and life shock events. Extract best/expected/worst.
#
# IMPORTS NEEDED:
#   numpy as np
#   from math_engine import (all 6 functions)
#   from tax_engine import calculate_ltcg
#   from models import UserProfile, DecisionParams
#
# RANDOMIZED VARIABLES PER RUN (use np.random):
#   Market return:    uniform(8, 16) % annually
#   Inflation:        uniform(5, 7) % annually
#   Salary growth:    uniform(5, 12) % annually
#   Life shock:       15% probability each year
#   Shock severity:   uniform(20, 40) % corpus loss if shock hits
#
# FUNCTIONS TO WRITE:
#
#   run_single_simulation(profile, decision, years)
#     Simulates one version of the future year by year
#     Each year: income grows, expenses grow with inflation,
#     investable amount compounds, shocks reduce corpus randomly
#     Returns: list of corpus values for each year (the curve)
#
#   run_monte_carlo(profile, decision, runs=500)
#     Calls run_single_simulation 500 times
#     Returns: list of 500 final corpus values
#
#   run_without_decision(profile, years)
#     Same as run_monte_carlo but with no EMI deduction
#     Produces the ghost comparison line
#     Returns: P10, P50, P90 arrays for ghost line
#
#   get_percentile(results, p)
#     Uses np.percentile to extract any percentile from results
#     Called with p=10 (worst), p=50 (expected), p=90 (best)
#
# OUTPUT SHAPE:
#   For each of best/expected/worst: a list of yearly corpus values
#   Length = goal_age - current_age (one value per year)
#
# TESTING BLOCK:
#   if __name__ == '__main__': run Riya's data, print P10/P50/P90
# ─────────────────────────────────────────────────────────────────
