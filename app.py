import os
import tempfile

import streamlit as st

from ingest_pdf import ingest_pdf
from rag_chatbot import query_rag


st.set_page_config(page_title="PDF Chatbot", page_icon="🤖", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>PDF Chatbot</h1>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Document")
    uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])
    enable_ocr = st.checkbox("Use OCR for scanned pages", value=True)
    st.markdown("---")
    st.caption("Powered by LangChain, FAISS, HuggingFace embeddings, and Groq.")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "db" not in st.session_state:
    st.session_state.db = None

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None


def reset_chat():
    st.session_state.messages = []
    st.session_state.db = None
    st.session_state.uploaded_file_name = None


if uploaded_pdf and uploaded_pdf.name != st.session_state.uploaded_file_name:
    reset_chat()
    st.session_state.uploaded_file_name = uploaded_pdf.name

    progress_text = st.empty()

    def show_progress(page, total_pages):
        progress_text.info(f"Processing page {page} of {total_pages}...")

    with st.spinner("Reading your PDF and creating the search index..."):
        suffix = os.path.splitext(uploaded_pdf.name)[1] or ".pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(uploaded_pdf.getbuffer())
            temp_path = temp_file.name

        try:
            st.session_state.db = ingest_pdf(
                temp_path,
                enable_ocr=enable_ocr,
                progress_callback=show_progress,
            )
            progress_text.success(f"Ready to chat with {uploaded_pdf.name}")
        except Exception as exc:
            progress_text.error(f"Could not process this PDF: {exc}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if not st.session_state.db:
    st.info("Upload a PDF from the sidebar to start chatting with it.")
    st.stop()


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])


query = st.chat_input("Ask a question about the uploaded PDF...")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("Thinking..."):
        answer = query_rag(query, st.session_state.db)

    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
