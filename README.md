# Arabic Grammar QA Assistant

This project provides an intelligent Question-Answering (QA) assistant that allows users to ask questions based on the content of the **Bayyinah Dream Textbook**. It features a modern web interface and leverages advanced NLP techniques for context-aware answers, including real-time web search.

---

## 📚 Description

The assistant helps learners and researchers interactively explore the Bayyinah Textbook. It extracts answers from PDF content using semantic search and large language models, and can optionally supplement answers with up-to-date web search results.

---

## 🏗️ Project Structure

- **backend/**: Python backend using Flask, LangChain, FAISS, and HuggingFace for embeddings and retrieval-based QA.
- **frontend/**: Blazor WebAssembly frontend for user interaction.
- **data/**: Contains extracted text, metadata, and raw PDFs.
- **kb/**: Stores chunked knowledge base and FAISS index files.
- **utils/**: Python utilities for chunking, embedding, and PDF extraction.

---

## 🛠 Technologies Used

- **Python 3.13**
- **Flask** – REST API for QA and search
- **LangChain** – Orchestrates document retrieval and LLM-based answering
- **FAISS** – Fast vector similarity search for document retrieval
- **HuggingFace Transformers** – For text embeddings
- **OpenAI GPT-4** – For answer generation (via LangChain)
- **PyPDF2** – PDF text extraction
- **Blazor WebAssembly** – Modern C# frontend

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/idrak-dareshani/arabic-qa-assistant.git
cd arabic-qa-assistant
```

### 2. Backend Setup

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Frontend Setup

Navigate to the frontend directory and restore dependencies:
```bash
cd frontend
dotnet restore
```

---

## 🚀 Usage

### Start the Backend API

From the `backend/` directory:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
This will start the Flask API server for QA.

### Start the Frontend

From the `frontend/` directory:
```bash
dotnet run
```
This will launch the Blazor WebAssembly frontend.

Open your browser and navigate to [http://localhost:5000](http://localhost:5000) (or the port shown in the terminal).

---

## 🧠 How It Works

- **Document Ingestion**: PDFs are processed and chunked, then embedded using HuggingFace models.
- **Semantic Search**: User queries are embedded and matched against the FAISS index for relevant context.
- **Answer Generation**: LangChain orchestrates retrieval and uses GPT-4 to generate answers based on the retrieved context.

---

## 🤝 Contributing

Contributions are welcome! You can help by:

- Improving PDF extraction and semantic search.
- Enhancing the frontend experience.
- Integrating new LLMs or search APIs.

Fork the repository, create a feature branch, and submit a pull request.

---

## 📝 License

This project is licensed under the GNU General Public License (GPL).

---

For issues, suggestions, or improvements, please open a GitHub [Issue](https://github.com/idrak-dareshani/arabic-qa-assistant/issues).
