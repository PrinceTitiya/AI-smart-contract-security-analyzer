from analyzer.embedder import get_embedding
from analyzer.vector_store import query_db

def process_contract(contract_code: str):
    embedding = get_embedding(contract_code)

    results = query_db(embedding)

    return results