import os

import fitz  # PyMuPDF
import pytesseract
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pdf2image import convert_from_path


DEFAULT_PDF_PATH = "CSR MODULES.pdf"
DEFAULT_VECTORSTORE_PATH = "vectorstore"
WINDOWS_TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def configure_tesseract():
    """Use the Windows executable when present; otherwise rely on the system PATH."""
    if os.path.exists(WINDOWS_TESSERACT_PATH):
        pytesseract.pytesseract.tesseract_cmd = WINDOWS_TESSERACT_PATH


def extract_pdf_documents(pdf_path, enable_ocr=True, progress_callback=None):
    configure_tesseract()
    documents = []

    with fitz.open(pdf_path) as doc:
        total_pages = len(doc)

        for page_number in range(total_pages):
            if progress_callback:
                progress_callback(page_number + 1, total_pages)
            else:
                print(f"Processing page {page_number + 1}/{total_pages}...")

            page = doc.load_page(page_number)
            pdf_text = page.get_text().strip()
            ocr_text = ""

            if enable_ocr:
                try:
                    images = convert_from_path(
                        pdf_path,
                        first_page=page_number + 1,
                        last_page=page_number + 1,
                    )
                    ocr_text = "\n".join(
                        pytesseract.image_to_string(image).strip()
                        for image in images
                    ).strip()
                except Exception as exc:
                    print(f"OCR skipped on page {page_number + 1}: {exc}")

            combined_text = f"{pdf_text}\n\n{ocr_text}".strip()
            if combined_text:
                documents.append(
                    Document(
                        page_content=combined_text,
                        metadata={"page": page_number + 1},
                    )
                )

    if not documents:
        raise ValueError("No readable text was found in this PDF.")

    return documents


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def build_vectorstore(documents):
    embedding = get_embedding_model()
    return FAISS.from_documents(documents, embedding)


def ingest_pdf(pdf_path, save_path=None, enable_ocr=True, progress_callback=None):
    documents = extract_pdf_documents(
        pdf_path,
        enable_ocr=enable_ocr,
        progress_callback=progress_callback,
    )
    db = build_vectorstore(documents)

    if save_path:
        db.save_local(save_path)

    return db


if __name__ == "__main__":
    print(f"Ingesting {DEFAULT_PDF_PATH}...")
    ingest_pdf(DEFAULT_PDF_PATH, save_path=DEFAULT_VECTORSTORE_PATH)
    print(f"Done! Vectorstore saved to '{DEFAULT_VECTORSTORE_PATH}/'")
