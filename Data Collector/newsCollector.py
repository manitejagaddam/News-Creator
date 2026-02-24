import os
import asyncio
import json
import requests
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

class AgenticNewsCollector:
    def __init__(self):
        self.headers = {'User-Agent': 'AI-News-Generator-Bot/1.0'}
        self.browser_config = BrowserConfig(headless=True)
        self.run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=10 ,
            wait_until="networkidle",      # Wait until network requests stop
            delay_before_return_html=2.0
        )

    def fetch_reddit(self, topic, limit=5):
        print(f"[*] Fetching Reddit for: {topic}...")
        # Switched to the global Reddit search endpoint
        safe_topic = urllib.parse.quote(topic)
        url = f"https://www.reddit.com/search.json?q={safe_topic}&sort=relevance&limit={limit}"
        try:
            res = requests.get(url, headers=self.headers).json()
            posts = []
            for post in res['data']['children']:
                p = post['data']
                posts.append({
                    "source": "Reddit",
                    "title": p['title'],
                    "link": f"https://reddit.com{p['permalink']}",
                    "score": p['ups'],
                    "summary": p.get('selftext', '')[:200],
                    "full_content": p.get('selftext', 'No text content.')
                })
            return posts
        except Exception as e:
            print(f"Error fetching Reddit: {e}")
            return []

    def fetch_arxiv(self, topic, limit=5):
        print(f"[*] Fetching ArXiv Metadata for: {topic}...")
        safe_topic = urllib.parse.quote(f'all:"{topic}"')
        base_url = 'http://export.arxiv.org/api/query?'
        search_query = f'search_query={safe_topic}&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending'
        results = []
        try:
            with urllib.request.urlopen(base_url + search_query) as response:
                xml_data = response.read().decode('utf-8')
                root = ET.fromstring(xml_data)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                for entry in root.findall('atom:entry', ns):
                    # 1. Get the standard abstract link
                    raw_link = entry.find('atom:id', ns).text.strip()
                    
                    # 2. Convert it to the full HTML paper link for Crawl4AI
                    html_link = raw_link.replace('/abs/', '/html/')
                    
                    results.append({
                        "source": "ArXiv",
                        "title": entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                        "link": html_link, # Pass the HTML version to the crawler
                        "score": "New",
                        "summary": entry.find('atom:summary', ns).text.strip()[:200]
                    })
        except Exception as e:
            print(f"Error fetching ArXiv: {e}")
        return results

    def fetch_semantic_scholar(self, topic, limit=5):
        print(f"[*] Fetching Semantic Scholar Metadata for: {topic}...")
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": topic, # The requests library handles encoding automatically here
            "limit": limit,
            "fields": "title,url,citationCount,abstract",
            "year": "2025-2026"
        }
        results = []
        try:
            res = requests.get(url, params=params).json()
            for paper in res.get('data', []):
                results.append({
                    "source": "Semantic Scholar",
                    "title": paper['title'],
                    "link": paper.get('url'),
                    "score": paper.get('citationCount', 0),
                    "summary": (paper.get('abstract') or "")[:200]
                })
        except Exception as e:
            print(f"Error fetching Semantic Scholar: {e}")
        return results

    def fetch_papers_with_code(self, topic, limit=5):
        print(f"[*] Fetching Papers With Code Metadata for: {topic}...")
        safe_topic = urllib.parse.quote(topic)
        # Added the 'q=' parameter to search the PWC database
        url = f"https://paperswithcode.com/api/v1/papers/?q={safe_topic}&items_per_page={limit}"
        results = []
        try:
            res = requests.get(url, headers=self.headers).json()
            for paper in res.get('results', []):
                results.append({
                    "source": "PapersWithCode",
                    "title": paper['title'],
                    "link": f"https://paperswithcode.com/paper/{paper['id']}",
                    "score": "Code Available",
                    "summary": paper.get('abstract', '')[:200]
                })
        except Exception as e:
            print(f"Error fetching Papers With Code: {e}")
        return results

    async def enrich_with_content(self, items):
        if not items: return []
        urls = [item['link'] for item in items if item.get('link')]
        print(f"\n[*] Crawl4AI initializing: Scraping {len(urls)} links concurrently...")
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            results = await crawler.arun_many(urls=urls, config=self.run_config)
            for i, res in enumerate(results):
                if res.success:
                    items[i]['full_content'] = res.markdown[:8000] 
                else:
                    items[i]['full_content'] = f"Crawl failed: {res.error_message}"
        return items

    async def run_all(self, topic):
        print(f"\n=== STARTING DATA COLLECTION FOR: {topic.upper()} ===")
        all_news = []
        
        # 1. Fetch Reddit (No crawling needed)
        all_news.extend(self.fetch_reddit(topic, limit=3))
        
        # 2. Gather URLs from academic sources
        to_crawl = []
        to_crawl.extend(self.fetch_arxiv(topic, limit=3))
        to_crawl.extend(self.fetch_semantic_scholar(topic, limit=3))
        to_crawl.extend(self.fetch_papers_with_code(topic, limit=3))
        
        # 3. Scrape all URLs using Crawl4AI
        enriched_items = await self.enrich_with_content(to_crawl)
        all_news.extend(enriched_items)
        
        # 4. Save output
        target_dir = os.path.join("..", "Data")

        # 2. Create the directory safely
        os.makedirs(target_dir, exist_ok=True)

        # 3. Construct the full file path
        filename = f"{topic.replace(' ', '_').lower()}_news.json"
        filepath = os.path.join(target_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(all_news, f, indent=4)
        print(f"\n[SUCCESS] Collected {len(all_news)} news items into {filename}")

if __name__ == "__main__":
    collector = AgenticNewsCollector()
    
    # You can change this single variable to whatever you want to research!
    SEARCH_TOPIC = "Autonomous AI Agents"
    
    asyncio.run(collector.run_all(SEARCH_TOPIC))