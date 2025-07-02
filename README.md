# autosolvemodel
# Base64 Image Labeling by OCR

This project provides Python scripts to decode base64-encoded images from JSON, or to process images directly from a folder, extract text from each image using OCR, and save each image with the extracted text as its filename. It also includes a robust renaming tool to merge and organize files with unique, sequential names.

## Features
- **JSON batch OCR:** Decodes images from a JSON file (`base64.json` or any `.json` in a folder) containing a list of base64-encoded images, and saves them with OCR-extracted filenames.
- **Image folder OCR:** Processes all images in a folder, performs OCR, and saves them with the extracted text as filenames.
- **Batch renaming:** Merges and renames files from multiple sources, ensuring all files with the same base name are sequentially numbered (no skips, no overwrites).
- Handles errors gracefully and prints clear output for each step.

## Requirements
- Python 3.7+
- [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki) (Windows: install from UB Mannheim builds)
- Python packages: `pillow`, `pytesseract`

## Setup

1. **Install Python dependencies:**
   ```sh
   pip install pillow pytesseract
   ```

2. **Install Tesseract-OCR:**
   - **Windows:** [Download the installer from UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and install. The script will automatically use the default install path (`C:\Program Files\Tesseract-OCR\tesseract.exe`).
   - **macOS:**
     ```sh
     brew install tesseract
     ```
   - **Linux (Debian/Ubuntu):**
     ```sh
     sudo apt-get install tesseract-ocr
     ```

---

## 1. OCR from JSON Files

### a. Single JSON file
Run the script from the command line:
```sh
python ocr_base64_to_image.py
```
- The script will read `base64.json` and save images in `output_images/`.

### b. Batch process all JSON files in a directory
```sh
python batch_ocr_processor.py input
```
- Place all your JSON files in the `input/` directory (or specify another directory).
- Output will be organized in `batch_output/<json_filename>/` for each file.

---

## 2. OCR from Images in a Folder

You can process all images in a folder and save them with OCR-extracted filenames:

```sh
python ocr_images_folder.py [input_images_folder] [output_images_folder]
```
- If no arguments are given, defaults are `input_images/` and `output_images/`.
- Supported image formats: PNG, JPG, JPEG, BMP, TIFF, GIF.
- Each image is copied to the output folder, renamed using the extracted text (or a fallback name if no text is found).
- Duplicate names are handled automatically.

**Example:**
```sh
python ocr_images_folder.py input_images output_images
```

---

## 3. Merging and Sequential Renaming of Files

When merging results from multiple OCR runs or sources, you may have duplicate or overlapping filenames (e.g., `345.png`, `345_1.png`, `345(2).png`, `345_1(2).png`, `image_51.png`, `image_51 (2).png`, etc.).

To organize all files in a folder with unique, sequential names for each base (e.g., `345`, `image_51`):

### **Use the renaming script:**
```sh
python sequential_rename.py [target_folder]
```
- If no folder is given, defaults to `output_images/`.
- The script will scan all files in the folder and, for each base (e.g., `345`, `image_51`), rename all variants sequentially:
  - `345.png`, `345_1.png`, `345_2.png`, ...
  - `image_51.png`, `image_51_1.png`, `image_51_2.png`, ...
- **No files are skipped or overwritten:** If a target name exists, the script keeps incrementing the number until it finds a free filename.
- Works with files from different sources, sets, or naming conventions.

**Example:**
```sh
python sequential_rename.py dupliName
```

---

## Complete Workflow Example

1. **Extract images from JSON or process images with OCR:**
   - Use `ocr_base64_to_image.py`, `batch_ocr_processor.py`, or `ocr_images_folder.py` as needed.
2. **Merge all output images into a single folder (e.g., `dupliName/`).**
3. **Run the renaming script to organize and sequentially rename all files:**
   ```sh
   python sequential_rename.py dupliName
   ```
4. **Result:** All files will be named sequentially for each base, with no skips or overwrites.

---

## Troubleshooting
- **Missing dependencies:**
  - If you see errors about missing `PIL` or `pytesseract`, install them with `pip install pillow pytesseract`.
- **Tesseract not found:**
  - Make sure Tesseract is installed and (on Windows) is at `C:\Program Files\Tesseract-OCR\tesseract.exe`.
  - If installed elsewhere, set the path manually in the script:
    ```python
    pytesseract.pytesseract.tesseract_cmd = r'YOUR_PATH_TO_TESSERACT.EXE'
    ```
- **OCR accuracy:**
  - OCR results depend on image quality. For best results, use clear, high-contrast images.

## License
This project is provided as-is for educational and practical use. 
