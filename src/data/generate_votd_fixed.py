import json
import random
from datetime import date, timedelta

# --- Configuration ---
INPUT_EN_BIBLE = 'en_kjv.json'
INPUT_ES_BIBLE = 'es_rvr.json'
INPUT_EXISTING_DATA = 'votd_data.json'
OUTPUT_FILE = 'votd_data_final.json'

# --- Helper Data: Book Name Mappings ---
BOOK_MAP = {
    "Genesis": "gn", "Exodus": "ex", "Leviticus": "lv", "Numbers": "nm", "Deuteronomy": "dt",
    "Joshua": "js", "Judges": "jud", "Ruth": "rt", "1 Samuel": "1sm", "2 Samuel": "2sm",
    "1 Kings": "1kgs", "2 Kings": "2kgs", "1 Chronicles": "1ch", "2 Chronicles": "2ch",
    "Ezra": "ezr", "Nehemiah": "ne", "Esther": "et", "Job": "job", "Psalms": "ps", "Psalm": "ps",
    "Proverbs": "prv", "Ecclesiastes": "ec", "Song of Solomon": "so", "Isaiah": "is",
    "Jeremiah": "jr", "Lamentations": "lm", "Ezekiel": "ez", "Daniel": "dn", "Hosea": "ho",
    "Joel": "jl", "Amos": "am", "Obadiah": "ob", "Jonah": "jn", "Micah": "mi", "Nahum": "na",
    "Habakkuk": "hk", "Zephaniah": "zp", "Haggai": "hg", "Zechariah": "zc", "Malachi": "ml",
    "Matthew": "mt", "Mark": "mk", "Luke": "lk", "John": "jo", "Acts": "act", "Romans": "rm",
    "1 Corinthians": "1co", "2 Corinthians": "2co", "Galatians": "gl", "Ephesians": "eph",
    "Philippians": "ph", "Colossians": "cl", "1 Thessalonians": "1ts", "2 Thessalonians": "2ts",
    "1 Timothy": "1tm", "2 Timothy": "2tm", "Titus": "tt", "Philemon": "phm", "Hebrews": "hb",
    "James": "jm", "1 Peter": "1pe", "2 Peter": "2pe", "1 John": "1jo", "2 John": "2jo",
    "3 John": "3jo", "Jude": "jd", "Revelation": "re"
}

