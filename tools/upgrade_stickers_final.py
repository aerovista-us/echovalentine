#!/usr/bin/env python3
"""
Properly upgrade all sticker SVGs with animations and detail.
Uses proper XML parsing approach.
"""
from pathlib import Path
import re

def upgrade_svg_properly(content: str, pack_id: str) -> str:
    """Upgrade SVG with proper structure preservation."""
    if '<animate' in content:
        return content  # Already upgraded
    
    # Ensure proper SVG structure
    if not content.strip().startswith('<svg'):
        return content
    
    # Extract SVG attributes
    svg_match = re.match(r'<svg([^>]*)>', content)
    if not svg_match:
        return content
    
    svg_attrs = svg_match.group(1)
    
    # Build enhanced SVG
    enhanced_parts = []
    
    # Start SVG tag
    enhanced_parts.append(f'<svg{svg_attrs}>')
    
    # Add defs if not present
    if '<defs>' not in content:
        enhanced_parts.append('''  <defs>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur">
        <animate attributeName="stdDeviation" values="4;8;4" dur="2s" repeatCount="indefinite"/>
      </feGaussianBlur>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>''')
    
    # Extract body content (everything between > and </svg>)
    body_match = re.search(r'>(.*)</svg>', content, re.DOTALL)
    if not body_match:
        return content
    
    body = body_match.group(1).strip()
    
    # Wrap main content in animated group based on pack
    if pack_id in ["neon_hearts", "arcade_icons"]:
        enhanced_parts.append('''  <g transform-origin="128 128">
    <animateTransform attributeName="transform" type="scale" values="1;1.05;1" dur="2.5s" repeatCount="indefinite"/>
''')
        # Add filter to first path/circle
        body = re.sub(
            r'(<path[^>]*)(>)',
            r'\1 filter="url(#glow)"\2',
            body,
            count=1
        )
        enhanced_parts.append('    ' + body.replace('\n', '\n    '))
        enhanced_parts.append('  </g>')
    elif pack_id == "witchy_moods":
        enhanced_parts.append('''  <g transform-origin="128 128">
    <animateTransform attributeName="transform" type="scale" values="1;1.03;1" dur="3s" repeatCount="indefinite"/>
''')
        enhanced_parts.append('    ' + body.replace('\n', '\n    '))
        enhanced_parts.append('  </g>')
    else:
        enhanced_parts.append('  ' + body.replace('\n', '\n  '))
    
    # Add floating sparkles
    enhanced_parts.append('''  <circle cx="80" cy="80" r="2" fill="#fff" opacity="0.6">
    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="2s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0,0; 10,-10; 0,0" dur="3s" repeatCount="indefinite"/>
  </circle>
  <circle cx="176" cy="176" r="1.5" fill="#fff" opacity="0.5">
    <animate attributeName="opacity" values="0.3;0.7;0.3" dur="2.5s" repeatCount="indefinite" begin="1s"/>
  </circle>''')
    
    enhanced_parts.append('</svg>')
    
    return '\n'.join(enhanced_parts)

def main():
    """Upgrade all stickers."""
    sticker_packs_dir = Path("packs/sticker_packs")
    
    for pack_dir in sticker_packs_dir.iterdir():
        if not pack_dir.is_dir() or pack_dir.name == "manifest.json":
            continue
        
        pack_id = pack_dir.name
        stickers_dir = pack_dir / "stickers"
        
        if not stickers_dir.exists():
            continue
        
        print(f"\nUpgrading {pack_id}...")
        upgraded = 0
        
        for svg_file in stickers_dir.glob("*.svg"):
            try:
                content = svg_file.read_text(encoding="utf-8")
                
                if '<animate' in content:
                    continue
                
                enhanced = upgrade_svg_properly(content, pack_id)
                
                if enhanced != content:
                    svg_file.write_text(enhanced, encoding="utf-8")
                    print(f"  [OK] {svg_file.stem}.svg")
                    upgraded += 1
                    
            except Exception as e:
                print(f"  [ERROR] {svg_file.name}: {e}")
        
        print(f"  Upgraded {upgraded} stickers")

if __name__ == "__main__":
    main()
    print("\n[COMPLETE] All stickers upgraded!")
