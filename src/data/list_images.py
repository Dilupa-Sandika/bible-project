import json
import os

# Files
VOTD_FILE = 'votd_data.json'
KJV_FILE = 'en_kjv.json'
OUTPUT_FILE = '../../required_images.txt' # Root folder එකේ හැදෙන්නේ

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        exit()

def get_filename(verse_data, lang, kjv_bible):
    # 1. Abbreviation එක ගන්නවා
    abbrev = verse_data.get('abbrev')
    
    # Fix known mismatches
    abbrev_map = {"jn": "jo", "jas": "jm", "php": "ph", "1th": "1ts", "1ti": "1tm", "jud": "jd", "sal": "ps"}
    if abbrev in abbrev_map:
        abbrev = abbrev_map[abbrev]

    # 2. English Book Name හොයාගන්නවා
    book_obj = next((b for b in kjv_bible if b['abbrev'] == abbrev), None)
    if not book_obj:
        return f"ERROR_BOOK_NOT_FOUND_{abbrev}"

    book_name = book_obj['name'].lower().replace(" ", "-")

    # 3. Numbers හදාගන්නවා
    # Ex: "1 Corinthians 13:4-5" -> "13:4-5" -> "13-4-5"
    ref_parts = verse_data['ref'].split(' ')
    chapter_verse = ref_parts[-1]
    numbers_slug = chapter_verse.replace(':', '-')

    # 4. Filename
    filename = f"{book_name}-{numbers_slug}"
    
    if lang == 'es':
        filename += "-es"
    
    return filename + ".png"

def main():
    print("Loading Data...")
    votd_data = load_json(VOTD_FILE)
    kjv_bible = load_json(KJV_FILE)

    print("Generating Image List with Text...")
    
    lines = []
    
    # --- English Images ---
    lines.append("=== ENGLISH IMAGES ===")
    for verse in votd_data['en']:
        fname = get_filename(verse, 'en', kjv_bible)
        # Format: Filename | Reference | Text
        lines.append(f"{fname} | {verse['ref']} | {verse['text']}")

    # --- Spanish Images ---
    lines.append("\n=== SPANISH IMAGES ===")
    for verse in votd_data['es']:
        fname = get_filename(verse, 'es', kjv_bible)
        # Format: Filename | Reference | Text
        lines.append(f"{fname} | {verse['ref']} | {verse['text']}")

    # Save to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"Done! Check 'required_images.txt' in your main folder.")
    print(f"Format: Filename | Reference | Verse Text")

if __name__ == "__main__":
    main()