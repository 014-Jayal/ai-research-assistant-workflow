import streamlit as st
import requests

st.set_page_config(page_title="Research Assistant", page_icon="✨", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #FAFAFA; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 600; color: #111827; }
    
    /* Clean up expander styling for the agent reports */
    .streamlit-expanderHeader { font-weight: bold; font-size: 1.1rem; }
    .st-emotion-cache-1z7sptj { padding: 1rem; }
    
    .stFileUploader > div > div { 
        background-color: #FFFFFF; 
        border-radius: 12px; 
        border: 1px dashed #D1D5DB; 
        padding: 1rem; 
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Please upload a research document in the sidebar to get started."}
    ]

# ==============================
# Sidebar
# ==============================
with st.sidebar:
    st.markdown("### 📚 Knowledge Base")
    st.caption("Upload documents to ground the AI's reasoning.")
    
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    
    if uploaded_file:
        if st.button("Process Document", type="primary", use_container_width=True):
            with st.spinner("Indexing document..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post("http://127.0.0.1:8000/upload", files=files)
                    if response.status_code == 200:
                        st.success("✨ Document indexed successfully!")
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f"I've successfully analyzed **{uploaded_file.name}**. What would you like to extract or summarize?"
                        })
                    else:
                        st.error("❌ Failed to process document.")
                except requests.exceptions.ConnectionError:
                    st.error("Backend unreachable. Ensure FastAPI is running on port 8000.")

    st.divider()
    st.markdown("⚙️ **Architecture:** Gemini + FAISS + FastAPI + LangChain Agents")

# ==============================
# Main Interface
# ==============================
st.title("✨ AI Research Assistant")

tab1, tab2 = st.tabs(["💬 Interactive Q&A", "🤖 Multi-Agent Briefing"])

with tab1:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if query := st.chat_input("Ask a question about your research..."):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🤔 Synthesizing insights...")
            try:
                response = requests.post("http://127.0.0.1:8000/ask", params={"query": query})
                if response.status_code == 200:
                    answer = response.json().get("answer", "No response generated.")
                    message_placeholder.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    message_placeholder.error("Error generating response.")
            except requests.exceptions.ConnectionError:
                 message_placeholder.error("Backend server is unreachable.")

with tab2:
    st.markdown("### Run Multi-Step Agent Analysis")
    st.caption("Triggers a sequential workflow: Analyst Agent ➔ Summary Agent ➔ Strategy Agent.")
    
    if st.button("🚀 Run Multi-Agent Synthesis", use_container_width=True):
        with st.spinner("Orchestrating agents... this may take a moment."):
            try:
                res = requests.post("http://127.0.0.1:8000/generate-report")
                if res.status_code == 200:
                    data = res.json()
                    st.success("✅ Workflow Complete! Report Generated.")
                    
                    st.divider()
                    
                    # Using expanders to keep the UI clean, with the markdown directly injected
                    with st.expander("🔬 1. Technical Insights (Analyst Agent)", expanded=True):
                        st.markdown(data["technical_insights"])
                        
                    with st.expander("📝 2. Executive Summary (Summary Agent)", expanded=True):
                        st.markdown(data["executive_summary"])
                        
                    with st.expander("💡 3. Strategic Recommendations (Business Agent)", expanded=True):
                        st.markdown(data["business_recommendations"])
                else:
                    st.error("Ensure a PDF is uploaded and processed first.")
            except Exception:
                st.error("Backend unreachable.")
