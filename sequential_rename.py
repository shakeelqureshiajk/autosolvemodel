import os
import re
from pathlib import Path
import sys

# Usage: python sequential_rename.py [target_folder]
def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else 'output_images'
    p = Path(folder)
    if not p.exists() or not p.is_dir():
        print(f"Directory not found: {folder}")
        return

    files = [f for f in p.iterdir() if f.is_file()]
    # Map: base_name (str) -> list of Path
    base_map = {}
    for f in files:
        # Match patterns like 345.png, 345_1.png, 345(2).png, image_51.png, image_51 (2).png, etc.
        m = re.match(r'^((?:\d{3})|(?:image_\d+))(?:_\d+)?(?: \(\d+\))?\.[a-zA-Z0-9]+$', f.name)
        if m:
            base = m.group(1)
            base_map.setdefault(base, []).append(f)

    for base, flist in base_map.items():
        # Sort files by their current number (if any), fallback to original order
        def extract_num(fname):
            # 345.png -> 0, 345_1.png -> 1, 345_2.png -> 2, 345(2).png -> 2, image_51.png -> 0, image_51_1.png -> 1, image_51 (2).png -> 2
            m = re.match(rf'^{re.escape(base)}(?:_(\d+))?(?: \((\d+)\))?\.[a-zA-Z0-9]+$', fname)
            if m:
                n1 = m.group(1)
                n2 = m.group(2)
                if n1 is not None:
                    return int(n1)
                if n2 is not None:
                    return int(n2)
            return 0
        flist_sorted = sorted(flist, key=lambda f: extract_num(f.name))
        # Gather all existing names for this base
        ext = flist_sorted[0].suffix.lower() if flist_sorted else '.png'
        existing_names = set(f.name for f in files if re.match(rf'^{re.escape(base)}(?:_\d+)?\{ext}$', f.name))
        # Rename sequentially, always finding the next available name
        used_names = set(existing_names)
        for i, f in enumerate(flist_sorted):
            if i == 0:
                new_name = f"{base}{ext}"
            else:
                new_name = f"{base}_{i}{ext}"
            # If the name is taken, increment until free
            count = i
            while new_name in used_names:
                count += 1
                new_name = f"{base}_{count}{ext}"
            new_path = p / new_name
            used_names.add(new_name)
            if f.name != new_name:
                print(f"Renaming: {f.name} -> {new_name}")
                f.rename(new_path)

if __name__ == "__main__":
    main() 