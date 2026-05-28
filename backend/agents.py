import os
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def extract_clean_text(response) -> str:
    """
    Safely extracts clean markdown text from LangChain/Gemini responses,
    stripping away raw JSON wrappers and metadata.
    """
    content = response.content
    
    # If the response is a list of blocks
    if isinstance(content, list) and len(content) > 0:
        return content[0].get("text", str(content))
        
    # If the response is a stringified JSON payload
    if isinstance(content, str):
        if '"type":"text"' in content and '"extras":' in content:
            # Regex to pull out ONLY the text payload
            match = re.search(r'"text"\s*:\s*"(.*?)"\n.*?"extras"', content, re.DOTALL)
            if match:
                raw_text = match.group(1)
                # Unescape formatting so markdown renders beautifully
                return raw_text.replace('\\n', '\n').replace('\\"', '"')
                
    return str(content)

def run_multi_agent_research(context: str) -> dict:
    """
    Accepts dynamic context retrieved from RAG and orchestrates a 
    multi-agent workflow to produce a structured research brief.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-lite-latest",
        temperature=0.3
    )

    # ==============================
    # Agent 1 — Research Analyst
    # ==============================
    research_prompt = f"""
    You are a Research Analyst. Analyze the following technical context and extract the core technical breakthroughs, methodologies, or data patterns.
    Return ONLY pure text. Do not use JSON formatting.
    
    Context:
    {context}
    """
    analyst_output = extract_clean_text(llm.invoke(research_prompt))

    # ==============================
    # Agent 2 — Summary Expert
    # ==============================
    summary_prompt = f"""
    You are a Summarization Expert. Review this Analyst's breakdown and generate a high-level, executive summary suitable for stakeholders.
    Return ONLY pure text. Do not use JSON formatting.
    
    Analyst Breakdown:
    {analyst_output}
    """
    summary_output = extract_clean_text(llm.invoke(summary_prompt))

    # ==============================
    # Agent 3 — Recommendation Expert
    # ==============================
    recommendation_prompt = f"""
    You are a Business Recommendation Expert. Based on the Analyst's technical insights and the Executive Summary, outline 3 concrete business use cases or strategic advantages this research enables.
    Return ONLY pure text. Do not use JSON formatting.
    
    Technical Insights: {analyst_output}
    Executive Summary: {summary_output}
    """
    recommendation_output = extract_clean_text(llm.invoke(recommendation_prompt))

    # Return structured results
    return {
        "technical_insights": analyst_output,
        "executive_summary": summary_output,
        "business_recommendations": recommendation_output
    }