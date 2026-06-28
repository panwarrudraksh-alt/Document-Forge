import streamlit as st
from mistralai import Mistral

# System prompt for the assistant
SYSTEM_PROMPT = """
You are a helpful career assistant for DocForge. Your expertise includes:
- Resume and CV writing best practices
- Cover letter tips
- Job search strategies
- Interview preparation
- Professional communication

Keep responses concise, friendly, and actionable. Use bullet points when helpful.
"""

def get_mistral_client():
    api_key = st.secrets.get("MISTRAL_API_KEY")
    if not api_key:
        return None
    return Mistral(api_key=api_key)

def chat_with_ai(user_message, history=None):
    """Send a message to Mistral and return the assistant's reply."""
    client = get_mistral_client()
    if not client:
        return "⚠️ AI assistant is unavailable. Please set your Mistral API key."

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=messages,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
