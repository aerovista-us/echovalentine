#!/usr/bin/env python3
"""
Upgrade sticker SVGs to be more detailed and dynamic with animations.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

def upgrade_neon_heart_svg(content: str) -> str:
    """Upgrade neon heart sticker with pulsing animation."""
    if '<animate' in content:
        return content  # Already upgraded
    
    # Add animated gradient and pulsing
    upgraded = content.replace(
        '<radialGradient id="g"',
        '''<radialGradient id="g">
      <animate attributeName="r" values="60%;80%;60%" dur="2s" repeatCount="indefinite"/>
      <stop offset="0%" stop-color="#ff7ad9" stop-opacity="1">
        <animate attributeName="stop-opacity" values="1;0.9;1" dur="1.5s" repeatCount="indefinite"/>
      </stop>'''
    )
    
    # Add pulsing animation to heart
    upgraded = upgraded.replace(
        'filter="url(#glow)"',
        '''filter="url(#glow)">
      <animate attributeName="opacity" values="0.9;1;0.9" dur="2s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="scale" values="1;1.05;1" dur="2s" repeatCount="indefinite"/>'''
    )
    
    return upgraded

def upgrade_cyberpunk_svg(content: str, sticker_id: str) -> str:
    """Upgrade cyberpunk stickers with dynamic effects."""
    if '<animate' in content:
        return content
    
    upgraded = content
    
    # Add animated grid lines
    if "grid" in sticker_id:
        upgraded = upgraded.replace(
            '<g stroke="#00e5ff"',
            '''<g stroke="#00e5ff">
      <animate attributeName="opacity" values="0.6;0.9;0.6" dur="3s" repeatCount="indefinite"/>'''
        )
        upgraded = upgraded.replace(
            '<circle cx="128"',
            '''<circle cx="128">
      <animate attributeName="r" values="30;35;30" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.8;1;0.8" dur="1.5s" repeatCount="indefinite"/>'''
        )
    
    # Add animated circuit patterns
    elif "circuit" in sticker_id:
        upgraded = upgraded.replace(
            '<path d="M128',
            '''<path d="M128">
      <animate attributeName="stroke-dasharray" values="0,200;200,0" dur="2s" repeatCount="indefinite"/>'''
        )
    
    # Add glitch effect
    elif "glitch" in sticker_id:
        upgraded = upgraded.replace(
            '<path d="M128',
            '''<path d="M128">
      <animateTransform attributeName="transform" type="translate" values="0,0;2,-2;0,0;-2,2;0,0" dur="0.3s" repeatCount="indefinite"/>'''
        )
    
    return upgraded

def upgrade_cute_svg(content: str, sticker_id: str) -> str:
    """Upgrade cute critter stickers with subtle animations."""
    if '<animate' in content:
        return content
    
    upgraded = content
    
    # Add gentle breathing animation
    if any(x in sticker_id for x in ["puppy", "kitten", "bunny", "panda", "fox", "owl", "bear", "sloth", "penguin", "hedgehog", "raccoon", "whale"]):
        # Find main shape and add animation
        upgraded = re.sub(
            r'(<circle cx="128"[^>]*>)',
            r'\1\n      <animateTransform attributeName="transform" type="scale" values="1;1.03;1" dur="3s" repeatCount="indefinite" transform-origin="128 128"/>',
            upgraded,
            count=1
        )
        
        # Add blinking eyes
        upgraded = re.sub(
            r'(<circle cx="\d+" cy="\d+" r="\d+" fill="#000"/>)',
            r'\1\n      <animate attributeName="r" values="\2;0;\2" dur="4s" repeatCount="indefinite"/>',
            upgraded
        )
    
    return upgraded

def upgrade_cosmic_svg(content: str, sticker_id: str) -> str:
    """Upgrade cosmic stickers with dynamic space effects."""
    if '<animate' in content:
        return content
    
    upgraded = content
    
    # Shooting star trail animation
    if "shooting_star" in sticker_id:
        upgraded = upgraded.replace(
            '<path d="M60 60',
            '''<path d="M60 60">
      <animate attributeName="stroke-dasharray" values="0,300;300,0" dur="1.5s" repeatCount="indefinite"/>'''
        )
        upgraded = upgraded.replace(
            '<circle cx="200"',
            '''<circle cx="200">
      <animate attributeName="r" values="15;20;15" dur="1s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="0,0;10,10" dur="1.5s" repeatCount="indefinite"/>'''
        )
    
    # Rotating galaxy
    elif "galaxy" in sticker_id:
        upgraded = upgraded.replace(
            '<circle cx="128" cy="128" r="80"',
            '''<circle cx="128" cy="128" r="80">
      <animateTransform attributeName="transform" type="rotate" values="0 128 128;360 128 128" dur="20s" repeatCount="indefinite"/>'''
        )
    
    # Pulsing planets
    elif "planet" in sticker_id:
        upgraded = upgraded.replace(
            '<circle cx="128"',
            '''<circle cx="128">
      <animate attributeName="r" values="50;55;50" dur="3s" repeatCount="indefinite"/>'''
        )
    
    # Twinkling stars
    elif "constellation" in sticker_id:
        upgraded = re.sub(
            r'(<circle[^>]*fill="[^"]*primary[^"]*"[^>]*>)',
            r'\1\n      <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite" begin="\2s"/>',
            upgraded
        )
    
    return upgraded

def upgrade_sticker_file(svg_path: Path, pack_id: str) -> None:
    """Upgrade a single sticker SVG file."""
    try:
        content = svg_path.read_text(encoding="utf-8")
        
        sticker_id = svg_path.stem
        
        # Determine theme from pack_id
        if pack_id in ["neon_hearts", "arcade_icons", "witchy_moods"]:
            if "neon_hearts" == pack_id:
                upgraded = upgrade_neon_heart_svg(content)
            elif "arcade_icons" == pack_id:
                upgraded = upgrade_cyberpunk_svg(content, sticker_id)
            else:
                upgraded = content  # Keep witchy as is for now
        elif pack_id == "cyberpunk_vibes":
            upgraded = upgrade_cyberpunk_svg(content, sticker_id)
        elif pack_id == "cute_critters":
            upgraded = upgrade_cute_svg(content, sticker_id)
        elif pack_id == "cosmic_dreams":
            upgraded = upgrade_cosmic_svg(content, sticker_id)
        else:
            upgraded = content
        
        if upgraded != content:
            svg_path.write_text(upgraded, encoding="utf-8")
            print(f"Upgraded: {svg_path.name}")
        else:
            print(f"Skipped (already upgraded or no changes): {svg_path.name}")
            
    except Exception as e:
        print(f"Error upgrading {svg_path}: {e}")

def main():
    """Upgrade all sticker SVGs."""
    sticker_packs_dir = Path("packs/sticker_packs")
    
    for pack_dir in sticker_packs_dir.iterdir():
        if not pack_dir.is_dir() or pack_dir.name == "manifest.json":
            continue
        
        pack_id = pack_dir.name
        stickers_dir = pack_dir / "stickers"
        
        if not stickers_dir.exists():
            continue
        
        print(f"\nUpgrading {pack_id}...")
        for svg_file in stickers_dir.glob("*.svg"):
            upgrade_sticker_file(svg_file, pack_id)
    
    print("\nUpgrade complete!")

if __name__ == "__main__":
    main()
