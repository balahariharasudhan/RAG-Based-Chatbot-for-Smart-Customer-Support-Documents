# ingest_pdf.py

import os
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Set path to tesseract executable (adjust if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# File path
pdf_path = "CSR MODULES.pdf"
doc = fitz.open(pdf_path)

all_text_chunks = []

# Loop through pages
for page_number in range(len(doc)):
    print(f"🔍 Processing page {page_number + 1}/{len(doc)}...")

    # Extract text via PyMuPDF
    page = doc.load_page(page_number)
    pdf_text = page.get_text()

    # Convert this page to image (for OCR)
    images = convert_from_path(pdf_path, first_page=page_number + 1, last_page=page_number + 1)
    ocr_text = ""
    for image in images:
        ocr_text += pytesseract.image_to_string(image)

    # Merge PDF + OCR text
    combined_text = f"{pdf_text.strip()}\n\n{ocr_text.strip()}"

    # Create LangChain Document
    page_doc = Document(page_content=combined_text, metadata={"page": page_number + 1})
    all_text_chunks.append(page_doc)

# Initialize embeddings
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Build vectorstore
print("🧠 Creating FAISS vectorstore...")
db = FAISS.from_documents(all_text_chunks, embedding)

# Save it locally
db.save_local("vectorstore")
print("✅ Done! Vectorstore saved to 'vectorstore/'")
