<<<<<<< HEAD
# autoanalyst-ai
Autonomous AI Data Analyst Agent with offline demo fallback
=======
# AutoAnalyst AI

AutoAnalyst AI is an autonomous data analyst agent that takes a CSV + a natural language question, generates an analysis plan, writes Python code, executes it on the dataset, and returns charts + insights.

## Features
- Upload CSV and ask a question
- Agent generates:
  - Analysis plan
  - Python code
  - Insights summary
- Executes generated code against a pandas DataFrame `df`
- Saves charts to `outputs/` and renders them in the UI
- Offline Demo Mode fallback for reliability

## Tech Stack
- Python
- Streamlit
- pandas, numpy, matplotlib
- Gemini API (optional / quota-dependent)

## How to Run
1. Create & activate venv
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install streamlit
>>>>>>> 07795f6 (Add AutoAnalyst AI application code)
