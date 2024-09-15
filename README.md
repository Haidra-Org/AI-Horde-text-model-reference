# AI-Horde-text-model-reference
A refeference of text models that can be used in the AI Horde

## How the `models.csv` file is converted to `db.json` by `convert.py`

All columns in the CSV file are added to the model record, with the following remarks:

- name: processed according to the needs of KoboldCPP and Aphrodite
- parameters_bn: converted to an integer `parameters` field in the model record
- tags: converted from a comma-separated string to a list of tags
- settings: converted from a JSON string to a dictionary
- model_name: assumed not present in CSV, set to the second part of slash-separated `name`
  (rationale: may enable front-ends to submit requests for models regardless of the prefix)
- display_name: if not present in CSV, set to a spaced-out version of `model_name`

Conversion will also:

- add the model's style to the tags (so that models with several styles can be filtered by tag)
- add a tag for the number of parameters (may simplify filtering by model size)

Keys and values from defaults.json are always present in the model record.
Values from defaults.json are used to fill in missing fields in the CSV file.

Keys from generation_params.json are used to validate the 'settings' field.
Values from generation_params.json are not used.

## Note to maintainers:

As of a [recent PR](https://github.com/Haidra-Org/AI-Horde-text-model-reference/pull/16), you will have to make sure that:

- All `csv` and `json` files are well-formed (no syntax errors).
- `python convert.py` is run
- The incoming files pass linting via `pre-commit`
  - `python -m pip install pre-commit` (first time only)
  - `pre-commit run --all-files`
