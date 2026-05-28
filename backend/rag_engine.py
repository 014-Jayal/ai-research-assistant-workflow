import os
import re
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def extract_clean_text(response) -> str:
    """Safely extracts clean markdown text from LangChain/Gemini responses."""
    content = response.content
    if isinstance(content, list) and len(content) > 0:
        return content[0].get("text", str(content))
    if isinstance(content, str):
        if '"type":"text"' in content and '"extras":' in content:
            match = re.search(r'"text"\s*:\s*"(.*?)"\n.*?"extras"', content, re.DOTALL)
            if match:
                return match.group(1).replace('\\n', '\n').replace('\\"', '"')
    return str(content)

# ==============================
# Build Vector Store
# ==============================
def build_vector_store(pdf_path, save_path="faiss_index"):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"\nLoaded {len(documents)} pages.\n")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,      
        chunk_overlap=250,    
        separators=["\n\n", "\n", "(?<=\. )", " ", ""] 
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} contextual chunks.\n")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    print("Embedding model loaded.\n")

    vector_store = FAISS.from_documents(chunks, embedding_model)
    vector_store.save_local(save_path)
    print(f"FAISS vector store saved to disk at '{save_path}'.\n")

    return True

# ==============================
# Ask Question (Standard RAG)
# ==============================
def ask_question(vector_store, query):
    results = vector_store.similarity_search(query, k=5)

    filtered_results = []
    noise_keywords = ["references", "arxiv", "et al."]
    
    for doc in results:
        text = doc.page_content.lower()
        if any(keyword in text for keyword in noise_keywords):
            continue
        filtered_results.append(doc)

    if not filtered_results:
        filtered_results = results

    context = "\n\n".join([doc.page_content for doc in filtered_results[:3]])

    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-lite-latest",
        temperature=0.3
    )

    prompt = f"""
    You are an advanced AI Research Assistant.
    Analyze the provided research context carefully and answer the question clearly.
    Focus on key findings, technical concepts, and important insights.
    If the context is insufficient, clearly mention it.
    Return ONLY pure text. Do not use JSON formatting.

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)
    return extract_clean_text(response)