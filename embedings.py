# build_vector_store.py

import pickle
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Load your chunks
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# Load embeddings model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create vector store
vectorstore = FAISS.from_documents(chunks, embeddings)

# Save vectorstore to file
vectorstore.save_local("faiss_store")

print("Vector store created and saved.")
