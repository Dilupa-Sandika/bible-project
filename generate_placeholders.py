import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# --- සැකසුම් ---
OUTPUT_DIR = 'final_posts'    # කෙලින්ම final folder එකට දාමු
DATA_FILE = 'required_images.txt'

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

# වර්ණ තේමාව (Golden Brown Theme)
# ඉහළ පාට (තද දුඹුරු/කළු)
COLOR_TOP = (30, 15, 0) 
# පහළ පාට (තද රන්වන්/දුඹුරු)
COLOR_BOTTOM = (80, 50, 10)

FONT_PATH = "arialbd.ttf"     
FONT_SIZE_MAIN = 60           
FONT_SIZE_REF = 40 
FONT_SIZE_WM = 30             

TEXT_COLOR = (255, 255, 255)  
GOLD_COLOR = (255, 215, 0)    
WATERMARK_TEXT = "ScriptureHub"

def create_gradient_background(width, height, top_color, bottom_color):
    """
    ඉහළ සිට පහළට වර්ණ දෙකක් මුසු කරන (Linear Gradient) පසුබිමක් සාදයි.
    """
    base = Image.new('RGB', (width, height), top_color)
    top = Image.new('RGB', (width, height), top_color)
    bottom = Image.new('RGB', (width, height), bottom_color)
    
    mask = Image.new('L', (width, height))
    mask_data = []
    
    for y in range(height):
        # 0 සිට 255 දක්වා අගය වැඩි වෙමින් යයි (Linear)
        mask_data.extend([int(255 * (y / height))] * width)
    
    mask.putdata(mask_data)
    
    # වර්ණ දෙක මුසු කිරීම
    base.paste(bottom, (0, 0), mask)
    return base

def generate_placeholders():
    # දත්ත කියවීම
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

    # Fonts Load කිරීම
    try:
        font_main = ImageFont.truetype(FONT_PATH, FONT_SIZE_MAIN)
        font_ref = ImageFont.truetype(FONT_PATH, FONT_SIZE_REF)
        font_wm = ImageFont.truetype(FONT_PATH, FONT_SIZE_WM)
    except:
        font_main = ImageFont.load_default()
        font_ref = ImageFont.load_default()
        font_wm = ImageFont.load_default()
        print("Using default font.")

    processed_count = 0
    total_count = len(verse_data)
    print(f"Starting to generate {total_count} placeholder images...")
    
    for filename, (ref, text) in verse_data.items():
        
        # 1. Gradient Background එකක් හදාගමු
        img = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT, COLOR_TOP, COLOR_BOTTOM)
        d = ImageDraw.Draw(img)

        # 2. Border එකක් (Optional - ලස්සන පෙනුමක් සඳහා)
        border_rect = [(50, 50), (IMAGE_WIDTH - 50, IMAGE_HEIGHT - 50)]
        d.rectangle(border_rect, outline=GOLD_COLOR, width=3)

        # 3. Main Verse Text
        wrapper = textwrap.TextWrapper(width=50) 
        lines = wrapper.wrap(text=f'"{text}"')
        
        total_text_height = (len(lines) * (FONT_SIZE_MAIN + 15)) + 60
        
        # මැදට ගමු
        start_y = (IMAGE_HEIGHT - total_text_height) / 2
        current_y = start_y

        for line in lines:
            bbox = d.textbbox((0, 0), line, font=font_main)
            w = bbox[2] - bbox[0]
            x = (IMAGE_WIDTH - w) / 2
            
            # Shadow
            o = 2
            d.text((x+o, current_y+o), line, font=font_main, fill=(0,0,0))
            # Text
            d.text((x, current_y), line, font=font_main, fill=TEXT_COLOR)
            current_y += (FONT_SIZE_MAIN + 15)

        # 4. Reference
        current_y += 20
        bbox_ref = d.textbbox((0, 0), ref, font=font_ref)
        w_ref = bbox_ref[2] - bbox_ref[0]
        x_ref = (IMAGE_WIDTH - w_ref) / 2
        d.text((x_ref, current_y), ref, font=font_ref, fill=GOLD_COLOR)

        # 5. Watermark (ScriptureHub)
        bbox_wm = d.textbbox((0, 0), WATERMARK_TEXT, font=font_wm)
        w_wm = bbox_wm[2] - bbox_wm[0]
        h_wm = bbox_wm[3] - bbox_wm[1]
        
        x_wm = IMAGE_WIDTH - w_wm - 70
        y_wm = IMAGE_HEIGHT - h_wm - 70
        
        d.text((x_wm, y_wm), WATERMARK_TEXT, font=font_wm, fill=(200, 200, 200))

        # Save
        img.save(os.path.join(OUTPUT_DIR, filename))
        processed_count += 1
        
        # Progress පෙන්වීම
        if processed_count % 10 == 0:
            print(f"Generated {processed_count}/{total_count} images...")

    print(f"✅ All Done! {processed_count} images saved to '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    generate_placeholders()