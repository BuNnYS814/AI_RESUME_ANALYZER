import re
import os
import google.generativeai as genai

# Load Gemini API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError('GEMINI_API_KEY environment variable not set')

genai.configure(api_key=GEMINI_API_KEY)

def extract_structured_fields(resume_text):
    # Simple regex-based extraction for demo purposes
    name = re.search(r"^[A-Z][a-z]+ [A-Z][a-z]+", resume_text)
    email = re.search(r"[\w\.-]+@[\w\.-]+", resume_text)
    phone = re.search(r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}", resume_text)
    education = re.findall(r"Education:.*", resume_text, re.IGNORECASE)
    experience = re.findall(r"Experience:.*", resume_text, re.IGNORECASE)
    skills = re.findall(r"Skills:.*", resume_text, re.IGNORECASE)
    certifications = re.findall(r"Certifications:.*", resume_text, re.IGNORECASE)
    
    return {
        "name": name.group(0) if name else None,
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "education": education,
        "experience": experience,
        "skills": skills,
        "certifications": certifications
    }

def ats_feedback(resume_text):
    feedback = []
    if 'table' in resume_text.lower():
        feedback.append("Warning: Tables detected. ATS may not parse tables correctly.")
    if 'image' in resume_text.lower():
        feedback.append("Warning: Images detected. ATS cannot read images.")
    if len(resume_text) > 10000:
        feedback.append("Warning: Resume is very long. ATS may truncate content.")
    if not feedback:
        feedback.append("No major ATS issues detected.")
    return feedback

def analyze_resume(resume_text):
    structured = extract_structured_fields(resume_text)
    ats = ats_feedback(resume_text)
    # Optionally, you can still use Gemini for deeper analysis
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    prompt = f"""
You are a professional resume analyzer. Analyze the following resume and extract key information such as:
- Name
- Contact Information
- Education
- Work Experience
- Skills
- Certifications
- Summary

Resume:
{resume_text}
"""
    response = model.generate_content(prompt)
    return {
        "structured": structured,
        "ats_feedback": ats,
        "gemini_analysis": response.text
    }

if __name__ == "__main__":
    # Example usage
    sample_resume = """
    John Doe
    johndoe@email.com
    123-456-7890
    Education: B.Sc. in Computer Science, XYZ University
    Experience: Software Engineer at ABC Corp (2018-2022)
    Skills: Python, Machine Learning, Data Analysis
    Certifications: AWS Certified Solutions Architect
    """
    result = analyze_resume(sample_resume)
    print(result)
