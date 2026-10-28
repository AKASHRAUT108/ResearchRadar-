from app.services.arxiv_fetcher import fetch_arxiv_papers, save_papers_to_json

if __name__ == "__main__":
    print("🚀 Starting arXiv ingestion for topic: 'Graph RAG'")
    
    # Fetch 5 papers just to test
    papers = fetch_arxiv_papers(query="Graph RAG", max_results=5)
    
    # Save them locally
    save_papers_to_json(papers, filename="backend/data/papers.json")
    
    # Print the first one to verify
    if papers:
        print("\n--- Sample Paper Fetched ---")
        print(f"Title: {papers[0]['title']}")
        print(f"Authors: {', '.join(papers[0]['authors'])}")
        print(f"ID: {papers[0]['arxiv_id']}")