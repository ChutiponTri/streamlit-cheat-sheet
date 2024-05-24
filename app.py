## the imports ##
import streamlit as st
import ollama
import subprocess

def run_custom_command(command):
    result = subprocess.run(command.split(), capture_output=True)
    if result.returncode == 0:
        return result.stdout.decode()
    else:
        return result.stderr.decode()

st.title("Custom Command Execution")

command = st.text_input("Enter Command:")
if st.button("Run Command"):
    output = run_custom_command(command)
    st.text_area("Output:", value=output, height=200)

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
