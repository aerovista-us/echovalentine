#!/usr/bin/env python3
"""
Generate sticker SVGs for sticker packs.
All stickers are 256x256 viewBox for consistent sizing.
"""
from __future__ import annotations
import json
from pathlib import Path

def generate_sticker_svg(sticker_id: str, theme: str) -> str:
    """Generate an SVG sticker based on ID and theme."""
    # Theme-specific colors
    themes = {
        "cyberpunk": {
            "primary": "#00e5ff",
            "secondary": "#ff4fd8",
            "accent": "#9b5cff",
            "bg": "#0a0a1a"
        },
        "cute": {
            "primary": "#ffb3d9",
            "secondary": "#ffd4e5",
            "accent": "#ff9ec7",
            "bg": "#fff5f9"
        },
        "cosmic": {
            "primary": "#ffd54a",
            "secondary": "#b86bff",
            "accent": "#00f0ff",
            "bg": "#0a0a1a"
        }
    }
    
    colors = themes.get(theme, themes["cyberpunk"])
    
    # Base SVG structure with defs
    defs_content = f'''  <defs>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>'''
    
    # Add gradient defs if needed
    if "galaxy" in sticker_id:
        defs_content += f'''
    <radialGradient id="galaxyGrad">
      <stop offset="0%" stop-color="{colors["primary"]}"/>
      <stop offset="50%" stop-color="{colors["secondary"]}"/>
      <stop offset="100%" stop-color="{colors["accent"]}"/>
    </radialGradient>'''
    
    defs_content += "\n  </defs>"
    
    base_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
{defs_content}
{{content}}
</svg>"""
    
    # Theme-specific colors
    themes = {
        "cyberpunk": {
            "primary": "#00e5ff",
            "secondary": "#ff4fd8",
            "accent": "#9b5cff",
            "bg": "#0a0a1a"
        },
        "cute": {
            "primary": "#ffb3d9",
            "secondary": "#ffd4e5",
            "accent": "#ff9ec7",
            "bg": "#fff5f9"
        },
        "cosmic": {
            "primary": "#ffd54a",
            "secondary": "#b86bff",
            "accent": "#00f0ff",
            "bg": "#0a0a1a"
        }
    }
    
    # Generate content based on sticker ID
    content = ""
    
    if theme == "cyberpunk":
        if "grid" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <g stroke="{colors["primary"]}" stroke-width="2" opacity="0.6">
    <line x1="0" y1="64" x2="256" y2="64"/>
    <line x1="0" y1="128" x2="256" y2="128"/>
    <line x1="0" y1="192" x2="256" y2="192"/>
    <line x1="64" y1="0" x2="64" y2="256"/>
    <line x1="128" y1="0" x2="128" y2="256"/>
    <line x1="192" y1="0" x2="192" y2="256"/>
  </g>
  <circle cx="128" cy="128" r="30" fill="{colors["primary"]}" filter="url(#glow)" opacity="0.8"/>'''
        elif "circuit" in sticker_id and "heart" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <path d="M128 200 Q80 160 80 120 Q80 90 110 90 Q130 90 128 110 Q126 90 146 90 Q176 90 176 120 Q176 160 128 200 Z" 
        fill="none" stroke="{colors["primary"]}" stroke-width="4" filter="url(#glow)"/>
  <circle cx="110" cy="90" r="4" fill="{colors["secondary"]}"/>
  <circle cx="146" cy="90" r="4" fill="{colors["secondary"]}"/>
  <path d="M100 140 L156 140 M128 120 L128 160" stroke="{colors["accent"]}" stroke-width="3"/>'''
        elif "hologram" in sticker_id and "star" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <path d="M128 40 L140 100 L200 100 L150 140 L170 200 L128 160 L86 200 L106 140 L56 100 L116 100 Z" 
        fill="{colors["primary"]}" filter="url(#glow)" opacity="0.9"/>
  <path d="M128 60 L135 95 L170 95 L145 120 L155 155 L128 135 L101 155 L111 120 L86 95 L121 95 Z" 
        fill="{colors["secondary"]}" opacity="0.6"/>'''
        elif "data_stream" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <g stroke="{colors["primary"]}" stroke-width="3" fill="none">
    <path d="M40 80 Q80 60 120 80 T200 80" filter="url(#glow)"/>
    <path d="M40 128 Q80 108 120 128 T200 128" filter="url(#glow)"/>
    <path d="M40 176 Q80 156 120 176 T200 176" filter="url(#glow)"/>
  </g>
  <circle cx="200" cy="80" r="6" fill="{colors["secondary"]}"/>
  <circle cx="200" cy="128" r="6" fill="{colors["secondary"]}"/>
  <circle cx="200" cy="176" r="6" fill="{colors["secondary"]}"/>'''
        elif "arrow" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <path d="M60 128 L180 128 M160 100 L180 128 L160 156" 
        stroke="{colors["primary"]}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
  <circle cx="60" cy="128" r="12" fill="{colors["secondary"]}"/>'''
        elif "eye" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <ellipse cx="128" cy="128" rx="60" ry="40" fill="none" stroke="{colors["primary"]}" stroke-width="4" filter="url(#glow)"/>
  <circle cx="128" cy="128" r="20" fill="{colors["secondary"]}"/>
  <circle cx="128" cy="128" r="8" fill="{colors["bg"]}"/>
  <path d="M80 100 Q128 90 176 100" stroke="{colors["accent"]}" stroke-width="3" fill="none"/>'''
        elif "glitch" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <path d="M128 200 Q80 160 80 120 Q80 90 110 90 Q130 90 128 110 Q126 90 146 90 Q176 90 176 120 Q176 160 128 200 Z" 
        fill="{colors["primary"]}" filter="url(#glow)" opacity="0.8"/>
  <path d="M125 200 Q77 160 77 120 Q77 90 107 90 Q127 90 125 110 Q123 90 143 90 Q173 90 173 120 Q173 160 125 200 Z" 
        fill="{colors["secondary"]}" opacity="0.6"/>
  <path d="M131 200 Q83 160 83 120 Q83 90 113 90 Q133 90 131 110 Q129 90 149 90 Q179 90 179 120 Q179 160 131 200 Z" 
        fill="{colors["accent"]}" opacity="0.6"/>'''
        elif "diamond" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <path d="M128 60 L180 128 L128 196 L76 128 Z" 
        fill="{colors["primary"]}" filter="url(#glow)" opacity="0.9"/>
  <path d="M128 60 L180 128 L128 196 L76 128 Z" 
        fill="none" stroke="{colors["secondary"]}" stroke-width="3"/>'''
        elif "pattern" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <g stroke="{colors["primary"]}" stroke-width="2" fill="none">
    <path d="M40 80 L80 120 L120 80 L160 120 L200 80 L216 96"/>
    <path d="M40 176 L80 136 L120 176 L160 136 L200 176 L216 160"/>
  </g>
  <circle cx="128" cy="128" r="20" fill="{colors["secondary"]}" filter="url(#glow)"/>'''
        elif "text" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <rect x="60" y="100" width="136" height="56" rx="8" fill="none" stroke="{colors["primary"]}" stroke-width="3" filter="url(#glow)"/>
  <line x1="80" y1="120" x2="176" y2="120" stroke="{colors["secondary"]}" stroke-width="4"/>
  <line x1="80" y1="136" x2="140" y2="136" stroke="{colors["secondary"]}" stroke-width="4"/>'''
        elif "bolt" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <path d="M128 60 L160 120 L140 120 L150 196 L128 140 L108 140 L128 60 Z" 
        fill="{colors["primary"]}" filter="url(#glow)" opacity="0.9"/>'''
        elif "skull" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <ellipse cx="128" cy="140" rx="60" ry="70" fill="none" stroke="{colors["primary"]}" stroke-width="4" filter="url(#glow)"/>
  <circle cx="110" cy="120" r="12" fill="{colors["secondary"]}"/>
  <circle cx="146" cy="120" r="12" fill="{colors["secondary"]}"/>
  <path d="M100 160 Q128 170 156 160" stroke="{colors["accent"]}" stroke-width="4" fill="none" stroke-linecap="round"/>'''
        else:
            # Default cyberpunk shape
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="128" r="50" fill="{colors["primary"]}" filter="url(#glow)" opacity="0.8"/>'''
    
    elif theme == "cute":
        if "puppy" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="100" r="40" fill="{colors["primary"]}"/>
  <ellipse cx="128" cy="180" rx="50" ry="40" fill="{colors["primary"]}"/>
  <circle cx="110" cy="95" r="8" fill="#000"/>
  <circle cx="146" cy="95" r="8" fill="#000"/>
  <ellipse cx="128" cy="110" rx="12" ry="8" fill="#000"/>
  <path d="M100 120 Q128 130 156 120" stroke="#000" stroke-width="2" fill="none"/>'''
        elif "kitten" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="100" r="35" fill="{colors["primary"]}"/>
  <path d="M128 80 L110 50 L128 60 L146 50 Z" fill="{colors["primary"]}"/>
  <path d="M128 80 L110 50 L128 60 L146 50 Z" fill="{colors["primary"]}" transform="translate(0,0)"/>
  <circle cx="118" cy="95" r="6" fill="#000"/>
  <circle cx="138" cy="95" r="6" fill="#000"/>
  <path d="M118 110 Q128 115 138 110" stroke="#000" stroke-width="2" fill="none"/>
  <ellipse cx="128" cy="160" rx="30" ry="50" fill="{colors["primary"]}"/>'''
        elif "bunny" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <ellipse cx="100" cy="80" rx="20" ry="50" fill="{colors["primary"]}"/>
  <ellipse cx="156" cy="80" rx="20" ry="50" fill="{colors["primary"]}"/>
  <circle cx="128" cy="120" r="35" fill="{colors["primary"]}"/>
  <circle cx="118" cy="115" r="6" fill="#000"/>
  <circle cx="138" cy="115" r="6" fill="#000"/>
  <ellipse cx="128" cy="130" rx="8" ry="6" fill="#000"/>'''
        elif "panda" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="120" r="50" fill="#fff"/>
  <circle cx="100" cy="100" r="20" fill="#000"/>
  <circle cx="156" cy="100" r="20" fill="#000"/>
  <ellipse cx="128" cy="130" rx="12" ry="8" fill="#000"/>
  <circle cx="110" cy="110" r="6" fill="#fff"/>
  <circle cx="146" cy="110" r="6" fill="#fff"/>'''
        elif "fox" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="110" r="40" fill="#ff8c42"/>
  <path d="M128 70 L140 50 L128 60 L116 50 Z" fill="#ff8c42"/>
  <circle cx="118" cy="105" r="6" fill="#000"/>
  <circle cx="138" cy="105" r="6" fill="#000"/>
  <path d="M118 120 Q128 125 138 120" stroke="#000" stroke-width="2" fill="none"/>
  <ellipse cx="128" cy="160" rx="25" ry="40" fill="#ff8c42"/>'''
        elif "owl" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="120" r="50" fill="{colors["primary"]}"/>
  <circle cx="110" cy="110" r="20" fill="#fff"/>
  <circle cx="146" cy="110" r="20" fill="#fff"/>
  <circle cx="110" cy="110" r="10" fill="#000"/>
  <circle cx="146" cy="110" r="10" fill="#000"/>
  <path d="M100 130 Q128 140 156 130" stroke="#000" stroke-width="3" fill="none"/>'''
        elif "bear" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="100" r="45" fill="#8b4513"/>
  <circle cx="110" cy="95" r="8" fill="#000"/>
  <circle cx="146" cy="95" r="8" fill="#000"/>
  <ellipse cx="128" cy="110" rx="15" ry="10" fill="#000"/>
  <circle cx="128" cy="180" r="50" fill="#8b4513"/>'''
        elif "sloth" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="120" r="40" fill="#6b4423"/>
  <circle cx="118" cy="110" r="6" fill="#000"/>
  <circle cx="138" cy="110" r="6" fill="#000"/>
  <path d="M100 130 Q128 140 156 130" stroke="#000" stroke-width="2" fill="none"/>
  <path d="M128 160 L120 200 L128 190 L136 200 Z" fill="#6b4423"/>'''
        elif "penguin" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <ellipse cx="128" cy="140" rx="40" ry="60" fill="#000"/>
  <ellipse cx="128" cy="140" rx="30" ry="50" fill="#fff"/>
  <circle cx="118" cy="120" r="6" fill="#000"/>
  <circle cx="138" cy="120" r="6" fill="#000"/>
  <ellipse cx="128" cy="130" rx="8" ry="6" fill="#ff8c42"/>'''
        elif "hedgehog" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <ellipse cx="128" cy="140" rx="35" ry="50" fill="#8b7355"/>
  <path d="M100 100 L128 80 L156 100 L140 90 L128 85 L116 90 Z" fill="#8b7355"/>
  <circle cx="118" cy="130" r="5" fill="#000"/>
  <circle cx="138" cy="130" r="5" fill="#000"/>'''
        elif "raccoon" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="110" r="40" fill="#808080"/>
  <circle cx="110" cy="100" r="12" fill="#000"/>
  <circle cx="146" cy="100" r="12" fill="#000"/>
  <circle cx="110" cy="100" r="6" fill="#fff"/>
  <circle cx="146" cy="100" r="6" fill="#fff"/>
  <path d="M118 120 Q128 125 138 120" stroke="#000" stroke-width="2" fill="none"/>'''
        elif "whale" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <ellipse cx="128" cy="140" rx="60" ry="50" fill="#4a90e2"/>
  <path d="M68 140 Q50 120 50 100 Q50 80 68 80" fill="#4a90e2"/>
  <circle cx="110" cy="130" r="8" fill="#fff"/>
  <path d="M180 120 L200 100 M180 160 L200 180" stroke="#4a90e2" stroke-width="8" stroke-linecap="round"/>'''
        else:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="128" r="50" fill="{colors["primary"]}"/>'''
    
    elif theme == "cosmic":
        if "shooting_star" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <path d="M60 60 L200 200" stroke="{colors["primary"]}" stroke-width="6" stroke-linecap="round" filter="url(#glow)"/>
  <circle cx="200" cy="200" r="15" fill="{colors["primary"]}" filter="url(#glow)"/>
  <path d="M180 180 L200 200 L190 195 L195 200 Z" fill="{colors["secondary"]}" opacity="0.8"/>'''
        elif "galaxy" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="128" r="80" fill="url(#galaxyGrad)" filter="url(#glow)"/>
  <circle cx="100" cy="100" r="20" fill="{colors["secondary"]}" opacity="0.6" filter="url(#glow)"/>
  <circle cx="156" cy="156" r="25" fill="{colors["accent"]}" opacity="0.5" filter="url(#glow)"/>'''
        elif "moon" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <path d="M128 60 Q180 128 128 196 Q76 128 128 60 Z" 
        fill="{colors["primary"]}" filter="url(#glow)" opacity="0.9"/>
  <circle cx="140" cy="120" r="30" fill="{colors["bg"]}" opacity="0.3"/>'''
        elif "planet" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="128" r="50" fill="{colors["primary"]}" filter="url(#glow)"/>
  <ellipse cx="128" cy="128" rx="70" ry="8" fill="{colors["secondary"]}" opacity="0.6"/>
  <ellipse cx="128" cy="128" rx="70" ry="8" fill="{colors["secondary"]}" opacity="0.6" transform="rotate(45 128 128)"/>'''
        elif "constellation" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="100" cy="80" r="4" fill="{colors["primary"]}" filter="url(#glow)"/>
  <circle cx="156" cy="80" r="4" fill="{colors["primary"]}" filter="url(#glow)"/>
  <circle cx="80" cy="140" r="4" fill="{colors["primary"]}" filter="url(#glow)"/>
  <circle cx="176" cy="140" r="4" fill="{colors["primary"]}" filter="url(#glow)"/>
  <circle cx="128" cy="180" r="4" fill="{colors["primary"]}" filter="url(#glow)"/>
  <path d="M100 80 L156 80 L80 140 L176 140 L128 180" 
        stroke="{colors["secondary"]}" stroke-width="2" fill="none" opacity="0.6"/>'''
        elif "comet" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="180" cy="80" r="12" fill="{colors["primary"]}" filter="url(#glow)"/>
  <path d="M180 80 L60 200" stroke="{colors["secondary"]}" stroke-width="8" stroke-linecap="round" opacity="0.8"/>
  <path d="M180 80 L80 180" stroke="{colors["accent"]}" stroke-width="4" stroke-linecap="round" opacity="0.6"/>'''
        elif "nebula" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <ellipse cx="128" cy="128" rx="80" ry="60" fill="{colors["primary"]}" opacity="0.6" filter="url(#glow)"/>
  <ellipse cx="100" cy="100" rx="40" ry="30" fill="{colors["secondary"]}" opacity="0.5"/>
  <ellipse cx="156" cy="156" rx="40" ry="30" fill="{colors["accent"]}" opacity="0.5"/>'''
        elif "astronaut" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="100" r="35" fill="#fff"/>
  <circle cx="128" cy="100" r="30" fill="none" stroke="#000" stroke-width="2"/>
  <circle cx="118" cy="95" r="4" fill="#000"/>
  <circle cx="138" cy="95" r="4" fill="#000"/>
  <path d="M118 105 Q128 110 138 105" stroke="#000" stroke-width="2" fill="none"/>
  <ellipse cx="128" cy="180" rx="40" ry="50" fill="#fff"/>'''
        elif "rocket" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <path d="M128 60 L110 200 L128 190 L146 200 Z" fill="{colors["primary"]}" filter="url(#glow)"/>
  <circle cx="128" cy="80" r="15" fill="{colors["secondary"]}"/>
  <path d="M110 200 L100 220 L110 210 M146 200 L156 220 L146 210" 
        stroke="{colors["accent"]}" stroke-width="4" stroke-linecap="round"/>'''
        elif "meteor" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="180" cy="80" r="20" fill="{colors["primary"]}" filter="url(#glow)"/>
  <path d="M180 80 L40 220" stroke="{colors["secondary"]}" stroke-width="12" stroke-linecap="round" opacity="0.9"/>
  <path d="M180 80 L60 200" stroke="{colors["accent"]}" stroke-width="6" stroke-linecap="round" opacity="0.7"/>'''
        elif "solar_system" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="128" r="15" fill="{colors["primary"]}" filter="url(#glow)"/>
  <circle cx="80" cy="128" r="8" fill="{colors["secondary"]}"/>
  <circle cx="176" cy="128" r="10" fill="{colors["accent"]}"/>
  <circle cx="128" cy="80" r="6" fill="{colors["primary"]}"/>
  <circle cx="128" cy="176" r="7" fill="{colors["secondary"]}"/>
  <path d="M80 128 A48 48 0 1 1 176 128" stroke="{colors["primary"]}" stroke-width="2" fill="none" opacity="0.3"/>'''
        elif "aurora" in sticker_id:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <path d="M0 100 Q64 80 128 100 T256 100" 
        stroke="{colors["primary"]}" stroke-width="8" fill="none" filter="url(#glow)" opacity="0.8"/>
  <path d="M0 140 Q64 120 128 140 T256 140" 
        stroke="{colors["secondary"]}" stroke-width="8" fill="none" filter="url(#glow)" opacity="0.7"/>
  <path d="M0 180 Q64 160 128 180 T256 180" 
        stroke="{colors["accent"]}" stroke-width="8" fill="none" filter="url(#glow)" opacity="0.6"/>'''
        else:
            content = f'''  <rect width="256" height="256" fill="{colors["bg"]}"/>
  <circle cx="128" cy="128" r="50" fill="{colors["primary"]}" filter="url(#glow)" opacity="0.8"/>'''
    
    return base_svg.format(content=content)

def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python tools/generate_sticker_svgs.py <pack_id> <theme>", file=sys.stderr)
        print("Themes: cyberpunk, cute, cosmic", file=sys.stderr)
        return 1
    
    pack_id = sys.argv[1]
    theme = sys.argv[2]
    
    pack_dir = Path(f"packs/sticker_packs/{pack_id}")
    sticker_pack_json = pack_dir / "sticker-pack.json"
    
    if not sticker_pack_json.exists():
        print(f"Error: {sticker_pack_json} not found", file=sys.stderr)
        return 1
    
    with open(sticker_pack_json, "r", encoding="utf-8") as f:
        pack_data = json.load(f)
    
    stickers_dir = pack_dir / "stickers"
    stickers_dir.mkdir(parents=True, exist_ok=True)
    
    for sticker in pack_data.get("stickers", []):
        sticker_id = sticker.get("id", "")
        svg = generate_sticker_svg(sticker_id, theme)
        svg_path = stickers_dir / sticker.get("src", "").replace("stickers/", "")
        svg_path.write_text(svg, encoding="utf-8")
        print(f"Generated: {svg_path}")
    
    print(f"Generated {len(pack_data.get('stickers', []))} stickers for {pack_id}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
