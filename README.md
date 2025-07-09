# README.md

# 🧠 AI Resume Analyzer + Feedback Coach

This project is a smart resume analyzer that uses NLP and GPT to give actionable, AI-generated feedback on your resume. It also matches your resume against job descriptions and provides a similarity score.

## 🚀 Features
- ✅ Upload your resume (PDF)
- 🔍 Extracts content and matches against job description
- 🧠 AI-powered feedback from GPT
- 📊 Resume score based on JD relevance

## 📦 Tech Stack
- Python, Streamlit
- PyMuPDF for PDF parsing
- Scikit-learn for similarity scoring
- OpenAI GPT-4 for coaching

## 🛠️ Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🧪 Sample Inputs
- Place your resume in `sample_data/resume.pdf`
- Paste any job description in `sample_data/job_description.txt`

## 🌐 Deployment
You can deploy this to Streamlit Cloud for free:
1. Push this project to GitHub
2. Go to https://streamlit.io/cloud and link your GitHub repo
3. Set environment variable `OPENAI_API_KEY`

## 📬 Contact
Feel free to connect with me on [LinkedIn](https://www.linkedin.com/) or raise issues on the GitHub repo.
