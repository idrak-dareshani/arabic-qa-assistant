import os
import fitz  # PyMuPDF
import json
import re
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Paths
RAW_DIR = "data/raw_pdfs"
CHUNK_DIR = "data/chunked"
TOC_DIR = "data/metadata"
INDEX_DIR = "data/index"
os.makedirs(CHUNK_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

SECTIONS = {
    "beginner": {
        "pdf": "section_1_beginner.pdf",
        "toc": "toc_beginner.json"
    },
    "intermediate": {
        "pdf": "section_2_intermediate.pdf",
        "toc": "toc_intermediate.json"
    },
    "advanced": {
        "pdf": "section_3_advanced.pdf",
        "toc": "toc_advanced.json"
    }
}


def load_toc(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        pages.append({"page": i, "text": text})
    return pages


def apply_toc(pages, toc, level):
    tagged = []
    for page in pages:
        matched = None
        for entry in toc:
            start = entry["page_start"]
            end = entry.get("page_end", start)
            if start <= page["page"] <= end:
                matched = entry
                break
        tagged.append({
            "level": level,
            "page": page["page"],
            "text": page["text"],
            "section_title": matched["title"] if matched else "Unknown"
        })
    return tagged


def chunk_pages(pages, max_len=800):
    chunks = []
    for p in pages:
        paras = re.split(r"\n{2,}", p["text"])
        buffer = ""
        for para in paras:
            if len(buffer + para) < max_len:
                buffer += para.strip() + "\n\n"
            else:
                chunks.append({
                    "text": buffer.strip(),
                    "metadata": {
                        "level": p["level"],
                        "section_title": p["section_title"],
                        "page": p["page"]
                    }
                })
                buffer = para.strip() + "\n\n"
        if buffer:
            chunks.append({
                "text": buffer.strip(),
                "metadata": {
                    "level": p["level"],
                    "section_title": p["section_title"],
                    "page": p["page"]
                }
            })
    return chunks


def build_all_chunks(skip_existing=True):
    all_chunks = []
    for level, config in SECTIONS.items():
        chunk_file = os.path.join(CHUNK_DIR, f"{level}_chunks.json")

        if skip_existing and os.path.exists(chunk_file):
            print(f"⚠️ Skipping {level} – chunks already exist.")
            with open(chunk_file, encoding="utf-8") as f:
                chunks = json.load(f)
        else:
            print(f"📘 Processing {level}...")
            toc = load_toc(os.path.join(TOC_DIR, config["toc"]))
            pages = extract_pages(os.path.join(RAW_DIR, config["pdf"]))
            tagged = apply_toc(pages, toc, level)
            chunks = chunk_pages(tagged)
            with open(chunk_file, "w", encoding="utf-8") as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
            print(f"✅ {len(chunks)} chunks written for {level}.")

        all_chunks.extend(chunks)

    return all_chunks


def embed_and_store(chunks, skip_if_exists=True):
    faiss_path = os.path.join(INDEX_DIR, "index.faiss")
    pkl_path = os.path.join(INDEX_DIR, "index.pkl")

    if skip_if_exists and os.path.exists(faiss_path) and os.path.exists(pkl_path):
        print("⚠️ FAISS index already exists. Skipping embedding.")
        return

    print("🔍 Generating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    store = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
    store.save_local(INDEX_DIR)
    print("✅ FAISS index and metadata saved.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build LangChain-compatible FAISS index.")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild of chunked data.")
    parser.add_argument("--rebuild-index", action="store_true", help="Force rebuild of FAISS index.")
    args = parser.parse_args()

    chunks = build_all_chunks(skip_existing=not args.rebuild)
    embed_and_store(chunks, skip_if_exists=not args.rebuild_index)
