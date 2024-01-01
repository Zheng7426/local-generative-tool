import streamlit as st
import random
import time
from openai import OpenAI


st.title("Chatbot 💬")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar='./static/olu.png'):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# react to user input
if prompt := st.chat_input("What is up?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    # display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # display assistant message in chat message container
    with st.chat_message("assistant", avatar='./static/olu.png'):
        message_placeholder = st.empty()
        full_response = ""

        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})