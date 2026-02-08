#!/usr/bin/env python3
"""
Create detailed, dynamic sticker SVGs with animations and better visuals.
Replaces existing stickers with upgraded versions.
"""
from __future__ import annotations
import json
from pathlib import Path

def create_detailed_neon_heart() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <radialGradient id="heartGrad" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#ff7ad9" stop-opacity="1">
        <animate attributeName="stop-opacity" values="1;0.8;1" dur="2s" repeatCount="indefinite"/>
      </stop>
      <stop offset="60%" stop-color="#9b5cff" stop-opacity="0.9">
        <animate attributeName="stop-opacity" values="0.9;1;0.9" dur="2.5s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#00e5ff" stop-opacity="0.2">
        <animate attributeName="stop-opacity" values="0.2;0.4;0.2" dur="3s" repeatCount="indefinite"/>
      </stop>
      <animate attributeName="r" values="60%;75%;60%" dur="3s" repeatCount="indefinite"/>
    </radialGradient>
    <filter id="heartGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8" result="blur">
        <animate attributeName="stdDeviation" values="8;12;8" dur="2s" repeatCount="indefinite"/>
      </feGaussianBlur>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="sparkle" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="sparkleBlur"/>
      <feMerge>
        <feMergeNode in="sparkleBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="256" height="256" fill="#0a0a1a" opacity="0.3"/>
  <path filter="url(#heartGlow)" fill="url(#heartGrad)"
    d="M128 216s-73-43-94-87c-15-31 4-69 38-77 21-5 44 2 56 18
       12-16 35-23 56-18 34 8 53 46 38 77-21 44-94 87-94 87z">
    <animateTransform attributeName="transform" type="scale" values="1;1.05;1" dur="2.5s" repeatCount="indefinite" transform-origin="128 128"/>
  </path>
  <circle cx="100" cy="100" r="4" fill="#00e5ff" filter="url(#sparkle)" opacity="0.9">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.5s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0,0; 10,-10; 0,0" dur="3s" repeatCount="indefinite"/>
  </circle>
  <circle cx="156" cy="90" r="3" fill="#ff7ad9" filter="url(#sparkle)" opacity="0.8">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" begin="0.5s"/>
    <animateTransform attributeName="transform" type="translate" values="0,0; -8,8; 0,0" dur="2.5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="140" cy="140" r="2.5" fill="#9b5cff" filter="url(#sparkle)" opacity="0.7">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.8s" repeatCount="indefinite" begin="1s"/>
  </circle>
</svg>'''

def create_detailed_cyberpunk_grid() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="gridGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.8">
        <animate attributeName="stop-opacity" values="0.8;1;0.8" dur="2s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#ff4fd8" stop-opacity="0.6">
        <animate attributeName="stop-opacity" values="0.6;0.9;0.6" dur="2.5s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
    <filter id="cyberGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="blur">
        <animate attributeName="stdDeviation" values="6;10;6" dur="2s" repeatCount="indefinite"/>
      </feGaussianBlur>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <pattern id="gridPattern" patternUnits="userSpaceOnUse" width="64" height="64">
      <path d="M0 0 L64 0 M0 0 L0 64" stroke="url(#gridGrad)" stroke-width="2" opacity="0.4">
        <animate attributeName="opacity" values="0.4;0.7;0.4" dur="3s" repeatCount="indefinite"/>
      </path>
    </pattern>
  </defs>
  <rect width="256" height="256" fill="#0a0a1a"/>
  <rect width="256" height="256" fill="url(#gridPattern)"/>
  <circle cx="128" cy="128" r="35" fill="url(#gridGrad)" filter="url(#cyberGlow)" opacity="0.9">
    <animate attributeName="r" values="35;42;35" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.9;1;0.9" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="128" cy="128" r="20" fill="#9b5cff" opacity="0.6">
    <animate attributeName="r" values="20;25;20" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <rect x="120" y="120" width="16" height="16" fill="#00e5ff" opacity="0.9">
    <animateTransform attributeName="transform" type="rotate" values="0 128 128;360 128 128" dur="4s" repeatCount="indefinite"/>
  </rect>
</svg>'''

