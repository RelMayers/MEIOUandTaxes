import os
import shutil
import traceback

def process_pop_file(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    with open(input_path, encoding="utf-8") as f:
        txt = f.read()

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
            print(f'  → Found province flag at {start / len(txt):.2%}')
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
            print(f'  → Found country flag at {start / len(txt):.2%}')
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

    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(txt)

    print(f"✅ Processed: {input_path} → {output_path}")


if __name__ == "__main__":
    print("Starting POP file processing...\n")

    for i in range(5):
        input_file = f'events/00-POP_Init-{i}.txt'
        backup_file = f'events/00-POP_Init-{i}_backup.disabled'
        temp_output = f'events/00-POP_Init-{i}_test.txt'

        # Step 1: Process and create _test.txt
        process_pop_file(input_file, temp_output)

        # Step 2: Backup original (rename to .disabled)
        if os.path.exists(input_file):
            if os.path.exists(backup_file):
                os.remove(backup_file)  # remove old backup if it exists
            shutil.move(input_file, backup_file)
            print(f"🔸 Renamed original to {backup_file}")

        # Step 3: Make the new file active
        shutil.move(temp_output, input_file)
        print(f"✅ Activated processed file: {input_file}\n")

    print("All done ✅")