import os

# ─────────────────────────────────────────────
#  Project structure definition
#  Each entry: (filepath, description comment)
# ─────────────────────────────────────────────

BASE = "ai_finance_simulator"

FILES = [

    # ── ROOT ──────────────────────────────────
    (
        "README.md",
        "# AI Financial Decision Simulation Engine\n\n"
        "> We don't predict your future. We let you live it before you decide.\n\n"
        "## Setup\n"
        "1. `cd backend && pip install -r requirements.txt`\n"
        "2. `ollama pull llama3.1:8b`\n"
        "3. Terminal 1: `ollama serve`\n"
        "4. Terminal 2: `uvicorn main:app --reload --port 8000`\n"
        "5. Terminal 3: `cd frontend && npm start`\n"
    ),

    # ── BACKEND ───────────────────────────────
    (
        "backend/requirements.txt",
        "fastapi\nuvicorn\nnumpy\npydantic\nrequests\n"
    ),

    (
        "backend/.env.example",
        "# Copy this to .env and fill in values\n"
        "OLLAMA_HOST=http://localhost:11434\n"
        "OLLAMA_MODEL=llama3.1:8b\n"
        "FRONTEND_URL=http://localhost:3000\n"
    ),

    (
        "backend/models.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# models.py — ALL Pydantic data shapes for the entire application\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# PURPOSE:\n"
        "#   Define the exact shape of every piece of data that flows\n"
        "#   through the system. Every other file imports from here.\n"
        "#   No logic lives here — only structure.\n"
        "#\n"
        "# MODELS TO DEFINE:\n"
        "#\n"
        "#   UserProfile\n"
        "#     age, monthly_income, monthly_expenses (default 60% of income),\n"
        "#     existing_savings (default 0), goal_amount, goal_age\n"
        "#\n"
        "#   DecisionParams\n"
        "#     type (LOAN / SIP / DELAY / LUMPSUM),\n"
        "#     amount, interest_rate, tenure_months,\n"
        "#     monthly_emi, cash_flow_reduction,\n"
        "#     monthly_sip, delay_years,\n"
        "#     instrument (equity / fd)\n"
        "#\n"
        "#   SimulationResult\n"
        "#     labels (year array), best_case, expected_case,\n"
        "#     worst_case, without_decision (ghost line),\n"
        "#     best_final, expected_final, worst_final,\n"
        "#     goal_achieved, shortfall,\n"
        "#     post_tax_expected_final, ltcg_tax_paid, story\n"
        "#\n"
        "#   ReverseResult\n"
        "#     required_monthly_sip, if_delayed_2_years, if_delayed_5_years,\n"
        "#     existing_savings_growth, total_contribution, total_returns, story\n"
        "#\n"
        "#   ProfileResponse\n"
        "#     post_tax_monthly_income, monthly_tax,\n"
        "#     investable_amount, profile_confirmed\n"
        "#\n"
        "#   OrchestrationRequest\n"
        "#     message, profile (optional UserProfile)\n"
        "#\n"
        "#   OrchestrationResponse\n"
        "#     route (FORWARD / REVERSE / CLARIFY),\n"
        "#     decision_type (optional), question (optional)\n"
        "#\n"
        "# IMPORTS NEEDED: pydantic BaseModel, Optional, List\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    (
        "backend/math_engine.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# math_engine.py — ALL pure financial math functions\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# PURPOSE:\n"
        "#   The foundation of the entire system. Every simulation engine\n"
        "#   calls these functions. No randomness, no AI, no API calls.\n"
        "#   Pure arithmetic only. Fully testable with print().\n"
        "#\n"
        "# IMPORTS NEEDED: math (standard library only)\n"
        "#\n"
        "# FUNCTIONS TO WRITE:\n"
        "#\n"
        "#   calculate_emi(principal, annual_rate, tenure_months)\n"
        "#     Formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)\n"
        "#     where r = annual_rate / 12 / 100\n"
        "#     Test: ₹5,00,000 at 12% for 36 months → should return ₹16,607\n"
        "#\n"
        "#   compound_growth(principal, annual_rate, years)\n"
        "#     Formula: P * (1 + r/100)^years\n"
        "#     Test: ₹50,000 at 12% for 24 years → should return ~₹8,00,000\n"
        "#\n"
        "#   calculate_sip_future_value(monthly_amount, annual_rate, years)\n"
        "#     Formula: FV = M * [((1+r)^n - 1) / r] * (1+r)\n"
        "#     where r = annual_rate/12/100, n = years*12\n"
        "#     Test: ₹8,200/month at 12% for 24 years → should return ~₹1 crore\n"
        "#\n"
        "#   inflation_adjust(amount, inflation_rate, years)\n"
        "#     Formula: amount / (1 + inflation_rate/100)^years\n"
        "#     Returns real value of a future amount in today's money\n"
        "#\n"
        "#   total_loan_cost(principal, annual_rate, tenure_months)\n"
        "#     Formula: EMI * tenure_months\n"
        "#     Returns total amount paid over entire loan life\n"
        "#\n"
        "#   calculate_net_investable(income, expenses, emi, monthly_tax)\n"
        "#     Formula: income - expenses - emi - monthly_tax\n"
        "#     This is the core number that feeds Monte Carlo\n"
        "#\n"
        "# TESTING BLOCK (run this file directly to verify):\n"
        "#   if __name__ == '__main__': print all test cases\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    (
        "backend/tax_engine.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# tax_engine.py — Indian tax calculations for simulation accuracy\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# PURPOSE:\n"
        "#   Pre-processing step that runs before any simulation.\n"
        "#   Makes simulation numbers realistic by using post-tax income.\n"
        "#   Not a full tax filing system — just the 4 rules that matter.\n"
        "#\n"
        "# IMPORTS NEEDED: none\n"
        "#\n"
        "# FUNCTIONS TO WRITE:\n"
        "#\n"
        "#   calculate_income_tax(annual_income)\n"
        "#     New Regime 2024-25 slabs:\n"
        "#       Up to ₹3L      → 0%\n"
        "#       ₹3L – ₹7L     → 5%\n"
        "#       ₹7L – ₹10L    → 10%\n"
        "#       ₹10L – ₹12L   → 15%\n"
        "#       ₹12L – ₹15L   → 20%\n"
        "#       Above ₹15L    → 30%\n"
        "#     Returns: monthly tax deduction (annual_tax / 12)\n"
        "#     Test: ₹6L annual (₹50K/month) → ₹15,000/year → ₹1,250/month\n"
        "#\n"
        "#   calculate_ltcg(total_gains)\n"
        "#     Rule: gains above ₹1,00,000 taxed at 10%\n"
        "#     Formula: max(0, total_gains - 100000) * 0.10\n"
        "#     Applied to final corpus at goal age before showing user\n"
        "#\n"
        "#   calculate_tds_on_fd(fd_interest)\n"
        "#     Rule: if fd_interest > ₹40,000 → 10% TDS\n"
        "#     Returns: tds amount (0 if interest <= 40000)\n"
        "#\n"
        "#   calculate_home_loan_benefit(annual_interest)\n"
        "#     Rule: Section 24 deduction, capped at ₹2,00,000/year\n"
        "#     Formula: min(annual_interest, 200000)\n"
        "#     Returns: annual deduction amount (reduces taxable income)\n"
        "#\n"
        "# TESTING BLOCK:\n"
        "#   if __name__ == '__main__': print all test cases\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    (
        "backend/monte_carlo.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# monte_carlo.py — 500-run forward simulation engine\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# PURPOSE:\n"
        "#   Run 500 different versions of the user's financial future.\n"
        "#   Each run has randomized market returns, inflation, salary\n"
        "#   growth, and life shock events. Extract best/expected/worst.\n"
        "#\n"
        "# IMPORTS NEEDED:\n"
        "#   numpy as np\n"
        "#   from math_engine import (all 6 functions)\n"
        "#   from tax_engine import calculate_ltcg\n"
        "#   from models import UserProfile, DecisionParams\n"
        "#\n"
        "# RANDOMIZED VARIABLES PER RUN (use np.random):\n"
        "#   Market return:    uniform(8, 16) % annually\n"
        "#   Inflation:        uniform(5, 7) % annually\n"
        "#   Salary growth:    uniform(5, 12) % annually\n"
        "#   Life shock:       15% probability each year\n"
        "#   Shock severity:   uniform(20, 40) % corpus loss if shock hits\n"
        "#\n"
        "# FUNCTIONS TO WRITE:\n"
        "#\n"
        "#   run_single_simulation(profile, decision, years)\n"
        "#     Simulates one version of the future year by year\n"
        "#     Each year: income grows, expenses grow with inflation,\n"
        "#     investable amount compounds, shocks reduce corpus randomly\n"
        "#     Returns: list of corpus values for each year (the curve)\n"
        "#\n"
        "#   run_monte_carlo(profile, decision, runs=500)\n"
        "#     Calls run_single_simulation 500 times\n"
        "#     Returns: list of 500 final corpus values\n"
        "#\n"
        "#   run_without_decision(profile, years)\n"
        "#     Same as run_monte_carlo but with no EMI deduction\n"
        "#     Produces the ghost comparison line\n"
        "#     Returns: P10, P50, P90 arrays for ghost line\n"
        "#\n"
        "#   get_percentile(results, p)\n"
        "#     Uses np.percentile to extract any percentile from results\n"
        "#     Called with p=10 (worst), p=50 (expected), p=90 (best)\n"
        "#\n"
        "# OUTPUT SHAPE:\n"
        "#   For each of best/expected/worst: a list of yearly corpus values\n"
        "#   Length = goal_age - current_age (one value per year)\n"
        "#\n"
        "# TESTING BLOCK:\n"
        "#   if __name__ == '__main__': run Riya's data, print P10/P50/P90\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    (
        "backend/reverse_engine.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# reverse_engine.py — Goal-based reverse simulation\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# PURPOSE:\n"
        "#   User sets a goal (₹1 crore by age 50).\n"
        "#   Engine works backwards to find required monthly SIP.\n"
        "#   Also calculates the penalty for delaying 2 or 5 years.\n"
        "#\n"
        "# IMPORTS NEEDED:\n"
        "#   from math_engine import compound_growth, calculate_sip_future_value\n"
        "#   from models import UserProfile\n"
        "#\n"
        "# FUNCTIONS TO WRITE:\n"
        "#\n"
        "#   reverse_simulate(goal, current_age, goal_age, savings, rate=0.12)\n"
        "#     Step 1: Calculate how much existing savings grow by goal_age\n"
        "#             corpus_from_savings = compound_growth(savings, rate, years)\n"
        "#     Step 2: remaining_gap = goal - corpus_from_savings\n"
        "#     Step 3: Use FV of annuity formula BACKWARDS to find monthly SIP\n"
        "#             SIP = remaining_gap * r / [((1+r)^n - 1) * (1+r)]\n"
        "#             where r = rate/12, n = years*12\n"
        "#     Returns: required monthly SIP amount\n"
        "#     Test: Riya (26→50, ₹1Cr goal, ₹50K savings) → ~₹8,200/month\n"
        "#\n"
        "#   calculate_delay_impact(goal, current_age, goal_age, savings, delay_years)\n"
        "#     Calls reverse_simulate with current_age + delay_years\n"
        "#     Returns: new required monthly SIP after delay\n"
        "#     Test: Riya + 2yr delay → ~₹10,400/month\n"
        "#     Test: Riya + 5yr delay → ~₹15,100/month\n"
        "#\n"
        "# TESTING BLOCK:\n"
        "#   if __name__ == '__main__': print Riya's 3 SIP values\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    (
        "backend/ollama_engine.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# ollama_engine.py — Local LLM story generation\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# PURPOSE:\n"
        "#   Take dry simulation numbers and turn them into a 3-sentence\n"
        "#   human story that users will actually remember and feel.\n"
        "#   Connects to Ollama running locally — no external API needed.\n"
        "#\n"
        "# IMPORTS NEEDED:\n"
        "#   import requests\n"
        "#   import json\n"
        "#   from models import UserProfile, DecisionParams, SimulationResult\n"
        "#   from models import ReverseResult\n"
        "#\n"
        "# OLLAMA DETAILS:\n"
        "#   URL: http://localhost:11434/api/generate\n"
        "#   Model: llama3.1:8b (or mistral:7b as fallback)\n"
        "#   Method: POST with JSON body\n"
        "#   Body: { model, prompt, stream: false }\n"
        "#   Response field: response.json()['response']\n"
        "#\n"
        "# FUNCTIONS TO WRITE:\n"
        "#\n"
        "#   call_ollama(prompt)\n"
        "#     Raw HTTP POST to Ollama\n"
        "#     Wraps in try/except — returns fallback string if Ollama is down\n"
        "#     Returns: plain string (the story text)\n"
        "#\n"
        "#   build_forward_prompt(profile, decision, result)\n"
        "#     Constructs the prompt string for forward simulation\n"
        "#     Tell Ollama:\n"
        "#       - User's age, income, goal\n"
        "#       - The decision they made (loan/SIP/etc)\n"
        "#       - Best / Expected / Worst final corpus\n"
        "#       - Whether goal is achieved in expected case\n"
        "#       - Post-tax corpus and LTCG paid\n"
        "#     Instruct Ollama:\n"
        "#       - Exactly 3 sentences\n"
        "#       - Use second person (you / your)\n"
        "#       - Use real life events (school fees, medical, retirement)\n"
        "#       - No jargon, no bullet points\n"
        "#       - Honest but not scary\n"
        "#\n"
        "#   build_reverse_prompt(profile, result)\n"
        "#     Constructs the prompt string for reverse simulation\n"
        "#     Tell Ollama:\n"
        "#       - User's goal and target age\n"
        "#       - Required monthly SIP\n"
        "#       - Cost of delaying 2 and 5 years\n"
        "#       - Total invested vs total returns\n"
        "#     Same 3-sentence, second-person, no-jargon instructions\n"
        "#\n"
        "#   get_story(profile, decision, result, mode)\n"
        "#     mode = 'forward' or 'reverse'\n"
        "#     Picks the right prompt builder based on mode\n"
        "#     Calls call_ollama with the built prompt\n"
        "#     Returns: story string\n"
        "#\n"
        "# FALLBACK BEHAVIOR:\n"
        "#   If Ollama is unreachable, return a generic but reasonable\n"
        "#   summary string so the app doesn't crash\n"
        "#\n"
        "# TESTING BLOCK:\n"
        "#   if __name__ == '__main__': hardcode Riya's result, print story\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    (
        "backend/orchestrator.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# orchestrator.py — Routes user message to correct engine\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# PURPOSE:\n"
        "#   User types plain language. Orchestrator reads it and decides\n"
        "#   whether to run forward simulation, reverse simulation,\n"
        "#   or ask a clarifying question. User never picks a mode manually.\n"
        "#\n"
        "# IMPORTS NEEDED:\n"
        "#   import re\n"
        "#   from ollama_engine import call_ollama\n"
        "#   from models import OrchestrationResponse\n"
        "#\n"
        "# KEYWORD LISTS TO DEFINE (as constants at top of file):\n"
        "#   LOAN_KEYWORDS    = ['loan', 'borrow', 'emi', 'debt', 'credit']\n"
        "#   SIP_KEYWORDS     = ['sip', 'mutual fund', 'invest monthly']\n"
        "#   DELAY_KEYWORDS   = ['delay', 'wait', 'later', 'postpone']\n"
        "#   LUMPSUM_KEYWORDS = ['lump sum', 'one time', 'stocks', 'fd']\n"
        "#   REVERSE_KEYWORDS = ['want ₹', 'goal', 'target', 'retire with',\n"
        "#                        'how do i reach', 'how much do i need']\n"
        "#   CLARIFY_KEYWORDS = ['help', \"don't know\", 'not sure', 'suggest',\n"
        "#                        'what should i do']\n"
        "#\n"
        "# FUNCTIONS TO WRITE:\n"
        "#\n"
        "#   rule_based_route(message)\n"
        "#     Lowercase the message\n"
        "#     Check each keyword list in order\n"
        "#     Return OrchestrationResponse with route + decision_type\n"
        "#     If no match found, return None (signals fallback needed)\n"
        "#\n"
        "#   ollama_route(message)\n"
        "#     Build a prompt asking Ollama to classify the message\n"
        "#     Tell Ollama to return ONLY valid JSON:\n"
        "#       { route: FORWARD/REVERSE/CLARIFY,\n"
        "#         decision_type: LOAN/SIP/DELAY/LUMPSUM or null }\n"
        "#     Parse the JSON response\n"
        "#     Return OrchestrationResponse\n"
        "#     Wrap in try/except — return CLARIFY if Ollama fails\n"
        "#\n"
        "#   smart_orchestrate(message, profile)\n"
        "#     Step 1: Try rule_based_route(message)\n"
        "#     Step 2: If None returned, try ollama_route(message)\n"
        "#     Returns: OrchestrationResponse\n"
        "#\n"
        "# ROUTING LOGIC:\n"
        "#   LOAN match      → FORWARD, decision_type=LOAN\n"
        "#   SIP match       → FORWARD, decision_type=SIP\n"
        "#   DELAY match     → FORWARD, decision_type=DELAY\n"
        "#   LUMPSUM match   → FORWARD, decision_type=LUMPSUM\n"
        "#   REVERSE match   → REVERSE\n"
        "#   CLARIFY match   → CLARIFY, question='What are you trying to do?'\n"
        "#   No match        → Ollama fallback\n"
        "#\n"
        "# TESTING BLOCK:\n"
        "#   if __name__ == '__main__': test 5 messages, print routes\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    (
        "backend/main.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# main.py — FastAPI application, all routes wired together\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# PURPOSE:\n"
        "#   Entry point for the entire backend. Creates the FastAPI app,\n"
        "#   sets up CORS, defines all 4 routes, and calls the right\n"
        "#   engines in the right order for each route.\n"
        "#\n"
        "# IMPORTS NEEDED:\n"
        "#   from fastapi import FastAPI\n"
        "#   from fastapi.middleware.cors import CORSMiddleware\n"
        "#   from models import (all models)\n"
        "#   from math_engine import calculate_net_investable\n"
        "#   from tax_engine import (all 4 tax functions)\n"
        "#   from monte_carlo import run_monte_carlo, run_without_decision, get_percentile\n"
        "#   from reverse_engine import reverse_simulate, calculate_delay_impact\n"
        "#   from ollama_engine import get_story\n"
        "#   from orchestrator import smart_orchestrate\n"
        "#\n"
        "# APP SETUP:\n"
        "#   app = FastAPI(title='AI Finance Simulator', version='1.0')\n"
        "#   Add CORSMiddleware allowing localhost:3000\n"
        "#\n"
        "# ── ROUTE 1: POST /api/profile ────────────────────────────────\n"
        "#   Receives: UserProfile\n"
        "#   Steps:\n"
        "#     1. If expenses not provided, default to 60% of income\n"
        "#     2. Calculate monthly tax via calculate_income_tax\n"
        "#     3. Calculate post-tax income = income - monthly_tax\n"
        "#     4. Calculate investable = income - expenses - monthly_tax\n"
        "#   Returns: ProfileResponse\n"
        "#\n"
        "# ── ROUTE 2: POST /api/orchestrate ───────────────────────────\n"
        "#   Receives: OrchestrationRequest (message + optional profile)\n"
        "#   Steps:\n"
        "#     1. Call smart_orchestrate(message, profile)\n"
        "#   Returns: OrchestrationResponse (route + decision_type or question)\n"
        "#\n"
        "# ── ROUTE 3: POST /api/simulate/forward ──────────────────────\n"
        "#   Receives: UserProfile + DecisionParams\n"
        "#   Steps:\n"
        "#     1. Calculate monthly tax\n"
        "#     2. If decision is LOAN: calculate EMI via math_engine\n"
        "#        If decision is HOME_LOAN: apply home loan tax benefit\n"
        "#     3. Calculate net investable amount\n"
        "#     4. Run 500 Monte Carlo simulations WITH decision\n"
        "#     5. Run 500 Monte Carlo simulations WITHOUT decision (ghost)\n"
        "#     6. Extract P10, P50, P90 for both\n"
        "#     7. Apply LTCG tax to final corpus values\n"
        "#     8. Build yearly curve arrays for each scenario\n"
        "#     9. Call get_story(profile, decision, result, 'forward')\n"
        "#   Returns: SimulationResult (all arrays + story)\n"
        "#\n"
        "# ── ROUTE 4: POST /api/simulate/reverse ──────────────────────\n"
        "#   Receives: UserProfile\n"
        "#   Steps:\n"
        "#     1. Calculate monthly tax\n"
        "#     2. Adjust savings with post-tax context\n"
        "#     3. Call reverse_simulate → required SIP now\n"
        "#     4. Call calculate_delay_impact(+2 years)\n"
        "#     5. Call calculate_delay_impact(+5 years)\n"
        "#     6. Calculate total_contribution and total_returns\n"
        "#     7. Call get_story(profile, None, result, 'reverse')\n"
        "#   Returns: ReverseResult (all SIP values + story)\n"
        "#\n"
        "# RUN COMMAND:\n"
        "#   uvicorn main:app --reload --port 8000\n"
        "#   Docs available at: http://localhost:8000/docs\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    # ── BACKEND TESTS ─────────────────────────────────────────────
    (
        "backend/tests/__init__.py",
        "# test package\n"
    ),

    (
        "backend/tests/test_math_engine.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# test_math_engine.py — Verify all math functions with known values\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# TEST CASES TO WRITE:\n"
        "#\n"
        "#   test_emi()\n"
        "#     Input:  principal=500000, rate=12, tenure=36\n"
        "#     Expect: ~16607\n"
        "#\n"
        "#   test_sip_future_value()\n"
        "#     Input:  monthly=8200, rate=12, years=24\n"
        "#     Expect: ~10000000 (₹1 crore)\n"
        "#\n"
        "#   test_compound_growth()\n"
        "#     Input:  principal=50000, rate=12, years=24\n"
        "#     Expect: ~800000\n"
        "#\n"
        "#   test_total_loan_cost()\n"
        "#     Input:  principal=500000, rate=12, tenure=36\n"
        "#     Expect: ~597852 (EMI * 36)\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    (
        "backend/tests/test_tax_engine.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# test_tax_engine.py — Verify all tax calculations\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# TEST CASES TO WRITE:\n"
        "#\n"
        "#   test_income_tax_riya()\n"
        "#     Input:  annual_income=600000\n"
        "#     Expect: 1250 (monthly tax)\n"
        "#\n"
        "#   test_income_tax_zero()\n"
        "#     Input:  annual_income=300000\n"
        "#     Expect: 0\n"
        "#\n"
        "#   test_ltcg_above_threshold()\n"
        "#     Input:  total_gains=500000\n"
        "#     Expect: 40000 (10% of 400000)\n"
        "#\n"
        "#   test_ltcg_below_threshold()\n"
        "#     Input:  total_gains=80000\n"
        "#     Expect: 0\n"
        "#\n"
        "#   test_tds_on_fd()\n"
        "#     Input:  fd_interest=50000\n"
        "#     Expect: 5000 (10% of 50000)\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    (
        "backend/tests/test_reverse_engine.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# test_reverse_engine.py — Verify reverse simulation with Riya\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# TEST CASES TO WRITE:\n"
        "#\n"
        "#   test_riya_sip_now()\n"
        "#     Input:  goal=10000000, current_age=26, goal_age=50,\n"
        "#             savings=50000, rate=0.12\n"
        "#     Expect: ~8200/month (allow +-500 margin)\n"
        "#\n"
        "#   test_riya_delay_2_years()\n"
        "#     Same inputs, delay_years=2\n"
        "#     Expect: ~10400/month\n"
        "#\n"
        "#   test_riya_delay_5_years()\n"
        "#     Same inputs, delay_years=5\n"
        "#     Expect: ~15100/month\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    (
        "backend/tests/test_routes.py",
        "# ─────────────────────────────────────────────────────────────────\n"
        "# test_routes.py — Integration tests for all 4 FastAPI endpoints\n"
        "# ─────────────────────────────────────────────────────────────────\n"
        "#\n"
        "# USE: httpx or requests to call the running server\n"
        "#\n"
        "# TEST CASES TO WRITE:\n"
        "#\n"
        "#   test_profile_endpoint()\n"
        "#     POST /api/profile with Riya's data\n"
        "#     Expect: post_tax_monthly_income = 48750, monthly_tax = 1250\n"
        "#\n"
        "#   test_orchestrate_loan()\n"
        "#     POST /api/orchestrate with message='I want to take a loan'\n"
        "#     Expect: route=FORWARD, decision_type=LOAN\n"
        "#\n"
        "#   test_orchestrate_reverse()\n"
        "#     POST /api/orchestrate with message='I want 1 crore by 50'\n"
        "#     Expect: route=REVERSE\n"
        "#\n"
        "#   test_orchestrate_clarify()\n"
        "#     POST /api/orchestrate with message=\"I don't know what to do\"\n"
        "#     Expect: route=CLARIFY, question not null\n"
        "#\n"
        "#   test_forward_simulation()\n"
        "#     POST /api/simulate/forward with Riya + loan params\n"
        "#     Expect: expected_final roughly between 6000000 and 8000000\n"
        "#\n"
        "#   test_reverse_simulation()\n"
        "#     POST /api/simulate/reverse with Riya's profile\n"
        "#     Expect: required_monthly_sip ~8200\n"
        "# ─────────────────────────────────────────────────────────────────\n"
    ),

    # ── FRONTEND PLACEHOLDER ──────────────────────────────────────
    (
        "frontend/.gitkeep",
        "# Frontend will be set up separately\n"
        "# Stack: React + Tailwind + Recharts + Axios\n"
        "# Run: npx create-react-app . inside this folder\n"
    ),

    # ── GIT ───────────────────────────────────────────────────────
    (
        ".gitignore",
        "# Python\n"
        "__pycache__/\n"
        "*.pyc\n"
        "*.pyo\n"
        "venv/\n"
        ".env\n"
        "\n"
        "# Node\n"
        "node_modules/\n"
        "frontend/build/\n"
        "\n"
        "# Ollama models (large files)\n"
        "*.gguf\n"
        "\n"
        "# OS\n"
        ".DS_Store\n"
        "Thumbs.db\n"
    ),
]


def create_structure():
    print("\n📁 Creating AI Finance Simulator project structure...\n")
    created_files = 0
    created_dirs = set()

    for relative_path, content in FILES:
        full_path = os.path.join(BASE, relative_path)
        dir_path = os.path.dirname(full_path)

        # Create directories if needed
        if dir_path and dir_path not in created_dirs:
            os.makedirs(dir_path, exist_ok=True)
            created_dirs.add(dir_path)

        # Write file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  ✅ {full_path}")
        created_files += 1

    print(f"\n✅ Done! Created {created_files} files across {len(created_dirs)} folders.\n")
    print("📂 Structure:")
    for root, dirs, files in os.walk(BASE):
        # skip hidden and cache dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        depth = root.replace(BASE, '').count(os.sep)
        indent = '    ' * depth
        folder_name = os.path.basename(root)
        print(f"{indent}📂 {folder_name}/")
        sub_indent = '    ' * (depth + 1)
        for file in files:
            print(f"{sub_indent}📄 {file}")

    print("\n─────────────────────────────────────────")
    print("NEXT STEPS:")
    print("  1. cd ai_finance_simulator/backend")
    print("  2. python -m venv venv")
    print("  3. source venv/bin/activate  (Mac/Linux)")
    print("     venv\\Scripts\\activate     (Windows)")
    print("  4. pip install -r requirements.txt")
    print("  5. Ask for code for each file one by one")
    print("─────────────────────────────────────────\n")


if __name__ == "__main__":
    create_structure()
