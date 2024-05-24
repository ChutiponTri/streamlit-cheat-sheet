## the imports ##
import streamlit as st
import ollama
import subprocess

result = subprocess.Popen(['ollama', 'pull', 'phi3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
result = subprocess.Popen(['ollama', 'pull', 'nomic-embed-text'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = result.communicate()

## the title
st.title("♿ ALL Wheelchair Chatbot")

## the first message of the AI assisstant ##
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello Wheelchair User! How can I help you today?"}]

### Message History ##
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="♿").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

## Configure the model to use (in our case, the Phi-3)
def generate_response():
    response = ollama.chat(model='phi3', stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})
