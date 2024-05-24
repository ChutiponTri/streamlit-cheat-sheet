import streamlit as st
from ollama import Ollama, OllamaException
import httpx

ollama = Ollama()

def generate_response():
    try:
        response = ollama.chat(model='phi3', stream=True, messages=st.session_state.messages)
        for partial_resp in response:
            token = partial_resp["message"]["content"]
            st.session_state["full_message"] += token
            yield token
    except (OllamaException, httpx.HTTPStatusError) as e:
        st.error(f"Error during Ollama request: {e}")
    except httpx.ConnectError as e:
        st.error(f"Connection error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Your Streamlit app logic
if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.text_input("Enter your message:")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    st.session_state["full_message"] = ""
    for response in generate_response():
        st.chat_message("assistant", avatar="🤖").write(response)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})
