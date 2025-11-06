import os
from docx import Document
import fitz  # PyMuPDF - ADD THIS IMPORT!

def load_documents(folder_path):
    all_texts = []
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist!")
        return all_texts
    
    # Check if folder is empty
    files = os.listdir(folder_path)
    if not files:
        print(f"Warning: Folder '{folder_path}' is empty!")
        return all_texts
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        
        try:
            if file.endswith(".pdf"):
                with fitz.open(file_path) as doc:
                    text = "".join(page.get_text() for page in doc)
                    if text.strip():  # Only add non-empty documents
                        all_texts.append(text)
                        print(f"✅ Loaded PDF: {file}")
                    else:
                        print(f"⚠️ Skipped empty PDF: {file}")
                        
            elif file.endswith(".docx"):
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
                if text.strip():  # Only add non-empty documents
                    all_texts.append(text)
                    print(f"✅ Loaded DOCX: {file}")
                else:
                    print(f"⚠️ Skipped empty DOCX: {file}")
        
        except Exception as e:
            print(f" Error loading {file}: {str(e)}")
    
    return all_texts

# Update this path to your actual documents folder
documents = load_documents("C:/Users/taniy/Desktop/documents")

print(f"\n Total documents loaded: {len(documents)}")

if documents:
    print("Type of first document:", type(documents[0]))
    print("First 200 characters of first document:", documents[0][:200])
else:
    print("⚠️ No documents were loaded! Please check:")
    print("1. The folder path is correct")
    print("2. The folder contains PDF or DOCX files")
    print("3. The files are not empty or corrupted")
