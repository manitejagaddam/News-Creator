import json
import os
from dotenv import load_dotenv
from typing import List, TypedDict
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END

load_dotenv()


class GraphState(TypedDict):
    news_items: List[dict]
    draft_summaries: List[str]
    final_newsletter: str
    
    
api_key = os.getenv("GOQ_API_KEY")

llm = ChatGroq( temperature=0.2,
                model_name="openai/gpt-oss-120b",
                api_key=api_key)

def summarize_news(state: GraphState):
    items = state.get("news_items", [])
    summaries = []
    
    prompt = PromptTemplate.from_template(
        "Summarize the following news article into a 3-sentence professional news segment. "
        "Focus on the core technical innovation or announcement.\n\n"
        "Title: {title}\nSource: {source}\nContent: {content}"
    )
    
    chain = prompt | llm
    
    for item in items:
        content_slice = item.get("full_content", "")[:4000] 
        res = chain.invoke({
            "title": item.get("title", ""),
            "source": item.get("source", ""),
            "content": content_slice
        })
        summaries.append(f"### {item.get('title')}\n*Source: {item.get('source')}*\n{res.content}\n[Read more]({item.get('link')})")
        
    return {"draft_summaries": summaries}

def compile_newsletter(state: GraphState):
    summaries = state.get("draft_summaries", [])
    combined_text = "\n\n".join(summaries)
    
    prompt = PromptTemplate.from_template(
        "You are an expert AI Tech Editor. Take the following news summaries and format them "
        "into a clean, cohesive Daily AI Newsletter in Markdown format. Add a brief, engaging introductory paragraph.\n\n"
        "Summaries:\n{summaries}"
    )
    
    chain = prompt | llm
    res = chain.invoke({"summaries": combined_text})
    
    return {"final_newsletter": res.content}

workflow = StateGraph(GraphState)

workflow.add_node("summarize_news", summarize_news)
workflow.add_node("compile_newsletter", compile_newsletter)

workflow.set_entry_point("summarize_news")
workflow.add_edge("summarize_news", "compile_newsletter")
workflow.add_edge("compile_newsletter", END)

app = workflow.compile()

def run_news_agent(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    top_items = data[:5]
    
    initial_state = {"news_items": top_items, "draft_summaries": [], "final_newsletter": ""}
    
    result = app.invoke(initial_state)
    
    with open("final_newsletter.md", "w", encoding="utf-8") as f:
        f.write(result["final_newsletter"])
        
    print(result["final_newsletter"])

if __name__ == "__main__":
    run_news_agent("../Data/autonomous_ai_agents_news.json")