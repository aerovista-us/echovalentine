#!/usr/bin/env python3
"""Generate anti-love cards with varied designs."""
from pathlib import Path

CARDS_DIR = Path(__file__).parent.parent / 'packs' / 'anti_love' / 'assets' / 'cards'

# Anti-love card designs with varied layouts
DESIGNS = [
    # 01 - Broken heart
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#000"/>
  <path d="M 450 200 L 500 250 L 550 200 L 500 300 L 450 350 L 400 300 L 350 200 L 400 250 Z" fill="none" stroke="#ff1493" stroke-width="4" stroke-dasharray="10 5"/>
  <line x1="400" y1="250" x2="500" y2="300" stroke="#ff1493" stroke-width="3"/>
  <text x="450" y="450" font-family="sans-serif" font-size="36" fill="#ff1493" text-anchor="middle" font-weight="bold">Be Mine? ❌</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 02 - X marks
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#1a1a1a"/>
  <line x1="300" y1="200" x2="600" y2="400" stroke="#ff1493" stroke-width="6"/>
  <line x1="600" y1="200" x2="300" y2="400" stroke="#ff1493" stroke-width="6"/>
  <circle cx="450" cy="300" r="120" fill="none" stroke="#ff1493" stroke-width="4" stroke-dasharray="8 8"/>
  <text x="450" y="500" font-family="sans-serif" font-size="32" fill="#ff1493" text-anchor="middle" font-weight="bold">I'm The Prize</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 03 - Diagonal split
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#000"/>
  <polygon points="0,0 900,600 900,0" fill="#ff1493" opacity="0.2"/>
  <polygon points="0,0 0,600 900,600" fill="#1a1a1a"/>
  <text x="450" y="280" font-family="sans-serif" font-size="40" fill="#ff1493" text-anchor="middle" font-weight="bold">NO THANKS</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 04 - Grid pattern
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#0b0d12"/>
  <g opacity="0.3">
    <line x1="0" y1="150" x2="900" y2="150" stroke="#ff1493" stroke-width="2"/>
    <line x1="0" y1="300" x2="900" y2="300" stroke="#ff1493" stroke-width="2"/>
    <line x1="0" y1="450" x2="900" y2="450" stroke="#ff1493" stroke-width="2"/>
    <line x1="225" y1="0" x2="225" y2="600" stroke="#ff1493" stroke-width="2"/>
    <line x1="450" y1="0" x2="450" y2="600" stroke="#ff1493" stroke-width="2"/>
    <line x1="675" y1="0" x2="675" y2="600" stroke="#ff1493" stroke-width="2"/>
  </g>
  <text x="450" y="300" font-family="sans-serif" font-size="36" fill="#ff1493" text-anchor="middle" font-weight="bold">PASS</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 05 - Shattered
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#000"/>
  <path d="M 450 200 L 480 240 L 520 220 L 500 260 L 540 280 L 500 320 L 460 300 L 440 340 L 420 300 L 380 320 L 400 280 L 360 260 L 400 240 L 420 200 Z" fill="none" stroke="#ff1493" stroke-width="3" stroke-dasharray="5 5"/>
  <line x1="420" y1="240" x2="480" y2="260" stroke="#ff1493" stroke-width="2"/>
  <line x1="400" y1="280" x2="500" y2="300" stroke="#ff1493" stroke-width="2"/>
  <text x="450" y="450" font-family="sans-serif" font-size="32" fill="#ff1493" text-anchor="middle" font-weight="bold">BROKEN</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 06 - Minimalist X
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#1a1a1a"/>
  <line x1="350" y1="200" x2="550" y2="400" stroke="#ff1493" stroke-width="8"/>
  <line x1="550" y1="200" x2="350" y2="400" stroke="#ff1493" stroke-width="8"/>
  <text x="450" y="500" font-family="sans-serif" font-size="28" fill="#ff1493" text-anchor="middle" font-weight="bold">NOT TODAY</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 07 - Zigzag
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#000"/>
  <polyline points="200,300 250,250 300,300 350,250 400,300 450,250 500,300 550,250 600,300 650,250 700,300" fill="none" stroke="#ff1493" stroke-width="6"/>
  <text x="450" y="450" font-family="sans-serif" font-size="36" fill="#ff1493" text-anchor="middle" font-weight="bold">NOPE</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 08 - Circles
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#0b0d12"/>
  <circle cx="300" cy="250" r="60" fill="none" stroke="#ff1493" stroke-width="4"/>
  <circle cx="600" cy="250" r="60" fill="none" stroke="#ff1493" stroke-width="4"/>
  <circle cx="450" cy="350" r="80" fill="none" stroke="#ff1493" stroke-width="4" stroke-dasharray="10 5"/>
  <text x="450" y="500" font-family="sans-serif" font-size="32" fill="#ff1493" text-anchor="middle" font-weight="bold">SKIP</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 09 - Stripe pattern
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#000"/>
  <rect x="0" y="0" width="900" height="60" fill="#ff1493" opacity="0.3"/>
  <rect x="0" y="120" width="900" height="60" fill="#ff1493" opacity="0.3"/>
  <rect x="0" y="240" width="900" height="60" fill="#ff1493" opacity="0.3"/>
  <rect x="0" y="360" width="900" height="60" fill="#ff1493" opacity="0.3"/>
  <rect x="0" y="480" width="900" height="60" fill="#ff1493" opacity="0.3"/>
  <text x="450" y="320" font-family="sans-serif" font-size="40" fill="#ff1493" text-anchor="middle" font-weight="bold">HARD PASS</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 10 - Corner X
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#1a1a1a"/>
  <line x1="100" y1="100" x2="200" y2="200" stroke="#ff1493" stroke-width="6"/>
  <line x1="200" y1="100" x2="100" y2="200" stroke="#ff1493" stroke-width="6"/>
  <line x1="700" y1="400" x2="800" y2="500" stroke="#ff1493" stroke-width="6"/>
  <line x1="800" y1="400" x2="700" y2="500" stroke="#ff1493" stroke-width="6"/>
  <text x="450" y="300" font-family="sans-serif" font-size="36" fill="#ff1493" text-anchor="middle" font-weight="bold">DECLINED</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 11 - Wavy lines
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#000"/>
  <path d="M 100 200 Q 250 150, 400 200 T 700 200" fill="none" stroke="#ff1493" stroke-width="4"/>
  <path d="M 100 300 Q 250 250, 400 300 T 700 300" fill="none" stroke="#ff1493" stroke-width="4"/>
  <path d="M 100 400 Q 250 350, 400 400 T 700 400" fill="none" stroke="#ff1493" stroke-width="4"/>
  <text x="450" y="500" font-family="sans-serif" font-size="32" fill="#ff1493" text-anchor="middle" font-weight="bold">NAH</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 12 - Boxed X
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#0b0d12"/>
  <rect x="300" y="200" width="300" height="200" fill="none" stroke="#ff1493" stroke-width="5"/>
  <line x1="350" y1="250" x2="550" y2="350" stroke="#ff1493" stroke-width="6"/>
  <line x1="550" y1="250" x2="350" y2="350" stroke="#ff1493" stroke-width="6"/>
  <text x="450" y="500" font-family="sans-serif" font-size="28" fill="#ff1493" text-anchor="middle" font-weight="bold">REJECTED</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 13 - Radial lines
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#1a1a1a"/>
  <line x1="450" y1="300" x2="300" y2="150" stroke="#ff1493" stroke-width="3"/>
  <line x1="450" y1="300" x2="600" y2="150" stroke="#ff1493" stroke-width="3"/>
  <line x1="450" y1="300" x2="300" y2="450" stroke="#ff1493" stroke-width="3"/>
  <line x1="450" y1="300" x2="600" y2="450" stroke="#ff1493" stroke-width="3"/>
  <circle cx="450" cy="300" r="80" fill="none" stroke="#ff1493" stroke-width="4"/>
  <text x="450" y="500" font-family="sans-serif" font-size="32" fill="#ff1493" text-anchor="middle" font-weight="bold">NO WAY</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 14 - Checkered
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#000"/>
  <rect x="200" y="150" width="50" height="50" fill="#ff1493" opacity="0.3"/>
  <rect x="300" y="200" width="50" height="50" fill="#ff1493" opacity="0.3"/>
  <rect x="400" y="150" width="50" height="50" fill="#ff1493" opacity="0.3"/>
  <rect x="500" y="200" width="50" height="50" fill="#ff1493" opacity="0.3"/>
  <rect x="600" y="150" width="50" height="50" fill="#ff1493" opacity="0.3"/>
  <rect x="250" y="250" width="50" height="50" fill="#ff1493" opacity="0.3"/>
  <rect x="350" y="300" width="50" height="50" fill="#ff1493" opacity="0.3"/>
  <rect x="450" y="250" width="50" height="50" fill="#ff1493" opacity="0.3"/>
  <rect x="550" y="300" width="50" height="50" fill="#ff1493" opacity="0.3"/>
  <text x="450" y="450" font-family="sans-serif" font-size="36" fill="#ff1493" text-anchor="middle" font-weight="bold">DENIED</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 15 - Arrow down
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#0b0d12"/>
  <polygon points="400,200 450,250 500,200 475,200 475,350 425,350 425,200" fill="#ff1493"/>
  <text x="450" y="450" font-family="sans-serif" font-size="32" fill="#ff1493" text-anchor="middle" font-weight="bold">DOWN</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 16 - Slash pattern
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#1a1a1a"/>
  <line x1="200" y1="150" x2="700" y2="450" stroke="#ff1493" stroke-width="8"/>
  <line x1="250" y1="150" x2="750" y2="450" stroke="#ff1493" stroke-width="6" opacity="0.5"/>
  <line x1="150" y1="150" x2="650" y2="450" stroke="#ff1493" stroke-width="6" opacity="0.5"/>
  <text x="450" y="500" font-family="sans-serif" font-size="36" fill="#ff1493" text-anchor="middle" font-weight="bold">CANCELLED</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 17 - Hexagon
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#000"/>
  <polygon points="450,200 550,250 550,350 450,400 350,350 350,250" fill="none" stroke="#ff1493" stroke-width="5"/>
  <line x1="400" y1="275" x2="500" y2="325" stroke="#ff1493" stroke-width="4"/>
  <line x1="500" y1="275" x2="400" y2="325" stroke="#ff1493" stroke-width="4"/>
  <text x="450" y="500" font-family="sans-serif" font-size="28" fill="#ff1493" text-anchor="middle" font-weight="bold">BLOCKED</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 18 - Dots
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#0b0d12"/>
  <circle cx="300" cy="200" r="15" fill="#ff1493"/>
  <circle cx="450" cy="200" r="15" fill="#ff1493"/>
  <circle cx="600" cy="200" r="15" fill="#ff1493"/>
  <circle cx="300" cy="300" r="15" fill="#ff1493"/>
  <circle cx="450" cy="300" r="15" fill="#ff1493"/>
  <circle cx="600" cy="300" r="15" fill="#ff1493"/>
  <circle cx="300" cy="400" r="15" fill="#ff1493"/>
  <circle cx="450" cy="400" r="15" fill="#ff1493"/>
  <circle cx="600" cy="400" r="15" fill="#ff1493"/>
  <text x="450" y="500" font-family="sans-serif" font-size="32" fill="#ff1493" text-anchor="middle" font-weight="bold">VOID</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 19 - Triangle
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#1a1a1a"/>
  <polygon points="450,200 600,400 300,400" fill="none" stroke="#ff1493" stroke-width="6"/>
  <line x1="400" y1="320" x2="500" y2="320" stroke="#ff1493" stroke-width="4"/>
  <text x="450" y="500" font-family="sans-serif" font-size="28" fill="#ff1493" text-anchor="middle" font-weight="bold">STOP</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 20 - Parallel lines
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#000"/>
  <line x1="250" y1="200" x2="650" y2="200" stroke="#ff1493" stroke-width="6"/>
  <line x1="250" y1="250" x2="650" y2="250" stroke="#ff1493" stroke-width="6"/>
  <line x1="250" y1="300" x2="650" y2="300" stroke="#ff1493" stroke-width="6"/>
  <line x1="250" y1="350" x2="650" y2="350" stroke="#ff1493" stroke-width="6"/>
  <text x="450" y="450" font-family="sans-serif" font-size="36" fill="#ff1493" text-anchor="middle" font-weight="bold">OUT</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 21 - Crosshair
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#0b0d12"/>
  <line x1="450" y1="150" x2="450" y2="450" stroke="#ff1493" stroke-width="4"/>
  <line x1="250" y1="300" x2="650" y2="300" stroke="#ff1493" stroke-width="4"/>
  <circle cx="450" cy="300" r="100" fill="none" stroke="#ff1493" stroke-width="3"/>
  <circle cx="450" cy="300" r="50" fill="none" stroke="#ff1493" stroke-width="2"/>
  <text x="450" y="500" font-family="sans-serif" font-size="28" fill="#ff1493" text-anchor="middle" font-weight="bold">TARGET</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 22 - Bars
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#1a1a1a"/>
  <rect x="300" y="200" width="40" height="200" fill="#ff1493"/>
  <rect x="380" y="220" width="40" height="180" fill="#ff1493"/>
  <rect x="460" y="180" width="40" height="220" fill="#ff1493"/>
  <rect x="540" y="240" width="40" height="160" fill="#ff1493"/>
  <text x="450" y="500" font-family="sans-serif" font-size="32" fill="#ff1493" text-anchor="middle" font-weight="bold">ZERO</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 23 - Spiral
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#000"/>
  <path d="M 450 300 A 50 50 0 1 1 500 300 A 100 100 0 1 1 350 300 A 150 150 0 1 1 600 300" fill="none" stroke="#ff1493" stroke-width="4"/>
  <text x="450" y="500" font-family="sans-serif" font-size="28" fill="#ff1493" text-anchor="middle" font-weight="bold">SPIRAL</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 24 - Final X
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <rect width="900" height="600" fill="#0b0d12"/>
  <rect x="200" y="150" width="500" height="300" fill="none" stroke="#ff1493" stroke-width="6"/>
  <line x1="250" y1="200" x2="650" y2="400" stroke="#ff1493" stroke-width="8"/>
  <line x1="650" y1="200" x2="250" y2="400" stroke="#ff1493" stroke-width="8"/>
  <text x="450" y="500" font-family="sans-serif" font-size="32" fill="#ff1493" text-anchor="middle" font-weight="bold">FINAL ANSWER</text>
  <text x="450" y="550" font-family="sans-serif" font-size="14" fill="#fff" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
]

def main():
    for i, design in enumerate(DESIGNS, start=1):
        card_num = f"{i:02d}"
        file_path = CARDS_DIR / f"albp-{card_num}.svg"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(design)
        print(f"Created: albp-{card_num}.svg")

if __name__ == '__main__':
    main()
