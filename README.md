<h1 align="center">AI Research Assistant: Multi-Agent RAG Workflow</h1>

<p align="center">
  <b>Enterprise Workflow Automation Prototype</b><br>
  Accelerating Document Analysis with Agentic AI & Semantic Retrieval
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white">
  <img src="https://img.shields.io/badge/Gemini_Flash_Lite-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white">
  <img src="https://img.shields.io/badge/FAISS-Vector_DB-00ADD8?style=for-the-badge">
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/014-Jayal/ai-research-assistant-workflow?style=social">
  <img src="https://img.shields.io/github/forks/014-Jayal/ai-research-assistant-workflow?style=social">
</p>

---

## Overview

This project presents a production-ready AI workflow automation system designed to process complex research documents.

Unlike standard conversational chatbots, this system utilizes a Retrieval-Augmented Generation (RAG) pipeline combined with a Multi-Agent Orchestration Workflow. It reads technical PDFs, retrieves context-aware information, and passes it through specialized AI agents (Analyst, Summarizer, Business Strategist) to automatically generate structured executive reports.

The architecture combines:

- Gemini Flash Lite
- LangChain orchestration
- FAISS vector retrieval
- HuggingFace MiniLM embeddings
- FastAPI backend APIs
- Streamlit frontend interfaces
- Multi-Agent AI workflows

---

## Key Contributions

- Multi-Agent Sequential Pipeline for layered document synthesis
- Stateless API Backend using FastAPI for scalable deployment
- Context-Aware Text Chunking preserving semantic continuity
- Custom Parsing Engine for clean Markdown rendering
- 100% Free / Cost-Optimized Stack
- Containerized Architecture ready for Docker deployment

---

## System Architecture

<p align="center">
  <img src="docs/System Architecture.png" alt="Architecture Diagram" width="100%">
</p>

<p align="center">
  <i>End-to-end Retrieval-Augmented Generation (RAG) workflow architecture</i>
</p>

---

## RAG Workflow Pipeline

```text
User Query
   ↓
Streamlit Frontend
   ↓
FastAPI Backend
   ↓
PDF Parsing & Chunking
   ↓
MiniLM Embedding Generation
   ↓
FAISS Vector Store
   ↓
Semantic Retrieval
   ↓
LangChain Orchestration
   ↓
Gemini Flash Lite
   ↓
AI-Generated Research Insights
```

---

## FastAPI Swagger Documentation

<p align="center">
  <img src="docs/screenshots/09_fastapi_api_documentation.png" width="95%">
</p>

---

## Technical Stack & Performance

| Component | Technology | Role | Cost Profile |
| :--- | :--- | :--- | :--- |
| **LLM Engine** | Gemini Flash Lite API | Reasoning & Summarization | Free Tier |
| **Backend API** | FastAPI | Async routing & file handling | Open Source |
| **Frontend UI** | Streamlit | Interactive AI dashboard | Open Source |
| **RAG Framework** | LangChain | Agent orchestration & prompts | Open Source |
| **Vector Database** | FAISS | Semantic similarity retrieval | Local Compute |
| **Embeddings** | MiniLM-L6-v2 | Dense vector generation | Local Compute |

---

## Project Structure

```text
ai-research-assistant-workflow/
├── backend/
│   ├── main.py
│   ├── rag_engine.py
│   ├── agents.py
│   └── rag_pipeline.py
│
├── frontend/
│   └── app.py
│
├── docs/
│   ├── architecture.png
│   ├── screenshots/
│   ├── AI-Powered Research Assistant Report.pdf
│   └── AI-Powered Research Assistant Report.docx
│
├── uploaded_files/
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```

---

## Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/014-Jayal/ai-research-assistant-workflow.git
cd ai-research-assistant-workflow
```

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## Docker Deployment

```bash
docker-compose up --build
```

---

## Running the Application

### Start FastAPI Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

API Docs:
`http://localhost:8000/docs`

---

### Start Streamlit Frontend

```bash
streamlit run frontend/app.py
```

Dashboard:
`http://localhost:8501`

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `/upload` | Upload and process PDFs |
| `/ask` | Contextual document question answering |
| `/generate-report` | Multi-agent synthesis workflow |

---

## Multi-Agent Workflow

| Agent | Responsibility |
|---|---|
| Analyst Agent | Extract technical insights |
| Summary Agent | Generate executive summaries |
| Strategy Agent | Produce strategic recommendations |

The sequential orchestration workflow improves:
- response structure,
- contextual grounding,
- report consistency,
- and modular AI task delegation.

---

## Core Engineering Insights

### Agentic Delegation

Standard monolithic prompts often suffer from:
- attention degradation,
- hallucinations,
- inconsistent outputs.

Splitting the workflow into:
1. Analysis
2. Summary
3. Strategy

produced significantly more structured and grounded outputs.

---

### Context-Aware Chunking

Rather than splitting documents purely by character count, the system uses:
- RecursiveCharacterTextSplitter
- paragraph-aware separation
- sentence-preserving overlap

to retain contextual continuity across highly technical PDFs.

---

### Safe Payload Extraction

A custom parsing layer intercepts Gemini API responses and strips raw JSON artifacts before frontend rendering, ensuring clean Markdown output formatting.

---

## Scalability & Future Improvements

Potential future improvements include:

- Pinecone or Weaviate vector databases
- Conversational memory systems
- Multi-document retrieval
- Enterprise authentication
- Persistent cloud indexing
- Distributed AI orchestration
- Citation-aware responses

---

## Author

### Jayal Shah

- GitHub: https://github.com/014-Jayal
- LinkedIn: https://www.linkedin.com/in/jayal-shah04/

---

## Acknowledgements

This project was developed as part of an AI Researcher / AI Innovation Engineer technical evaluation assignment focused on:
- Retrieval-Augmented Generation (RAG)
- Semantic Search Systems
- AI Workflow Automation
- Multi-Agent AI Systems
- Practical AI Engineering
- Production-Oriented AI Architecture

---

<p align="center">
  <b>Built with Gemini • LangChain • FastAPI • Streamlit • FAISS</b>
</p>
