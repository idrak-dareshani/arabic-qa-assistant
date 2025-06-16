from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS     

import json
import os

INDEX_DIR = "kb/faiss_index"
os.makedirs(INDEX_DIR, exist_ok=True)

def embed_and_store():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    all_texts = []
    all_metadata = []

    for level in ["beginner", "intermediate", "advanced"]:
        chunk_file = f"kb/chunked/{level}_chunks.json"
        with open(chunk_file, encoding="utf-8") as f:
            chunks = json.load(f)
        for chunk in chunks:
            all_texts.append(chunk["text"])
            all_metadata.append(chunk["metadata"])

    # Create embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_texts(all_texts, embedding_model, metadatas=all_metadata)
    db.save_local(INDEX_DIR)
    print(f"Index saved to {INDEX_DIR}")

if __name__ == "__main__":
    embed_and_store()
