import streamlit as st
import requests

st.title("Conversational RAG App")

# Input fields
session_id = st.text_input("Enter session ID", value="abc123")
user_question = st.text_input("Enter your question")

# Button to ask the question
if st.button("Ask"):
    if session_id and user_question:
        # Make a POST request to the FastAPI backend
        response = requests.post(
            "http://127.0.0.1:8001/ask",  # URL of your FastAPI server
            json={"session_id": session_id, "input": user_question}
        )
        
        # Handle the response
        if response.status_code == 200:
            st.success(f"Answer: {response.json()['answer']}")
        else:
            st.error(f"Error: {response.text}")