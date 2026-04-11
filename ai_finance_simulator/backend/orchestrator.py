import json
from typing import Dict, Any
from ollama_engine import call_ollama

def keyword_route(message: str) -> Dict[str, Any]:
    """Fast zero-AI keyword router (handles 80% of cases)."""
    msg = message.lower().strip()
    
    forward_kw = ["loan", "borrow", "emi", "personal loan", "take a loan", "buy on emi", "lump sum"]
    reverse_kw = ["goal", "retire", "retirement", "crore by", "lakh by", "want ₹", "save for", "reach ₹", "by age", "₹1 crore"]
    
    if any(kw in msg for kw in forward_kw):
        decision_type = "LOAN"
        if "sip" in msg or "monthly investment" in msg:
            decision_type = "SIP"
        elif "lump sum" in msg:
            decision_type = "LUMPSUM"
        return {"route": "FORWARD", "decision_type": decision_type, "question": None}
    
    elif any(kw in msg for kw in reverse_kw):
        return {"route": "REVERSE", "decision_type": None, "question": None}
    
    return {"route": "CLARIFY", "decision_type": None, "question": None}

def ollama_route(message: str) -> Dict[str, Any]:
    """Ollama fallback router (20% of unclear cases)."""
    prompt = f'''You are a smart router for a financial simulation app.

User message: "{message}"

Decide:
- FORWARD → user wants to simulate a decision (loan, EMI, SIP, lump sum)
- REVERSE → user has a goal (₹X by age Y, retire, etc.)
- CLARIFY → too vague

Respond with EXACTLY this JSON and nothing else:

{{
  "route": "FORWARD" or "REVERSE" or "CLARIFY",
  "decision_type": "LOAN" or "SIP" or "LUMPSUM" or "DELAY" or null,
  "question": "one short clarifying question" or null
}}'''

    raw = call_ollama(prompt)
    
    try:
        # Extract JSON even if LLM adds extra text
        start = raw.find("{")
        end = raw.rfind("}") + 1
        json_str = raw[start:end]
        result = json.loads(json_str)
        return result
    except:
        # Safe fallback
        return {
            "route": "CLARIFY",
            "decision_type": None,
            "question": "What specific financial decision or goal are you thinking about?"
        }

def smart_orchestrate(message: str, profile: Dict[str, Any] = None) -> Dict[str, Any]:
    """Main function used by main.py — keywords first, Ollama only if needed."""
    result = keyword_route(message)
    if result["route"] != "CLARIFY":
        return result
    return ollama_route(message)
