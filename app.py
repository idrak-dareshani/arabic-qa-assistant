import streamlit as st
import json
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

# --- Config ---
INDEX_DIR = "data/index"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Setup ---
st.set_page_config(page_title="Arabic Grammar QA", layout="centered")

st.title("📘 Arabic Grammar Q&A Assistant")

@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)

@st.cache_resource
def load_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    prompt = PromptTemplate(
        template="""
You are an expert in Arabic grammar. Use the following context to answer clearly and concisely.

Context:
{context}

Question: {question}
Answer:""",
        input_variables=["context", "question"]
    )

    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model="gpt-4"),
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

qa_chain = load_chain()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter")
level = st.sidebar.selectbox("Grammar Level", ["", "beginner", "intermediate", "advanced"])
section = st.sidebar.text_input("Section (optional)")

# --- Input Form ---
with st.form("qa_form"):
    query = st.text_input("Ask your grammar question:", placeholder="What is a nominal sentence in Arabic?")
    submitted = st.form_submit_button("Ask")

if submitted and query:
    with st.spinner("Thinking..."):
        retriever = qa_chain.retriever

        # Custom filter
        def metadata_filter(meta):
            if level and meta.get("level", "") != level:
                return False
            if section and section not in meta.get("section_title", ""):
                return False
            return True

        retriever.search_kwargs["filter"] = metadata_filter
        result = qa_chain.invoke({"query": query})

        # --- Answer ---
        st.markdown("### 📖 Answer")
        st.markdown(f"> {result['result']}")

        # --- Sources ---
        st.markdown("### 📚 Sources")
        for doc in result["source_documents"]:
            meta = doc.metadata
            st.markdown(f"- **{meta['section_title']}** — *{meta['level'].title()}*, Page {meta['page']}")

# --- Optional Intro Page ---
with st.expander("ℹ️ About / Introduction"):
    try:
        with open("data/metadata/intro.json", encoding="utf-8") as f:
            intro = json.load(f)
            st.markdown(intro.get("text", ""))
    except:
        st.info("Intro content not available.")