# --- Helper Data: Extra Verses to ensure 366 days ---
EXTRA_VERSES = [
    ("Genesis", 1, "1", "Creation"), ("Psalm", 23, "1", "The Shepherd"),
    ("Jeremiah", 29, "11", "Future Hope"), ("Philippians", 4, "13", "Strength"),
    ("John", 3, "16", "God's Love"), ("Romans", 8, "28", "Purpose"),
    ("Isaiah", 41, "10", "Fear Not"), ("Psalm", 46, "1", "Refuge"),
    ("Galatians", 5, "22-23", "Fruit of Spirit"), ("Hebrews", 11, "1", "Faith"),
    ("2 Timothy", 1, "7", "Power & Love"), ("Proverbs", 3, "5-6", "Trust"),
    ("Isaiah", 40, "31", "Renewed Strength"), ("Joshua", 1, "9", "Courage"),
    ("Matthew", 11, "28", "Rest"), ("Romans", 12, "2", "Transformation"),
    ("Philippians", 4, "6-7", "Anxiety"), ("Ephesians", 2, "8-9", "Grace"),
    ("Lamentations", 3, "22-23", "Faithfulness"), ("John", 14, "6", "The Way"),
    ("Psalm", 119, "105", "Guidance"), ("Colossians", 3, "23", "Work"),
    ("Matthew", 28, "19-20", "Great Commission"), ("Isaiah", 9, "6", "Prophecy"),
    ("Luke", 2, "11", "Christmas"), ("Matthew", 6, "33", "Kingdom First"),
    ("1 Peter", 5, "7", "Casting Cares"), ("Micah", 6, "8", "Justice"),
    ("Romans", 3, "23", "Sin"), ("Romans", 6, "23", "Eternal Life"),
    ("1 John", 1, "9", "Confession"), ("Revelation", 3, "20", "Invitation"),
    ("Psalm", 19, "14", "Words of Mouth"), ("1 Corinthians", 10, "13", "Temptation"),
    ("Zephaniah", 3, "17", "God is with You"), ("2 Corinthians", 5, "17", "New Creation"),
    ("1 Thessalonians", 5, "16-18", "Rejoice"), ("Hebrews", 4, "12", "Word of God"),
    ("Psalm", 34, "8", "Taste and See"), ("James", 1, "2-3", "Trials"),
    ("Psalm", 27, "1", "Light and Salvation"), ("1 John", 4, "19", "Love"),
    ("Proverbs", 17, "17", "Friendship"), ("Psalm", 118, "24", "The Day"),
    ("John", 10, "10", "Abundant Life"), ("Romans", 8, "31", "God for Us"),
    ("Isaiah", 26, "3", "Perfect Peace"), ("Psalm", 37, "4", "Desires of Heart"),
    ("Ephesians", 6, "11", "Armor of God"), ("Psalm", 100, "5", "Goodness"),
    ("Matthew", 5, "16", "Light"), ("1 Peter", 2, "9", "Chosen People"),
    ("Deuteronomy", 31, "6", "Courage"), ("John", 16, "33", "Overcoming"),
    ("Psalm", 139, "14", "Fearfully Made"), ("Proverbs", 4, "23", "Heart"),
    ("Isaiah", 43, "2", "Protection"), ("Galatians", 2, "20", "Crucified"),
    ("Psalm", 56, "3", "Trust"), ("1 John", 3, "1", "Children of God"),
    ("Colossians", 3, "14", "Love"), ("Romans", 8, "38-39", "Inseparable"),
    ("Psalm", 51, "10", "Clean Heart"), ("Matthew", 22, "37-39", "Great Commandment"),
    ("Isaiah", 53, "5", "Healing"), ("John", 8, "12", "Light of World"),
    ("Psalm", 103, "12", "Forgiveness"), ("2 Chronicles", 7, "14", "Humility"),
    ("Hebrews", 12, "2", "Fixing Eyes"), ("Psalm", 1, "1-2", "Blessed Man"),
    ("1 Timothy", 6, "12", "Good Fight"), ("Psalm", 91, "1-2", "Refuge"),
    ("James", 4, "7", "Submit to God"), ("1 Peter", 5, "6", "Humble"),
    ("Romans", 1, "16", "Gospel Power"), ("Psalm", 121, "1-2", "Help"),
    ("Proverbs", 18, "10", "Strong Tower"), ("Ephesians", 4, "32", "Kindness"),
    ("Philippians", 1, "6", "Confidence"), ("Psalm", 8, "9", "Majesty"),
    ("John", 15, "5", "The Vine"), ("Romans", 5, "8", "Love Demonstrated"),
    ("Hebrews", 13, "8", "Unchanging"), ("Psalm", 107, "1", "Thanksgiving"),
    ("1 Corinthians", 16, "14", "Do in Love"), ("Psalm", 150, "6", "Praise"),
    ("Matthew", 28, "6", "Resurrection"), ("Luke", 24, "6", "He is Risen"),
    ("Acts", 1, "8", "Power"), ("Romans", 12, "12", "Hope"),
    ("Psalm", 42, "11", "Hope in God"), ("John", 14, "27", "Peace"),
    ("Ecclesiastes", 3, "1", "Seasons"), ("2 Corinthians", 12, "9", "Grace"),
    ("Galatians", 6, "9", "Perseverance"), ("Ephesians", 3, "20", "Abundance"),
    ("Psalm", 34, "18", "Brokenhearted"), ("Matthew", 11, "29", "Yoke"),
    ("Proverbs", 16, "9", "Plans"), ("Isaiah", 55, "8-9", "God's Ways"),
    ("Jeremiah", 33, "3", "Call to Me"), ("Romans", 8, "1", "No Condemnation"),
    ("Psalm", 16, "11", "Joy"), ("1 Corinthians", 15, "57", "Victory"),
    ("Philippians", 2, "3-4", "Humility"), ("Colossians", 3, "2", "Mind Set"),
    ("1 Thessalonians", 5, "11", "Encourage"), ("1 Timothy", 4, "12", "Youth"),
    ("Hebrews", 10, "24-25", "Fellowship"), ("James", 1, "5", "Wisdom"),
    ("1 Peter", 1, "3", "Living Hope"), ("1 John", 4, "7", "Love One Another"),
    ("Revelation", 21, "4", "No More Tears"), ("Psalm", 24, "1", "Earth is Lord's"),
    ("Isaiah", 40, "8", "Word Stands"), ("Luke", 6, "31", "Golden Rule")
]

# --- Functions ---

