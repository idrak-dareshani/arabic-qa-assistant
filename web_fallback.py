import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_web(query, max_results=3):
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    data = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        results = response.json().get("results", [])
        return format_result(results)
    else:
        return f"Tavily Error {response.status_code}: {response.text}"

from langchain_community.tools.tavily_search import TavilySearchResults

def search_tool(query):
    tool = TavilySearchResults(k=3)
    results = tool.run(query)
    return format_result(results)

def format_result(results):
    output = []
    for res in results:
        title = res.get("title", "No Title")
        content = res.get("content", "No Content")
        link = res.get("url", "No URL")
        output.append(f"🔗 **{title}**\n{content}\n{link}")
    return "\n\n".join(output)