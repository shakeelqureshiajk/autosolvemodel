import os
import sys
from pathlib import Path
from PIL import Image
import pytesseract
import shutil

# Set Tesseract path for Windows (UB Mannheim default)
if sys.platform.startswith('win'):
    default_tess_path = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    if os.path.exists(default_tess_path):
        pytesseract.pytesseract.tesseract_cmd = default_tess_path

def sanitize_filename(text):
    import re
    text = re.sub(r'[^\w\-_\. ]', '_', text)
    return text.strip() or 'no_text'

def main():
    # Input and output directories
    input_dir = sys.argv[1] if len(sys.argv) > 1 else 'input_images'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'output_images'
    os.makedirs(output_dir, exist_ok=True)

    # Supported image extensions
    exts = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif'}
    images = [f for f in Path(input_dir).iterdir() if f.suffix.lower() in exts and f.is_file()]

    if not images:
        print(f"No images found in {input_dir}")
        return

    print(f"Found {len(images)} image(s) in {input_dir}")

    for idx, img_path in enumerate(images):
        try:
            image = Image.open(img_path)
        except Exception as e:
            print(f"[{idx}] Failed to open {img_path.name}: {e}")
            continue

        try:
            text = pytesseract.image_to_string(image).strip()
            filename = sanitize_filename(text)
            if not filename or filename == 'no_text':
                filename = f'image_{idx+1}'
            out_path = Path(output_dir) / f"{filename}{img_path.suffix.lower()}"
            # Avoid overwriting files with the same name
            count = 1
            orig_out_path = out_path
            while out_path.exists():
                out_path = Path(output_dir) / f"{filename}_{count}{img_path.suffix.lower()}"
                count += 1
            shutil.copy2(img_path, out_path)
            print(f"[{idx}] Saved as '{out_path.name}' (Extracted text: '{text}')")
        except Exception as e:
            print(f"[{idx}] OCR or save failed for {img_path.name}: {e}")

if __name__ == "__main__":
    main() 