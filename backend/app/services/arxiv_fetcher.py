import arxiv
import json
import os

def fetch_arxiv_papers(query: str, max_results: int = 10):
    # Create the client
    client = arxiv.Client()
    
    # Construct the search
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    papers = []
    # Iterate through results
    for result in client.results(search):
        papers.append({
            "arxiv_id": result.entry_id.split("/")[-1],
            "title": result.title,
            "abstract": result.summary.replace("\n", " "), # Clean up newlines
            "authors": [a.name for a in result.authors],
            "categories": result.categories,
            "primary_category": result.primary_category,
            "published": result.published.isoformat()
        })
    return papers

def save_papers_to_json(papers: list, filename: str = "data/papers.json"):
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    print(f"✅ Successfully saved {len(papers)} papers to {filename}")