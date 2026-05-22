import json

with open("Main.ipynb", "r", encoding="utf-8") as f:
    data = json.load(f)

for cell in data.get("cells", []):
    if cell.get("cell_type") == "code":
        cell["outputs"] = []
        cell["execution_count"] = None

with open("Main.ipynb", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=1)

print("Notebook outputs cleared successfully!")