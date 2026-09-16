import streamlit as st
import sys
import os

# Ensure the root directory is in the path to import the agent
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from agent.agent import ask

st.set_page_config(page_title="AI Sales Intelligence Assistant", page_icon="📊", layout="wide")

st.title("AI Sales Intelligence Assistant 📊")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for example questions
with st.sidebar:
    st.header("Example Questions")
    st.markdown("""
    - What are total sales?
    - Which region has highest profit?
    - Why is Furniture underperforming?
    - What are next 3 months forecast?
    """)
    st.markdown("---")
    st.markdown("Ask anything about our sales data and the AI will analyze it for you.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me about sales performance..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            try:
                response = ask(prompt, history=st.session_state.messages[:-1])
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error while analyzing the data. Please try again. ({str(e)})"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
