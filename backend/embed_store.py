import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from ingest import load_all_documents, chunk_documents

load_dotenv()  # ✅ Load the OpenAI key from .env

EMBEDDING_MODEL = OpenAIEmbeddings()
VECTORSTORE_PATH = "outputs/vector_store"

def create_vectorstore():
    print("📄 Loading and chunking documents...")
    docs = chunk_documents(load_all_documents())

    print("🧠 Creating embeddings and storing in FAISS...")
    vectorstore = FAISS.from_documents(docs, EMBEDDING_MODEL)

    os.makedirs("outputs", exist_ok=True)
    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"✅ Vector store saved to: {VECTORSTORE_PATH}")

if __name__ == "__main__":
    create_vectorstore()
