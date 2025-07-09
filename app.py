import streamlit as st
import fitz  # PyMuPDF
from resume_parser import analyze_resume
from ai_feedback import get_gemini_feedback

st.set_page_config(page_title="Resume Analyzer with Gemini AI")
st.title("Resume Analyzer with Gemini AI")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    # Extract text from PDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    resume_text = " ".join([page.get_text() for page in doc])
    st.subheader("Extracted Resume Text:")
    st.text_area("Resume Text", resume_text, height=300)

    if st.button("Analyze with Gemini AI"):
        with st.spinner("Analyzing resume with Gemini..."):
            # Get structured analysis
            analysis = analyze_resume(resume_text)
            st.subheader("Gemini Resume Analysis:")
            st.write(analysis)

            # Get feedback
            feedback = get_gemini_feedback(resume_text)
            st.subheader("Gemini Resume Feedback:")
            st.write(feedback)
