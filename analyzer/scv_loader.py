import json
from analyzer.embedder import get_embedding
from analyzer.vector_store import add_to_db

def load_scv_dataset(file_path="data/scv_dataset.jsonl", limit=100):
    """Load SCV dataset and add to vectorDB"""
    count = 0

    with open(file_path, "r") as f:
        for line in f:
            entry = json.loads(line)

            # only use vulnerable entries
            if not entry.get("vulnerable",True):
                continue

            code = entry["code_snippet"].strip()

            if len(code)<20:
                continue

            #get_embbedings
            embedding = get_embedding(code)

            add_to_db(
                id=entry["id"],
                text=code,
                embedding=embedding,
                metadata={
                    "vulnerability": entry["category"],
                    "description":entry["description"],
                    "severity": entry["severity"],
                    "source":"scv_dataset"
                }
            )

            count += 1
            if count >= limit:
                break

    print(f"Loaded {count} vulnerable smart contracts entries into vector db")