def load_json(filename):
    """Loads JSON file with utf-8-sig to handle BOM."""
    try:
        # Changed encoding to 'utf-8-sig' to fix the error you saw
        with open(filename, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error reading {filename}: {e}")
        return None

def parse_ref(ref_string):
    """Parses 'John 3:16' into ('John', 3, '16')."""
    try:
        parts = ref_string.rsplit(' ', 1)
        book_name = parts[0]
        chapter_verse = parts[1].split(':')
        chapter = int(chapter_verse[0])
        verse_str = chapter_verse[1]
        return book_name, chapter, verse_str
    except:
        return None, None, None

def get_bible_text(bible_data, book_abbr, chapter, verse_range):
    """Retrieves text for a specific book/chapter/verse(s)."""
    if not book_abbr: return None
    
    # Find the book in the list
    book = next((b for b in bible_data if b['abbrev'] == book_abbr), None)
    if not book:
        return None
    
    try:
        chap_idx = chapter - 1
        # Check if chapter exists
        if chap_idx >= len(book['chapters']):
            return None
            
        verses = book['chapters'][chap_idx]
        
        if '-' in verse_range:
            # Handle ranges like "1-3"
            start_v, end_v = map(int, verse_range.split('-'))
            text_list = []
            for v in range(start_v, end_v + 1):
                if v <= len(verses):
                    text_list.append(verses[v-1])
            return " ".join(text_list)
        else:
            # Handle single verse "16"
            v_idx = int(verse_range) - 1
            if v_idx < len(verses):
                return verses[v_idx]
    except IndexError:
        return None
    except ValueError:
        return None
    return None

def main():
    print("Loading files...")
    en_bible = load_json(INPUT_EN_BIBLE)
    es_bible = load_json(INPUT_ES_BIBLE)
    existing_data = load_json(INPUT_EXISTING_DATA)
    
    if not (en_bible and es_bible and existing_data):
        print("Failed to load one or more files. Check filenames.")
        return

    print("Processing verses...")
    
    # 1. Collect Existing Verses
    # Use a dictionary to avoid duplicates: Key = "RefString"
    verse_pool = {} 
    
    # Check if existing data structure is a dict with 'en' key or a list
    source_list = existing_data.get('en', []) if isinstance(existing_data, dict) else existing_data

    # Add existing items first (to keep them)
    for item in source_list:
        ref = item.get('ref')
        if ref and ref not in verse_pool:
            verse_pool[ref] = {
                'theme': item.get('theme', 'Inspiration'),
                'ref': ref,
                'image': item.get('image', '')
            }

    # 2. Add New/Extra Verses to ensure we cover 366 days
    for b, c, v, t in EXTRA_VERSES:
        ref = f"{b} {c}:{v}"
        if ref not in verse_pool:
             verse_pool[ref] = {
                'theme': t,
                'ref': ref,
                'image': '' 
            }

    # 3. Create list and ensure enough items for 366 days
    unique_refs = list(verse_pool.keys())
    
    # Simple logic: cycle through if we don't have enough distinct verses
    # (Ideally, you would add more to EXTRA_VERSES above)
    final_refs_list = unique_refs[:]
    while len(final_refs_list) < 366:
        final_refs_list += unique_refs[:366-len(final_refs_list)]
    
    # 4. Generate the Final Arrays
    final_en = []
    final_es = []
    
    start_date = date(2024, 1, 1) # Leap year to get 366
    
    for i in range(366):
        current_date = start_date + timedelta(days=i)
        date_id = f"{current_date.month}-{current_date.day}"
        
        ref_key = final_refs_list[i]
        item_data = verse_pool[ref_key]
        
        # Parse Ref
        book_name, chapter, verse = parse_ref(ref_key)
        
        # Determine Abbreviation
        abbrev = BOOK_MAP.get(book_name)
        if not abbrev:
            # Try approximate matching if book name varies (e.g. "Psalms" vs "Psalm")
            if book_name == "Psalm": abbrev = "ps"
            elif book_name == "Psalms": abbrev = "ps"
            elif book_name == "Song of Songs": abbrev = "so"
        
        if not abbrev:
            print(f"Skipping {ref_key}: Could not map book name '{book_name}'")
            continue

        # Fetch Text from JSON Bibles
        text_en = get_bible_text(en_bible, abbrev, chapter, verse)
        text_es = get_bible_text(es_bible, abbrev, chapter, verse)
        
        # If we can't find text, try to fallback to existing text if available, or skip
        if not text_en:
            # Attempt to find it in original data if it was there
            original = next((x for x in source_list if x.get('ref') == ref_key), None)
            if original and original.get('text'):
                text_en = original.get('text')
            else:
                text_en = "[Text not found]"

        if not text_es:
            # No Spanish fallback usually in source, so use placeholder
            text_es = "[Texto no encontrado]"

        # English Entry
        final_en.append({
            "dateId": date_id,
            "theme": item_data['theme'],
            "ref": ref_key,
            "text": text_en,
            "abbrev": abbrev,
            "chapter": chapter,
            "image": item_data['image']
        })
        
        # Spanish Entry
        # Logic: use same image filename but add "-es" suffix if image exists
        img_es = ""
        if item_data['image']:
            # e.g. /images/verses/acts-1-8.png -> /images/verses/acts-1-8-es.png
            if "-es.png" not in item_data['image']:
                img_es = item_data['image'].replace(".png", "-es.png")
            else:
                img_es = item_data['image']

        final_es.append({
            "dateId": date_id,
            "theme": item_data['theme'], # You might want to translate themes manually later
            "ref": ref_key, 
            "text": text_es,
            "abbrev": abbrev,
            "chapter": chapter,
            "image": img_es
        })

    # 5. Write to File
    final_output = {
        "en": final_en,
        "es": final_es
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    
    print(f"Success! Created {OUTPUT_FILE} with {len(final_en)} entries.")

if __name__ == "__main__":
    main()