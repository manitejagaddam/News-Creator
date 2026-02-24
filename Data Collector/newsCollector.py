import requests
import arxiv
import json
from datetime import datetime
from paperswithcode import PapersWithCodeClient
import urllib.request
import xml.etree.ElementTree as ET

class NewsCollector:
    def __init__(self):
        self.pwc_client = PapersWithCodeClient()
        self.headers = {'User-Agent': 'AI-News-Generator-Bot/1.0'}

    def fetch_reddit(self, subreddit="MachineLearning", limit=5):
        """Fetches trending posts from a specific subreddit."""
        print(f"[*] Fetching Reddit: r/{subreddit}...")
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
        try:
            res = requests.get(url, headers=self.headers).json()
            posts = []
            for post in res['data']['children']:
                p = post['data']
                posts.append({
                    "source": f"Reddit/r/{subreddit}",
                    "title": p['title'],
                    "link": f"https://reddit.com{p['permalink']}",
                    "score": p['ups'],
                    "summary": p.get('selftext', '')[:200] + "..."
                })
            return posts
        except Exception as e:
            return [{"error": f"Reddit failed: {e}"}]

    def fetch_arxiv(self, query="all:electron", limit=5):
        print("[*] Fetching ArXiv (Official API)...")
        # 1. Build the URL
        base_url = 'http://export.arxiv.org/api/query?'
        search_query = f'search_query={query}&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending'
        
        results = []
        try:
            # 2. Make the request
            with urllib.request.urlopen(base_url + search_query) as response:
                xml_data = response.read().decode('utf-8')
                
                # 3. Parse the XML response
                root = ET.fromstring(xml_data)
                # namespaces are required to find tags in Atom feeds
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                
                for entry in root.findall('atom:entry', ns):
                    title = entry.find('atom:title', ns).text.strip()
                    link = entry.find('atom:id', ns).text.strip()
                    summary = entry.find('atom:summary', ns).text.strip()
                    
                    results.append({
                        "source": "ArXiv (Official)",
                        "title": title.replace('\n', ' '),
                        "link": link,
                        "score": "New",
                        "summary": summary[:200] + "..."
                    })
        except Exception as e:
            print(f"Error fetching ArXiv: {e}")
            
        return results

    def fetch_semantic_scholar(self, query="Large Language Models", limit=5):
        """Fetches highly cited papers from Semantic Scholar."""
        print("[*] Fetching Semantic Scholar...")
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,url,citationCount,abstract",
            "year": "2025-2026"
        }
        try:
            res = requests.get(url, params=params).json()
            results = []
            for paper in res.get('data', []):
                results.append({
                    "source": "Semantic Scholar",
                    "title": paper['title'],
                    "link": paper.get('url'),
                    "score": paper.get('citationCount', 0),
                    "summary": (paper.get('abstract') or "")[:200] + "..."
                })
            return results
        except Exception as e:
            return []

    def fetch_papers_with_code(self, limit=5):
        """Fetches papers that have associated code repositories."""
        print("[*] Fetching Papers With Code...")
        try:
            papers = self.pwc_client.paper_list(items_per_page=limit)
            results = []
            for paper in papers.results:
                results.append({
                    "source": "PapersWithCode",
                    "title": paper.title,
                    "link": f"https://paperswithcode.com/paper/{paper.id}",
                    "score": "Code Available",
                    "summary": f"Repository: {paper.repository}" if paper.repository else "No repo linked yet."
                })
            return results
        except Exception as e:
            return []

    def run_all(self):
        all_news = []
        all_news.extend(self.fetch_reddit("MachineLearning"))
        all_news.extend(self.fetch_reddit("LocalLLaMA"))
        all_news.extend(self.fetch_arxiv())
        all_news.extend(self.fetch_semantic_scholar())
        all_news.extend(self.fetch_papers_with_code())
        
        # Save to JSON
        with open("news_feed.json", "w", encoding="utf-8") as f:
            json.dump(all_news, f, indent=4)
        print(f"\n[SUCCESS] Collected {len(all_news)} news items into news_feed.json")

if __name__ == "__main__":
    collector = NewsCollector()
    collector.run_all()