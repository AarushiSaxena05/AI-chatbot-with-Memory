import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_prompt(user_input, user_profile, history):
    system_prompt = (
        "You are a helpful AI assistant with memory.\n"
        "You remember user preferences and past conversations."
    )

    profile_context = f"""
User Profile:
Name: {user_profile.name if user_profile else 'Unknown'}
Interests: {user_profile.interests if user_profile else ''}
Skills: {user_profile.skills if user_profile else ''}
"""

    history_text = ""
    for msg in history:
        history_text += f"{msg.role}: {msg.content}\n"

    final_prompt = f"""
{system_prompt}

{profile_context}

Conversation History:
{history_text}

User: {user_input}
Assistant:
"""

    return final_prompt


def generate_response(user_input, user_profile, history):
    prompt = build_prompt(user_input, user_profile, history)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content