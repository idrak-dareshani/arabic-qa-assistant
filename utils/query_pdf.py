# utils/query_pdf.py
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

def query_pdf(question: str, persist_directory: str = "db"):
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    context_docs = retriever.invoke(question)
    total_tokens = sum(len(doc.page_content.split()) for doc in context_docs)
    print(f"Total estimated tokens: {total_tokens}")

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain.invoke({"query": question})
    return result["result"]
