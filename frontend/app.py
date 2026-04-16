import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Chatbot with Memory", layout="wide")

st.title("🤖 Chatbot with Memory")

# Sidebar
st.sidebar.header("User Profile")

name = st.sidebar.text_input("Name")
interests = st.sidebar.text_area("Interests")
skills = st.sidebar.text_area("Skills")

if st.sidebar.button("Save Profile"):
    requests.post(f"{API_URL}/user", json={
        "name": name,
        "interests": interests,
        "skills": skills
    })
    st.sidebar.success("Profile Saved!")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        response = requests.post(f"{API_URL}/chat", json={
            "user_id": 1,
            "content": user_input
        })

        reply = response.json()["response"]

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)