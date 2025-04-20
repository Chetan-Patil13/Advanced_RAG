import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.rag_chain import ask_rag
import streamlit as st
st.set_page_config(page_title="Advanced RAG Chat", layout="wide")

# Sidebar: Chat history
with st.sidebar:
    st.title("🧠 Chat History")
    if "history" not in st.session_state:
        st.session_state.history = []

    for idx, (q, a) in enumerate(st.session_state.history):
        with st.expander(f"🔹 {q}", expanded=False):
            st.markdown(a, unsafe_allow_html=True)

# Main Chat UI
st.title("📘 Ask Your Knowledge Base")

query = st.chat_input("Ask a question about your documents...")

if query:
    with st.spinner("Thinking..."):
        response = ask_rag(query)

    # Store Q&A
    st.session_state.history.append((query, response))

    # Display current chat
    st.markdown(f"**🧑‍💻 You:** {query}")
    st.markdown(response, unsafe_allow_html=True)
