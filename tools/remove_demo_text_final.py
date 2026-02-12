#!/usr/bin/env python3
"""Remove demo text from all dearest_mother SVG files."""
from pathlib import Path
import re

CARDS_DIR = Path(__file__).parent.parent / 'packs' / 'dearest_mother' / 'assets' / 'cards'

def fix_file(svg_path):
    """Remove demo text from SVG file."""
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the two demo text lines (with any whitespace/newlines)
    # Match the full text element including all attributes
    pattern1 = r'<text[^>]*>Inside message goes here</text>\s*\n?'
    pattern2 = r'<text[^>]*>\(User-customizable in composer\)</text>\s*\n?'
    
    original = content
    content = re.sub(pattern1, '', content, flags=re.MULTILINE)
    content = re.sub(pattern2, '', content, flags=re.MULTILINE)
    
    if content != original:
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = sorted(CARDS_DIR.glob('mom_*.svg'))
    print(f'Processing {len(files)} files...')
    
    updated = 0
    for svg_file in files:
        if fix_file(svg_file):
            print(f'  ✓ {svg_file.name}')
            updated += 1
        else:
            print(f'  - {svg_file.name} (no changes)')
    
    print(f'\nUpdated {updated} of {len(files)} files.')

if __name__ == '__main__':
    main()
