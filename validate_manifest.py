# validate_manifest.py
#!/usr/bin/env python3
"""
Validates the GIF manifest file (gifs/index.json) against the JSON schema
definition (gif-schema.json) using the jsonschema library.
"""
import json
import sys
from typing import Any, Dict
import jsonschema

# --- Constants ---
# Corrected schema path based on uploaded file name
SCHEMA_PATH = "gif-schema.json"
DATA_PATH = "gifs/index.json"

def load_json(path: str) -> Dict[str, Any]:
    """Loads a JSON file from the given path with robust error handling."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            print(f"Loading {path}...")
            return json.load(f)
    except FileNotFoundError:
        print(f"\n--- VALIDATION FAILED ---")
        print(f"Error: Required file not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\n--- VALIDATION FAILED ---")
        print(f"Error: Invalid JSON in {path}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n--- VALIDATION FAILED ---")
        print(f"Unexpected error loading {path}: {e}")
        sys.exit(1)


class ManifestValidator:
    """Encapsulates the logic for loading the schema and manifest, and performing validation."""

    def __init__(self, schema_path: str, data_path: str):
        """Initializes the validator with paths to the schema and data."""
        self.schema_path = schema_path
        self.data_path = data_path

    def validate(self) -> None:
        """
        Performs the JSON schema validation.

        Exits with code 0 on success, 1 on failure.
        """
        print("--- Starting Manifest Validation ---")

        # Load schema and data using the SRP-adhering utility function
        schema = load_json(self.schema_path)
        data = load_json(self.data_path)

        try:
            # Perform the validation
            jsonschema.validate(instance=data, schema=schema)
            print(f"Success: {self.data_path} is valid against {self.schema_path}.")
            sys.exit(0)
        except jsonschema.ValidationError as e:
            # Detailed and clean error reporting
            print("\n--- VALIDATION FAILED ---")
            print(f"Manifest failed schema validation!")
            print(f"Error: {e.message}")
            if e.path:
                print("Path:", " -> ".join(map(str, e.path)))
            if e.context:
                print("Schema context:", e.context[0].json_path)
            
            # Print a helpful summary for the user
            print("\nEnsure your JSON data adheres to the rules in 'gif-schema.json'.")
            sys.exit(1)
        except Exception as e:
            print(f"\n--- VALIDATION FAILED ---")
            print(f"An unexpected error occurred during validation: {e}")
            sys.exit(1)


def main():
    """Main execution function."""
    validator = ManifestValidator(SCHEMA_PATH, DATA_PATH)
    validator.validate()


if __name__ == "__main__":
    main()
