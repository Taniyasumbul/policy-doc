# split_chunks.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import pickle
from data_extraction import documents 

# Check if documents were loaded
if not documents:
    print("❌ ERROR: No documents were loaded!")
    print("Please check data_extraction.py and ensure documents are in the folder.")
    exit(1)

# Convert to Document objects
document_objs = [Document(page_content=text, metadata={"source": f"doc_{i}"}) 
                 for i, text in enumerate(documents)]

print(f"📄 Processing {len(document_objs)} documents...")

# Split documents into manageable chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(document_objs)

# Check if chunks were created
if not chunks:
    print("❌ ERROR: No chunks were created!")
    exit(1)

# Save chunks to a file
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print(f"✅ Done! Split into {len(chunks)} chunks.")
print(f"💾 Chunks saved to chunks.pkl")
