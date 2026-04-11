import urllib.request
import json
data = json.dumps({
    "profile": {"age": 20, "monthly_income": 50000, "monthly_expenses": 30000, "existing_savings": 0, "goal_amount": 10000000, "goal_age": 30},
    "decision": {"type": "SIP", "monthly_sip": 5000, "amount": 0, "interest_rate": 0, "tenure_months": 0, "cash_flow_reduction": 0, "delay_years": 0, "instrument": "equity"}
}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/api/simulate/forward', data=data, headers={'Content-Type': 'application/json'})
res = urllib.request.urlopen(req)
print(res.read().decode())
