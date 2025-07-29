# app.py

import streamlit as st
from rag_chatbot import query_rag

st.set_page_config(page_title="PDF Chatbot", page_icon="🤖", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>📘 CSR PDF Chatbot</h1>", unsafe_allow_html=True
)

with st.sidebar:
    st.header("Ask Me Anything 🤖")
    st.markdown("Based on: **CSR MODULES.pdf**")
    st.markdown("---")
    st.markdown("👨‍💻 Powered by:")
    st.markdown("- LangChain + FAISS")
    st.markdown("- HuggingFace MiniLM")
    st.markdown("- Groq LLaMA3 API")
    st.markdown("---")
    st.caption("Made with ❤️ by Bala")

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input box
query = st.chat_input("Type your question here...")

if query:
    # Display user message
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Loading spinner while getting answer
    with st.spinner("🤔 Thinking..."):
        answer = query_rag(query)

    # Display bot answer
    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
