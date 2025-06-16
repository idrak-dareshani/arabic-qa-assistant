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

# Initialize LLM
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Build QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True,
    chain_type_kwargs={
        "prompt": prompt
    }
)

def answer_question(query: str):
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
