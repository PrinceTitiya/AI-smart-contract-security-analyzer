import subprocess
import json
import os

def run_slither(file_path: str):
    try:
        output_file = "result.json"
        # Run slither with JSON output
        result = subprocess.run(
            ["slither", file_path, "--json", output_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if not os.path.exists(output_file):
            print("Slither JSON not generated")
            return None

        with open(output_file) as f:
            data = json.load(f)

        os.remove("result.json")
        return data

    except Exception as e:
        raise Exception(f"Slither execution failed: {e}")