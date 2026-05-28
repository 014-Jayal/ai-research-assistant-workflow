from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
import uuid

from backend.rag_engine import build_vector_store, ask_question
from backend.agents import run_multi_agent_research
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

app = FastAPI(title="AI Research Assistant")

FAISS_INDEX_PATH = "faiss_index"

@app.get("/")
def home():
    return {"message": "AI Research Assistant API is running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    build_vector_store(file_path, FAISS_INDEX_PATH)

    return JSONResponse({
        "original_filename": file.filename,
        "saved_filename": unique_filename,
        "message": "PDF uploaded and processed successfully"
    })

@app.post("/ask")
async def ask(query: str):
    if not os.path.exists(FAISS_INDEX_PATH):
        return JSONResponse(status_code=400, content={"error": "Please upload a PDF first."})

    try:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.load_local(FAISS_INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)
        answer = ask_question(vector_store, query)

        return JSONResponse({"question": query, "answer": answer})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/generate-report")
async def generate_comprehensive_report():
    if not os.path.exists(FAISS_INDEX_PATH):
        return JSONResponse(status_code=400, content={"error": "Please upload a PDF first."})
        
    try:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.load_local(FAISS_INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)
        
        # Pull core themes for the multi-agent synthesis
        results = vector_store.similarity_search("core objectives key findings summary methodology", k=4)
        context = "\n\n".join([doc.page_content for doc in results])
        
        report_data = run_multi_agent_research(context)
        return JSONResponse(report_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))