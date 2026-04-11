# ─────────────────────────────────────────────────────────────────
# test_tax_engine.py — Verify all tax calculations
# ─────────────────────────────────────────────────────────────────
#
# TEST CASES TO WRITE:
#
#   test_income_tax_riya()
#     Input:  annual_income=600000
#     Expect: 1250 (monthly tax)
#
#   test_income_tax_zero()
#     Input:  annual_income=300000
#     Expect: 0
#
#   test_ltcg_above_threshold()
#     Input:  total_gains=500000
#     Expect: 40000 (10% of 400000)
#
#   test_ltcg_below_threshold()
#     Input:  total_gains=80000
#     Expect: 0
#
#   test_tds_on_fd()
#     Input:  fd_interest=50000
#     Expect: 5000 (10% of 50000)
# ─────────────────────────────────────────────────────────────────
