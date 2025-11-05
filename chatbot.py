import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()

st.set_page_config(page_title="Policy Document Q&A", layout="centered")
st.title("📄 Document Q&A Chatbot using Gemini")

# Keep state for FAISS DB
if "db" not in st.session_state:
    st.session_state.db = None

# PDF uploader
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    loader = PyPDFLoader("temp.pdf")
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(pages)

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    st.session_state.db = FAISS.from_documents(docs, embedding_model)
    st.success("✅ PDF processed successfully!")

# Question input (always visible)
user_query = st.text_input("💬 Ask a question from the document:")

if user_query:
    if st.session_state.db is None:
        st.warning("Please upload a PDF first.")
    else:
        # Use the correct Gemini model name
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",  # or "gemini-1.5-pro"
            temperature=0.3
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, 
            retriever=st.session_state.db.as_retriever(), 
            chain_type="stuff"
        )
        
        with st.spinner("Thinking..."):
            response = qa_chain.run(user_query)

        # Show response
        st.subheader("📌 Answer")
        st.write(response)

