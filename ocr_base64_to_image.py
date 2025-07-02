import base64
import json
import os
import sys
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    print("Pillow is required. Install with: pip install pillow")
    sys.exit(1)

try:
    import pytesseract
except ImportError:
    print("pytesseract is required. Install with: pip install pytesseract")
    sys.exit(1)

# Set Tesseract path for Windows (UB Mannheim default)
if sys.platform.startswith('win'):
    default_tess_path = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    if os.path.exists(default_tess_path):
        pytesseract.pytesseract.tesseract_cmd = default_tess_path

# Load base64 images from JSON
INPUT_JSON = 'base64.json'
OUTPUT_DIR = 'output_images'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(text):
    # Remove or replace characters not allowed in filenames
    import re
    text = re.sub(r'[^\w\-_\. ]', '_', text)
    return text.strip() or 'no_text'

def main():
    try:
        with open(INPUT_JSON, 'r', encoding='utf-8') as f:
            images_b64 = json.load(f)
    except Exception as e:
        print(f"Error reading {INPUT_JSON}: {e}")
        return

    if not isinstance(images_b64, list):
        print(f"Expected a list in {INPUT_JSON}, got {type(images_b64)}")
        return

    for idx, img_b64 in enumerate(images_b64):
        try:
            img_data = base64.b64decode(img_b64)
            image = Image.open(BytesIO(img_data))
        except Exception as e:
            print(f"[{idx}] Failed to decode image: {e}")
            continue

        try:
            text = pytesseract.image_to_string(image).strip()
            filename = sanitize_filename(text)
            if not filename or filename == 'no_text':
                filename = f'image_{idx+1}'
            filepath = os.path.join(OUTPUT_DIR, f"{filename}.png")
            # Avoid overwriting files with the same name
            count = 1
            orig_filepath = filepath
            while os.path.exists(filepath):
                filepath = os.path.join(OUTPUT_DIR, f"{filename}_{count}.png")
                count += 1
            image.save(filepath)
            print(f"[{idx}] Saved image as '{filepath}' (Extracted text: '{text}')")
        except Exception as e:
            print(f"[{idx}] OCR or save failed: {e}")

if __name__ == "__main__":
    main() 