from pdf_loader import extract_text_from_pdf
from vector_store import create_vector_store, load_vector_store
from qa_engine import answer_question

pdf_path = "data/Dream_Textbook.pdf"
text = extract_text_from_pdf(pdf_path)

# Step 1: Create index
db = create_vector_store(text)

# Step 2: Ask a question
while True:
    q = input("\nAsk a question (or type 'exit'): ")
    if q.lower() == "exit":
        break
    answer = answer_question(db, q)
    print("Answer:", answer)
