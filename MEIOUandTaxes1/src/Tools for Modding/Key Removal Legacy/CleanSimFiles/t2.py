# To use this script:
# 1. Place all files to be processed in the 'input' directory. 
#    What files? The sim files: 00-POP_Init-0.txt, 00-POP_Init-1.txt, etc.
# 2. Run the script. Processed files will be saved in the 'output' directory.
# 3. Copy the result back to your mod folder.

import os

def process_pop_file(text: str):
    txt = text
    # Simple replacements
    txt = txt.replace('_v=', 'set_variable=')
    txt = txt.replace('{v=', '{which=')
    txt = txt.replace(' n=', ' value=')
    txt = txt.replace('} _pf={f=', ' set_province_flag=')
    txt = txt.replace('_pf={f=', '{set_province_flag=')

    # Inline set_province_flag
    prev = 0
    while True:
        start = txt.find('{set_province_flag=', prev)
        if start != -1:
            # print(f'  → Found province flag at {start / len(txt):.2%}')
            end = txt.find('}', start)
            if end == -1:
                break
            block = txt[start:end + 1]
            txt = txt.replace(block, block[1:-1])
            prev = start + len(block) - 2
        else:
            break

    txt = txt.replace('} _cf={f=', ' set_country_flag=')
    txt = txt.replace('_cf={f=', '{set_country_flag=')

    # Inline set_country_flag
    prev = 0
    while True:
        start = txt.find('{set_country_flag=', prev)
        if start != -1:
            # print(f'  → Found country flag at {start / len(txt):.2%}')
            end = txt.find('}', start)
            if end == -1:
                break
            block = txt[start:end + 1]
            txt = txt.replace(block, block[1:-1])
            prev = start + len(block) - 2
        else:
            break

    # Modifiers
    txt = txt.replace('_pm={m=', 'add_province_modifier={duration=-1 name=')
    txt = txt.replace('_pmh={m=', 'add_province_modifier={duration=-1 hidden=yes name=')
    txt = txt.replace('_ppm={m=', 'add_permanent_province_modifier={duration=-1 name=')
    txt = txt.replace('_ppmh={m=', 'add_permanent_province_modifier={duration=-1 hidden=yes name=')
    txt = txt.replace('_cm={m=', 'add_country_modifier={duration=-1 name=')
    txt = txt.replace('_cmh={m=', 'add_country_modifier={duration=-1 hidden=yes name=')
    
    return txt

def process_directory(input_dir, output_dir):
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

            # Read, replace, and write
            replaced_text = process_pop_file(text)
            
            with open(output_path, 'w', encoding='utf-8') as outfile:
                outfile.write(replaced_text)

            print(f"✅ Processed: {relative_path}")


if __name__ == "__main__":
    print("Starting POP file processing...\n")

    input_dir = "input"
    output_dir = "output"

    process_directory(input_dir, output_dir)
    
    print("All done ✅")