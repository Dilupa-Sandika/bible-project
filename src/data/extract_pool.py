import json
import os

# Files
TOPICS_FILE = 'topics_db.json'
OUTPUT_FILE = '../../verse_pool.txt' # Root folder එකේ සේව් වෙන්න

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        exit()

def main():
    print("Reading Topics DB...")
    topics = load_json(TOPICS_FILE)
    
    unique_verses = {} # Use dict to avoid duplicates (Ref -> Theme)
    
    count = 0
    for topic in topics:
        theme_name = topic['title_en']
        
        # English Verses
        if 'verses' in topic and 'en' in topic['verses']:
            for v in topic['verses']['en']:
                ref = v['ref']
                # Add to pool if not exists (Keep the first theme found)
                if ref not in unique_verses:
                    unique_verses[ref] = theme_name
                    count += 1

    print(f"Found {count} unique verses in themes.")
    
    # Write to verse_pool.txt
    print(f"Updating {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for ref, theme in unique_verses.items():
            f.write(f"{ref} | {theme}\n")
            
    print("✅ Success! Your verse pool is now huge.")

if __name__ == "__main__":
    main()