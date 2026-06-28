"""
chat_utils.py – Chatbot using Mistral API directly (no SDK)
"""

import streamlit as st
import requests
import time

SYSTEM_PROMPT = """
You are a helpful career assistant for DocForge. Your expertise includes:
- Resume and CV writing best practices
- Cover letter tips
- Job search strategies
- Interview preparation
- Professional communication

Keep responses concise, friendly, and actionable. Use bullet points when helpful.
"""

def call_mistral_api(prompt, max_tokens=300, retries=2):
    """
    Send a prompt to Mistral's API using direct HTTP requests.
    Returns the generated text or an error message.
    """
    api_key = st.secrets.get("MISTRAL_API_KEY")
    if not api_key:
        return "⚠️ AI assistant unavailable. Please add your Mistral API key in Streamlit secrets."

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


def chat_with_ai(user_message, history=None):
    """
    Send a user message to the AI assistant with conversation history.
    Returns the assistant's reply.
    """
    # Build the full conversation history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    # Convert to a single prompt for the API
    # Since the API only supports a single user message, we combine history into one prompt.
    # For a more advanced approach, you could use the chat completion endpoint with a list of messages,
    # but we'll keep it simple and concatenate.
    conversation = ""
    for msg in messages:
        if msg["role"] == "system":
            conversation += f"System: {msg['content']}\n"
        elif msg["role"] == "user":
            conversation += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            conversation += f"Assistant: {msg['content']}\n"

    # Add the final user message
    # But we already have it in the loop; we'll just use the last user message.
    # Actually, we'll just send the last user message with context in the prompt.
    # For better context, we could include the whole history in the prompt.
    # We'll do that: include the entire history.
    prompt = conversation + f"Assistant:"
    return call_mistral_api(prompt, max_tokens=300)
