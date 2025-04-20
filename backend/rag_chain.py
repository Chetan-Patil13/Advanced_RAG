import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_core.documents import Document
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnableLambda


load_dotenv()

VECTORSTORE_PATH = "outputs/vector_store"
EMBED_MODEL = "text-embedding-3-small"
MODEL_NAME = "gpt-3.5-turbo"  # Or "gpt-4" if needed

# 1. Load vectorstore and retriever


def get_retriever():
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore.as_retriever(search_type="similarity", k=4)


# 2. Setup prompt
system_prompt = """You are an expert assistant. Use the context below to answer the user query in a helpful, structured format.
- Use bullet points, headings, or markdown if needed.
- If tables/images/flowcharts are referenced, mention their page or file name if available in metadata.
- Answer precisely and clearly.

Context:
{context}

Question:
{question}
"""

prompt = ChatPromptTemplate.from_template(system_prompt)

# 3. Setup OpenAI chat model
llm = ChatOpenAI(model=MODEL_NAME)

# 4. Create RAG chain
retriever = get_retriever()

# Fix input mapping
rag_chain = (
    RunnableMap({
        "context": lambda x: retriever.get_relevant_documents(x["question"]),
        "question": lambda x: x["question"],
    })
    | prompt
    | llm
    | StrOutputParser()
)

# 5. Query function
def ask_rag(query: str) -> str:
    return rag_chain.invoke({"question": query})
