from neo4j import GraphDatabase
from app.services.nlp_extractor import extract_concepts

class GraphBuilder:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("🧹 Cleared existing graph database.")

    def ingest_papers(self, papers):
        with self.driver.session() as session:
            for p in papers:
                # 1. Extract NLP concepts from the abstract
                concepts = extract_concepts(p['abstract'])
                
                # 2. Run the Cypher query to build the graph
                session.run("""
                    MERGE (paper:Paper {arxiv_id: $arxiv_id})
                    SET paper.title = $title, 
                        paper.abstract = $abstract, 
                        paper.published = $published
                    
                    WITH paper
                    UNWIND $authors AS author_name
                    MERGE (a:Author {name: author_name})
                    MERGE (a)-[:AUTHORED]->(paper)
                    
                    WITH paper
                    UNWIND $categories AS cat
                    MERGE (c:Category {code: cat})
                    MERGE (paper)-[:HAS_CATEGORY]->(c)
                    
                    WITH paper
                    UNWIND $concepts AS concept_name
                    MERGE (concept:Concept {name: concept_name})
                    MERGE (paper)-[:MENTIONS]->(concept)
                """, **p, concepts=concepts)
                
                print(f"   🕸️  Added to graph: {p['title'][:40]}...")