def create_detailed_cute_puppy() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <radialGradient id="puppyGrad" cx="50%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#ffd4e5"/>
      <stop offset="100%" stop-color="#ffb3d9"/>
    </radialGradient>
    <filter id="softShadow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="256" height="256" fill="#fff5f9" rx="20"/>
  <g transform-origin="128 140">
    <animateTransform attributeName="transform" type="scale" values="1;1.02;1" dur="3s" repeatCount="indefinite"/>
    <circle cx="128" cy="100" r="42" fill="url(#puppyGrad)" filter="url(#softShadow)"/>
    <ellipse cx="128" cy="180" rx="52" ry="42" fill="url(#puppyGrad)" filter="url(#softShadow)"/>
    <circle cx="110" cy="95" r="9" fill="#000">
      <animate attributeName="r" values="9;0;9" dur="4s" repeatCount="indefinite" begin="2s"/>
    </circle>
    <circle cx="146" cy="95" r="9" fill="#000">
      <animate attributeName="r" values="9;0;9" dur="4s" repeatCount="indefinite" begin="2.1s"/>
    </circle>
    <ellipse cx="128" cy="110" rx="14" ry="10" fill="#000">
      <animate attributeName="ry" values="10;8;10" dur="2s" repeatCount="indefinite"/>
    </ellipse>
    <path d="M100 120 Q128 132 156 120" stroke="#000" stroke-width="3" fill="none" stroke-linecap="round">
      <animate attributeName="d" values="M100 120 Q128 132 156 120;M100 122 Q128 130 156 122;M100 120 Q128 132 156 120" dur="3s" repeatCount="indefinite"/>
    </path>
    <ellipse cx="120" cy="85" rx="8" ry="12" fill="#fff" opacity="0.8"/>
    <ellipse cx="136" cy="85" rx="8" ry="12" fill="#fff" opacity="0.8"/>
    <path d="M110 100 L118 108 M146 100 L138 108" stroke="#fff" stroke-width="2" opacity="0.6"/>
  </g>
  <circle cx="90" cy="70" r="3" fill="#ff9ec7" opacity="0.6">
    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="166" cy="75" r="2.5" fill="#ff9ec7" opacity="0.5">
    <animate attributeName="opacity" values="0.3;0.7;0.3" dur="2.5s" repeatCount="indefinite" begin="0.5s"/>
  </circle>
</svg>'''

def create_detailed_shooting_star() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="starGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffd54a" stop-opacity="1"/>
      <stop offset="50%" stop-color="#ffeb3b" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#fff" stop-opacity="0.8"/>
    </linearGradient>
    <filter id="starGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8" result="blur">
        <animate attributeName="stdDeviation" values="8;12;8" dur="1.5s" repeatCount="indefinite"/>
      </feGaussianBlur>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="256" height="256" fill="#0a0a1a"/>
  <g>
    <animateTransform attributeName="transform" type="translate" values="0,0; 20,20" dur="2s" repeatCount="indefinite"/>
    <path d="M60 60 L200 200" stroke="url(#starGrad)" stroke-width="8" stroke-linecap="round" filter="url(#starGlow)" opacity="0.9">
      <animate attributeName="stroke-dasharray" values="0,300;300,0" dur="1.5s" repeatCount="indefinite"/>
    </path>
    <circle cx="200" cy="200" r="18" fill="url(#starGrad)" filter="url(#starGlow)">
      <animate attributeName="r" values="18;24;18" dur="1s" repeatCount="indefinite"/>
    </circle>
    <path d="M180 180 L200 200 L190 195 L195 200 Z" fill="#b86bff" opacity="0.9">
      <animate attributeName="opacity" values="0.6;1;0.6" dur="1s" repeatCount="indefinite"/>
    </path>
    <circle cx="70" cy="70" r="3" fill="#00f0ff" opacity="0.8">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="1s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="0,0; 130,130" dur="1.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="80" cy="80" r="2" fill="#ffd54a" opacity="0.7">
      <animate attributeName="opacity" values="0.3;0.9;0.3" dur="1.2s" repeatCount="indefinite" begin="0.3s"/>
      <animateTransform attributeName="transform" type="translate" values="0,0; 120,120" dur="1.5s" repeatCount="indefinite"/>
    </circle>
  </g>
  <circle cx="50" cy="50" r="2" fill="#fff" opacity="0.6">
    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="220" cy="220" r="1.5" fill="#b86bff" opacity="0.5">
    <animate attributeName="opacity" values="0.3;0.7;0.3" dur="2.5s" repeatCount="indefinite" begin="1s"/>
  </circle>
</svg>'''

