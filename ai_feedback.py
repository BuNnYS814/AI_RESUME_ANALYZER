import google.generativeai as genai
import os

# Set your Gemini API key here (or use an environment variable for security)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError('GEMINI_API_KEY environment variable not set')

genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_feedback(resume_text, jd_text=None):
    prompt = f"""
You are a professional resume coach. Review the following resume and suggest:
1. Improvements in content and formatting
2. Keywords to add based on current trends
3. If JD is provided, give job-specific feedback.

Resume:
{resume_text}
"""

    if jd_text:
        prompt += f"\nJob Description:\n{jd_text}\n"

    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# Example usage
def main():
    sample_resume = """
    Jane Smith
    janesmith@email.com
    987-654-3210
    Education: M.Sc. in Data Science, ABC University
    Experience: Data Analyst at XYZ Inc (2019-2023)
    Skills: SQL, Python, Data Visualization
    Certifications: Google Data Analytics Professional Certificate
    """
    sample_jd = "Data Scientist position requiring Python, SQL, and experience with data visualization tools."
    feedback = get_gemini_feedback(sample_resume, sample_jd)
    print(feedback)

if __name__ == "__main__":
    main()
