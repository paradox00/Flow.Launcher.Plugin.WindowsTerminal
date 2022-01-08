import json
from pathlib import Path

def json_load_comments(path: Path):
    lines = list()
    with open(path, "r") as f:
        for line in f:
            if line.strip().startswith("//"):
                continue

            lines.append(line)
    
    content = "".join(lines)
    return json.loads(content)