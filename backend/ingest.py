import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

DATA_DIR = "data"

def load_all_documents(data_dir: str = DATA_DIR) -> List[Document]:
    docs = []

    for root, _, files in os.walk(data_dir):
        for file in files:
            path = os.path.join(root, file)
            ext = file.lower().split(".")[-1]

            if ext == "pdf":
                loader = PyPDFLoader(path)
            elif ext in ["docx"]:
                loader = UnstructuredWordDocumentLoader(path)
            elif ext in ["xlsx", "xls"]:
                loader = UnstructuredExcelLoader(path)
            else:
                print(f"Skipped unsupported file: {file}")
                continue

            loaded = loader.load()
            for doc in loaded:
                doc.metadata["source"] = path
            docs.extend(loaded)

    return docs

def chunk_documents(documents: List[Document], chunk_size=800, chunk_overlap=100) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

if __name__ == "__main__":
    print("📄 Loading documents...")
    raw_docs = load_all_documents()
    print(f"✅ Loaded {len(raw_docs)} raw documents")

    print("🔪 Splitting into chunks...")
    chunks = chunk_documents(raw_docs)
    print(f"✅ Created {len(chunks)} chunks")

    # Optional: Save chunks to a file or embed next
