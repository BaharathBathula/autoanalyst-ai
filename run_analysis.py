import pandas as pd
from agent import analyze_question
from executor import extract_python_code, run_user_code

print("✅ AutoAnalyst AI — Day 2 Run")

df = pd.read_csv("data/sample_data.csv")
print("✅ Loaded dataset:", df.shape)

question = (
    "Perform EDA on df. "
    "1) Print missing values per column. "
    "2) Print summary stats for numeric columns. "
    "3) Create at least ONE matplotlib chart: "
    "   - If numeric columns exist, plot a histogram for the most important numeric column. "
    "   - If categorical columns exist, plot top 10 categories by count as a bar chart. "
    "End your code with plt.tight_layout(). "
    "Return python code only."
)

gemini_text = analyze_question(question)

print("\n========== GEMINI OUTPUT (first 800 chars) ==========\n")
print(gemini_text[:800])

code = extract_python_code(gemini_text)

print("\n✅ Executing generated code...")
stdout, charts = run_user_code(code, df)

print("\n========== CODE STDOUT ==========\n")
print(stdout)

print("\n✅ Charts saved:")
for c in charts:
    print(" -", c)

print("\n✅ Done.")
