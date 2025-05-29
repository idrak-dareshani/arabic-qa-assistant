import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
embeddings = OpenAIEmbeddings()

def create_vector_store(text, index_path="faiss_index"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents([text])
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(index_path)
    return db

def load_vector_store(index_path="faiss_index"):
    return FAISS.load_local(index_path, embeddings)
