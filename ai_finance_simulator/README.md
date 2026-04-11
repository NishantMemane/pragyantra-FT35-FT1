# AI Financial Decision Simulation Engine

> We don't predict your future. We let you live it before you decide.

## Setup
1. `cd backend && pip install -r requirements.txt`
2. `ollama pull llama3.1:8b`
3. Terminal 1: `ollama serve`
4. Terminal 2: `uvicorn main:app --reload --port 8000`
5. Terminal 3: `cd frontend && npm start`
