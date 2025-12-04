import json
import time
from deep_translator import GoogleTranslator

FILE_PATH = 'topics_db.json'

def translate_topics():
    try:
        # Load JSON
        with open(FILE_PATH, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        translator = GoogleTranslator(source='en', target='es')
        print(f"Starting translation for {len(data)} topics...")

        for i, topic in enumerate(data):
            title_en = topic.get('title_en', '')
            current_es = topic.get('title_es', '')

            # Spanish නම, English නමට සමාන නම් හෝ හිස් නම් විතරක් Translate කරන්න
            if title_en and (current_es == title_en or not current_es):
                try:
                    # Translate Title
                    translated_title = translator.translate(title_en)
                    topic['title_es'] = translated_title
                    
                    # Translate SEO details too
                    if 'seo' in topic and 'es' in topic['seo']:
                        topic['seo']['es']['title'] = f"Versículos Bíblicos sobre {translated_title}"
                        topic['seo']['es']['description'] = f"Descubre poderosos versículos bíblicos sobre {translated_title}."
                        topic['seo']['es']['alt_text'] = f"Fondo de versículos bíblicos sobre {translated_title}"

                    print(f"[{i+1}] Translated: {title_en} -> {translated_title}")
                    
                    # පොඩි විරාමයක් (Server එකට කරදරයක් නොවෙන්න)
                    time.sleep(0.2)

                except Exception as e:
                    print(f"Error translating {title_en}: {e}")
            else:
                print(f"[{i+1}] Skipped: {title_en} (Already valid: {current_es})")

        # Save back to JSON
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print("\n✅ Success! topics_db.json updated with Spanish titles.")

    except FileNotFoundError:
        print(f"Error: Could not find {FILE_PATH}")

if __name__ == "__main__":
    translate_topics()