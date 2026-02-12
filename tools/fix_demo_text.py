#!/usr/bin/env python3
"""Remove demo text from dearest_mother SVG files."""
from pathlib import Path

CARDS_DIR = Path(__file__).parent.parent / 'packs' / 'dearest_mother' / 'assets' / 'cards'

def remove_demo_text(svg_path):
    """Remove demo text lines from SVG file."""
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    # Remove text elements containing demo text - escape parentheses in regex
    patterns = [
        r'<text[^>]*>Inside message goes here</text>\s*\n?',
        r'<text[^>]*>\(User-customizable in composer\)</text>\s*\n?'
    ]
    
    original_content = content
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)
    
    if content != original_content:
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    updated = 0
    for svg_file in sorted(CARDS_DIR.glob('mom_*.svg')):
        if remove_demo_text(svg_file):
            print(f"Updated: {svg_file.name}")
            updated += 1
    
    print(f"\nUpdated {updated} files.")

if __name__ == '__main__':
    main()
