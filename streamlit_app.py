import pandas as pd
import streamlit as st

from executor import extract_python_code, run_user_code
from mock_gemini import mock_gemini_response

st.set_page_config(page_title="AutoAnalyst AI", layout="wide")

st.title("AutoAnalyst AI")
st.caption("Autonomous AI Data Analyst Agent (Gemini-powered) with offline demo fallback.")

# =========================
# Sidebar controls
# =========================
st.sidebar.header("Settings")
use_offline = st.sidebar.checkbox("Force Offline Demo Mode", value=False)
st.sidebar.markdown("**Tip:** If Gemini quota fails, the app automatically falls back to offline mode.")

# =========================
# 1) Upload CSV
# =========================
uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

# Disable analyze until file uploaded
run_btn = st.button("Analyze", disabled=(uploaded is None))

# Load dataframe
df = None
if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        st.success(f"Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")
        st.dataframe(df.head(20), use_container_width=True)
    except Exception as e:
        st.error("❌ Failed to read CSV")
        st.exception(e)
        st.stop()
else:
    st.info("Upload a CSV to start.")

# =========================
# 2) Question input
# (keep it visible; still safe even before upload)
# =========================
question = st.text_area(
    "Ask a question about your data",
    value="Perform EDA: missing values, summary stats, and generate at least one chart.",
    height=120,
)

# =========================
# 3) Analyze flow
# =========================
if run_btn:
    # Safety check (should not happen because button disabled, but keep it)
    if df is None:
        st.error("Please upload a CSV first.")
        st.stop()

    with st.spinner("Analyzing..."):
        st.write("✅ Analyze button clicked")
        st.write("Question:", question)

        # -------------------------
        # A) Get “Gemini” output (live or offline)
        # -------------------------
        gemini_text = None

        if not use_offline:
            try:
                from agent import analyze_question  # your live agent
                gemini_text = analyze_question(question)
                st.info("✅ Live Gemini mode used.")
            except Exception as e:
                st.warning("⚠️ Live Gemini failed. Switching to Offline Demo Mode.")
                st.exception(e)
                gemini_text = mock_gemini_response(list(df.columns), question)
        else:
            st.info("✅ Offline Demo Mode forced.")
            gemini_text = mock_gemini_response(list(df.columns), question)

        if not gemini_text or not isinstance(gemini_text, str):
            st.error("❌ Agent returned empty output.")
            st.stop()

        # -------------------------
        # B) Show agent output
        # -------------------------
        st.subheader("Agent Output")
        st.text(gemini_text[:3000])

        # -------------------------
        # C) Extract + run code
        # -------------------------
        st.subheader("Execution")
        code = extract_python_code(gemini_text)

        if not code or not code.strip():
            st.error("❌ No Python code found in agent output.")
            st.stop()

        st.markdown("**Extracted Python code:**")
        st.code(code, language="python")

        # Run code safely
        try:
            stdout, charts = run_user_code(code, df)
        except Exception as e:
            st.error("❌ Code execution failed")
            st.exception(e)
            st.stop()

    # =========================
    # 4) Display results (outside spinner)
    # =========================
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Console output:**")
        st.text(stdout if stdout else "(no stdout)")

    with col2:
        st.markdown("**Charts:**")
        if charts:
            for c in charts:
                # charts may be file paths or image bytes depending on your executor
                try:
                    st.image(c, use_container_width=True)
                except Exception as e:
                    st.warning("Could not render one chart.")
                    st.exception(e)
        else:
            st.error("No charts were generated.")