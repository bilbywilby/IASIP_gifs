# generate_placeholders.py
#!/usr/bin/env python3
"""
Generates placeholder GIF files in the 'gifs' directory for entries found in 
the manifest file (gifs/index.json) that do not yet exist.

This ensures that the repository contains all files listed in the index, 
allowing continuous integration/deployment (CI/CD) or GitHub Pages to track 
the file paths even if the full GIF content is added later.
"""
import json
import sys
import argparse
from typing import Any, Dict, List
from pathlib import Path

# --- Constants ---

# Minimal valid 1x1 transparent GIF (GIF89a)
# This is used as the default placeholder content
MINIMAL_GIF = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'


def _load_manifest(path: Path) -> List[Dict[str, Any]]:
    """Loads and validates the GIF manifest JSON file."""
    print(f"Loading manifest from {path}...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
            
        if not isinstance(manifest, list):
            print(f"Error: Expected JSON array (list) in {path}")
            sys.exit(1)
            
        return manifest
        
    except FileNotFoundError:
        print(f"Error: Manifest file not found at {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {path}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during manifest loading: {e}")
        sys.exit(1)


class PlaceholderGenerator:
    """
    Manages the creation of placeholder GIF files based on a manifest.
    """
    def __init__(self, gif_dir: Path, write_minimal: bool):
        """
        Initializes the generator.

        Args:
            gif_dir: The directory where GIFs should be placed.
            write_minimal: If True, writes the MINIMAL_GIF bytes; if False,
                           it only touches (creates empty) the file.
        """
        self.gif_dir = gif_dir
        self.write_minimal = write_minimal
        # Ensure the output directory exists
        self.gif_dir.mkdir(parents=True, exist_ok=True)
        print(f"GIF directory set to: {self.gif_dir}")

    def _write_placeholder(self, file_path: Path) -> None:
        """Writes the placeholder file content."""
        try:
            if self.write_minimal:
                with open(file_path, 'wb') as out:
                    out.write(MINIMAL_GIF)
            else:
                # 'touch' equivalent: create empty file if it doesn't exist
                file_path.touch(exist_ok=True)
        except Exception as e:
            print(f"Failed to create placeholder at {file_path}: {e}")
            raise

    def generate(self, manifest_entries: List[Dict[str, Any]]) -> int:
        """
        Iterates through manifest entries and creates missing placeholder files.
        
        Returns:
            The count of new files created.
        """
        print("\n--- Starting GIF Placeholder Generation ---")
        created_count = 0
        
        for entry in manifest_entries:
            filename = entry.get("filename")
            
            if not filename or not filename.endswith('.gif'):
                print(f"Warning: Entry missing a valid 'filename'; skipping entry: {entry}")
                continue
                
            path = self.gif_dir / filename
            
            if path.exists():
                # print(f"Skipping (exists): {filename}") # Verbose logging removed for cleaner output
                continue

            try:
                self._write_placeholder(path)
                created_count += 1
                print(f"Created placeholder: {filename}")
            except Exception:
                # Error already printed in _write_placeholder, just continue
                continue

        print(f"\nFinished: Created {created_count} new placeholder file(s).")
        return created_count


def main():
    """Parses arguments and orchestrates the placeholder generation process."""
    parser = argparse.ArgumentParser(
        description="Generate placeholder GIF files for manifest entries."
    )
    parser.add_argument(
        '--index-path',
        type=Path,
        default=Path("gifs/index.json"),
        help="Path to the GIF manifest file (default: gifs/index.json)"
    )
    parser.add_argument(
        '--gif-dir',
        type=Path,
        default=Path("gifs"),
        help="Directory to place the GIF files (default: gifs)"
    )
    parser.add_argument(
        '--touch',
        action='store_true',
        help="If set, only create empty files (touch) instead of writing the minimal GIF bytes."
    )
    
    args = parser.parse_args()
    
    # 1. Load the manifest data
    manifest_data = _load_manifest(args.index_path)
    
    # 2. Initialize the generator
    generator = PlaceholderGenerator(
        gif_dir=args.gif_dir,
        write_minimal=not args.touch
    )
    
    # 3. Execute generation
    generator.generate(manifest_data)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
