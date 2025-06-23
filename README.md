# Arabic Grammar QA Assistant

This project provides an intelligent Question-Answering (QA) assistant that allows users to ask questions based on the content of the **Bayyinah Dream Textbook**. It features a modern web interface and leverages advanced NLP techniques for context-aware answers, including real-time web search.

---

## 📚 Description

The assistant helps learners and researchers interactively explore the Bayyinah Textbook. It extracts answers from PDF content using semantic search and large language models, and can optionally supplement answers with up-to-date web search results.

---

## 🏗️ Project Structure

- **app.py**: Streamlit app for interactive QA.
- **build_index.py**: Script for processing PDFs, chunking, and building the FAISS index.
- **data/**: Contains extracted text, metadata, chunked data, indexes, and raw PDFs.
  - **raw_pdfs/**: Original textbook PDFs.
  - **chunked/**: Chunked JSON files for each level.
  - **index/**: FAISS index and pickle files.
  - **metadata/**: TOC and intro metadata.
- **requirements.txt**: Python dependencies.
- **.streamlit/**: Streamlit configuration.
- **.env**: Environment variables (API keys, etc).

---

## 🛠 Technologies Used

- **Python 3.13**
- **Streamlit** – Interactive web UI for QA
- **LangChain** – Orchestrates document retrieval and LLM-based answering
- **FAISS** – Fast vector similarity search for document retrieval
- **HuggingFace Transformers** – For text embeddings
- **OpenAI GPT-4** – For answer generation (via LangChain)
- **PyMuPDF (fitz)** – PDF text extraction

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
# On Unix/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1. Build the Knowledge Base

Before running the app, process the PDFs and build the FAISS index:
```bash
python build_index.py
```

This will extract, chunk, and embed the textbook content, saving processed data in the `data/` directory.

### 2. Start the Streamlit App

```bash
streamlit run app.py
```

Open your browser and navigate to the provided local URL (usually [http://localhost:8501](http://localhost:8501)).

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