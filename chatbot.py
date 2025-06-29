import os
import threading
import pyttsx3
import streamlit as st
from dotenv import load_dotenv
import cohere

# Load environment variables
load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Voice output
def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# Use Cohere for response
def ask_cohere(user_input):
    try:
        response = co.chat(message=user_input)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
def main():
    st.title("🤖 Smart Chatbot (Powered by Cohere)")
    st.write("Ask anything you like — I'm your AI assistant!")

    user_input = st.text_input("You:", key="input")

    if user_input:
        response = ask_cohere(user_input)
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

    if "chat_history" in st.session_state:
        st.subheader("Chat History (Latest on top)")
        for sender, message in reversed(st.session_state.chat_history):
            st.markdown(f"**{sender}:** {message}")

        if st.button("🔊 Speak Last Bot Reply"):
            for sender, message in reversed(st.session_state.chat_history):
                if sender == "Bot":
                    speak(message)
                    break

if __name__ == "__main__":
    main()
