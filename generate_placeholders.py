import os
import json

def generate_gif_placeholders(index_file_path="gifs/index.json", gif_dir="gifs"):
    """
    Reads the index.json file and creates empty placeholder files
    for each GIF listed in the manifest.
    """
    print(f"--- Starting GIF Placeholder Generation ---")

    # 1. Ensure the GIFs directory exists
    if not os.path.exists(gif_dir):
        os.makedirs(gif_dir)
        print(f"Created directory: {gif_dir}/")
    else:
        print(f"Directory already exists: {gif_dir}/")


    # 2. Load the GIF manifest
    try:
        with open(index_file_path, 'r') as f:
            manifest = json.load(f)
        
        if not isinstance(manifest, list):
             print(f"Error: Expected manifest file at {index_file_path} to be a JSON array ([]).")
             return

        print(f"Loaded {len(manifest)} entries from {index_file_path}")
    except FileNotFoundError:
        print(f"Error: Manifest file not found at {index_file_path}. Please ensure it exists.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {index_file_path}. Check for syntax errors.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return


    # 3. Create the placeholder files
    created_count = 0
    for entry in manifest:
        filename = entry.get("filename")
        if not filename:
            print(f"Warning: Entry missing 'filename' key. Skipping.")
            continue

        file_path = os.path.join(gif_dir, filename)

        if not os.path.exists(file_path):
            # Create an empty file with the correct .gif extension.
            try:
                # 'a' mode creates the file if it doesn't exist and closes it immediately.
                with open(file_path, 'a') as temp_f:
                    pass 
                print(f"Created placeholder: {filename}")
                created_count += 1
            except Exception as e:
                print(f"Failed to create file {file_path}: {e}")
        else:
            print(f"Skipping: {filename} already exists.")

    print(f"\nSuccessfully created {created_count} placeholder files.")
    print(f"--- Finished Generation ---")


if __name__ == "__main__":
    generate_gif_placeholders()
