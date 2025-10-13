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
    """Replace exact matches of values in text with their keys."""
    # Build a regex pattern that matches any value as a whole word
    pattern = r'\b(' + '|'.join(re.escape(value) for value in mapping.keys()) + r')\b'
    return re.sub(pattern, lambda m: mapping[m.group(0)], text)


if __name__ == "__main__":
    # Example usage:
    mapping_file = "keys.txt"
    input_file = "input/00-locs.txt"
    output_file = "output/output.txt"

    # Load mapping
    mapping = load_mapping(mapping_file)

    # Read input text
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Replace all exact occurrences
    replaced_text = replace_values_with_keys(text, mapping)

    # Write to output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(replaced_text)

    print("✅ Replacement complete. Output saved to", output_file)
