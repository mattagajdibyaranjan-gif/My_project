import os
import sys
from fastapi import FastAPI
import uvicorn

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    import ai_engine
    import assessment_engine
except ModuleNotFoundError as e:
    print(f"Error importing modules: {e}")

app = FastAPI(title="AI Training Agent API")

@app.get("/get-plan")
async def get_plan(topic: str, level: str):
    return {"plan": ai_engine.generate_training_plan(topic, level)}

@app.get("/assessment/quiz")
async def get_assessment_quiz(topic: str, level: str, api_key: str):
    return {"quiz": assessment_engine.generate_assessment_quiz(topic, level, api_key)}

if __name__ == "__main__":
    # Start FastAPI backend directly on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)