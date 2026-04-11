# ─────────────────────────────────────────────────────────────────
# models.py — ALL Pydantic data shapes for the entire application
# ─────────────────────────────────────────────────────────────────
#
# PURPOSE:
#   Define the exact shape of every piece of data that flows
#   through the system. Every other file imports from here.
#   No logic lives here — only structure.
#
# MODELS TO DEFINE:
#
#   UserProfile
#     age, monthly_income, monthly_expenses (default 60% of income),
#     existing_savings (default 0), goal_amount, goal_age
#
#   DecisionParams
#     type (LOAN / SIP / DELAY / LUMPSUM),
#     amount, interest_rate, tenure_months,
#     monthly_emi, cash_flow_reduction,
#     monthly_sip, delay_years,
#     instrument (equity / fd)
#
#   SimulationResult
#     labels (year array), best_case, expected_case,
#     worst_case, without_decision (ghost line),
#     best_final, expected_final, worst_final,
#     goal_achieved, shortfall,
#     post_tax_expected_final, ltcg_tax_paid, story
#
#   ReverseResult
#     required_monthly_sip, if_delayed_2_years, if_delayed_5_years,
#     existing_savings_growth, total_contribution, total_returns, story
#
#   ProfileResponse
#     post_tax_monthly_income, monthly_tax,
#     investable_amount, profile_confirmed
#
#   OrchestrationRequest
#     message, profile (optional UserProfile)
#
#   OrchestrationResponse
#     route (FORWARD / REVERSE / CLARIFY),
#     decision_type (optional), question (optional)
#
# IMPORTS NEEDED: pydantic BaseModel, Optional, List
# ─────────────────────────────────────────────────────────────────
