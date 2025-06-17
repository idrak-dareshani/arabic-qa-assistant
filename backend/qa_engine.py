from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load embeddings + FAISS
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("index", embeddings, allow_dangerous_deserialization=True)

# Define a grammar-specific prompt
prompt = PromptTemplate(
    template="""
You are an expert in Arabic grammar. Use the following context to answer clearly and concisely.

Context:
{context}

Question: {question}
Answer:""",
    input_variables=["context", "question"]
)

def answer_question(query: str, filters: dict = None):
    if filters:
        def filter_fn(metadata):
            for k, v in filters.items():
                if k in metadata and v.lower() not in metadata[k].lower():
                    return False
            return True
        retriever = db.as_retriever(search_kwargs={"k": 5, "filter": filter_fn})
    else:
        retriever = db.as_retriever(search_kwargs={"k": 5})

    # Build QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain.invoke({"query": query})
    return {
        "answer": result["result"],
        "sources": [
            {
                "section_title": doc.metadata.get("section_title", ""),
                "page": doc.metadata.get("page", 0),
                "level": doc.metadata.get("level", "")
            }
            for doc in result["source_documents"]
        ]
    }
