import csv
import json

input_file = "models.csv"
output_file = "db.json"

data = {}

with open(input_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
        name = row[0]
        model_name = name.split("/")[1] if "/" in name else name
        params = row[1]

        
        data[name] = {
            "name": name,
            "baseline": "opt",
            "parameters": int(params),
            "description": "Add me",
            "version": "1",
            "style": "generalist",
            "nsfw": False
        }
        data[f"aphrodite/{name}"] = {
            "name": f"aphrodite/{name}",
            "baseline": "opt",
            "parameters": int(params),
            "description": "Add me",
            "version": "1",
            "style": "generalist",
            "nsfw": False
        }
        data[f"koboldcpp/{model_name}"] = {
            "name": f"koboldcpp/{model_name}",
            "baseline": "opt",
            "parameters": int(params),
            "description": "Add me",
            "version": "1",
            "style": "generalist",
            "nsfw": False
        }

with open(output_file, "w") as f:
    json.dump(data, f, indent=4)
