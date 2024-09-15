import csv
import json
import os
import re

input_file = "models.csv"
output_file = "db.json"

# All columns in the CSV file are added to the model record
# with the following remarks:
# - name: processed according to the needs of KoboldCPP and Aphrodite
# - parameters_bn: converted to an integer 'parameters' field in the model record
# - tags: converted from a comma-separated string to a list of tags
# - settings: converted from a JSON string to a dictionary
# - model_name: assumed not present in CSV, set to the second part of slash-separated 'name'
#   (rationale: may enable front-ends to submit requests for models regardless of the prefix)
# - display_name: if not present in CSV, set to a spaced-out version of model_name

# We also:
# - add the model's style to the tags (so that models with several styles can be filtered by tag)
# - add a tag for the number of parameters (may simplify filtering by model size)

# Keys and values from defaults.json are always present in the model record.
# Values from defaults.json are used to fill in missing fields in the CSV file.
defaults = json.load(open("defaults.json", "r"))

# Keys from generation_params.json are used to validate the 'settings' field.
# Values from generation_params.json are not used.
params = json.load(open("generation_params.json", "r"))

data = {}

with open(input_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row: dict
        name = row.pop("name")
        model_name = name.split("/")[1] if "/" in name else name

        # Convert the parameter value to billions
        params_str = row.pop("parameters_bn")
        try:
            params_f = float(params_str)
            row["parameters"] = int(params_f * 1_000_000_000)
        except ValueError as e:
            print(e)
            print(f"Error converting {params_str} in {name} to an integer")
            exit(1)

        # Convert the tags to a list
        # assuming they are comma-separated
        tags = set([t.strip() for t in row["tags"].split(",")] if row["tags"] else [])
        if style := row.get("style"):
            tags.add(style)
        tags.add(f"{round(params_f, 0):.0f}B")
        row["tags"] = sorted(list(tags))

        # Convert the settings to a dictionary
        # assuming it's a JSON dictionary
        try:
            row["settings"] = json.loads(row["settings"]) if row["settings"] else {}
            assert isinstance(row["settings"], dict), f"{name}: settings must be a JSON dictionary"
            assert all(k in params for k in row["settings"]), f"{name}: settings must be a subset of generation_params.json"
        except json.JSONDecodeError as e:
            print(e)
            print(f"Error decoding settings for {name}")
            exit(1)

        # Set a display name if it's not already set
        # by adding spaces around underscores and hyphens
        if not row.get("display_name"):
            row["display_name"] = re.sub(r" +", " ", re.sub(r"[-_]", " ", model_name)).strip()

        # Remove empty values
        row = {k: v for k, v in row.items() if v}

        # Add the model record to the data
        for key_format in ["{name}", "aphrodite/{name}", "koboldcpp/{model_name}"]:
            key = key_format.format(name=name, model_name=model_name)
            data[key] = {"name": key, "model_name": model_name, **defaults, **row}

        # data[name] = {"name": name, "model_name": model_name, **defaults, **row}
        # data[f"aphrodite/{name}"] = {"name": f"aphrodite/{name}", "model_name": model_name, **defaults, **row}
        # data[f"koboldcpp/{model_name}"] = {"name": f"koboldcpp/{model_name}", "model_name": model_name, **defaults, **row}

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
        print(
            "db.json and db_test.json are different. Did you forget to run `convert.py`?"
        )
        exit(1)
else:
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
        f.write("\n")
