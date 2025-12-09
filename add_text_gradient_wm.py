import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# --- සැකසුම් ---
INPUT_DIR = 'raw_images'      
OUTPUT_DIR = 'final_posts_wm'  # Watermark තියෙන ඒවා වෙනම ෆෝල්ඩරයකට දාමු (පටලැවෙන්නේ නැති වෙන්න)
DATA_FILE = 'required_images.txt'

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

# පහළින් අඳුරු විය යුතු ප්‍රමාණය
GRADIENT_HEIGHT = 500  

FONT_PATH = "arialbd.ttf"     
FONT_SIZE_MAIN = 55           
FONT_SIZE_REF = 35 
FONT_SIZE_WM = 25             # Watermark එකේ අකුරු ප්‍රමාණය

TEXT_COLOR = (255, 255, 255)  
GOLD_COLOR = (255, 215, 0)    
WATERMARK_TEXT = "ScriptureHub" # ඔබේ Brand Name එක

def create_gradient_bar(width, height):
    """
    පහළ සිට ඉහළට ක්‍රමයෙන් විනිවිද පෙනෙන (Transparent) වන ලෙස 
    කළු පැහැති තීරුවක් සාදා ගනී.
    """
    gradient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)

    for y in range(height):
        # පහළම කොටස තද කළු (Opacity 220), ඉහළට යද්දී 0 වේ.
        opacity = int(255 * (y / height) * 0.9) 
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, opacity))
    
    return gradient

def add_text_gradient_wm():
    verse_data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    fname = parts[0].strip()
                    if not fname.endswith('.png'): fname += ".png"
                    ref = parts[1].strip()
                    txt = parts[2].strip()
                    verse_data[fname] = (ref, txt)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        font_main = ImageFont.truetype(FONT_PATH, FONT_SIZE_MAIN)
        font_ref = ImageFont.truetype(FONT_PATH, FONT_SIZE_REF)
        font_wm = ImageFont.truetype(FONT_PATH, FONT_SIZE_WM)
    except:
        font_main = ImageFont.load_default()
        font_ref = ImageFont.load_default()
        font_wm = ImageFont.load_default()

    processed_count = 0
    
    for filename in os.listdir(INPUT_DIR):
        if filename in verse_data:
            ref, text = verse_data[filename]
            
            img_path = os.path.join(INPUT_DIR, filename)
            try:
                img = Image.open(img_path).convert("RGB")
            except:
                continue
            
            # 1. Resize & Crop (Cover Mode)
            target_ratio = IMAGE_WIDTH / IMAGE_HEIGHT
            img_ratio = img.width / img.height

            if img_ratio > target_ratio:
                new_height = IMAGE_HEIGHT
                new_width = int(new_height * img_ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                left = (new_width - IMAGE_WIDTH) // 2
                img = img.crop((left, 0, left + IMAGE_WIDTH, IMAGE_HEIGHT))
            else:
                new_width = IMAGE_WIDTH
                new_height = int(new_width / img_ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                top = (new_height - IMAGE_HEIGHT) // 2
                img = img.crop((0, top, IMAGE_WIDTH, top + IMAGE_HEIGHT))
            
            # 2. Apply Gradient
            gradient_overlay = create_gradient_bar(IMAGE_WIDTH, GRADIENT_HEIGHT)
            img.paste(gradient_overlay, (0, IMAGE_HEIGHT - GRADIENT_HEIGHT), mask=gradient_overlay)
            
            d = ImageDraw.Draw(img)
            
            # 3. Text Wrapping & Positioning
            wrapper = textwrap.TextWrapper(width=60) 
            lines = wrapper.wrap(text=f'"{text}"')
            
            total_text_height = (len(lines) * (FONT_SIZE_MAIN + 10)) + 50
            
            # Reference Position
            ref_y = IMAGE_HEIGHT - 80 
            
            # Reference
            bbox_ref = d.textbbox((0, 0), ref, font=font_ref)
            w_ref = bbox_ref[2] - bbox_ref[0]
            x_ref = (IMAGE_WIDTH - w_ref) / 2
            d.text((x_ref, ref_y), ref, font=font_ref, fill=GOLD_COLOR)
            
            # Main Verse Text
            current_y = ref_y - total_text_height + 20 
            
            for line in lines:
                bbox = d.textbbox((0, 0), line, font=font_main)
                w = bbox[2] - bbox[0]
                x = (IMAGE_WIDTH - w) / 2
                
                # Shadow
                o = 2
                d.text((x+o, current_y+o), line, font=font_main, fill=(0,0,0))
                
                d.text((x, current_y), line, font=font_main, fill=TEXT_COLOR)
                current_y += (FONT_SIZE_MAIN + 10)

            # --- 4. Watermark (ScriptureHub) ---
            # දකුණු පස පහළ කෙළවරේ (Bottom Right)
            bbox_wm = d.textbbox((0, 0), WATERMARK_TEXT, font=font_wm)
            w_wm = bbox_wm[2] - bbox_wm[0]
            h_wm = bbox_wm[3] - bbox_wm[1]

            x_wm = IMAGE_WIDTH - w_wm - 30  # දකුණෙන් 30px ඉඩක්
            y_wm = IMAGE_HEIGHT - h_wm - 20 # පහළින් 20px ඉඩක් (කළු කොටසේ නිසා පැහැදිලිව පෙනෙයි)

            # Watermark එක ලා අළු පාටින් (Light Grey) දාමු, කැපී පෙනෙන්න ඕන නම් White දාන්න
            d.text((x_wm, y_wm), WATERMARK_TEXT, font=font_wm, fill=(200, 200, 200))

            # Save
            img.save(os.path.join(OUTPUT_DIR, filename))
            processed_count += 1
            print(f"Finished (WM): {filename}")

    print(f"Done! Created {processed_count} posts with watermark in '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    add_text_gradient_wm()