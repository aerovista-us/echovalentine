#!/usr/bin/env python3
"""Add baseline overlay configs to all pack.json files that don't have them."""
import json
import os
from pathlib import Path

BASELINE_OVERLAY = {
    "toFrom": {
        "top": "57.5%",
        "gap": "2em",
        "fontSize": "clamp(14px, 3vw, 20px)",
        "color": "rgba(255,252,248,.98)"
    },
    "message": {
        "top": "62%",
        "width": "82%",
        "maxWidth": "90%",
        "fontSize": "clamp(17px, 4vw, 26px)",
        "color": "rgba(255,252,248,.98)"
    }
}

def add_overlay_to_pack(pack_path):
    """Add overlay config to a pack.json file if it doesn't have one."""
    with open(pack_path, 'r', encoding='utf-8') as f:
        pack = json.load(f)
    
    if 'overlay' in pack:
        return False  # Already has overlay
    
    pack['overlay'] = BASELINE_OVERLAY
    
    with open(pack_path, 'w', encoding='utf-8') as f:
        json.dump(pack, f, indent=2, ensure_ascii=False)
    
    return True

def main():
    packs_dir = Path(__file__).parent.parent / 'packs'
    updated = 0
    
    for pack_json in packs_dir.rglob('pack.json'):
        if add_overlay_to_pack(pack_json):
            print(f"Added overlay to: {pack_json.relative_to(packs_dir.parent)}")
            updated += 1
        else:
            print(f"Skipped (has overlay): {pack_json.relative_to(packs_dir.parent)}")
    
    print(f"\nUpdated {updated} pack files.")

if __name__ == '__main__':
    main()
