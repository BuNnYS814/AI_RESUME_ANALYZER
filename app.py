import streamlit as st
import fitz  # PyMuPDF
from resume_parser import analyze_resume
from ai_feedback import get_gemini_feedback
import requests
import os
import urllib.parse

st.set_page_config(page_title="Resume Analyzer with Gemini AI")
st.title("Resume Analyzer with Gemini AI")

# LinkedIn OAuth settings
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "YOUR_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8501/"
SCOPE = "r_liteprofile r_emailaddress"

# Step 1: Show LinkedIn login button
params = {
    "response_type": "code",
    "client_id": LINKEDIN_CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "state": "random_string123"
}
login_url = f"https://www.linkedin.com/oauth/v2/authorization?{urllib.parse.urlencode(params)}"

st.markdown(f"[Connect with LinkedIn]({login_url})")

# Step 2: Handle redirect and fetch profile
query_params = st.query_params
if "code" in query_params:
    code = query_params["code"][0]
    # Exchange code for access token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET
    }
    resp = requests.post(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    if resp.ok:
        access_token = resp.json()["access_token"]
        # Fetch profile data
        profile_resp = requests.get(
            "https://api.linkedin.com/v2/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if profile_resp.ok:
            st.subheader("LinkedIn Profile Data:")
            st.json(profile_resp.json())
        else:
            st.error("Failed to fetch LinkedIn profile data.")
    else:
        st.error("Failed to get LinkedIn access token.")

# --- Existing Resume Analyzer UI ---
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    # Extract text from PDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    resume_text = " ".join([page.get_text() for page in doc])
    st.subheader("Extracted Resume Text:")
    st.text_area("Resume Text", resume_text, height=300)

    if st.button("Analyze with Gemini AI"):
        with st.spinner("Analyzing resume with Gemini..."):
            result = analyze_resume(resume_text)
            st.subheader("Structured Resume Data:")
            st.json(result["structured"])
            st.subheader("ATS Feedback:")
            st.write(result["ats_feedback"])
            st.subheader("Gemini Resume Analysis:")
            st.write(result["gemini_analysis"])

            feedback = get_gemini_feedback(resume_text)
            st.subheader("Gemini Resume Feedback:")
            st.write(feedback)
