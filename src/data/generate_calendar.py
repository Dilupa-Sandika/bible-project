import json
import re
import random
import sys
import os
from datetime import date, timedelta

# --- Configuration ---
INPUT_EN = 'en_kjv.json'
INPUT_ES = 'es_rvr.json'
# verse_pool.txt තියෙන්නේ Root folder එකේ නම් (src/data එකට පිටින්), අපි පියවර 2ක් පස්සට යන්න ඕන.
POOL_FILE = '../../verse_pool.txt' 

# --- Translation Maps ---
THEME_MAP = {
    "Faith": "Fe", "Love": "Amor", "Hope": "Esperanza", "Peace": "Paz",
    "Strength": "Fortaleza", "Grace": "Gracia", "Trust": "Confianza",
    "Wisdom": "Sabiduría", "Comfort": "Consuelo", "Courage": "Valentía",
    "Forgiveness": "Perdón", "Joy": "Gozo", "Prayer": "Oración",
    "Salvation": "Salvación", "Humility": "Humildad", "Light": "Luz",
    "Guidance": "Guía", "Patience": "Paciencia", "Giving": "Dar",
    "New Beginnings": "Nuevos Comienzos", "Justice": "Justicia",
    "Blessing": "Bendición", "Triumph": "Triunfo", "Sacrifice": "Sacrificio",
    "Resurrection": "Resurrección", "Motherhood": "Maternidad",
    "Holy Spirit": "Espíritu Santo", "Fatherhood": "Paternidad",
    "Freedom": "Libertad", "Honor": "Honor", "Gratitude": "Gratitud",
    "Messiah": "Mesías", "Reflection": "Reflexión", "Healing": "Sanidad",
    "Protection": "Protección", "Creation": "Creación", "Obedience": "Obediencia",
    "Rest": "Descanso", "Promises": "Promesas", "Truth": "Verdad",
    "Friendship": "Amistad", "Family": "Familia", "Work": "Trabajo",
    "Worship": "Adoración", "Kindness": "Bondad", "Scripture": "Escritura",
    "Mindset": "Mentalidad", "Provision": "Provisión", "Fruit": "Fruto",
    "Transformation": "Transformación", "Mission": "Misión", "Life": "Vida",
    "Priorities": "Prioridades", "Invitation": "Invitación"
}

# --- Date Calculation Logic ---

