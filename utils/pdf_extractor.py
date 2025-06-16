import os
import json
import fitz  # PyMuPDF
from langdetect import detect

# Define directories
INPUT_DIR = "data/raw_pdfs"
TEXT_OUTPUT_DIR = "data/extracted_text"
METADATA_DIR = "data/metadata"

os.makedirs(TEXT_OUTPUT_DIR, exist_ok=True)

# File mapping (user-supplied TOC must exist for each section)
SECTIONS = {
    "beginner": {
        "content_pdf": "Section1.pdf",
        "toc_json": "toc_beginner.json"
    },
    "intermediate": {
        "content_pdf": "Section2.pdf",
        "toc_json": "toc_intermediate.json"
    },
    "advanced": {
        "content_pdf": "Section3.pdf",
        "toc_json": "toc_advanced.json"
    }
}


def load_manual_toc(json_path):
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def extract_content(pdf_path, level_tag):
    doc = fitz.open(pdf_path)
    pages = []

    for page_num, page in enumerate(doc, 1):
        text = page.get_text("text").strip()
        try:
            lang = detect(text)
        except:
            lang = "unknown"

        pages.append({
            "level": level_tag,
            "page": page_num,
            "text": text,
            "language": lang
        })

    return pages


def tag_with_toc(pages, toc_entries):
    for page in pages:
        for entry in toc_entries:
            start = entry["page_start"]
            end = entry.get("page_end", start)
            if start <= page["page"] <= end:
                page["section_title"] = entry["title"]
                break
    return pages


def process_section(level, files):
    print(f"📘 Processing: {level.capitalize()}")

    content_pdf_path = os.path.join(INPUT_DIR, files["content_pdf"])
    toc_json_path = os.path.join(METADATA_DIR, files["toc_json"])

    toc_entries = load_manual_toc(toc_json_path)
    pages = extract_content(content_pdf_path, level)
    tagged_pages = tag_with_toc(pages, toc_entries)

    output_path = os.path.join(TEXT_OUTPUT_DIR, f"{level}_tagged.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tagged_pages, f, indent=2, ensure_ascii=False)


def run_all_sections():
    for level, files in SECTIONS.items():
        process_section(level, files)


if __name__ == "__main__":
    run_all_sections()
    print("✅ Content extraction and manual TOC tagging complete.")
