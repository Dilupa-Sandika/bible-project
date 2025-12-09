import os
import codecs

# පිරිසිදු කළ යුතු ෆයිල් ලිස්ට් එක
files_to_clean = [
    'en_kjv.json',
    'es_rvr.json',
    '../../verse_pool.txt', # Root folder එකේ තියෙන නිසා
    'topics_db.json'
]

def clean_file(filepath):
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return

    print(f"Cleaning {filepath}...")
    
    try:
        # 1. Read content (Handle BOM automatically)
        with codecs.open(filepath, 'r', 'utf-8-sig') as f:
            content = f.read()
        
        # 2. Write content back as clean UTF-8 (No BOM)
        with codecs.open(filepath, 'w', 'utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully cleaned: {filepath}")
        
    except Exception as e:
        print(f"❌ Error cleaning {filepath}: {e}")

if __name__ == "__main__":
    print("--- Starting File Cleanup ---")
    for file in files_to_clean:
        clean_file(file)
    print("--- Done! Now try running your calendar script. ---")