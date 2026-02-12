#!/usr/bin/env python3
"""Generate remaining arcade-themed cards with varied designs."""
from pathlib import Path

CARDS_DIR = Path(__file__).parent.parent / 'packs' / 'arcade_love_90s' / 'assets' / 'cards'

# Card designs with different arcade themes
DESIGNS = [
    # 09 - Pixel art explosion
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s9" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s9)"/>
  <g transform="translate(450, 300)">
    <rect x="-20" y="-20" width="10" height="10" fill="#ff00ff"/>
    <rect x="-10" y="-20" width="10" height="10" fill="#00ffff"/>
    <rect x="0" y="-20" width="10" height="10" fill="#ff00ff"/>
    <rect x="10" y="-20" width="10" height="10" fill="#00ffff"/>
    <rect x="20" y="-20" width="10" height="10" fill="#ff00ff"/>
    <rect x="-20" y="-10" width="10" height="10" fill="#00ffff"/>
    <rect x="-10" y="-10" width="10" height="10" fill="#ff00ff"/>
    <rect x="0" y="-10" width="10" height="10" fill="#00ff41"/>
    <rect x="10" y="-10" width="10" height="10" fill="#ff00ff"/>
    <rect x="20" y="-10" width="10" height="10" fill="#00ffff"/>
    <rect x="-20" y="0" width="10" height="10" fill="#ff00ff"/>
    <rect x="-10" y="0" width="10" height="10" fill="#00ff41"/>
    <rect x="0" y="0" width="10" height="10" fill="#ffff00"/>
    <rect x="10" y="0" width="10" height="10" fill="#00ff41"/>
    <rect x="20" y="0" width="10" height="10" fill="#ff00ff"/>
    <rect x="-20" y="10" width="10" height="10" fill="#00ffff"/>
    <rect x="-10" y="10" width="10" height="10" fill="#ff00ff"/>
    <rect x="0" y="10" width="10" height="10" fill="#00ff41"/>
    <rect x="10" y="10" width="10" height="10" fill="#ff00ff"/>
    <rect x="20" y="10" width="10" height="10" fill="#00ffff"/>
    <rect x="-20" y="20" width="10" height="10" fill="#ff00ff"/>
    <rect x="-10" y="20" width="10" height="10" fill="#00ffff"/>
    <rect x="0" y="20" width="10" height="10" fill="#ff00ff"/>
    <rect x="10" y="20" width="10" height="10" fill="#00ffff"/>
    <rect x="20" y="20" width="10" height="10" fill="#ff00ff"/>
  </g>
  <text x="450" y="200" font-family="monospace" font-size="32" fill="#00ffff" text-anchor="middle" font-weight="bold">BONUS ROUND</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 10 - Score multiplier
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s10" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s10)"/>
  <rect x="300" y="200" width="300" height="200" fill="#000" stroke="#00ffff" stroke-width="3"/>
  <text x="450" y="260" font-family="monospace" font-size="24" fill="#00ff41" text-anchor="middle">SCORE</text>
  <text x="450" y="320" font-family="monospace" font-size="56" fill="#ff00ff" text-anchor="middle" font-weight="bold">x2</text>
  <text x="450" y="360" font-family="monospace" font-size="20" fill="#00ffff" text-anchor="middle">MULTIPLIER</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 11 - Power-up
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s11" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s11)"/>
  <circle cx="450" cy="300" r="80" fill="#ff00ff" opacity="0.3" stroke="#00ffff" stroke-width="3"/>
  <circle cx="450" cy="300" r="60" fill="#00ff41" opacity="0.2" stroke="#ff00ff" stroke-width="2"/>
  <circle cx="450" cy="300" r="40" fill="#00ffff" opacity="0.4" stroke="#00ff41" stroke-width="2"/>
  <text x="450" y="310" font-family="monospace" font-size="32" fill="#fff" text-anchor="middle" font-weight="bold">POWER</text>
  <text x="450" y="200" font-family="monospace" font-size="36" fill="#00ffff" text-anchor="middle" font-weight="bold">POWER-UP</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 12 - Lives display
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s12" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s12)"/>
  <text x="450" y="200" font-family="monospace" font-size="36" fill="#00ffff" text-anchor="middle" font-weight="bold">LIVES</text>
  <g transform="translate(350, 280)">
    <path d="M 0 0 L 10 -15 L 20 0 L 10 20 Z" fill="#ff00ff"/>
  </g>
  <g transform="translate(450, 280)">
    <path d="M 0 0 L 10 -15 L 20 0 L 10 20 Z" fill="#ff00ff"/>
  </g>
  <g transform="translate(550, 280)">
    <path d="M 0 0 L 10 -15 L 20 0 L 10 20 Z" fill="#ff00ff"/>
  </g>
  <text x="450" y="380" font-family="monospace" font-size="24" fill="#00ff41" text-anchor="middle">x ∞</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 13 - Arcade marquee
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s13" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s13)"/>
  <rect x="100" y="100" width="700" height="80" fill="#1a1a2e" stroke="#00ffff" stroke-width="3"/>
  <rect x="120" y="120" width="660" height="40" fill="#000" stroke="#ff00ff" stroke-width="2"/>
  <text x="450" y="150" font-family="monospace" font-size="28" fill="#00ffff" text-anchor="middle" font-weight="bold">LOVE QUEST</text>
  <rect x="200" y="250" width="500" height="200" fill="#000" stroke="#00ff41" stroke-width="2"/>
  <text x="450" y="350" font-family="monospace" font-size="32" fill="#ff00ff" text-anchor="middle">READY</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 14 - Button mash
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s14" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s14)"/>
  <circle cx="300" cy="300" r="50" fill="#ff00ff" stroke="#fff" stroke-width="3"/>
  <circle cx="450" cy="300" r="50" fill="#00ffff" stroke="#fff" stroke-width="3"/>
  <circle cx="600" cy="300" r="50" fill="#00ff41" stroke="#fff" stroke-width="3"/>
  <text x="300" y="310" font-family="monospace" font-size="20" fill="#fff" text-anchor="middle" font-weight="bold">A</text>
  <text x="450" y="310" font-family="monospace" font-size="20" fill="#000" text-anchor="middle" font-weight="bold">B</text>
  <text x="600" y="310" font-family="monospace" font-size="20" fill="#000" text-anchor="middle" font-weight="bold">C</text>
  <text x="450" y="200" font-family="monospace" font-size="32" fill="#00ffff" text-anchor="middle" font-weight="bold">MASH BUTTONS</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 15 - Combo meter
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s15" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s15)"/>
  <rect x="300" y="200" width="300" height="40" fill="#000" stroke="#00ffff" stroke-width="2"/>
  <rect x="310" y="210" width="280" height="20" fill="#00ff41"/>
  <text x="450" y="280" font-family="monospace" font-size="36" fill="#00ffff" text-anchor="middle" font-weight="bold">COMBO x50</text>
  <text x="450" y="330" font-family="monospace" font-size="24" fill="#ff00ff" text-anchor="middle">PERFECT MATCH</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 16 - Achievement unlock
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s16" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s16)"/>
  <rect x="300" y="200" width="300" height="200" fill="#000" stroke="#ffff00" stroke-width="4"/>
  <text x="450" y="250" font-family="monospace" font-size="24" fill="#ffff00" text-anchor="middle">ACHIEVEMENT</text>
  <text x="450" y="300" font-family="monospace" font-size="32" fill="#00ffff" text-anchor="middle" font-weight="bold">UNLOCKED</text>
  <text x="450" y="350" font-family="monospace" font-size="20" fill="#ff00ff" text-anchor="middle">TRUE LOVE</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 17 - Loading screen
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s17" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s17)"/>
  <rect x="200" y="250" width="500" height="100" fill="#000" stroke="#00ffff" stroke-width="2"/>
  <rect x="220" y="270" width="460" height="20" fill="#00ff41"/>
  <text x="450" y="320" font-family="monospace" font-size="24" fill="#00ffff" text-anchor="middle">LOADING...</text>
  <text x="450" y="200" font-family="monospace" font-size="32" fill="#ff00ff" text-anchor="middle" font-weight="bold">LOADING LOVE</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 18 - Boss battle
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s18" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s18)"/>
  <rect x="250" y="150" width="400" height="300" fill="#000" stroke="#ff00ff" stroke-width="4"/>
  <text x="450" y="220" font-family="monospace" font-size="28" fill="#ff00ff" text-anchor="middle">BOSS BATTLE</text>
  <rect x="300" y="280" width="300" height="40" fill="#1a1a2e" stroke="#00ffff" stroke-width="2"/>
  <rect x="310" y="290" width="280" height="20" fill="#00ff41"/>
  <text x="450" y="320" font-family="monospace" font-size="24" fill="#00ffff" text-anchor="middle">HP: 100%</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 19 - Pause menu
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s19" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s19)"/>
  <rect x="300" y="200" width="300" height="200" fill="#000" stroke="#00ffff" stroke-width="3"/>
  <text x="450" y="250" font-family="monospace" font-size="36" fill="#00ffff" text-anchor="middle" font-weight="bold">PAUSED</text>
  <text x="450" y="300" font-family="monospace" font-size="24" fill="#ff00ff" text-anchor="middle">PRESS START</text>
  <text x="450" y="340" font-family="monospace" font-size="20" fill="#00ff41" text-anchor="middle">TO RESUME</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 20 - Extra life
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s20" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s20)"/>
  <circle cx="450" cy="300" r="100" fill="#ff00ff" opacity="0.2" stroke="#00ffff" stroke-width="4"/>
  <path d="M 450 250 L 470 290 L 510 300 L 480 330 L 490 370 L 450 350 L 410 370 L 420 330 L 390 300 L 430 290 Z" fill="#ff00ff" stroke="#00ffff" stroke-width="2"/>
  <text x="450" y="200" font-family="monospace" font-size="32" fill="#00ffff" text-anchor="middle" font-weight="bold">EXTRA LIFE</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 21 - Time attack
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s21" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s21)"/>
  <rect x="300" y="200" width="300" height="200" fill="#000" stroke="#ffff00" stroke-width="3"/>
  <text x="450" y="250" font-family="monospace" font-size="24" fill="#ffff00" text-anchor="middle">TIME</text>
  <text x="450" y="300" font-family="monospace" font-size="48" fill="#00ffff" text-anchor="middle" font-weight="bold">∞</text>
  <text x="450" y="350" font-family="monospace" font-size="20" fill="#ff00ff" text-anchor="middle">FOREVER</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 22 - Perfect score
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s22" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s22)"/>
  <rect x="200" y="150" width="500" height="300" fill="#000" stroke="#00ff41" stroke-width="4"/>
  <text x="450" y="220" font-family="monospace" font-size="28" fill="#00ff41" text-anchor="middle">PERFECT</text>
  <text x="450" y="280" font-family="monospace" font-size="56" fill="#00ffff" text-anchor="middle" font-weight="bold">100%</text>
  <text x="450" y="340" font-family="monospace" font-size="24" fill="#ff00ff" text-anchor="middle">COMPLETE</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 23 - New record
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s23" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s23)"/>
  <rect x="250" y="200" width="400" height="200" fill="#000" stroke="#ffff00" stroke-width="4"/>
  <text x="450" y="260" font-family="monospace" font-size="32" fill="#ffff00" text-anchor="middle" font-weight="bold">NEW RECORD!</text>
  <text x="450" y="320" font-family="monospace" font-size="24" fill="#00ffff" text-anchor="middle">BEST MATCH</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
    
    # 24 - Game complete
    '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs><pattern id="s24" patternUnits="userSpaceOnUse" width="2" height="2"><rect width="2" height="1" fill="#00ff41" opacity="0.08"/></pattern></defs>
  <rect width="900" height="600" fill="#0a0a1a"/>
  <rect width="900" height="600" fill="url(#s24)"/>
  <rect x="150" y="150" width="600" height="300" fill="#000" stroke="#00ff41" stroke-width="4"/>
  <text x="450" y="230" font-family="monospace" font-size="36" fill="#00ff41" text-anchor="middle" font-weight="bold">GAME COMPLETE</text>
  <text x="450" y="290" font-family="monospace" font-size="28" fill="#00ffff" text-anchor="middle">THANK YOU</text>
  <text x="450" y="340" font-family="monospace" font-size="24" fill="#ff00ff" text-anchor="middle">FOR PLAYING</text>
  <text x="450" y="550" font-family="monospace" font-size="14" fill="#00ff41" text-anchor="middle" opacity="0.6">HAPPY VALENTINE'S</text>
</svg>''',
]

def main():
    print(f"Writing to: {CARDS_DIR}")
    for i, design in enumerate(DESIGNS, start=9):
        card_num = f"{i:02d}"
        file_path = CARDS_DIR / f"al90-{card_num}.svg"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(design)
            print(f"✓ Created: al90-{card_num}.svg")
        except Exception as e:
            print(f"✗ Error creating al90-{card_num}.svg: {e}")

if __name__ == '__main__':
    main()
