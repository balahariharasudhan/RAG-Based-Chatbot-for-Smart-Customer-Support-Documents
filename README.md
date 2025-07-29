<!-- Core Technologies -->
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b?logo=streamlit&logoColor=white)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-green?logo=vector)
![OCR](https://img.shields.io/badge/OCR-PyMuPDF%20+%20Pytesseract-purple?logo=files)

<!-- LLM & Embeddings -->
![LLM](https://img.shields.io/badge/LLM-Groq%20LLaMA3%208B-lightgrey?logo=openai)
![Embeddings](https://img.shields.io/badge/Embeddings-all--MiniLM--L6--v2-yellow?logo=semanticweb)

<!-- Project Type -->
![RAG](https://img.shields.io/badge/Model-Retrieval--Augmented%20Generation-orange?logo=readthedocs&logoColor=white)
![PDF-QA](https://img.shields.io/badge/UseCase-PDF--QA-red?logo=adobeacrobatreader)

<!-- Dev & Infra -->
![HuggingFace](https://img.shields.io/badge/Transformers-HuggingFace-ffcc00?logo=huggingface&logoColor=black)
![Local](https://img.shields.io/badge/Execution-Local%20+%20GroqAPI-brightgreen?logo=powerbi)
![CLI](https://img.shields.io/badge/Interface-CLI%20%2B%20UI-orange?logo=windowsterminal)

<!-- Meta Info -->
![License](https://img.shields.io/badge/License-MIT-green)
![Repo Size](https://img.shields.io/github/repo-size/balahariharasudhan/RAG-Based-Chatbot-for-Smart-Customer-Support-Documents)
![Last Commit](https://img.shields.io/github/last-commit/balahariharasudhan/RAG-Based-Chatbot-for-Smart-Customer-Support-Documents)


# RAG-Based Chatbot for Smart Customer Support Documents

This project implements a **Retrieval-Augmented Generation (RAG)** based chatbot to intelligently answer questions using a PDF document containing both **text and images**. It uses local embedding models and the **Groq API** for high-performance, cost-free generation, avoiding any paid APIs.

## 💡 Features

- Extracts both text (using PyMuPDF) and image data from PDF using OCR (Tesseract).
- Converts PDF into vector embeddings using `all-MiniLM-L6-v2`.
- Stores the embeddings in a FAISS vector database.
- Uses the **Groq API (LLaMA3)** for generating context-based answers.
- Runs locally in **Visual Studio / VS Code** using Python virtual environment.
- Simple test script (`test.py`) to query the bot.
- Clean architecture for maintainability and extension.

---

## 📁 Project Structure

- `.gitignore` – Files/folders ignored by Git
- `app.py` – 🚀 Streamlit or UI interface
- `CSR MODULES.pdf` – 📄 Input PDF file (text + image content)
- `images/` – 🌅 Auto-extracted images from PDF for OCR
- `ingest_pdf.py` – ⚙️ PDF parser, OCR, and embedding logic
- `rag_chatbot.py` – 🤖 Core RAG chatbot pipeline
- `requirements.txt` – 📦 Python dependencies
- `test.py` – 🧪 CLI script to interact with the chatbot
- `vectorstore/` – 🧠 Local FAISS vector database
- `README.md` – 📘 You're reading it now!


---

## 🛠️ Setup Instructions

### 1. Clone the Repository

- git clone https://github.com/balahariharasudhan/RAG-Based-Chatbot-for-Smart-Customer-Support-Documents.git

- Change the directory to the cloned repo by using -> cd RAG-Based-Chatbot-for-Smart-Customer-Support-Documents

### 2. Create and activate a Virtual Environment (To work separately without disturbing the existing versions)

- python -m venv venv
 
- .\venv\Scripts\activate       # For Windows

### 3. Install Requirements

- pip install -r requirements.txt

### 4. Configure Environment Variables (For ensuring security)

- Create a .env file and store your Groq API (Free):

- It should be in the form of: GROQ_API_KEY=your_groq_api_key

### 5. 📄 Ingest PDF

- You can either use the built-in PDF or upload your personal company documents as a PDF and chat with the bot

- Run the following to process your PDF and store the vector embeddings: python ingest_pdf.py

After successful running, it will:

- Extracts text.

- Extracts images and runs OCR using Tesseract.

- Embeds content using Sentence Transformers.

- Stores embeddings in FAISS DB (vectorstore/).

### 6. 🤖 Query Your Chatbot

- Use the test.py script to ask questions by: python test.py

### 7. 🌐 Launch Streamlit UI

- After successful completion, make sure to run the UI by using: streamlit run app.py 

-------------------------------------------------------------------------

### Sample interaction:

Q: What are the key objectives of CSR?
A: [Answer from context]

### 💬 Model Used

1) Embeddings: all-MiniLM-L6-v2 from Sentence Transformers (free, local).

2) LLM: llama3-8b-8192 via Groq API (free and fast inference).

## 📸 Screenshots

### 🔹 Sample Query and Response in terminal
![Chatbot Response](screenshots/Testing_on_Terminal.png)

### 🔹 Streamlit UI 
![UI Screenshot](screenshots/Streamlit_UI.png)

------------------------------------------------------------------------

✅ Key Learnings

- Used LangChain (0.3.27) with new modular packages like:

-> langchain-community

-> langchain-core

-> langchain-huggingface

- Enabled FAISS with allow_dangerous_deserialization=True for local use.

- OCR setup using pytesseract + pdf2image + Tesseract executable path config.

- Dealt with deprecated imports and updated LangChain compatibility manually.

### 🧠 Future Scope

- Expand to real-time document search (external knowledge integration).

🙋‍♂️ Author

- Balahariharasudhan T

- GitHub: https://github.com/balahariharasudhan

📜 License

- This project is for educational and research purposes only.
