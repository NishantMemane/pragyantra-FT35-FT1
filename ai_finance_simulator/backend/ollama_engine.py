# ─────────────────────────────────────────────────────────────────
# ollama_engine.py — Local LLM story generation
# ─────────────────────────────────────────────────────────────────
#
# PURPOSE:
#   Take dry simulation numbers and turn them into a 3-sentence
#   human story that users will actually remember and feel.
#   Connects to Ollama running locally — no external API needed.
#
# IMPORTS NEEDED:
#   import requests
#   import json
#   from models import UserProfile, DecisionParams, SimulationResult
#   from models import ReverseResult
#
# OLLAMA DETAILS:
#   URL: http://localhost:11434/api/generate
#   Model: llama3.1:8b (or mistral:7b as fallback)
#   Method: POST with JSON body
#   Body: { model, prompt, stream: false }
#   Response field: response.json()['response']
#
# FUNCTIONS TO WRITE:
#
#   call_ollama(prompt)
#     Raw HTTP POST to Ollama
#     Wraps in try/except — returns fallback string if Ollama is down
#     Returns: plain string (the story text)
#
#   build_forward_prompt(profile, decision, result)
#     Constructs the prompt string for forward simulation
#     Tell Ollama:
#       - User's age, income, goal
#       - The decision they made (loan/SIP/etc)
#       - Best / Expected / Worst final corpus
#       - Whether goal is achieved in expected case
#       - Post-tax corpus and LTCG paid
#     Instruct Ollama:
#       - Exactly 3 sentences
#       - Use second person (you / your)
#       - Use real life events (school fees, medical, retirement)
#       - No jargon, no bullet points
#       - Honest but not scary
#
#   build_reverse_prompt(profile, result)
#     Constructs the prompt string for reverse simulation
#     Tell Ollama:
#       - User's goal and target age
#       - Required monthly SIP
#       - Cost of delaying 2 and 5 years
#       - Total invested vs total returns
#     Same 3-sentence, second-person, no-jargon instructions
#
#   get_story(profile, decision, result, mode)
#     mode = 'forward' or 'reverse'
#     Picks the right prompt builder based on mode
#     Calls call_ollama with the built prompt
#     Returns: story string
#
# FALLBACK BEHAVIOR:
#   If Ollama is unreachable, return a generic but reasonable
#   summary string so the app doesn't crash
#
# TESTING BLOCK:
#   if __name__ == '__main__': hardcode Riya's result, print story
# ─────────────────────────────────────────────────────────────────
