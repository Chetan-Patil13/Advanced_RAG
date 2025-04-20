# 💬 RAG Chatbot for Organizational Knowledge Access

## 🧠 Problem Statement

### ❗ Key Challenges

1. **Scattered Knowledge, Delayed Access**

   - System/procedure knowledge is hidden in emails, files, or individuals' minds.
   - Searching is time-consuming → slows down operations and reduces productivity.

2. **Dependency on Human Gatekeepers**
   - Employees rely on colleagues to retrieve info → bottlenecks and delays.
   - Risk of inconsistent or outdated information.

### 🔍 Impact

- Delayed decision-making
- Compliance gaps
- Reduced operational efficiency and scalability across plants

---

## ✅ Solution: LLM-Powered RAG System

### 🧠 Intuition

- **Human-Centric Access**: Replace fragmented searching with natural language Q&A.
- **Centralize, Don’t Scatter**: Unify knowledge across departments into one searchable brain.

### 💡 The Idea

An **LLM-powered chatbot** that acts as a single gateway for:

- 📚 System/procedure documentation
- 📄 Real-time compliance updates
- 🔄 Cross-departmental workflows

### ✨ Impact

- Ask like you’d ask a colleague
- Answers are instant, consistent, and audit-ready
- No gatekeeping, no delays

---

## 🛠️ Technical Stack

### 📂 Document Ingestion

File types supported:

- PDFs (`PyPDFLoader`)
- Word docs (`UnstructuredWordDocumentLoader`)
- Excel sheets (`UnstructuredExcelLoader`)

📄 Files from `/data/` are parsed and loaded using LangChain document loaders.

### ✂️ Chunking

- **LangChain Component**: `RecursiveCharacterTextSplitter`
- Long documents are split into overlapping chunks (800 characters with 100 overlap) for better context retrieval.

### 🧠 Embedding & Storage

- **Embedding Model**: `OpenAIEmbeddings` (`text-embedding-3-small`)
- **Vector DB**: `FAISS` for fast similarity search
- Stored locally in `outputs/vector_store`

### 🤖 Retrieval-Augmented Generation (RAG)

- **Retriever**: FAISS-based retriever (`k=4`) using LangChain's `.as_retriever()`
- **LLM**: `gpt-3.5-turbo` via `ChatOpenAI`
- **Prompting**: Custom system prompt for structured, clean answers with support for references to pages/images

```python
system_prompt = '''
You are an expert assistant. Use the context below to answer the user query in a helpful, structured format.
- Use bullet points, headings, or markdown if needed.
- If tables/images/flowcharts are referenced, mention their page or file name if available in metadata.
- Answer precisely and clearly.
'''
```

### 🧩 RAG Chain with LangChain Components

```python
RunnableMap({
    "context": lambda x: retriever.get_relevant_documents(x["question"]),
    "question": lambda x: x["question"],
})
| prompt
| ChatOpenAI
| StrOutputParser()
```

---

## 🔍 Files Overview

| File             | Purpose                             |
| ---------------- | ----------------------------------- |
| `ingest.py`      | Load and chunk documents            |
| `embed_store.py` | Embed chunks and store in FAISS     |
| `rag_chain.py`   | Query engine with retriever and LLM |

---

## 🎓 Learnings

- Importance of preprocessing diverse file types (PDF, Word, Excel)
- How vector DBs like FAISS help in fast semantic search
- Prompt engineering for clean and structured answers
- Using LangChain's modular components like `RunnableMap`, `ChatPromptTemplate`

---

## 🔮 Future Improvements

- ✅ Add table/image/flowchart extraction with visual rendering _(WIP)_
- 🖼️ OCR-based support for scanned documents
- 💬 Streamlit UI with chat history and responsive layout
- 📑 Source links, citations, and file preview

---

## 📹 Demo

👉 [Google Drive Link to Video Demo](<[Link](https://drive.google.com/file/d/1R77z66KJ7-7zdMEydlM97MwABTvBDIbU/view?usp=sharing)>)

---
