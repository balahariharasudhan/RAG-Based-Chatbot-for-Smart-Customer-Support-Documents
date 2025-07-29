# rag_chatbot.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Embeddings and Vector DB
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize embedding model
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load the FAISS vectorstore (safe since you created it)
db = FAISS.load_local("vectorstore", embedding, allow_dangerous_deserialization=True)

# Prompt template
TEMPLATE = """You are a helpful assistant. Use the following context to answer the user's question accurately and clearly.

Context:
{context}

Question:
{question}

Answer:"""

def generate_prompt(context, question):
    return TEMPLATE.format(context=context, question=question)

def query_rag(user_question):
    # Step 1: Search vector DB
    docs = db.similarity_search(user_question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Step 2: Build final prompt
    final_prompt = generate_prompt(context, user_question)

    # Step 3: Query Groq API (using llama3-8b)
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": final_prompt}],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"
