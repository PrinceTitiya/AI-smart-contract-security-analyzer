import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection(name="contracts")

def add_to_db(id: str, text: str, embedding, metadata: dict):
    collection.add(
        ids=[id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )

def query_db(query_embedding, n_results=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results