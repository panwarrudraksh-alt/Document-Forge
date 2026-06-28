"""
ai_utils.py – Mistral AI integration using `requests` (no SDK)
"""

import streamlit as st
import requests
import time


def call_mistral(prompt, max_tokens=300, retries=2):
    """
    Send a prompt to Mistral's API using direct HTTP requests.
    Returns the generated text or an error message.
    """
    api_key = st.secrets.get("MISTRAL_API_KEY")
    if not api_key:
        return "⚠️ AI features unavailable. Please add your Mistral API key in Streamlit secrets."

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    for attempt in range(retries):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                error_msg = response.json().get("error", {}).get("message", str(response.status_code))
                return f"⚠️ API Error: {error_msg}"
        except requests.exceptions.Timeout:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return "⚠️ Request timed out. Please try again."
        except Exception as e:
            return f"⚠️ Error: {str(e)}"
    return "⚠️ Max retries exceeded. Please try again later."


def ai_suggest_improvements(section, content):
    """Suggest improvements for a specific resume section."""
    if not content or len(content) < 10:
        return "Please enter more text to get useful suggestions."
    prompt = f"""I have a {section} section in my resume. Suggest specific improvements to make it more impactful, professional, and ATS-friendly.

Current content:
{content}

Provide your suggestions as a numbered list of bullet points. Keep each suggestion concise and actionable.
"""
    return call_mistral(prompt, max_tokens=300)


def ai_generate_summary(name, title, skills, experience):
    """Generate a 3‑4 sentence professional summary."""
    prompt = f"""Write a compelling professional summary for a {title} named {name}.
Skills: {skills}
Relevant experience: {experience}

Keep it to 3‑4 sentences, using a confident and professional tone. Do not use bullet points.
"""
    return call_mistral(prompt, max_tokens=200)


def ai_generate_cover_letter(name, job_title, company, skills, experience):
    """Generate a full cover letter."""
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
    """Suggest a comma‑separated list of top skills for a job title."""
    prompt = f"List the top 8 skills for a {job_title} separated by commas. Only list the skills, no extra text."
    return call_mistral(prompt, max_tokens=100)


def ai_improve_text(text, context=""):
    """Generic text improver."""
    if not text or len(text) < 10:
        return "Please enter more text to improve."
    prompt = f"Improve the following {context} to be more professional, impactful, and concise:\n\n{text}"
    return call_mistral(prompt, max_tokens=300)
