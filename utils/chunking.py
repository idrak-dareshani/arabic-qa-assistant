from typing import List
import json
import os
import re

CHUNK_OUTPUT_DIR = "kb/chunked"
os.makedirs(CHUNK_OUTPUT_DIR, exist_ok=True)

def chunk_text_by_paragraph(pages: List[dict], chunk_size: int = 800) -> List[dict]:
    chunks = []
    for page in pages:
        text = page["text"]
        paragraphs = re.split(r'\n{2,}', text)
        buffer = ""
        for para in paragraphs:
            if len(buffer + para) < chunk_size:
                buffer += para.strip() + "\n\n"
            else:
                chunks.append({
                    "text": buffer.strip(),
                    "metadata": {
                        "level": page["level"],
                        "page": page["page"],
                        "section_title": page.get("section_title", "Unknown")
                    }
                })
                buffer = para.strip() + "\n\n"
        if buffer:
            chunks.append({
                "text": buffer.strip(),
                "metadata": {
                    "level": page["level"],
                    "page": page["page"],
                    "section_title": page.get("section_title", "Unknown")
                }
            })
    return chunks


def chunk_all_levels():
    INPUT_DIR = "data/extracted_text"
    for level in ["beginner", "intermediate", "advanced"]:
        input_path = os.path.join(INPUT_DIR, f"{level}_tagged.json")
        with open(input_path, encoding="utf-8") as f:
            pages = json.load(f)
        chunks = chunk_text_by_paragraph(pages)
        output_path = os.path.join(CHUNK_OUTPUT_DIR, f"{level}_chunks.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        print(f"✅ Chunked {level}: {len(chunks)} chunks")


if __name__ == "__main__":
    chunk_all_levels()
