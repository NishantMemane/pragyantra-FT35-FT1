# ─────────────────────────────────────────────────────────────────
# orchestrator.py — Routes user message to correct engine
# ─────────────────────────────────────────────────────────────────
#
# PURPOSE:
#   User types plain language. Orchestrator reads it and decides
#   whether to run forward simulation, reverse simulation,
#   or ask a clarifying question. User never picks a mode manually.
#
# IMPORTS NEEDED:
#   import re
#   from ollama_engine import call_ollama
#   from models import OrchestrationResponse
#
# KEYWORD LISTS TO DEFINE (as constants at top of file):
#   LOAN_KEYWORDS    = ['loan', 'borrow', 'emi', 'debt', 'credit']
#   SIP_KEYWORDS     = ['sip', 'mutual fund', 'invest monthly']
#   DELAY_KEYWORDS   = ['delay', 'wait', 'later', 'postpone']
#   LUMPSUM_KEYWORDS = ['lump sum', 'one time', 'stocks', 'fd']
#   REVERSE_KEYWORDS = ['want ₹', 'goal', 'target', 'retire with',
#                        'how do i reach', 'how much do i need']
#   CLARIFY_KEYWORDS = ['help', "don't know", 'not sure', 'suggest',
#                        'what should i do']
#
# FUNCTIONS TO WRITE:
#
#   rule_based_route(message)
#     Lowercase the message
#     Check each keyword list in order
#     Return OrchestrationResponse with route + decision_type
#     If no match found, return None (signals fallback needed)
#
#   ollama_route(message)
#     Build a prompt asking Ollama to classify the message
#     Tell Ollama to return ONLY valid JSON:
#       { route: FORWARD/REVERSE/CLARIFY,
#         decision_type: LOAN/SIP/DELAY/LUMPSUM or null }
#     Parse the JSON response
#     Return OrchestrationResponse
#     Wrap in try/except — return CLARIFY if Ollama fails
#
#   smart_orchestrate(message, profile)
#     Step 1: Try rule_based_route(message)
#     Step 2: If None returned, try ollama_route(message)
#     Returns: OrchestrationResponse
#
# ROUTING LOGIC:
#   LOAN match      → FORWARD, decision_type=LOAN
#   SIP match       → FORWARD, decision_type=SIP
#   DELAY match     → FORWARD, decision_type=DELAY
#   LUMPSUM match   → FORWARD, decision_type=LUMPSUM
#   REVERSE match   → REVERSE
#   CLARIFY match   → CLARIFY, question='What are you trying to do?'
#   No match        → Ollama fallback
#
# TESTING BLOCK:
#   if __name__ == '__main__': test 5 messages, print routes
# ─────────────────────────────────────────────────────────────────
