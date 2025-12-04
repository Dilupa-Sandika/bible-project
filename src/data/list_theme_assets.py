import json
import os

TOPICS_FILE = 'topics_db.json'
KJV_FILE = 'en_kjv.json'
OUTPUT_FILE = '../../theme_image_tasks.txt'

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def get_verse_filename(verse, kjv_bible):
    # Abbreviation Fixer
    abbrev_map = {"jn": "jo", "jas": "jm", "php": "ph", "1th": "1ts", "1ti": "1tm", "jud": "jd", "sal": "ps"}
    abbrev = verse.get('book') # In topics_db it's 'book', not 'abbrev'
    if abbrev in abbrev_map: abbrev = abbrev_map[abbrev]

    # Find Book Name
    book_obj = next((b for b in kjv_bible if b['abbrev'] == abbrev), None)
    if not book_obj: return "ERROR"

    book_slug = book_obj['name'].lower().replace(" ", "-")
    
    # Verse Number Logic (Handling ranges like "4-5")
    # Note: topics_db verse format might be different than votd. 
    # It seems to be just a string "16" or "4-5"
    verse_num = str(verse['verse']).replace(":", "-") 
    
    return f"{book_slug}-{verse['chapter']}-{verse_num}.png"

def main():
    topics = load_json(TOPICS_FILE)
    kjv = load_json(KJV_FILE)
    
    lines = []
    
    # 1. COVER IMAGES
    lines.append("=== PART 1: THEME COVER IMAGES (16:9 or 1:1) ===")
    lines.append("Format: Filename | Theme Title | Description for AI")
    lines.append("-" * 50)
    
    for topic in topics:
        # Theme ID එක පාවිච්චි කරලා නම හදමු
        filename = f"{topic['id']}.jpg"
        desc = topic['seo']['en']['description']
        lines.append(f"{filename} | {topic['title_en']} | {desc}")

    # 2. VERSE IMAGES
    lines.append("\n\n=== PART 2: VERSE IMAGES (16:9) ===")
    lines.append("Format: Filename | Reference | Text")
    lines.append("-" * 50)
    
    unique_verses = set()

    for topic in topics:
        for verse in topic['verses']['en']:
            # Generate filename
            fname = get_verse_filename(verse, kjv)
            
            # Avoid duplicates (Same verse in multiple themes)
            if fname not in unique_verses and fname != "ERROR":
                unique_verses.add(fname)
                ref = f"{verse['book']} {verse['chapter']}:{verse['verse']}"
                lines.append(f"{fname} | {ref} | {verse['text']}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"Success! Image task list saved to: theme_image_tasks.txt")

if __name__ == "__main__":
    main()