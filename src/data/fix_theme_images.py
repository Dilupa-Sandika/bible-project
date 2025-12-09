import json
import os

FILE_PATH = 'topics_db.json'

def fix_images():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)

        count = 0
        for topic in data:
            # ID එකට ගැලපෙන්න Image Name එක වෙනස් කරනවා
            new_image = f"/images/themes/{topic['id']}.jpg"
            
            if topic['image'] != new_image:
                topic['image'] = new_image
                count += 1

        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Fixed {count} image paths to match new Topic IDs.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_images()