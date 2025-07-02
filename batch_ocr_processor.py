import base64
import json
import os
import sys
import glob
from io import BytesIO
from pathlib import Path

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

def sanitize_filename(text):
    """Remove or replace characters not allowed in filenames"""
    import re
    text = re.sub(r'[^\w\-_\. ]', '_', text)
    return text.strip() or 'no_text'

def process_json_file(json_file_path, output_base_dir):
    """Process a single JSON file containing base64 images"""
    json_filename = Path(json_file_path).stem
    output_dir = os.path.join(output_base_dir, json_filename)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nProcessing: {json_file_path}")
    print(f"Output directory: {output_dir}")
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {json_file_path}: {e}")
        return
    
    # Handle different JSON structures
    if isinstance(data, list):
        images_b64 = data
    elif isinstance(data, dict):
        # Look for common keys that might contain image arrays
        possible_keys = ['images', 'data', 'base64_images', 'captchas', 'samples']
        images_b64 = None
        for key in possible_keys:
            if key in data and isinstance(data[key], list):
                images_b64 = data[key]
                break
        if images_b64 is None:
            print(f"No recognizable image array found in {json_file_path}")
            return
    else:
        print(f"Unexpected data type in {json_file_path}: {type(data)}")
        return
    
    processed_count = 0
    error_count = 0
    
    for idx, img_b64 in enumerate(images_b64):
        try:
            img_data = base64.b64decode(img_b64)
            image = Image.open(BytesIO(img_data))
        except Exception as e:
            print(f"[{idx}] Failed to decode image: {e}")
            error_count += 1
            continue

        try:
            text = pytesseract.image_to_string(image).strip()
            filename = sanitize_filename(text)
            if not filename or filename == 'no_text':
                filename = f'image_{idx+1}'
            
            filepath = os.path.join(output_dir, f"{filename}.png")
            
            # Avoid overwriting files with the same name
            count = 1
            while os.path.exists(filepath):
                filepath = os.path.join(output_dir, f"{filename}_{count}.png")
                count += 1
            
            image.save(filepath)
            print(f"[{idx}] Saved: {os.path.basename(filepath)} (Text: '{text}')")
            processed_count += 1
            
        except Exception as e:
            print(f"[{idx}] OCR or save failed: {e}")
            error_count += 1
    
    print(f"Completed: {processed_count} images processed, {error_count} errors")
    return processed_count, error_count

def main():
    # Get input directory from command line or use current directory
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    else:
        input_dir = "."
    
    if not os.path.exists(input_dir):
        print(f"Directory not found: {input_dir}")
        return
    
    # Find all JSON files
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    
    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return
    
    print(f"Found {len(json_files)} JSON file(s) to process:")
    for f in json_files:
        print(f"  - {f}")
    
    # Create output directory
    output_base_dir = "batch_output"
    os.makedirs(output_base_dir, exist_ok=True)
    
    total_processed = 0
    total_errors = 0
    
    # Process each JSON file
    for json_file in json_files:
        processed, errors = process_json_file(json_file, output_base_dir)
        total_processed += processed
        total_errors += errors
    
    print(f"\n=== BATCH PROCESSING COMPLETE ===")
    print(f"Total images processed: {total_processed}")
    print(f"Total errors: {total_errors}")
    print(f"Output directory: {output_base_dir}")

if __name__ == "__main__":
    main() 