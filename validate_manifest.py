#!/usr/bin/env python3
import json, sys
import jsonschema

SCHEMA_PATH = "manifest.schema.json"
DATA_PATH = "gifs/index.json"

def load(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Missing file: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: {e}")
        sys.exit(1)

def main():
    print("--- Starting Manifest Validation ---")
    schema = load(SCHEMA_PATH)
    data = load(DATA_PATH)
    try:
        jsonschema.validate(instance=data, schema=schema)
        print(f"Success: {DATA_PATH} is valid against {SCHEMA_PATH}.")
        sys.exit(0)
    except jsonschema.ValidationError as e:
        print("\n--- VALIDATION FAILED ---")
        print(f"Error: {e.message}")
        if e.path:
            print("Path:", " -> ".join(map(str, e.path)))
        sys.exit(1)

if __name__ == "__main__":
    main()
