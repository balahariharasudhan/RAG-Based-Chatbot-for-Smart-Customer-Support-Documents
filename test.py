from ingest_pdf import DEFAULT_PDF_PATH, DEFAULT_VECTORSTORE_PATH, ingest_pdf
from rag_chatbot import query_rag

question = "What are the key objectives of CSR?"
db = ingest_pdf(DEFAULT_PDF_PATH, save_path=DEFAULT_VECTORSTORE_PATH)

print("Q:", question)
print("A:", query_rag(question, db))
