import json
import os
import sys

# Files (Make sure these exist in src/data/)
VOTD_FILE = 'votd_data.json'
TOPICS_FILE = 'topics_db.json'
KJV_FILE = 'en_kjv.json'
OUTPUT_FILE = '../../required_images.txt'

# Console Colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def load_json(filepath):
    if not os.path.exists(filepath):
        print(f"{RED}Error: File not found: {filepath}{RESET}")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"{RED}Error: Could not decode JSON in {filepath}: {e}{RESET}")
        return None

# Mapping for Bible book abbreviations
abbrev_map = {"jn": "jo", "jas": "jm", "php": "ph", "1th": "1ts", "1ti": "1tm", "jud": "jd", "sal": "ps"}

def get_verse_filename(ref, book_abbrev, lang, kjv_bible):
    # 1. Fix Abbreviation
    if book_abbrev in abbrev_map: 
        book_abbrev = abbrev_map[book_abbrev]

    # 2. Find Book Name from KJV Bible
    book_obj = next((b for b in kjv_bible if b['abbrev'] == book_abbrev), None)
    
    if not book_obj: 
        # If book not found, return None to skip or handle error
        return None

    book_slug = book_obj['name'].lower().replace(" ", "-")

    # 3. Get Numbers (3:16 or 13:4-5)
    try:
        ref_parts = ref.split(' ')
        chapter_verse = ref_parts[-1]
        numbers_slug = chapter_verse.replace(':', '-')
    except:
        return None

    # 4. Filename Construction
    filename = f"{book_slug}-{numbers_slug}"
    if lang == 'es': 
        filename += "-es"
    
    return filename + ".png"

def main():
    print("--- Starting Image List Generation ---")

    # 1. Load Data
    votd_data = load_json(VOTD_FILE)
    topics_data = load_json(TOPICS_FILE)
    kjv_bible = load_json(KJV_FILE)

    if not kjv_bible:
        print(f"{RED}CRITICAL ERROR: en_kjv.json is missing or invalid.{RESET}")
        return

    lines = []
    unique_images = set()

    # --- 2. PROCESS THEME COVERS ---
    theme_count = 0
    if topics_data:
        lines.append("=== THEME COVERS (16:9 or 1:1) ===")
        lines.append("Save to: public/images/themes/")
        lines.append("-" * 50)
        
        for topic in topics_data:
            fname = f"{topic['id']}.jpg"
            lines.append(f"[ ] {fname}  |  Title: {topic['title_en']}")
            theme_count += 1
        lines.append("\n")
        print(f"✅ Loaded {theme_count} Theme Covers.")
    else:
        print(f"{RED}Warning: topics_db.json not loaded or empty.{RESET}")

    # --- 3. PROCESS VERSE IMAGES ---
    lines.append("=== VERSE IMAGES (English & Spanish) ===")
    lines.append("Save to: public/images/verses/")
    lines.append("Format: Filename | Reference | Text")
    lines.append("-" * 50)

    verse_img_count = 0
    
    # A. Process Daily Verses (VOTD)
    if votd_data:
        # English
        for item in votd_data.get('en', []):
            fname = get_verse_filename(item['ref'], item['abbrev'], 'en', kjv_bible)
            if fname and fname not in unique_images:
                unique_images.add(fname)
                lines.append(f"{fname} | {item['ref']} | {item['text']}")
                verse_img_count += 1
        
        # Spanish
        for item in votd_data.get('es', []):
            fname = get_verse_filename(item['ref'], item['abbrev'], 'es', kjv_bible)
            if fname and fname not in unique_images:
                unique_images.add(fname)
                lines.append(f"{fname} | {item['ref']} | {item['text']}")
                verse_img_count += 1
        print(f"✅ Processed VOTD Data.")
    else:
        print(f"{RED}Warning: votd_data.json not loaded or empty.{RESET}")

    # B. Process Theme Verses
    if topics_data:
        for topic in topics_data:
            # English
            if 'verses' in topic and 'en' in topic['verses']:
                for v in topic['verses']['en']:
                    abbr = v.get('book') or v.get('abbrev')
                    fname = get_verse_filename(v['ref'], abbr, 'en', kjv_bible)
                    if fname and fname not in unique_images:
                        unique_images.add(fname)
                        lines.append(f"{fname} | {v['ref']} | {v['text']}")
                        verse_img_count += 1
            
            # Spanish
            if 'verses' in topic and 'es' in topic['verses']:
                for v in topic['verses']['es']:
                    abbr = v.get('book') or v.get('abbrev')
                    fname = get_verse_filename(v['ref'], abbr, 'es', kjv_bible)
                    if fname and fname not in unique_images:
                        unique_images.add(fname)
                        lines.append(f"{fname} | {v['ref']} | {v['text']}")
                        verse_img_count += 1
        print(f"✅ Processed Theme Verses.")

    # --- 4. SAVE FILE ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print("-" * 30)
    print(f"{GREEN}SUCCESS!{RESET}")
    print(f"Total Unique Images Required: {len(unique_images) + theme_count}")
    print(f"List saved to: required_images.txt")

if __name__ == "__main__":
    main()