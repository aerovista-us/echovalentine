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
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1000" viewBox="0 0 900 600">
  <defs>
    <linearGradient id="bg" x1="0" x2="1">
      <stop offset="0" stop-color="{bg1}"/>
      <stop offset="1" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="grad" x1="0" x2="1">
      <stop offset="0" stop-color="{accent1}"/>
      <stop offset="1" stop-color="{accent2}"/>
    </linearGradient>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="800" height="1200" fill="url(#bg)"/>
  <g opacity="0.20">
    <circle cx="120" cy="210" r="140" fill="{accent1}"/>
    <circle cx="690" cy="980" r="180" fill="{accent2}"/>
    <path d="M0 980 C180 910, 300 1200, 520 1100 S710 980, 800 1080 V1200 H0 Z" fill="{accent1}"/>
  </g>
  <g filter="url(#glow)">
    <text x="70" y="420" font-family="system-ui,Segoe UI,Arial" font-size="66" font-weight="850" fill="url(#grad)">{front_text}</text>
  </g>
  <text x="72" y="500" font-family="system-ui,Segoe UI,Arial" font-size="26" fill="#e7ecff" opacity="0.92">{subtitle}</text>
  <g opacity="0.9">
    <rect x="70" y="560" width="660" height="480" rx="28" fill="#0b0b12" opacity="0.28"/>
    <text x="100" y="640" font-family="system-ui,Segoe UI,Arial" font-size="22" fill="#c7d2fe" opacity="0.95">Inside message goes here →</text>
    <text x="100" y="680" font-family="system-ui,Segoe UI,Arial" font-size="20" fill="#c7d2fe" opacity="0.75">(User-customizable in composer)</text>
  </g>
  <text x="70" y="1135" font-family="system-ui,Segoe UI,Arial" font-size="18" fill="#9fb0ff" opacity="0.9">{footer}</text>
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
