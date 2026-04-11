import requests
import os
from typing import Dict, Any, Optional

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def call_ollama(prompt: str, model: str = "llama3.1:8b") -> str:
    """Raw HTTP call to Ollama (no extra libraries needed)."""
    url = "http://192.168.1.10.66.4.44:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 500
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except Exception as e:
        return f"[Ollama Error: {str(e)} — Is 'ollama serve' running?]"

def build_forward_prompt(profile: Dict[str, Any], decision: Dict[str, Any], result: Dict[str, Any]) -> str:
    age = profile.get("age", 26)
    income = profile.get("monthly_income", 50000)
    goal = profile.get("goal_amount", 10000000)
    goal_age = profile.get("goal_age", 50)
    dec_type = decision.get("type", "LOAN")
    dec_amt = decision.get("amount", 0)
    decision_str = f"{dec_type} of ₹{int(dec_amt):,}" if dec_amt > 0 else dec_type

    best = result.get("best_final", 0)
    expected = result.get("expected_final", 0)
    worst = result.get("worst_final", 0)
    achieved = result.get("goal_achieved", False)

    return f"""You are a friendly, honest financial coach talking directly to the user.

User profile:
- Age: {age}
- Monthly take-home income: ₹{int(income):,}
- Goal: ₹{int(goal):,} by age {goal_age}

Decision they are considering: {decision_str}

Simulation results (if they do the decision):
- Best case final corpus: ₹{int(best):,}
- Expected case: ₹{int(expected):,}
- Worst case: ₹{int(worst):,}
- Goal achieved: {'Yes' if achieved else 'No'}

Write EXACTLY 3 sentences in second person ("You will..."). 
Use real-life examples like school fees, medical emergencies, or retirement. 
No jargon. Be honest but encouraging and not scary.
Exactly 3 sentences only. Nothing else."""

def build_reverse_prompt(profile: Dict[str, Any], result: Dict[str, Any]) -> str:
    age = profile.get("age", 26)
    income = profile.get("monthly_income", 50000)
    goal = profile.get("goal_amount", 10000000)
    goal_age = profile.get("goal_age", 50)

    sip_now = result.get("required_monthly_sip", 0)
    sip_2y = result.get("if_delayed_2_years", 0)
    sip_5y = result.get("if_delayed_5_years", 0)

    return f"""You are a friendly, honest financial coach talking directly to the user.

User profile:
- Age: {age}
- Monthly take-home income: ₹{int(income):,}
- Goal: ₹{int(goal):,} by age {goal_age}

Simulation results:
- Monthly SIP needed if you start NOW: ₹{int(sip_now):,}
- If you delay by 2 years: ₹{int(sip_2y):,}
- If you delay by 5 years: ₹{int(sip_5y):,}

Write EXACTLY 3 sentences in second person ("You will..."). 
Use real-life examples like school fees, medical emergencies, or retirement. 
No jargon. Be honest but encouraging.
Exactly 3 sentences only. Nothing else."""

def get_story(
    profile: Dict[str, Any],          # required
    result: Dict[str, Any],           # required (fixed position)
    decision: Optional[Dict[str, Any]] = None,   # optional
    mode: str = "forward"
) -> str:
    """Returns exactly 3 sentences from Ollama."""
    if mode == "forward":
        prompt = build_forward_prompt(profile, decision or {}, result)
    else:
        prompt = build_reverse_prompt(profile, result)
    
    story = call_ollama(prompt)
    
    # Clean up to exactly 3 sentences
    sentences = [s.strip() for s in story.split(".") if s.strip()]
    if len(sentences) >= 3:
        story = ". ".join(sentences[:3]) + "."
    return story
