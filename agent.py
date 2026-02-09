import os
import google.generativeai as genai


SYSTEM_PROMPT = """
You are an autonomous AI Data Analyst.

Your job is to:
1. Understand the user's analytical question.
2. Create a clear, step-by-step analysis plan.
3. Generate valid Python code to execute the plan.
4. Explain insights clearly to a non-technical user.

Rules:
- Always create an analysis plan before writing code.
- Use pandas, numpy, matplotlib.
- Assume the dataset is already loaded as a pandas DataFrame called df.
- Do NOT hallucinate data.
- If the question cannot be answered with the data, clearly say so.
- IMPORTANT: The Python code MUST generate at least one matplotlib chart.
- IMPORTANT: Do NOT use seaborn.

Output format:
ANALYSIS_PLAN:
- Step 1: ...

PYTHON_CODE:
[python code here]

INSIGHTS:
- Bullet points with findings.
"""


def setup_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Set it in your environment first.")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("models/gemini-2.0-flash")



def analyze_question(question: str) -> str:
    model = setup_gemini()
    prompt = SYSTEM_PROMPT + "\n\nUSER QUESTION:\n" + question
    response = model.generate_content(prompt)
    return response.text


def fix_code(question: str, bad_code: str, error_text: str) -> str:
    return genai.GenerativeModel("models/gemini-2.0-flash")
    prompt = SYSTEM_PROMPT + "\n\n"
    prompt += "The previously generated Python code FAILED during execution.\n\n"
    prompt += "USER QUESTION:\n" + question + "\n\n"
    prompt += "FAILED PYTHON CODE:\n" + bad_code + "\n\n"
    prompt += "ERROR MESSAGE:\n" + error_text + "\n\n"
    prompt += "Return ONLY corrected Python code. The corrected code MUST:\n"
    prompt += "- Use the existing DataFrame df\n"
    prompt += "- Generate at least one matplotlib chart\n"
    prompt += "- End with plt.tight_layout()\n"

    response = model.generate_content(prompt)
    return response.text
