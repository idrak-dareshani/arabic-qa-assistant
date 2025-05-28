from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableLambda, RunnableMap
from langchain.schema.document import Document

# Initialize model
llm = ChatOpenAI(temperature=0)

# Prompt template expects a "context" string and "question"
prompt = ChatPromptTemplate.from_template(
    "Use the following context to answer the question.\n\n{context}\n\nQuestion: {question}\nAnswer:"
)

def answer_question(db, query):
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # Step 1: Fetch documents from retriever
    def fetch_context(input_dict):
        docs = retriever.invoke(input_dict["question"])
        return {"context": "\n\n".join(doc.page_content for doc in docs), "question": input_dict["question"]}

    # Step 2: Build chain
    chain = RunnableLambda(fetch_context) | prompt | llm

    # Step 3: Run chain
    result = chain.invoke({"question": query})
    return result.content