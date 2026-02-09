import os
import pandas as pd
import streamlit as st

from executor import extract_python_code, run_user_code
from mock_gemini import mock_gemini_response

st.set_page_config(page_title="AutoAnalyst AI", layout="wide")

st.title("AutoAnalyst AI")
st.caption("Autonomous AI Data Analyst Agent (Gemini-powered) with offline demo fallback.")

# Sidebar controls
st.sidebar.header("Settings")
use_offline = st.sidebar.checkbox("Force Offline Demo Mode", value=False)

st.sidebar.markdown("**Tip:** If Gemini quota fails, the app automatically falls back to offline mode.")

uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

question = st.text_area(
    "Ask a question about your data",
    value="Perform EDA: missing values, summary stats, and generate at least one chart.",
    height=120,
)

run_btn = st.button("Analyze")

if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.success(f"Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")
    st.dataframe(df.head(20), use_container_width=True)
else:
    df = None

if run_btn:
    if df is None:
        st.error("Please upload a CSV first.")
        st.stop()

    # Get “Gemini” output (live or offline)
    gemini_text = None

    if not use_offline:
        try:
            from agent import analyze_question
            gemini_text = analyze_question(question)
            st.info("✅ Live Gemini mode used.")
        except Exception as e:
            st.warning("⚠️ Live Gemini failed (quota or API error). Switching to Offline Demo Mode.")
            st.code(str(e)[:400])
            gemini_text = mock_gemini_response(list(df.columns))
    else:
        st.info("✅ Offline Demo Mode forced.")
        gemini_text = mock_gemini_response(list(df.columns))

    # Show model output
    st.subheader("Agent Output")
    st.text(gemini_text[:3000])

    # Extract + run code
    st.subheader("Execution")
    code = extract_python_code(gemini_text)

    st.markdown("**Extracted Python code:**")
    st.code(code, language="python")

    stdout, charts = run_user_code(code, df)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Console output:**")
        st.text(stdout if stdout else "(no stdout)")

    with col2:
        st.markdown("**Charts:**")
        if charts:
            for c in charts:
                st.image(c, use_container_width=True)
        else:
            st.error("No charts were generated.")
