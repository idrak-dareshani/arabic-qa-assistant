import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
embeddings = OpenAIEmbeddings()

def create_vector_store(pdf_path="data/Dream_Textbook.pdf", index_path="faiss_index"):
    #splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    #docs = splitter.create_documents([text])
    #loader = PyPDFLoader(pdf_path)
    #pages = loader.load()

    pdf_files = ["data/Section1.pdf", "data/Section2.pdf", "data/Section3.pdf"]

    all_docs = []
    for file in pdf_files:
        loader = PyPDFLoader(file)
        docs = loader.load()
        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n", ".", "،", " "]
    )
    chunks = splitter.split_documents(all_docs)

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(index_path)
    return db

def load_vector_store(index_path="faiss_index"):
    return FAISS.load_local(index_path, embeddings)
