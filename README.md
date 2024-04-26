# AI-Horde-text-model-reference
A refeference of text models that can be used in the AI Horde

#### Note to maintainers:

As of a [recent PR](https://github.com/Haidra-Org/AI-Horde-text-model-reference/pull/16), you will have to make sure that:

- All `csv` and `json` files are well-formed (no syntax errors).
- `python convert.py` is run
- The incoming files pass linting via `pre-commit`
  - `python -m pip install pre-commit` (first time only)  
  - `pre-commit run --all-files`
