from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ==============================
# STEP 1 — Load PDF
# ==============================

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pdf_path = os.path.join(BASE_DIR, "sample_data", "sample.pdf")

loader = PyPDFLoader(pdf_path)

documents = loader.load()

print(f"\nLoaded {len(documents)} pages.\n")


# ==============================
# STEP 2 — Split into chunks
# ==============================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks.\n")


# ==============================
# STEP 3 — Create Embeddings
# ==============================

print("Loading embedding model...\n")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded.\n")


# ==============================
# STEP 4 — Store in FAISS
# ==============================

print("Creating FAISS vector store...\n")

vector_store = FAISS.from_documents(
    chunks,
    embedding_model
)

print("FAISS vector store created.\n")


# ==============================
# STEP 5 — User Query
# ==============================

query = "Summarize the key topics discussed in this document."


# ==============================
# STEP 6 — Retrieve Relevant Chunks
# ==============================

results = vector_store.similarity_search(query, k=2)

context = "\n\n".join([doc.page_content for doc in results])

print("\nRetrieved Context:\n")
print(context[:500])

# ==============================
# STEP 7 — Gemini Question Answering
# ==============================

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    temperature=0.3
)

prompt = f"""
You are an AI Research Assistant.

Answer the following question using ONLY the provided context.

Context:
{context}

Question:
{query}
"""

response = llm.invoke(prompt)

print("\nAI RESPONSE:\n")
print(response.content)