# Map of sticker IDs to detailed creation functions
DETAILED_STICKERS = {
    "neon_hearts": {
        "heart_glow": create_detailed_neon_heart,
    },
    "cyberpunk_vibes": {
        "neon_grid": create_detailed_cyberpunk_grid,
    },
    "cute_critters": {
        "puppy": create_detailed_cute_puppy,
    },
    "cosmic_dreams": {
        "shooting_star": create_detailed_shooting_star,
    }
}

def upgrade_all_stickers():
    """Upgrade all stickers with detailed versions."""
    sticker_packs_dir = Path("packs/sticker_packs")
    
    for pack_dir in sticker_packs_dir.iterdir():
        if not pack_dir.is_dir() or pack_dir.name == "manifest.json":
            continue
        
        pack_id = pack_dir.name
        stickers_dir = pack_dir / "stickers"
        
        if not stickers_dir.exists():
            continue
        
        print(f"\nUpgrading {pack_id}...")
        
        # Get pack-specific detailed stickers
        pack_stickers = DETAILED_STICKERS.get(pack_id, {})
        
        for svg_file in stickers_dir.glob("*.svg"):
            sticker_id = svg_file.stem
            
            # If we have a detailed version, use it
            if sticker_id in pack_stickers:
                detailed_svg = pack_stickers[sticker_id]()
                svg_file.write_text(detailed_svg, encoding="utf-8")
                print(f"  Upgraded: {sticker_id}.svg")
            else:
                # Enhance existing sticker with animations
                try:
                    content = svg_file.read_text(encoding="utf-8")
                    enhanced = enhance_with_animations(content, pack_id, sticker_id)
                    if enhanced != content:
                        svg_file.write_text(enhanced, encoding="utf-8")
                        print(f"  Enhanced: {sticker_id}.svg")
                except Exception as e:
                    print(f"  Error enhancing {sticker_id}: {e}")

def enhance_with_animations(content: str, pack_id: str, sticker_id: str) -> str:
    """Add animations to existing SVG content."""
    if '<animate' in content:
        return content  # Already has animations
    
    enhanced = content
    
    # Add pulsing glow to filters
    if 'filter id="glow"' in enhanced:
        enhanced = enhanced.replace(
            '<feGaussianBlur stdDeviation="4"',
            '''<feGaussianBlur stdDeviation="4">
        <animate attributeName="stdDeviation" values="4;8;4" dur="2s" repeatCount="indefinite"/>'''
        )
    
    # Add subtle scale animation to main shapes
    if pack_id in ["neon_hearts", "cute_critters"]:
        # Find main path or circle and add scale animation
        if '<path' in enhanced and 'fill=' in enhanced:
            enhanced = enhanced.replace(
                '<path',
                '''<g transform-origin="128 128">
    <animateTransform attributeName="transform" type="scale" values="1;1.03;1" dur="3s" repeatCount="indefinite"/>
    <path'''
            )
            # Close the group before </svg>
            enhanced = enhanced.replace('</svg>', '  </g>\n</svg>')
    
    # Add opacity pulsing for cosmic stickers
    if pack_id == "cosmic_dreams":
        if '<circle' in enhanced and 'fill=' in enhanced:
            enhanced = enhanced.replace(
                '<circle',
                '''<circle>
      <animate attributeName="opacity" values="0.8;1;0.8" dur="2s" repeatCount="indefinite"/>'''
            )
    
    return enhanced

if __name__ == "__main__":
    upgrade_all_stickers()
    print("\nAll stickers upgraded!")
