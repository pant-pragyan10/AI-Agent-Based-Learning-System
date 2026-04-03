import os
import sys
import streamlit as st

# Make imports work whether this file is run from the project root or the ui/ folder.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pipeline.pipeline import run_pipeline

st.set_page_config(page_title="AI Agent System", layout="wide")

st.title("🤖 AI Agent-Based Learning System")

grade = st.number_input("Enter Grade", min_value=1, max_value=10, value=4)
topic = st.text_input("Enter Topic", "Types of angles")

if st.button("Generate Content"):
    with st.spinner("Running AI agents..."):
        result = run_pipeline(grade, topic)

    st.subheader("📘 Generator Output")
    st.json(result["initial"])

    st.subheader("🧠 Reviewer Feedback")
    st.json(result["review"])

    if result.get("refined"):
        st.subheader("🔄 Refined Output")
        st.json(result["refined"])
