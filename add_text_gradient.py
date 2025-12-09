import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# --- සැකසුම් ---
INPUT_DIR = 'raw_images'      
OUTPUT_DIR = 'final_posts'    
DATA_FILE = 'required_images.txt'

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

# පහළින් අඳුරු විය යුතු ප්‍රමාණය (උසින් කොච්චර ප්‍රමාණයක්ද?)
GRADIENT_HEIGHT = 500  # පහළ pixel 500ක් ටිකෙන් ටික අඳුරු වේ

FONT_PATH = "arialbd.ttf"     
FONT_SIZE_MAIN = 55           
FONT_SIZE_REF = 35            

TEXT_COLOR = (255, 255, 255)  
GOLD_COLOR = (255, 215, 0)    

def create_gradient_bar(width, height):
    """
    පහළ සිට ඉහළට ක්‍රමයෙන් විනිවිද පෙනෙන (Transparent) වන ලෙස 
    කළු පැහැති තීරුවක් සාදා ගනී.
    """
    gradient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)

    for y in range(height):
        # පහළම (y=height) කොටස තද කළු (Opacity 220), ඉහළට යද්දී 0 වේ.
        # මෙය Linear Gradient එකක් ලෙස සකසමු.
        opacity = int(255 * (y / height) * 0.9) # 0.9 මගින් උපරිම කළු බව පාලනය කරයි
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, opacity))
    
    return gradient

def add_text_gradient():
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
    except:
        font_main = ImageFont.load_default()
        font_ref = ImageFont.load_default()

    processed_count = 0
    
    for filename in os.listdir(INPUT_DIR):
        if filename in verse_data:
            ref, text = verse_data[filename]
            
            img_path = os.path.join(INPUT_DIR, filename)
            try:
                img = Image.open(img_path).convert("RGB")
            except:
                continue
            
            # 1. පින්තූරය 1920x1080 ලෙස Resize කරමු (Aspect Ratio රැකගෙන Crop කරමු - "Cover" Mode)
            target_ratio = IMAGE_WIDTH / IMAGE_HEIGHT
            img_ratio = img.width / img.height

            if img_ratio > target_ratio:
                # පින්තූරය පළල වැඩියි -> උස සමාන කර, දෙපැත්තෙන් කපමු
                new_height = IMAGE_HEIGHT
                new_width = int(new_height * img_ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                # මැදින් Crop කිරීම
                left = (new_width - IMAGE_WIDTH) // 2
                img = img.crop((left, 0, left + IMAGE_WIDTH, IMAGE_HEIGHT))
            else:
                # පින්තූරය උස වැඩියි -> පළල සමාන කර, උඩින්/යටින් කපමු
                new_width = IMAGE_WIDTH
                new_height = int(new_width / img_ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                # මැදින් Crop කිරීම (Center)
                top = (new_height - IMAGE_HEIGHT) // 2
                img = img.crop((0, top, IMAGE_WIDTH, top + IMAGE_HEIGHT))
            
            # 2. Gradient එක සකසා පින්තූරය මත ඇලවීම
            # Gradient එක වෙනම හදාගෙන Paste කරමු
            gradient_overlay = create_gradient_bar(IMAGE_WIDTH, GRADIENT_HEIGHT)
            
            # Gradient එක අලවන්නේ පින්තූරයේ පහළම කොටසටයි
            img.paste(gradient_overlay, (0, IMAGE_HEIGHT - GRADIENT_HEIGHT), mask=gradient_overlay)
            
            d = ImageDraw.Draw(img)
            
            # 3. Text ලිවීම (පහළ කොටසේ)
            wrapper = textwrap.TextWrapper(width=60) 
            lines = wrapper.wrap(text=f'"{text}"')
            
            total_text_height = (len(lines) * (FONT_SIZE_MAIN + 10)) + 50
            
            # පින්තූරයේ පහළ සිට 80px පමණ උඩින් Reference එක පටන් ගමු
            ref_y = IMAGE_HEIGHT - 80 
            
            # Reference ලිවීම
            bbox_ref = d.textbbox((0, 0), ref, font=font_ref)
            w_ref = bbox_ref[2] - bbox_ref[0]
            x_ref = (IMAGE_WIDTH - w_ref) / 2
            d.text((x_ref, ref_y), ref, font=font_ref, fill=GOLD_COLOR)
            
            # Verse Text ලිවීම (Reference එකට උඩින්)
            current_y = ref_y - total_text_height + 20 # පොඩි ඉඩක්
            
            for line in lines:
                bbox = d.textbbox((0, 0), line, font=font_main)
                w = bbox[2] - bbox[0]
                x = (IMAGE_WIDTH - w) / 2
                
                # Shadow (අකුරු තවත් පැහැදිලි වීමට)
                o = 2
                d.text((x+o, current_y+o), line, font=font_main, fill=(0,0,0))
                
                d.text((x, current_y), line, font=font_main, fill=TEXT_COLOR)
                current_y += (FONT_SIZE_MAIN + 10)

            # Save
            img.save(os.path.join(OUTPUT_DIR, filename))
            processed_count += 1
            print(f"Finished: {filename}")

    print(f"Done! Created {processed_count} gradient style posts.")

if __name__ == "__main__":
    add_text_gradient()