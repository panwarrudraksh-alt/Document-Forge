"""
ai_utils.py – AI-powered helpers using Mistral API
"""

import streamlit as st
from mistralai import Mistral


# ----------------------------------------------------------------------
# Initialize Mistral client (cached)
# ----------------------------------------------------------------------
@st.cache_resource
def get_mistral_client():
    """Return a Mistral client instance using the API key from secrets."""
    api_key = st.secrets.get("MISTRAL_API_KEY")
    if not api_key:
        st.warning("Mistral API key not set. AI features will be disabled.")
        return None
    return Mistral(api_key=api_key)


# ----------------------------------------------------------------------
# Core API call with error handling and basic retry
# ----------------------------------------------------------------------
def call_mistral(prompt, model="mistral-small-latest", max_tokens=300, retries=2):
    """
    Send a prompt to Mistral and return the generated text.
    Uses a small model by default to stay within free tier limits.
    """
    client = get_mistral_client()
    if not client:
        return "⚠️ AI features unavailable – please add your Mistral API key in Streamlit secrets."

    for attempt in range(retries):
        try:
            response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "rate_limit" in str(e).lower() and attempt < retries - 1:
                import time
                time.sleep(2 ** attempt)   # exponential backoff
                continue
            return f"⚠️ Error: {str(e)}"
    return "⚠️ Rate limit exceeded. Please try again later."


# ----------------------------------------------------------------------
# Document improvement functions
# ----------------------------------------------------------------------
def ai_suggest_improvements(section, content):
    """
    Suggest specific improvements for a given section of a resume or other document.
    section: e.g., "job description", "professional summary"
    content: the current text
    """
    if not content or len(content) < 10:
        return "Please enter more text to get useful suggestions."

    prompt = f"""I have a {section} section in my resume. Suggest specific improvements to make it more impactful, professional, and ATS-friendly.

Current content:
{content}

Provide your suggestions as a numbered list of bullet points. Keep each suggestion concise and actionable.
"""
    return call_mistral(prompt, max_tokens=300)


def ai_generate_summary(name, title, skills, experience):
    """
    Generate a 3‑4 sentence professional summary based on user data.
    """
    prompt = f"""Write a compelling professional summary for a {title} named {name}.
Skills: {skills}
Relevant experience: {experience}

Keep it to 3‑4 sentences, using a confident and professional tone. Do not use bullet points.
"""
    return call_mistral(prompt, max_tokens=200)


def ai_generate_cover_letter(name, job_title, company, skills, experience):
    """
    Generate a full cover letter for a job application.
    """
    prompt = f"""Write a professional cover letter for {name} applying for the position of {job_title} at {company}.
Skills: {skills}
Relevant experience: {experience}

Structure:
- Opening paragraph: express interest and mention the role.
- Middle paragraph: highlight relevant skills and experience.
- Closing paragraph: express enthusiasm and request an interview.

Keep the tone formal yet warm, and keep it to 3 short paragraphs.
"""
    return call_mistral(prompt, max_tokens=500)


def ai_autofill_skills(job_title):
    """
    Suggest a comma‑separated list of top skills for a given job title.
    """
    prompt = f"List the top 8 skills for a {job_title} separated by commas. Only list the skills, no extra text."
    return call_mistral(prompt, max_tokens=100)


def ai_improve_text(text, context=""):
    """
    Generic text improver – used for user‑provided custom text.
    """
    if not text or len(text) < 10:
        return "Please enter more text to improve."
    prompt = f"Improve the following {context} to be more professional, impactful, and concise:\n\n{text}"
    return call_mistral(prompt, max_tokens=300)
    try:
    from mistralai import Mistral
except ImportError:
    Mistral = None
    st.warning("Mistral package not installed. AI features disabled.")
