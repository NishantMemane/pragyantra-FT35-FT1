from ollama_engine import get_story
 
profile = {"age": 26, "monthly_income": 50000, "goal_amount": 10000000, "goal_age": 50}
decision = {"type": "LOAN", "amount": 500000}
result = {
    "best_final": 12400000,
    "expected_final": 7100000,
    "worst_final": 4000000,
    "goal_achieved": False
}

story = get_story(profile, result, decision, mode="forward")
print("STORY GENERATED:\n", story)
