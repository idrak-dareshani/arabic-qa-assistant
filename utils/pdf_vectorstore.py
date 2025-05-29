# utils/pdf_vectorstore.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings  # Or HuggingFaceEmbeddings

import os

def load_and_index_pdf(pdf_path: str, persist_directory: str = "db"):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n", ".", "،", " "]
    )
    chunks = splitter.split_documents(pages)

    embeddings = OpenAIEmbeddings()  # Or any model you have
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    #vectordb.persist()
    return vectordb
