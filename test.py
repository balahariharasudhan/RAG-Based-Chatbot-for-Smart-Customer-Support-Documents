# test.py
from rag_chatbot import query_rag

question = "What are the key objectives of CSR?"
print("Q:", question)
print("A:", query_rag(question))
