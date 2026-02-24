import arxiv

def get_latest_arxiv(topic="cs.AI", max_results=5):
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    return [{"title": r.title, "link": r.pdf_url} for r in search.results()]