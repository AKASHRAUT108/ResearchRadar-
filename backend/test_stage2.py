import json
import os
from app.services.graph_builder import GraphBuilder

# Neo4j connection details (matches the Docker command we ran)
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "password123"

def main():
    # 1. Load the papers we fetched in Stage 1
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, "data", "papers.json")
    
    if not os.path.exists(filepath):
        print(f"❌ Cannot find {filepath}. Run test_stage1.py first!")
        return
        
    with open(filepath, "r", encoding="utf-8") as f:
        papers = json.load(f)

    print(f"📚 Loaded {len(papers)} papers from JSON.")

    # 2. Connect to Neo4j
    print("🔌 Connecting to Neo4j...")
    builder = GraphBuilder(URI, USER, PASSWORD)
    
    # 3. Clear old data and build the graph
    builder.clear_database()
    builder.ingest_papers(papers)
    builder.close()
    
    print("✅ Graph construction complete!")

if __name__ == "__main__":
    main()