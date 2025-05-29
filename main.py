from utils.pdf_loader import extract_text_from_pdf
from utils.vector_store import create_vector_store, load_vector_store
from utils.qa_engine import answer_question
from utils.web_fallback import search_web, search_tool

#pdf_path = "data/Dream_Textbook.pdf"
#text = extract_text_from_pdf(pdf_path)

# Step 1: Create index
db = create_vector_store()

# Step 2: Ask a question
while True:
    q = input("\nAsk a question (or type 'exit'): ")
    if q.lower() == "exit":
        break
    answer = answer_question(db, q)
    print("Answer:", answer)

    fallback = input("\n Do you want more info from the web? (yes/no): ").lower()
    if fallback == "yes":
        #web_info = search_web(q)
        web_info = search_tool(q)
        print("\n Info from the web:")
        print(web_info)
