# ─────────────────────────────────────────────────────────────────
# test_routes.py — Integration tests for all 4 FastAPI endpoints
# ─────────────────────────────────────────────────────────────────
#
# USE: httpx or requests to call the running server
#
# TEST CASES TO WRITE:
#
#   test_profile_endpoint()
#     POST /api/profile with Riya's data
#     Expect: post_tax_monthly_income = 48750, monthly_tax = 1250
#
#   test_orchestrate_loan()
#     POST /api/orchestrate with message='I want to take a loan'
#     Expect: route=FORWARD, decision_type=LOAN
#
#   test_orchestrate_reverse()
#     POST /api/orchestrate with message='I want 1 crore by 50'
#     Expect: route=REVERSE
#
#   test_orchestrate_clarify()
#     POST /api/orchestrate with message="I don't know what to do"
#     Expect: route=CLARIFY, question not null
#
#   test_forward_simulation()
#     POST /api/simulate/forward with Riya + loan params
#     Expect: expected_final roughly between 6000000 and 8000000
#
#   test_reverse_simulation()
#     POST /api/simulate/reverse with Riya's profile
#     Expect: required_monthly_sip ~8200
# ─────────────────────────────────────────────────────────────────
