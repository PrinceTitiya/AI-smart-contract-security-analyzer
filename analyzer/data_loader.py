import json
import os
from analyzer.embedder import get_embedding
from analyzer.vector_store import add_to_db

DATA_DIR = "data/vulnerable_contracts"

def load_dataset():
    with open("data/metadata.json") as f:
        metadata_list = json.load(f)

    for item in metadata_list:
        file_path = os.path.join(DATA_DIR, item["file"])

        with open(file_path, "r") as f:
            code = f.read()

        embedding = get_embedding(code)

        add_to_db(
            id=item["id"],
            text=code,
            embedding=embedding,
            metadata={
                "vulnerability": item["vulnerability"],
                "description": item["description"]
            }
        )

    print("Dataset loaded into vector DB successfully!")