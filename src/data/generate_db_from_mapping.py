import json
import re
import os

# Files
INPUT_FILE = '../../mappings.txt'
KJV_FILE = 'en_kjv.json'
RVR_FILE = 'es_rvr.json'
OUTPUT_FILE = 'topics_db.json'

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

# Book Mapping
book_map = {
    "genesis": "gn", "exodus": "ex", "leviticus": "lv", "numbers": "nm", "deuteronomy": "dt",
    "joshua": "js", "judges": "jud", "ruth": "rt", "1 samuel": "1sm", "2 samuel": "2sm",
    "1 kings": "1kgs", "2 kings": "2kgs", "1 chronicles": "1ch", "2 chronicles": "2ch",
    "ezra": "ezr", "nehemiah": "ne", "esther": "et", "job": "job", "psalms": "ps", "psalm": "ps",
    "proverbs": "prv", "ecclesiastes": "ec", "song of solomon": "so", "isaiah": "is",
    "jeremiah": "jr", "lamentations": "lm", "ezekiel": "ez", "daniel": "dn", "hosea": "ho",
    "joel": "jl", "amos": "am", "obadiah": "ob", "jonah": "jn", "micah": "mi", "nahum": "na",
    "habakkuk": "hk", "zephaniah": "zp", "haggai": "hg", "zechariah": "zc", "malachi": "ml",
    "matthew": "mt", "mark": "mk", "luke": "lk", "john": "jo", "acts": "act", "romans": "rm",
    "1 corinthians": "1co", "2 corinthians": "2co", "galatians": "gl", "ephesians": "eph",
    "philippians": "ph", "colossians": "cl", "1 thessalonians": "1ts", "2 thessalonians": "2ts",
    "1 timothy": "1tm", "2 timothy": "2tm", "titus": "tt", "philemon": "phm", "hebrews": "hb",
    "james": "jm", "1 peter": "1pe", "2 peter": "2pe", "1 john": "1jo", "2 john": "2jo",
    "3 john": "3jo", "jude": "jd", "revelation": "re"
}

def get_verse_text(bible_data, abbrev, chapter, verse_range):
    book = next((b for b in bible_data if b['abbrev'] == abbrev), None)
    if not book: return None
    try:
        chap_text = book['chapters'][chapter - 1]
        if "-" in str(verse_range):
            start, end = map(int, str(verse_range).split("-"))
            verses = []
            for v in range(start, end + 1):
                if v <= len(chap_text): verses.append(chap_text[v-1])
            return " ".join(verses)
        else:
            v = int(verse_range)
            return chap_text[v-1] if v <= len(chap_text) else None
    except: return None

def main():
    print("Loading Bibles...")
    en_bible = load_json(KJV_FILE)
    es_bible = load_json(RVR_FILE)
    
    print("Reading Mappings...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: mappings.txt not found in root folder.")
        exit()

    # Dictionary to group verses by topic
    # Key: topic_id, Value: Topic Object
    topics_dict = {}

    for line in lines:
        if " - " not in line: continue
        
        # Split Reference and Themes
        # Example: "Acts 1:10-11" - "Ascension, Second coming"
        parts = line.strip().split(' - ')
        if len(parts) < 2: continue
        
        ref_str = parts[0].strip()
        themes_str = parts[1].strip()
        
        # Clean Themes List (remove empty, strip spaces)
        themes = [t.strip() for t in themes_str.split(',') if t.strip()]
        
        # Parse Reference
        match = re.match(r"(.+?)\s+(\d+):(\d+(?:-\d+)?)", ref_str)
        if not match:
            print(f"Skipping invalid reference: {ref_str}")
            continue
            
        book_name = match.group(1).strip().lower()
        chapter = int(match.group(2))
        verse_num = match.group(3)
        
        abbrev = book_map.get(book_name)
        if not abbrev:
            print(f"Book not found: {book_name}")
            continue
            
        # Get Texts
        text_en = get_verse_text(en_bible, abbrev, chapter, verse_num)
        text_es = get_verse_text(es_bible, abbrev, chapter, verse_num)
        
        if not text_en or not text_es:
            print(f"Text missing for {ref_str}")
            continue

        # Add to each Topic
        for theme in themes:
            topic_id = theme.lower().replace(" ", "-")
            
            # Initialize Topic if new
            if topic_id not in topics_dict:
                topics_dict[topic_id] = {
                    "id": topic_id,
                    "title_en": theme,
                    "title_es": theme, # Manual translation needed later
                    "image": f"/images/themes/{topic_id}.jpg",
                    "seo": {
                        "en": {
                            "title": f"Bible Verses about {theme}",
                            "description": f"Bible verses on {theme}",
                            "alt_text": f"{theme} bible verse"
                        },
                        "es": {
                            "title": f"Versículos sobre {theme}",
                            "description": f"Versículos sobre {theme}",
                            "alt_text": f"Versículo de {theme}"
                        }
                    },
                    "verses": { "en": [], "es": [] }
                }
            
            # Add Verse to Topic (Avoid duplicates if existing)
            exists = any(v['ref'] == ref_str for v in topics_dict[topic_id]['verses']['en'])
            if not exists:
                topics_dict[topic_id]['verses']['en'].append({
                    "ref": ref_str, "text": text_en, "book": abbrev, "chapter": chapter, "verse": verse_num
                })
                topics_dict[topic_id]['verses']['es'].append({
                    "ref": ref_str, "text": text_es, "book": abbrev, "chapter": chapter, "verse": verse_num
                })

    # Convert to List and Save
    final_list = list(topics_dict.values())
    # Sort by title
    final_list.sort(key=lambda x: x['title_en'])
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)

    print(f"✅ Success! Generated {len(final_list)} topics in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()