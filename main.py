# main.py
# FastAPI Microservice Entrypoint for AI Training & Assessment Engine
import os
import sys
from fastapi import FastAPI
import uvicorn

# Path configuration to ensure local modules are imported smoothly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    import ai_engine
    import assessment_engine
except ModuleNotFoundError as e:
    print(f"Error importing local modules: {e}")

app = FastAPI(title="TechMahindra AI Assessment Microservice Engine")

@app.get("/get-plan")
async def get_plan(topic: str, level: str):
    """API endpoint to get training plan."""
    plan_text = ai_engine.generate_training_plan(topic, level)
    return {"status": "Success", "topic": topic, "level": level, "plan": plan_text}

@app.get("/assessment/quiz")
async def get_assessment_quiz(topic: str, level: str):
    """API endpoint to get assessment quiz using local open-source AI engine."""
    quiz_data = assessment_engine.generate_assessment_quiz(topic, level)
    return {"status": "Success", "topic": topic, "level": level, "quiz": quiz_data}

if __name__ == "__main__":
    # Start FastAPI backend directly on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)