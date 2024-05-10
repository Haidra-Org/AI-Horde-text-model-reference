import csv
import json
import os

input_file = "models.csv"
output_file = "db.json"

data = {}

with open(input_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
        name = row[0]
        model_name = name.split("/")[1] if "/" in name else name
        params_str = row[1]  # Store the parameter value as a string

        # Convert the parameter value to billions, handling fractional values
        if "." in params_str:
            params_float = float(params_str)
            params = int(params_float * 1_000_000_000)
        else:
            params = int(params_str) * 1_000_000_000

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

TESTS_ONGOING = os.getenv("TESTS_ONGOING", False)
if TESTS_ONGOING and os.path.exists(output_file):
    # If tests are ongoing, we don't want to overwrite the db.json file
    # Instead, we'll write to a new file and make sure the two files are the same
    # by comparing them as strings
    with open("db_test.json", "w") as f:
        json.dump(data, f, indent=4)
        f.write("\n")

    with open(output_file, "r") as f:
        old_data = f.read()

    with open("db_test.json", "r") as f:
        new_data = f.read()

    if old_data != new_data:
        print("db.json and db_test.json are different. Did you forget to run `convert.py`?")
        exit(1)
else:
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
        f.write("\n")
