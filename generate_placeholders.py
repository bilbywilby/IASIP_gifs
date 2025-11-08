#!/usr/bin/env python3
import os
import json
from pathlib import Path

INDEX_PATH = "gifs/index.json"
GIF_DIR = "gifs"
# Minimal valid 1x1 transparent GIF (GIF89a)
MINIMAL_GIF = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

def generate_gif_placeholders(index_file_path=INDEX_PATH, gif_dir=GIF_DIR, write_minimal=True):
    print("--- Starting GIF Placeholder Generation ---")
    os.makedirs(gif_dir, exist_ok=True)

    try:
        with open(index_file_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        if not isinstance(manifest, list):
            print(f"Error: Expected JSON array in {index_file_path}")
            return 0
    except FileNotFoundError:
        print(f"Error: Manifest not found at {index_file_path}")
        return 0
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {index_file_path}: {e}")
        return 0

    created = 0
    for entry in manifest:
        filename = entry.get("filename")
        if not filename:
            print("Warning: entry missing 'filename'; skipping.")
            continue
        path = Path(gif_dir) / filename
        if path.exists():
            print(f"Skipping (exists): {filename}")
            continue
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            if write_minimal:
                with open(path, 'wb') as out:
                    out.write(MINIMAL_GIF)
            else:
                path.touch(exist_ok=True)
            created += 1
            print(f"Created placeholder: {filename}")
        except Exception as e:
            print(f"Failed to create {filename}: {e}")

    print(f"Finished: created {created} placeholder(s).")
    return created

if __name__ == "__main__":
    generate_gif_placeholders()
