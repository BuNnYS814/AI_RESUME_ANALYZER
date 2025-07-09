import os
import google.generativeai as genai

# Load Gemini API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError('GEMINI_API_KEY environment variable not set')

genai.configure(api_key=GEMINI_API_KEY)

def analyze_resume(resume_text):
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
    return response.text

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
