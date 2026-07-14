from langchain_google_genai import ChatGoogleGenerativeAI
import json

def get_llm(api_key: str):
    # Fallback to a dummy key if none provided (for API usage)
    key = api_key if api_key else "DUMMY_KEY"
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=key)

def plan_assessment(topic: str, level: str, api_key: str = None) -> str:
    """Generates an evaluation blueprint mapping what skills should be tested."""
    llm = get_llm(api_key)
    prompt = f"""Act as an academic coordinator. Create a brief assessment blueprint/syllabus 
    for evaluating a student's knowledge in '{topic}' at a '{level}' level. 
    Outline 3-4 specific core competencies or practical skills they should be tested on."""
    return llm.invoke(prompt).content

def generate_assessment_quiz(topic: str, level: str, api_key: str = None) -> str:
    """Generates a structured test based on the topic."""
    llm = get_llm(api_key)
    prompt = f"""Act as an expert technical examiner. Create a 3-question quiz to test knowledge on '{topic}' at a '{level}' level.
    Provide the questions clearly numbered. Do not show the answers."""
    return llm.invoke(prompt).content

def generate_report(quiz: str, user_answers: str, api_key: str = None) -> str:
    """Grades the answers and compiles a brief report card."""
    llm = get_llm(api_key)
    prompt = f"""Act as an encouraging technical instructor. Review this quiz and the student's answers:
    
    QUIZ:
    {quiz}
    
    STUDENT ANSWERS:
    {user_answers}
    
    Provide a scorecard, correct any mistakes gently, and suggest 1-2 practical next steps."""
    return llm.invoke(prompt).content