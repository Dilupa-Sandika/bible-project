import os
import csv

# --- සැකසුම් ---
INPUT_FILE = 'required_images.txt'
OUTPUT_CSV = 'google_studio_prompts.csv'

# Prompt එක 16:9 සඳහා සකස් කිරීම
PROMPT_TEMPLATE = (
    "A cinematic 16:9 wide-angle 3D animated scene representing the bible verse: '{verse_text}'. "
    "Style: High-quality 3D animation (Pixar/Disney style), warm golden and brown color palette, "
    "volumetric lighting, divine atmosphere, peaceful and majestic. "
    "Wide shot, detailed background. "
    "No text, no words on image, 8k resolution, masterpiece."
)

def create_prompts():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} ගොනුව සොයාගත නොහැක.")
        return

    prompts_list = []

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Header එක සහ අනවශ්‍ය කොටස් ඉවත් කිරීම (Theme කොටස් වගේ)
    clean_lines = [line for line in lines if "|" in line and not line.startswith("===") and not line.startswith("[ ]")]

    print(f"Verses found: {len(clean_lines)}")

    for line in clean_lines:
        parts = line.strip().split('|')
        if len(parts) >= 3:
            filename = parts[0].strip()
            # .png අගට නැත්නම් දාමු, තිබේ නම් තබමු
            if not filename.endswith('.png'):
                filename += ".png"
                
            text = parts[2].strip()

            full_prompt = PROMPT_TEMPLATE.format(verse_text=text)
            prompts_list.append([filename, full_prompt])

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filename', 'Prompt'])
        writer.writerows(prompts_list)

    print(f"Success! '{OUTPUT_CSV}' ගොනුව සාදන ලදී.")

if __name__ == "__main__":
    create_prompts()