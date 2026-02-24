from paperswithcode import PapersWithCodeClient

client = PapersWithCodeClient()
papers = client.paper_list(items_per_page=10)

for paper in papers.results:
    print(f"Title: {paper.title}")
    print(f"ArXiv ID: {paper.arxiv_id}")
    print(f"Repository: {paper.repository}\n")