import json
import re
import os

# ෆයිල් නම්
INPUT_TEXT_FILE = '../../raw_topics.txt'
KJV_FILE = 'en_kjv.json'
RVR_FILE = 'es_rvr.json'
OUTPUT_FILE = 'topics_db.json'

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        exit()

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
    print("Loading Bible Data...")
    en_bible = load_json(KJV_FILE)
    es_bible = load_json(RVR_FILE)
    
    # Book Map (Standard Name -> Abbreviation)
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

    print("Processing Topics...")
    try:
        with open(INPUT_TEXT_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        print("Error: Create 'raw_topics.txt' in root folder first.")
        exit()

    topics_dict = {}

    for line in lines:
        if "|" not in line: continue
        parts = line.strip().split('|')
        if len(parts) < 2: continue
        
        topic_name = parts[0].strip()
        reference = parts[1].strip()
        topic_id = topic_name.lower().replace(" ", "-")
        
        if topic_id not in topics_dict:
            topics_dict[topic_id] = {
                "id": topic_id,
                "title_en": topic_name,
                "title_es": topic_name, # Manual translate needed later
                "image": f"/images/themes/{topic_id}.jpg",
                "seo": {
                    "en": { "title": f"Verses about {topic_name}", "description": f"Bible verses on {topic_name}", "alt_text": f"{topic_name} bible verse" },
                    "es": { "title": f"Versículos sobre {topic_name}", "description": f"Versículos bíblicos sobre {topic_name}", "alt_text": f"Versículo de {topic_name}" }
                },
                "verses": { "en": [], "es": [] }
            }
            
        match = re.match(r"(.+?)\s+(\d+):(\d+(?:-\d+)?)", reference)
        if match:
            book_str = match.group(1).strip().lower()
            chapter = int(match.group(2))
            verse_num = match.group(3)
            abbrev = book_map.get(book_str)
            
            if abbrev:
                text_en = get_verse_text(en_bible, abbrev, chapter, verse_num)
                text_es = get_verse_text(es_bible, abbrev, chapter, verse_num)
                
                if text_en and text_es:
                    topics_dict[topic_id]['verses']['en'].append({
                        "ref": reference, "text": text_en, "book": abbrev, "chapter": chapter, "verse": verse_num
                    })
                    topics_dict[topic_id]['verses']['es'].append({
                        "ref": reference, "text": text_es, "book": abbrev, "chapter": chapter, "verse": verse_num
                    })

    # Save
    final_list = list(topics_dict.values())
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)

    print(f"✅ Done! Created {len(final_list)} topics in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()