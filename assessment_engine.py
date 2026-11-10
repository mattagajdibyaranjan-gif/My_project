# assessment_engine.py
from langchain_community.chat_models import ChatOllama

def get_llm():
    # Local Open-Source Ollama Model (No API Key Required)
    return ChatOllama(model="llama3.2:1b", temperature=0.7)

def plan_assessment(topic: str, level: str) -> str:
    """Generates an evaluation blueprint mapping what skills should be tested."""
    llm = get_llm()
    prompt = f"""Act as an academic coordinator. Create a brief assessment blueprint/syllabus 
    for evaluating a student's knowledge in '{topic}' at a '{level}' level. 
    Outline 3-4 specific core competencies or practical skills they should be tested on."""
    response = llm.invoke(prompt)
    return response.content

def generate_assessment_quiz(topic: str, level: str) -> str:
    """Generates a structured test based on the topic."""
    llm = get_llm()
    prompt = f"""Act as an expert technical examiner. Create a 3-question quiz to test knowledge on '{topic}' at a '{level}' level.
    Provide the questions clearly numbered. Do not show the answers."""
    response = llm.invoke(prompt)
    return response.content

def generate_report(quiz: str, user_answers: str) -> str:
    """Grades the answers and compiles a brief report card."""
    llm = get_llm()
    prompt = f"""Act as an encouraging technical instructor. Review this quiz and the student's answers:
    
    QUIZ:
    {quiz}
    
    STUDENT ANSWERS:
    {user_answers}
    
    Provide a scorecard, correct any mistakes gently, and suggest 1-2 practical next steps."""
    response = llm.invoke(prompt)
    return response.content