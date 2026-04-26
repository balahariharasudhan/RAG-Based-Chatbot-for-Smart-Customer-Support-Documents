import os

import requests
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

from ingest_pdf import get_embedding_model


load_dotenv()


DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"

TEMPLATE = """You are a helpful assistant. Use the following context to answer the user's question accurately and clearly.

Context:
{context}

Question:
{question}

Answer:"""


def get_groq_api_key():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to .env locally or Streamlit secrets when deployed.")
    return api_key


def generate_prompt(context, question):
    return TEMPLATE.format(context=context, question=question)


def load_vectorstore(path="vectorstore"):
    embedding = get_embedding_model()
    return FAISS.load_local(path, embedding, allow_dangerous_deserialization=True)


def query_rag(user_question, db, api_key=None):
    docs = db.similarity_search(user_question, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)
    final_prompt = generate_prompt(context, user_question)

    headers = {
        "Authorization": f"Bearer {api_key or get_groq_api_key()}",
        "Content-Type": "application/json",
    }

    body = {
        "model": os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL),
        "messages": [{"role": "user", "content": final_prompt}],
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body,
        timeout=60,
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]

    return f"Error {response.status_code}: {response.text}"
