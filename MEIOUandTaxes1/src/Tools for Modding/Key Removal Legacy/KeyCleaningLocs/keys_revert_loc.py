# To use this script:
# 1. Place all files to be processed in the 'input' directory. 
#    What files? The loc files: 00-locs_l_english.yml, 00-locs.txt
# 2. Run the script. Processed files will be saved in the 'output' directory.
# 3. Copy the result back to your mod folder.

import os
import re

def load_mapping(filename):
    """Load key-value pairs from the mapping file into a dictionary."""
    mapping = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                key, value = [part.strip() for part in line.split(':', 1)]
                mapping[value] = key
    return mapping


def replace_values_with_keys(text, mapping):
    """Replace exact matches of mapping values with their keys."""
    pattern = r'\b(' + '|'.join(re.escape(value) for value in mapping.keys()) + r')\b'
    return re.sub(pattern, lambda m: mapping[m.group(0)], text)


def process_directory(input_dir, output_dir, mapping):
    """Replace all values in all files from input_dir and save results in output_dir."""
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for filename in files:
            input_path = os.path.join(root, filename)
            relative_path = os.path.relpath(input_path, input_dir)
            output_path = os.path.join(output_dir, relative_path)

            # Make sure output subdirectories exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Read, replace, and write
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
                text = infile.read()

            replaced_text = replace_values_with_keys(text, mapping)

            with open(output_path, 'w', encoding='utf-8') as outfile:
                outfile.write(replaced_text)

            print(f"✅ Processed: {relative_path}")


if __name__ == "__main__":
    mapping_file = "keys.txt"
    input_dir = "input"
    output_dir = "output"

    mapping = load_mapping(mapping_file)
    process_directory(input_dir, output_dir, mapping)

    print("\n All files processed. Results saved in:", output_dir)
