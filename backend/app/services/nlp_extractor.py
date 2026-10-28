import spacy
nlp=spacy.load("en_core_web_sm")
def extract_concepts(text:str,max_concepts:int=5)->list[str]:
    doc=nlp(text)
    concepts=[]
    for chunk in doc.noun_chunks:
        concept=chunk.text.lower().strip()
        if len(concept)>3 and concept not in concepts:
            concepts.append(concept)
    return concepts[:max_concepts]
