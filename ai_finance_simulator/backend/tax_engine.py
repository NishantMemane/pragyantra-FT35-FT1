# ─────────────────────────────────────────────────────────────────
# tax_engine.py — Indian tax calculations for simulation accuracy
# ─────────────────────────────────────────────────────────────────
#
# PURPOSE:
#   Pre-processing step that runs before any simulation.
#   Makes simulation numbers realistic by using post-tax income.
#   Not a full tax filing system — just the 4 rules that matter.
#
# IMPORTS NEEDED: none
#
# FUNCTIONS TO WRITE:
#
#   calculate_income_tax(annual_income)
#     New Regime 2024-25 slabs:
#       Up to ₹3L      → 0%
#       ₹3L – ₹7L     → 5%
#       ₹7L – ₹10L    → 10%
#       ₹10L – ₹12L   → 15%
#       ₹12L – ₹15L   → 20%
#       Above ₹15L    → 30%
#     Returns: monthly tax deduction (annual_tax / 12)
#     Test: ₹6L annual (₹50K/month) → ₹15,000/year → ₹1,250/month
#
#   calculate_ltcg(total_gains)
#     Rule: gains above ₹1,00,000 taxed at 10%
#     Formula: max(0, total_gains - 100000) * 0.10
#     Applied to final corpus at goal age before showing user
#
#   calculate_tds_on_fd(fd_interest)
#     Rule: if fd_interest > ₹40,000 → 10% TDS
#     Returns: tds amount (0 if interest <= 40000)
#
#   calculate_home_loan_benefit(annual_interest)
#     Rule: Section 24 deduction, capped at ₹2,00,000/year
#     Formula: min(annual_interest, 200000)
#     Returns: annual deduction amount (reduces taxable income)
#
# TESTING BLOCK:
#   if __name__ == '__main__': print all test cases
# ─────────────────────────────────────────────────────────────────
