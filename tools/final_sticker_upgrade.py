#!/usr/bin/env python3
"""
Final comprehensive upgrade for all sticker SVGs - adds animations and detail.
"""
from pathlib import Path
import re

def add_animations_to_svg(content: str, sticker_id: str, pack_id: str) -> str:
    """Add animations and enhancements to SVG content."""
    if '<animate' in content:
        return content  # Already has animations
    
    enhanced = content
    
    # Add defs if missing
    if '<defs>' not in enhanced:
        enhanced = enhanced.replace('<svg', '<svg>\n  <defs>\n    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">\n      <feGaussianBlur stdDeviation="4" result="blur">\n        <animate attributeName="stdDeviation" values="4;8;4" dur="2s" repeatCount="indefinite"/>\n      </feGaussianBlur>\n      <feMerge>\n        <feMergeNode in="blur"/>\n        <feMergeNode in="SourceGraphic"/>\n      </feMerge>\n    </filter>\n  </defs>')
    
    # Enhance based on pack theme
    if pack_id in ["neon_hearts", "arcade_icons"]:
        # Add pulsing glow to main shapes
        if '<path' in enhanced and 'fill=' in enhanced:
            # Wrap path in animated group
            enhanced = re.sub(
                r'(<path[^>]*fill="[^"]*"[^>]*>)',
                r'<g transform-origin="128 128">\n    <animateTransform attributeName="transform" type="scale" values="1;1.05;1" dur="2.5s" repeatCount="indefinite"/>\n    \1',
                enhanced,
                count=1
            )
            # Close group before </svg>
            if '</g>' not in enhanced[-50:]:
                enhanced = enhanced.replace('</svg>', '  </g>\n</svg>')
        
        # Add filter to paths
        enhanced = re.sub(
            r'(<path[^>]*)(>)',
            r'\1 filter="url(#glow)"\2',
            enhanced,
            count=1
        )
    
    elif pack_id == "witchy_moods":
        # Add mystical pulsing
        if '<path' in enhanced or '<circle' in enhanced:
            enhanced = re.sub(
                r'(<path[^>]*fill="[^"]*"[^>]*>|<circle[^>]*fill="[^"]*"[^>]*>)',
                r'<g transform-origin="128 128">\n    <animateTransform attributeName="transform" type="scale" values="1;1.03;1" dur="3s" repeatCount="indefinite"/>\n    \1',
                enhanced,
                count=1
            )
            if '</g>' not in enhanced[-50:]:
                enhanced = enhanced.replace('</svg>', '  </g>\n</svg>')
        
        # Add opacity pulsing
        enhanced = re.sub(
            r'(opacity="[^"]*")',
            r'\1>\n      <animate attributeName="opacity" values="0.8;1;0.8" dur="2s" repeatCount="indefinite"/>',
            enhanced,
            count=1
        )
    
    # Add sparkles/floating elements for all packs
    sparkle_code = '''
  <circle cx="80" cy="80" r="2" fill="#fff" opacity="0.6">
    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="2s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0,0; 10,-10; 0,0" dur="3s" repeatCount="indefinite"/>
  </circle>
  <circle cx="176" cy="176" r="1.5" fill="#fff" opacity="0.5">
    <animate attributeName="opacity" values="0.3;0.7;0.3" dur="2.5s" repeatCount="indefinite" begin="1s"/>
  </circle>'''
    
    if '</svg>' in enhanced and sparkle_code not in enhanced:
        enhanced = enhanced.replace('</svg>', sparkle_code + '\n</svg>')
    
    return enhanced

def upgrade_all_stickers():
    """Upgrade all stickers that don't have animations."""
    sticker_packs_dir = Path("packs/sticker_packs")
    
    for pack_dir in sticker_packs_dir.iterdir():
        if not pack_dir.is_dir() or pack_dir.name == "manifest.json":
            continue
        
        pack_id = pack_dir.name
        stickers_dir = pack_dir / "stickers"
        
        if not stickers_dir.exists():
            continue
        
        print(f"\nUpgrading {pack_id}...")
        upgraded_count = 0
        
        for svg_file in stickers_dir.glob("*.svg"):
            try:
                content = svg_file.read_text(encoding="utf-8")
                
                # Skip if already has animations
                if '<animate' in content:
                    continue
                
                sticker_id = svg_file.stem
                enhanced = add_animations_to_svg(content, sticker_id, pack_id)
                
                if enhanced != content:
                    svg_file.write_text(enhanced, encoding="utf-8")
                    print(f"  [OK] {sticker_id}.svg")
                    upgraded_count += 1
                    
            except Exception as e:
                print(f"  [ERROR] Error upgrading {svg_file.name}: {e}")
        
        print(f"  Upgraded {upgraded_count} stickers")

if __name__ == "__main__":
    upgrade_all_stickers()
    print("\n[COMPLETE] All stickers upgraded!")
