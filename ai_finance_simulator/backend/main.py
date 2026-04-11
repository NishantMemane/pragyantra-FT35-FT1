# ─────────────────────────────────────────────────────────────────
# main.py — FastAPI application, all routes wired together
# ─────────────────────────────────────────────────────────────────
#
# PURPOSE:
#   Entry point for the entire backend. Creates the FastAPI app,
#   sets up CORS, defines all 4 routes, and calls the right
#   engines in the right order for each route.
#
# IMPORTS NEEDED:
#   from fastapi import FastAPI
#   from fastapi.middleware.cors import CORSMiddleware
#   from models import (all models)
#   from math_engine import calculate_net_investable
#   from tax_engine import (all 4 tax functions)
#   from monte_carlo import run_monte_carlo, run_without_decision, get_percentile
#   from reverse_engine import reverse_simulate, calculate_delay_impact
#   from ollama_engine import get_story
#   from orchestrator import smart_orchestrate
#
# APP SETUP:
#   app = FastAPI(title='AI Finance Simulator', version='1.0')
#   Add CORSMiddleware allowing localhost:3000
#
# ── ROUTE 1: POST /api/profile ────────────────────────────────
#   Receives: UserProfile
#   Steps:
#     1. If expenses not provided, default to 60% of income
#     2. Calculate monthly tax via calculate_income_tax
#     3. Calculate post-tax income = income - monthly_tax
#     4. Calculate investable = income - expenses - monthly_tax
#   Returns: ProfileResponse
#
# ── ROUTE 2: POST /api/orchestrate ───────────────────────────
#   Receives: OrchestrationRequest (message + optional profile)
#   Steps:
#     1. Call smart_orchestrate(message, profile)
#   Returns: OrchestrationResponse (route + decision_type or question)
#
# ── ROUTE 3: POST /api/simulate/forward ──────────────────────
#   Receives: UserProfile + DecisionParams
#   Steps:
#     1. Calculate monthly tax
#     2. If decision is LOAN: calculate EMI via math_engine
#        If decision is HOME_LOAN: apply home loan tax benefit
#     3. Calculate net investable amount
#     4. Run 500 Monte Carlo simulations WITH decision
#     5. Run 500 Monte Carlo simulations WITHOUT decision (ghost)
#     6. Extract P10, P50, P90 for both
#     7. Apply LTCG tax to final corpus values
#     8. Build yearly curve arrays for each scenario
#     9. Call get_story(profile, decision, result, 'forward')
#   Returns: SimulationResult (all arrays + story)
#
# ── ROUTE 4: POST /api/simulate/reverse ──────────────────────
#   Receives: UserProfile
#   Steps:
#     1. Calculate monthly tax
#     2. Adjust savings with post-tax context
#     3. Call reverse_simulate → required SIP now
#     4. Call calculate_delay_impact(+2 years)
#     5. Call calculate_delay_impact(+5 years)
#     6. Calculate total_contribution and total_returns
#     7. Call get_story(profile, None, result, 'reverse')
#   Returns: ReverseResult (all SIP values + story)
#
# RUN COMMAND:
#   uvicorn main:app --reload --port 8000
#   Docs available at: http://localhost:8000/docs
# ─────────────────────────────────────────────────────────────────
