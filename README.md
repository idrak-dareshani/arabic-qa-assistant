# Arabic Language QA Assistant

This project provides an intelligent Question-Answering (QA) assistant that allows users to ask questions based on the content of the **Bayyinah Textbook**. In addition to document-based responses, it also supports real-time web search functionality to enhance answer accuracy and relevance.

## 📚 Description

The assistant is designed to help learners and researchers engage more interactively with the Bayyinah Textbook by extracting context-aware answers from the PDF content. Users can also enable web-based search to find up-to-date or supplementary information related to their questions.

## 🛠 Technologies Used

- **Python 3.13**
- **Flask** – for web interface
- **PyPDF2** – for reading and extracting text from PDF files
- **LangChain** – for orchestrating question answering over documents
- **FAISS** – for fast document similarity search
- **Tavily API** – for real-time web search

## ⚙️ Installation

To set up the project locally:

### 1. Clone the repository
```bash
git clone https://github.com/idrak-dareshani/arabic-qa-assistant.git
cd arabic-qa-assistant
```
### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
## 🚀 Usage

### CLI Mode:
```bash
python main.py
```
Follow the prompts to enter a question based on the Bayyinah Textbook.

### Web Interface:
```bash
python app.py
```
Open your browser and navigate to http://127.0.0.1:5000 to use the web interface.

## 🤝 Contributing
Contributions are welcome to enhance the assistant’s capabilities. Areas of interest include:

* Improving PDF text extraction and semantic understanding.

* Enhancing the integration and ranking of web search results.

* Please fork the repository, create a new branch for your features or fixes, and submit a pull request.

## 📝 License
This project is licensed under the GNU General Public License (GPL).

---

For issues, suggestions, or improvements, feel free to open a GitHub [Issue](https://github.com/idrak-dareshani/arabic-qa-assistant/issues).
