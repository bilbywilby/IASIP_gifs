#!/usr/bin/env python3
import json
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def validate_gif_entry(entry):
    """
    Validate individual GIF entry for required fields and format
    """
    required_fields = ['filename', 'tags', 'description']
    
    # Check for required fields
    for field in required_fields:
        if field not in entry:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate filename format
    if not entry['filename'].endswith('.gif'):
        raise ValueError(f"Invalid filename format: {entry['filename']}")
    
    # Validate tags
    if not entry['tags'] or not isinstance(entry['tags'], list):
        raise ValueError("Tags must be a non-empty list")
    
    # Validate description length
    if len(entry['description']) < 10 or len(entry['description']) > 200:
        raise ValueError("Description must be between 10 and 200 characters")

def generate_placeholders(json_path='gifs/index.json', gifs_dir='gifs'):
    """
    Generate placeholder GIF files for entries in the index
    """
    try:
        # Read the JSON file
        with open(json_path, 'r') as f:
            gif_entries = json.load(f)
        
        # Ensure gifs directory exists
        os.makedirs(gifs_dir, exist_ok=True)
        
        # Track changes
        placeholders_created = 0
        
        # Process each entry
        for entry in gif_entries:
            # Validate the entry
            validate_gif_entry(entry)
            
            filename = entry['filename']
            filepath = os.path.join(gifs_dir, filename)
            
            # Create placeholder if file doesn't exist
            if not os.path.exists(filepath):
                # Create a minimal, valid GIF placeholder
                with open(filepath, 'wb') as placeholder:
                    # Minimal GIF89a header + a single transparent pixel
                    placeholder.write(b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
                
                logger.info(f"Created placeholder for {filename}")
                placeholders_created += 1
        
        # Log summary
        logger.info(f"Placeholder generation complete. {placeholders_created} new placeholders created.")
        
        return placeholders_created > 0
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON format in index file")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during placeholder generation: {e}")
        return False

def main():
    try:
        # Check if placeholders were generated
        if generate_placeholders():
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        logger.error(f"Script failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
