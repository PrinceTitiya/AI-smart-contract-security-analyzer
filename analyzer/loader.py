def load_contract(file_path: str) -> str:
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Error loading contract: {e}")