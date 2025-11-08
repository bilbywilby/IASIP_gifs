# add_gif_cli.py
#!/usr/bin/env python3
"""
Automated CLI tool to add a new GIF entry.
1. Downloads GIF from a URL.
2. Interactively collects description and tags.
3. Validates the new entry against gif-schema.json.
4. Appends the entry to gifs/index.json.
5. Stages the new GIF and the updated manifest for commit.
"""
import json
import sys
import argparse
from typing import Dict, Any, List
from pathlib import Path
import requests
import jsonschema
import subprocess
import os

# --- Configuration ---
GIFS_DIR = Path("gifs")
MANIFEST_PATH = GIFS_DIR / "index.json"
SCHEMA_PATH = Path("gif-schema.json")
MAX_FILE_SIZE_MB = 5  # Enforce a reasonable size limit


# --- Utility Functions ---

def load_json(path: Path) -> Any:
    """Loads a JSON file with error handling."""
    if not path.exists():
        if path == MANIFEST_PATH:
            print(f"Creating empty manifest file at {path}...")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)
            return []
        print(f"Error: Required file not found: {path}")
        sys.exit(1)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {path}: {e}")
        sys.exit(1)

def download_gif(url: str, output_path: Path):
    """Downloads the GIF, checking file size and content type."""
    try:
        print(f"Downloading GIF from: {url}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        # Basic content and size checks
        if 'image/gif' not in response.headers.get('Content-Type', '').lower():
            raise ValueError(f"URL did not return a GIF (Content-Type: {response.headers.get('Content-Type')})")
        
        content_length = int(response.headers.get('Content-Length', 0))
        if content_length > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValueError(f"File size exceeds limit of {MAX_FILE_SIZE_MB}MB.")

        GIFS_DIR.mkdir(exist_ok=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Successfully downloaded to {output_path}. Size: {output_path.stat().st_size / 1024:.2f} KB.")
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error during download: {e}")
        sys.exit(1)

def get_metadata(filename: str) -> Dict[str, Any]:
    """Interactively collects metadata from the user."""
    print("\n--- Enter Metadata ---")
    
    # 1. Description
    while True:
        desc = input("Description (e.g., Mac's ocular pat-down): ").strip()
        if len(desc) >= 10 and len(desc) <= 200:
            break
        print("Description must be between 10 and 200 characters.")
        
    # 2. Tags
    while True:
        tags_input = input("Tags (comma separated, e.g., mac,patdown,ocular): ").strip().lower()
        tags = [t.strip() for t in tags_input.split(',') if t.strip()]
        if tags:
            break
        print("Please enter at least one tag.")

    return {
        "filename": filename,
        "description": desc,
        "tags": tags
    }

def validate_entry(entry: Dict[str, Any]):
    """Validates the new manifest entry against the schema."""
    schema = load_json(SCHEMA_PATH)
    try:
        jsonschema.validate(instance=[entry], schema={"type": "array", "items": schema['items']})
        print("Metadata passed schema validation.")
    except jsonschema.ValidationError as e:
        print("\n--- METADATA VALIDATION FAILED ---")
        print(f"Error: {e.message}")
        print("Path:", " -> ".join(map(str, e.path)))
        if Path(entry['filename']).exists(): os.remove(Path(entry['filename'])); # Clean up the downloaded file
        sys.exit(1)

def update_manifest(entry: Dict[str, Any], manifest_path: Path):
    """Appends the new entry to the manifest file."""
    manifest = load_json(manifest_path)
    # Check for duplicate filename
    if any(g['filename'] == entry['filename'] for g in manifest):
        print(f"Error: Filename '{entry['filename']}' already exists in manifest. Aborting.")
        if Path(entry['filename']).exists(): os.remove(Path(entry['filename'])); # Clean up the downloaded file
        sys.exit(1)
        
    manifest.append(entry)
    manifest.sort(key=lambda x: x['filename'].lower()) # Sort for consistency

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    print(f"Successfully updated and sorted manifest: {manifest_path}")

def run_git_add_commit(gif_path: Path, manifest_path: Path):
    """Stages and commits the changes."""
    print("\n--- Staging Changes ---")
    try:
        subprocess.run(['git', 'add', str(gif_path)], check=True, capture_output=True)
        subprocess.run(['git', 'add', str(manifest_path)], check=True, capture_output=True)
        
        commit_message = f"Add new GIF: {gif_path.name}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True)
        
        print("Success! GIF and manifest committed.")
        print(f"Next step: `git push` to publish.")
    except subprocess.CalledProcessError as e:
        print("Error during git commit:")
        print(e.stderr.decode())
        print("Ensure you have run 'git init' and configured your user identity.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Automated CLI tool for adding a new GIF to the IASIP repository."
    )
    parser.add_argument('url', type=str, help="The direct URL to the GIF file (e.g., https://media.giphy.com/media/xyz.gif).")
    parser.add_argument('filename', type=str, help="The desired local filename (must end with .gif, e.g., mac_patdown.gif).")
    args = parser.parse_args()

    # Normalize and validate filename
    local_filename = args.filename.lower().replace(' ', '_')
    if not local_filename.endswith('.gif'):
        print("Error: Filename must end with '.gif'.")
        sys.exit(1)
        
    gif_path = GIFS_DIR / local_filename

    # 1. Download
    if gif_path.exists():
        print(f"Error: GIF file '{local_filename}' already exists locally. Aborting.")
        sys.exit(1)
        
    download_gif(args.url, gif_path)

    # 2. Get and Validate Metadata
    new_entry = get_metadata(local_filename)
    validate_entry(new_entry) # Uses the existing gif-schema.json

    # 3. Update Manifest and Commit
    update_manifest(new_entry, MANIFEST_PATH)
    run_git_add_commit(gif_path, MANIFEST_PATH)
    
    print("\n✅ New GIF added and committed successfully.")


if __name__ == "__main__":
    main()
