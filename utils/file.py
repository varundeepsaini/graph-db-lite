import json
import os

def write_json_to_file(data: dict, filename: str):
    with open(filename, "w") as f:
        json.dump(data, f)

    return

def read_json_from_file(filename: str) -> dict:
    if not os.path.exists(filename):
        return {"graphs": []}
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            if not content:
                return {"graphs": []}
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return {"graphs": []}

def read_file(filename: str) -> str:
    with open(filename, "r") as f:
        data = f.read()

    return data

def write_file(filename: str, data: str):
    with open(filename, "w") as f:
        f.write(data)

    return