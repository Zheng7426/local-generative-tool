import streamlit as st
import random
import time


st.title("Simple chat")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# react to user input
if prompt := st.chat_input("What is up?"):
    # display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
        )
        # simulate stream of response with a bit delay 
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})