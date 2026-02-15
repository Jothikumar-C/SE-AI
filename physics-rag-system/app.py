"""
Streamlit UI Application:
"""

import streamlit as st
from rag_pipeline import PhysicsRAG
from document_loader import load_pdf
import tempfile

st.set_page_config(page_title="Physics RAG System", layout="wide")

st.title(" Physics Document RAG System")

rag = PhysicsRAG()

# Upload Section
uploaded_file = st.file_uploader("Upload Physics PDF", type=["pdf"])

if uploaded_file:

    with st.spinner("Data Upload – Loading..."):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        docs = load_pdf(temp_file.name)
        st.success("Data Upload – OK")

    with st.spinner("Embedding Database – Creating..."):
        rag.build_index(docs)
        st.success("Embedding Database – Completed")

# Query Section
query = st.text_input("Ask Physics Question")

if query:
    with st.spinner("Retrieval – Processing..."):
        st.success("Retrieval – Completed")

    with st.spinner("Answer Generation – Generating..."):
        answer = rag.ask(query)
        st.success("Answer Generation – Completed")

    st.markdown("### 📖 Answer")
    st.write(answer)


