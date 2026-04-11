from orchestrator import smart_orchestrate
tests = [
    "I want to take a loan",
    "I want ₹1 crore by 50",
    "I dont know",
    "Should I buy a car on EMI?",
    "How much do I need to save to retire?"
]
for t in tests:
    print(t, "→", smart_orchestrate(t))
