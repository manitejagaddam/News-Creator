import requests

def get_semantic_scholor_news(query : str = "Latest Open source Models", year : str = "2026"):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": query, "year": year, "fields": "title,citationCount,url"}
    # Note: API key is optional for low volume but recommended
    return requests.get(url, params=params).json().get('data', [])