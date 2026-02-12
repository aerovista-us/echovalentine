#!/usr/bin/env python3
"""Remove demo text from dearest_mother SVG files."""
import os
from pathlib import Path

CARDS_DIR = Path(__file__).parent.parent / 'packs' / 'dearest_mother' / 'assets' / 'cards'

def remove_demo_text(svg_path):
    """Remove demo text lines from SVG file."""
    with open(svg_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    skip_next = False
    for i, line in enumerate(lines):
        # Skip lines with demo text
        if 'Inside message goes here' in line or '(User-customizable in composer)' in line:
            continue
        new_lines.append(line)
    
    # Only write if we actually removed something
    if len(new_lines) < len(lines):
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def main():
    updated = 0
    for svg_file in sorted(CARDS_DIR.glob('mom_*.svg')):
        if remove_demo_text(svg_file):
            print(f"Updated: {svg_file.name}")
            updated += 1
        else:
            print(f"No changes: {svg_file.name}")
    
    print(f"\nUpdated {updated} files.")

if __name__ == '__main__':
    main()