def calculate_easter(year):
    """Calculates Western Easter Date."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def get_nth_weekday_of_month(year, month, weekday, n):
    count = 0
    d = date(year, month, 1)
    while d.month == month:
        if d.weekday() == weekday:
            count += 1
            if count == n:
                return d
        d += timedelta(days=1)
    return None

def get_last_weekday_of_month(year, month, weekday):
    d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    while d.month == month:
        if d.weekday() == weekday:
            return d
        d -= timedelta(days=1)
    return None

def get_special_days(year):
    easter = calculate_easter(year)
    good_friday = easter - timedelta(days=2)
    palm_sunday = easter - timedelta(days=7)
    pentecost = easter + timedelta(days=49)
    
    thanksgiving = get_nth_weekday_of_month(year, 11, 3, 4) 
    mothers_day = get_nth_weekday_of_month(year, 5, 6, 2)   
    fathers_day = get_nth_weekday_of_month(year, 6, 6, 3)   
    mlk_day = get_nth_weekday_of_month(year, 1, 0, 3)       
    memorial_day = get_last_weekday_of_month(year, 5, 0)    
    
    specials = {
        "1-1":   {"ref": "Isaiah 43:19", "theme": "New Beginnings"},
        "2-14":  {"ref": "1 Corinthians 13:4-7", "theme": "Love"},
        "3-17":  {"ref": "Psalm 5:12", "theme": "Blessing"},
        "7-4":   {"ref": "Galatians 5:1", "theme": "Freedom"},
        "10-31": {"ref": "2 Timothy 1:7", "theme": "Courage"},
        "11-11": {"ref": "Psalm 33:12", "theme": "Honor"},
        "12-24": {"ref": "Luke 2:10-11", "theme": "Joy"},
        "12-25": {"ref": "Isaiah 9:6", "theme": "Messiah"},
        "12-31": {"ref": "Psalm 90:12", "theme": "Reflection"},
        
        f"{easter.month}-{easter.day}": {"ref": "Matthew 28:6", "theme": "Resurrection"},
        f"{good_friday.month}-{good_friday.day}": {"ref": "Isaiah 53:5", "theme": "Sacrifice"},
        f"{palm_sunday.month}-{palm_sunday.day}": {"ref": "John 12:13", "theme": "Triumph"},
        f"{pentecost.month}-{pentecost.day}": {"ref": "Acts 2:4", "theme": "Holy Spirit"},
        f"{thanksgiving.month}-{thanksgiving.day}": {"ref": "Psalm 107:1", "theme": "Gratitude"},
        f"{mothers_day.month}-{mothers_day.day}": {"ref": "Proverbs 31:28", "theme": "Motherhood"},
        f"{fathers_day.month}-{fathers_day.day}": {"ref": "Proverbs 20:7", "theme": "Fatherhood"},
        f"{mlk_day.month}-{mlk_day.day}": {"ref": "Amos 5:24", "theme": "Justice"},
        f"{memorial_day.month}-{memorial_day.day}": {"ref": "John 15:13", "theme": "Sacrifice"},
    }
    return specials

# --- Bible Data Helpers ---

def load_json(filepath):
    try:
        # HERE IS THE FIX: utf-8-sig
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON {filepath}: {e}")
        sys.exit(1)

def load_verse_pool(filepath):
    try:
        # HERE IS THE FIX: utf-8-sig
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        pool = []
        for line in lines:
            if "|" in line:
                pool.append(line.strip().split(" | "))
        return pool
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        print(f"Please make sure 'verse_pool.txt' is in the ROOT folder.")
        sys.exit(1)

def build_book_map(bible_data):
    mapping = {}
    for book in bible_data:
        name = book['name'].lower()
        abbrev = book['abbrev']
        mapping[name] = abbrev
        if "song of" in name:
            mapping["song of solomon"] = abbrev
            mapping["song of songs"] = abbrev
        if "psalm" in name:
             mapping["psalm"] = abbrev
             mapping["psalms"] = abbrev
    return mapping

def build_spanish_name_map(es_data):
    mapping = {}
    for book in es_data:
        if 'name' in book:
            mapping[book['abbrev']] = book['name']
    return mapping

def parse_reference(ref_str, book_map):
    match = re.match(r"^(\d?\s?[A-Za-z ]+?)\s+(\d+):(\d+)(-(\d+))?$", ref_str)
    if not match: return None
    
    book_name = match.group(1).strip().lower()
    chapter = int(match.group(2))
    start_verse = int(match.group(3))
    end_verse = match.group(5)
    
    verses = list(range(start_verse, int(end_verse) + 1)) if end_verse else [start_verse]
    
    abbr = book_map.get(book_name)
    return abbr, chapter, verses

def get_verse_text(bible_data, abbr, chapter, verses):
    for book in bible_data:
        if book['abbrev'] == abbr:
            if chapter > len(book['chapters']): return "Chapter not found."
            chap_text = book['chapters'][chapter - 1]
            text_parts = []
            for v_num in verses:
                if v_num <= len(chap_text): 
                    text_parts.append(chap_text[v_num - 1])
            return " ".join(text_parts)
    return "Book not found."

def reconstruct_ref_es(spanish_name, chapter, verses):
    if len(verses) > 1:
        is_continuous = all(verses[i] == verses[i-1] + 1 for i in range(1, len(verses)))
        v_str = f"{verses[0]}-{verses[-1]}" if is_continuous else ",".join(map(str, verses))
    else:
        v_str = str(verses[0])
    return f"{spanish_name} {chapter}:{v_str}"

def get_months_map():
    return {1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
            7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec"}

# --- Main ---

def main():
    try:
        input_year = input("Enter the year to generate (e.g., 2026): ").strip()
        if not input_year:
            year = 2026 
        else:
            year = int(input_year)
    except ValueError:
        print("Invalid year. Defaulting to 2026.")
        year = 2026

    output_file = f'daily_verses_{year}.json'
    print(f"Generating for {year}...")

    en_bible = load_json(INPUT_EN)
    es_bible = load_json(INPUT_ES)
    verse_pool_raw = load_verse_pool(POOL_FILE)
    
    if not verse_pool_raw:
        print("Error: Verse pool is empty!")
        sys.exit(1)

    book_map_en = build_book_map(en_bible)
    spanish_name_map = build_spanish_name_map(es_bible)
    
    special_days = get_special_days(year)

    general_pool = verse_pool_raw.copy()
    random.shuffle(general_pool)

    final_output = {"en": [], "es": []}
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    delta = timedelta(days=1)
    current_date = start_date
    months_map = get_months_map()
    used_verses = set()

    while current_date <= end_date:
        date_id = f"{current_date.month}-{current_date.day}"
        
        if date_id in special_days:
            entry = special_days[date_id]
            ref_str = entry['ref']
            theme_en = entry['theme']
        else:
            attempts = 0
            while True:
                if not general_pool:
                    general_pool = verse_pool_raw.copy()
                    random.shuffle(general_pool)
                
                ref_str, theme_en = general_pool.pop()
                
                if ref_str not in used_verses or attempts > 100:
                    used_verses.add(ref_str)
                    break
                attempts += 1
        
        parsed = parse_reference(ref_str, book_map_en)
        if not parsed:
            print(f"Warning: Could not parse {ref_str}. Skipping.")
            current_date += delta
            continue
            
        abbr, chapter, verses = parsed
        
        text_en = get_verse_text(en_bible, abbr, chapter, verses)
        text_es = get_verse_text(es_bible, abbr, chapter, verses)
        
        theme_es = THEME_MAP.get(theme_en, theme_en)
        spanish_book_name = spanish_name_map.get(abbr, "Unknown")
        ref_es = reconstruct_ref_es(spanish_book_name, chapter, verses)
        
        # Image Filename Logic (Updated to match Astro)
        en_book_obj = next((b for b in en_bible if b['abbrev'] == abbr), None)
        en_book_name_safe = en_book_obj['name'].lower().replace(" ", "-") if en_book_obj else "unknown"
        
        v_str = f"{verses[0]}-{verses[-1]}" if len(verses) > 1 and verses[-1] == verses[0] + len(verses) -1 else str(verses[0])
        v_str_clean = v_str.replace(":", "-")
        
        image_filename_en = f"{en_book_name_safe}-{chapter}-{v_str_clean}.png"
        image_filename_es = f"{en_book_name_safe}-{chapter}-{v_str_clean}-es.png"

        final_output["en"].append({
            "dateId": date_id,
            "theme": theme_en,
            "ref": ref_str,
            "text": text_en,
            "abbrev": abbr,
            "chapter": chapter,
            "image": f"/images/verses/{image_filename_en}"
        })
        
        final_output["es"].append({
            "dateId": date_id,
            "theme": theme_es,
            "ref": ref_es,
            "text": text_es,
            "abbrev": abbr,
            "chapter": chapter,
            "image": f"/images/verses/{image_filename_es}"
        })
        
        current_date += delta

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    print(f"Success! Created {output_file} with {len(final_output['en'])} entries.")

if __name__ == "__main__":
    main()