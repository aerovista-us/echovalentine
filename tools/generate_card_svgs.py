#!/usr/bin/env python3
"""
Generate per-card SVGs from cards/cards.json.

Usage:
  python tools/generate_card_svgs.py packs/yo_bro
  python tools/generate_card_svgs.py packs/dearest_mother
"""
from __future__ import annotations
import json, sys
from pathlib import Path

def xesc(s: str) -> str:
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def card_svg(front_text: str, subtitle: str, theme: str, footer: str):
    if theme == "yo":
        bg1,bg2,accent1,accent2 = "#0b1020","#121a36","#00e5ff","#ff4fd8"
    else:
        bg1,bg2,accent1,accent2 = "#0f172a","#1f2a4a","#ffd54a","#ff7ad9"
    front_text = xesc(front_text)
    subtitle = xesc(subtitle)
    # Use landscape format: 1500x1000 with viewBox 0 0 900 600
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1000" viewBox="0 0 900 600">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{bg1}"/>
      <stop offset="1" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="grad" x1="0" x2="1">
      <stop offset="0" stop-color="{accent1}"/>
      <stop offset="1" stop-color="{accent2}"/>
    </linearGradient>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softShadow">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="rgba(0,0,0,0.4)"/>
    </filter>
  </defs>
  <rect width="900" height="600" rx="20" fill="url(#bg)"/>
  <g opacity="0.25">
    <circle cx="150" cy="120" r="100" fill="{accent1}"/>
    <circle cx="750" cy="480" r="120" fill="{accent2}"/>
    <path d="M0 450 C150 400, 300 600, 500 550 S750 450, 900 500 V600 H0 Z" fill="{accent1}" opacity="0.3"/>
  </g>
  <g filter="url(#glow)">
    <text x="450" y="280" text-anchor="middle" font-family="system-ui,Segoe UI,Arial" font-size="56" font-weight="800" fill="url(#grad)" filter="url(#softShadow)">{front_text}</text>
  </g>
  <text x="450" y="330" text-anchor="middle" font-family="system-ui,Segoe UI,Arial" font-size="22" fill="rgba(255,255,255,0.85)" opacity="0.9">{subtitle}</text>
  <g opacity="0.85">
    <rect x="100" y="380" width="700" height="160" rx="16" fill="rgba(0,0,0,0.35)" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
    <text x="450" y="430" text-anchor="middle" font-family="system-ui,Segoe UI,Arial" font-size="18" fill="rgba(255,255,255,0.7)" opacity="0.9">Inside message goes here</text>
    <text x="450" y="460" text-anchor="middle" font-family="system-ui,Segoe UI,Arial" font-size="14" fill="rgba(255,255,255,0.6)" opacity="0.8">(User-customizable in composer)</text>
  </g>
  <text x="450" y="570" text-anchor="middle" font-family="system-ui,Segoe UI,Arial" font-size="16" fill="rgba(255,255,255,0.6)" opacity="0.8" letter-spacing="2">{footer}</text>
</svg>
"""

def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/generate_card_svgs.py <pack_dir>", file=sys.stderr)
        return 2
    pack_dir = Path(sys.argv[1])
    cards_path = pack_dir / "cards" / "cards.json"
    data = json.loads(cards_path.read_text(encoding="utf-8"))
    theme = "yo" if pack_dir.name == "yo_bro" else "mom"
    footer = "YO, BRO" if theme == "yo" else "DEAREST MOTHER"
    out_dir = pack_dir / "assets" / "cards"
    out_dir.mkdir(parents=True, exist_ok=True)
    for c in data.get("cards", []):
        svg = card_svg(c.get("front",""), c.get("title",""), theme, footer)
        (out_dir / f"{c['id']}.svg").write_text(svg, encoding="utf-8")
    print(f"Wrote {len(data.get('cards',[]))} SVGs to {out_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
