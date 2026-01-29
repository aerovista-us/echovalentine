
3 packs (each 12 stickers = 36 total)
A matching sticker-pack.json for each
Consistent sizing: 256×256 (viewBox="0 0 256 256")
All SVGs are self-contained (no external fonts/assets)


Folder structure
Create:
sticker_packs/
  neon_hearts/
    sticker-pack.json
    stickers/
      heart_glow.svg
      heart_broken.svg
      ...
  arcade_icons/
    sticker-pack.json
    stickers/
      pixel_star.svg
      coin.svg
      ...
  witchy_moods/
    sticker-pack.json
    stickers/
      moon.svg
      candle.svg
      ...


Pack 1 — Neon Hearts (12)
sticker_packs/neon_hearts/sticker-pack.json
{
  "id": "neon_hearts",
  "name": "Neon Hearts",
  "version": "1.0.0",
  "stickers": [
    { "id": "heart_glow", "src": "stickers/heart_glow.svg", "w": 256, "h": 256, "tags": ["heart","neon","love"] },
    { "id": "heart_broken", "src": "stickers/heart_broken.svg", "w": 256, "h": 256, "tags": ["heart","broken","anti"] },
    { "id": "sparkle_heart", "src": "stickers/sparkle_heart.svg", "w": 256, "h": 256, "tags": ["heart","sparkle"] },
    { "id": "double_hearts", "src": "stickers/double_hearts.svg", "w": 256, "h": 256, "tags": ["hearts","cute"] },
    { "id": "heartbeat", "src": "stickers/heartbeat.svg", "w": 256, "h": 256, "tags": ["ekg","pulse"] },
    { "id": "kiss_mark", "src": "stickers/kiss_mark.svg", "w": 256, "h": 256, "tags": ["kiss","lipstick"] },
    { "id": "rose", "src": "stickers/rose.svg", "w": 256, "h": 256, "tags": ["rose","flower"] },
    { "id": "arrow", "src": "stickers/arrow.svg", "w": 256, "h": 256, "tags": ["cupid","arrow"] },
    { "id": "love_note", "src": "stickers/love_note.svg", "w": 256, "h": 256, "tags": ["note","message"] },
    { "id": "crown", "src": "stickers/crown.svg", "w": 256, "h": 256, "tags": ["crown","queen","king"] },
    { "id": "glitter_stars", "src": "stickers/glitter_stars.svg", "w": 256, "h": 256, "tags": ["stars","sparkle"] },
    { "id": "halo", "src": "stickers/halo.svg", "w": 256, "h": 256, "tags": ["halo","angel"] }
  ]
}

stickers/heart_glow.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <radialGradient id="g" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#ff7ad9" stop-opacity="1"/>
      <stop offset="60%" stop-color="#9b5cff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#00e5ff" stop-opacity="0.2"/>
    </radialGradient>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <path filter="url(#glow)" fill="url(#g)"
    d="M128 216s-73-43-94-87c-15-31 4-69 38-77 21-5 44 2 56 18
       12-16 35-23 56-18 34 8 53 46 38 77-21 44-94 87-94 87z"/>
</svg>

stickers/heart_broken.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="g" x1="0" x2="1">
      <stop offset="0" stop-color="#ff2d55"/>
      <stop offset="1" stop-color="#7c4dff"/>
    </linearGradient>
  </defs>
  <path fill="url(#g)"
    d="M128 216s-73-43-94-87c-15-31 4-69 38-77 21-5 44 2 56 18
       12-16 35-23 56-18 34 8 53 46 38 77-21 44-94 87-94 87z"/>
  <path fill="#0b0b12" opacity="0.55"
    d="M126 58l18 24-18 20 20 28-18 18 18 22-22 18-16-18 10-18-18-26 18-18-18-26 16-16-10-18z"/>
  <path fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"
    d="M126 58l18 24-18 20 20 28-18 18 18 22-22 18"/>
</svg>

stickers/sparkle_heart.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="h" x1="0" x2="1">
      <stop offset="0" stop-color="#ff6bd6"/>
      <stop offset="1" stop-color="#00e5ff"/>
    </linearGradient>
  </defs>
  <path fill="url(#h)"
    d="M128 212s-67-40-86-80c-14-29 3-64 35-71 19-4 40 2 51 17
       11-15 32-21 51-17 32 7 49 42 35 71-19 40-86 80-86 80z"/>
  <g fill="#ffffff" opacity="0.95">
    <path d="M196 56l6 14 14 6-14 6-6 14-6-14-14-6 14-6z"/>
    <path d="M58 120l5 11 11 5-11 5-5 11-5-11-11-5 11-5z"/>
    <path d="M186 146l4 9 9 4-9 4-4 9-4-9-9-4 9-4z"/>
  </g>
</svg>

stickers/double_hearts.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="a" x1="0" x2="1">
      <stop offset="0" stop-color="#ff4fd8"/>
      <stop offset="1" stop-color="#8a5cff"/>
    </linearGradient>
    <linearGradient id="b" x1="0" x2="1">
      <stop offset="0" stop-color="#00e5ff"/>
      <stop offset="1" stop-color="#7cff6b"/>
    </linearGradient>
  </defs>
  <path fill="url(#a)"
    d="M112 190s-52-31-67-62c-11-22 2-49 26-54 14-3 29 2 37 13
       8-11 23-16 37-13 24 5 37 32 26 54-15 31-67 62-67 62z"/>
  <path fill="url(#b)" opacity="0.92"
    d="M168 214s-48-28-62-57c-10-20 2-45 24-50 13-3 27 2 34 12
       7-10 21-15 34-12 22 5 34 30 24 50-14 29-62 57-62 57z"/>
</svg>

stickers/heartbeat.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <rect x="28" y="88" width="200" height="80" rx="18" fill="#101026"/>
  <path d="M44 128h52l14-30 22 60 18-36h48"
        fill="none" stroke="#00e5ff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M46 128h50l14-30 22 60 18-36h54"
        fill="none" stroke="#ff4fd8" stroke-width="4" opacity="0.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

stickers/kiss_mark.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="k" x1="0" x2="1">
      <stop offset="0" stop-color="#ff2d55"/>
      <stop offset="1" stop-color="#ff7ad9"/>
    </linearGradient>
  </defs>
  <path fill="url(#k)"
    d="M60 140c18-26 38-40 68-40s50 14 68 40c-14 26-36 44-68 44s-54-18-68-44z"/>
  <path fill="#0b0b12" opacity="0.2"
    d="M84 146c14 14 28 22 44 22s30-8 44-22c-12-14-26-22-44-22s-32 8-44 22z"/>
  <path fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.8"
    d="M84 144c10 10 22 16 44 16s34-6 44-16"/>
</svg>

stickers/rose.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#1b7f4a" d="M126 242c18-62 10-120-10-160l14-8c24 52 30 114 10 168z"/>
  <path fill="#2ad37a" d="M112 150c-18-8-34-6-48 10 22 6 38 16 46 32 10-14 10-28 2-42z"/>
  <path fill="#ff2d55" d="M132 40c26 0 48 22 48 48 0 36-30 54-52 68-22-14-52-32-52-68 0-26 22-48 56-48z"/>
  <path fill="#ff7ad9" opacity="0.7" d="M138 56c16 0 28 12 28 28 0 20-18 34-34 44-14-10-34-24-34-44 0-16 12-28 40-28z"/>
</svg>

stickers/arrow.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#00e5ff" d="M46 196l18-18 130-130 18 18-130 130 18 18-54 4z"/>
  <path fill="#ff4fd8" d="M186 42l28 28-18 18-28-28z"/>
</svg>

stickers/love_note.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <rect x="44" y="56" width="168" height="144" rx="18" fill="#101026"/>
  <path d="M60 86h136M60 112h104M60 138h120" stroke="#00e5ff" stroke-width="8" stroke-linecap="round" opacity="0.9"/>
  <path fill="#ff4fd8" d="M176 152c10 0 18 8 18 18 0 14-12 22-18 26-6-4-18-12-18-26 0-10 8-18 18-18z"/>
</svg>

stickers/crown.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#ffd54a" d="M44 176l18-88 52 52 14-64 14 64 52-52 18 88z"/>
  <rect x="54" y="176" width="148" height="28" rx="10" fill="#ffb300"/>
  <g fill="#fff">
    <circle cx="62" cy="176" r="6"/><circle cx="98" cy="176" r="6"/><circle cx="128" cy="176" r="6"/>
    <circle cx="158" cy="176" r="6"/><circle cx="194" cy="176" r="6"/>
  </g>
</svg>

stickers/glitter_stars.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <g fill="#ffffff" opacity="0.95">
    <path d="M128 36l14 38 38 14-38 14-14 38-14-38-38-14 38-14z"/>
    <path d="M56 154l8 22 22 8-22 8-8 22-8-22-22-8 22-8z"/>
    <path d="M196 152l6 16 16 6-16 6-6 16-6-16-16-6 16-6z"/>
  </g>
  <circle cx="172" cy="72" r="6" fill="#00e5ff"/>
  <circle cx="92" cy="206" r="6" fill="#ff4fd8"/>
</svg>

stickers/halo.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <ellipse cx="128" cy="78" rx="84" ry="30" fill="none" stroke="#ffd54a" stroke-width="14"/>
  <ellipse cx="128" cy="78" rx="84" ry="30" fill="none" stroke="#fff" stroke-width="4" opacity="0.6"/>
</svg>


Pack 2 — Arcade Icons (12)
sticker_packs/arcade_icons/sticker-pack.json
{
  "id": "arcade_icons",
  "name": "Arcade Icons",
  "version": "1.0.0",
  "stickers": [
    { "id": "pixel_star", "src": "stickers/pixel_star.svg", "w": 256, "h": 256, "tags": ["pixel","star"] },
    { "id": "coin", "src": "stickers/coin.svg", "w": 256, "h": 256, "tags": ["coin","gold"] },
    { "id": "heart_pixel", "src": "stickers/heart_pixel.svg", "w": 256, "h": 256, "tags": ["pixel","heart"] },
    { "id": "controller", "src": "stickers/controller.svg", "w": 256, "h": 256, "tags": ["game","controller"] },
    { "id": "sword", "src": "stickers/sword.svg", "w": 256, "h": 256, "tags": ["rpg","blade"] },
    { "id": "shield", "src": "stickers/shield.svg", "w": 256, "h": 256, "tags": ["rpg","shield"] },
    { "id": "cherry", "src": "stickers/cherry.svg", "w": 256, "h": 256, "tags": ["arcade","fruit"] },
    { "id": "bolt", "src": "stickers/bolt.svg", "w": 256, "h": 256, "tags": ["energy","zap"] },
    { "id": "skull", "src": "stickers/skull.svg", "w": 256, "h": 256, "tags": ["danger","boss"] },
    { "id": "portal", "src": "stickers/portal.svg", "w": 256, "h": 256, "tags": ["portal","warp"] },
    { "id": "chat_bubble", "src": "stickers/chat_bubble.svg", "w": 256, "h": 256, "tags": ["bubble","msg"] },
    { "id": "music_note", "src": "stickers/music_note.svg", "w": 256, "h": 256, "tags": ["music","note"] }
  ]
}

Arcade SVGs (12)
<!-- sticker_packs/arcade_icons/stickers/pixel_star.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#ffd54a" d="M120 40h16v40h40v16h-24l18 32-14 8-28-24-28 24-14-8 18-32H80V80h40z"/>
  <path fill="#fff" opacity="0.25" d="M136 40h8v40h40v8h-40z"/>
</svg>

<!-- coin.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <circle cx="128" cy="128" r="82" fill="#ffb300"/>
  <circle cx="128" cy="128" r="62" fill="#ffd54a"/>
  <path fill="#ffb300" d="M120 78h16v20h20v16h-20v20h20v16h-20v20h-16v-20H100v-16h20v-20H100V98h20z"/>
</svg>

<!-- heart_pixel.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#ff2d55" d="M72 84h32v16h16V84h32v16h16v32h-16v16h-16v16h-16v16h-16v-16h-16v-16H88v-16H72v-32h16z"/>
</svg>

<!-- controller.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#101026" d="M64 120c0-22 18-40 40-40h48c22 0 40 18 40 40 0 46-22 64-44 64-14 0-24-8-28-18h-24c-4 10-14 18-28 18-22 0-44-18-44-64z"/>
  <path fill="#00e5ff" d="M92 124h16v-16h12v16h16v12h-16v16h-12v-16H92z"/>
  <circle cx="170" cy="124" r="10" fill="#ff4fd8"/>
  <circle cx="190" cy="140" r="10" fill="#7cff6b"/>
</svg>

<!-- sword.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#cfd8dc" d="M168 44l44 44-20 20-10-10-78 78 10 10-20 20-28-28 20-20 10 10 78-78-10-10z"/>
  <rect x="56" y="180" width="36" height="22" rx="8" fill="#ff4fd8"/>
</svg>

<!-- shield.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#00e5ff" d="M128 40l76 28v62c0 54-34 84-76 106-42-22-76-52-76-106V68z"/>
  <path fill="#101026" opacity="0.35" d="M128 40v196c42-22 76-52 76-106V68z"/>
  <path fill="none" stroke="#fff" stroke-width="8" opacity="0.6" d="M128 64l48 18v44c0 38-22 60-48 76-26-16-48-38-48-76V82z"/>
</svg>

<!-- cherry.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <circle cx="104" cy="164" r="32" fill="#ff2d55"/>
  <circle cx="156" cy="164" r="32" fill="#ff4fd8"/>
  <path fill="none" stroke="#2ad37a" stroke-width="10" stroke-linecap="round" d="M104 132c0-44 36-72 84-80"/>
  <path fill="none" stroke="#2ad37a" stroke-width="10" stroke-linecap="round" d="M156 132c0-40 16-56 32-80"/>
</svg>

<!-- bolt.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#ffd54a" d="M140 24L56 148h68l-8 84 84-124h-68z"/>
</svg>

<!-- skull.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#ffffff" d="M128 44c44 0 80 32 80 72 0 28-14 52-36 64v28c0 12-10 22-22 22H106c-12 0-22-10-22-22v-28c-22-12-36-36-36-64 0-40 36-72 80-72z"/>
  <circle cx="98" cy="120" r="16" fill="#101026"/>
  <circle cx="158" cy="120" r="16" fill="#101026"/>
  <rect x="118" y="150" width="20" height="14" rx="6" fill="#101026"/>
</svg>

<!-- portal.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="p" x1="0" x2="1">
      <stop offset="0" stop-color="#00e5ff"/>
      <stop offset="1" stop-color="#9b5cff"/>
    </linearGradient>
  </defs>
  <circle cx="128" cy="128" r="82" fill="none" stroke="url(#p)" stroke-width="16"/>
  <circle cx="128" cy="128" r="52" fill="#101026" opacity="0.9"/>
  <path d="M96 128c18-18 46-18 64 0" fill="none" stroke="#fff" stroke-width="8" opacity="0.6" stroke-linecap="round"/>
</svg>

<!-- chat_bubble.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#101026" d="M56 72h144c14 0 26 12 26 26v60c0 14-12 26-26 26H110l-36 28v-28H56c-14 0-26-12-26-26V98c0-14 12-26 26-26z"/>
  <path d="M76 114h104M76 138h76" stroke="#00e5ff" stroke-width="10" stroke-linecap="round"/>
</svg>

<!-- music_note.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#ff4fd8" d="M168 52v118c0 20-18 36-40 36s-40-16-40-36 18-36 40-36c10 0 18 2 24 6V74l-72 16v92c0 20-18 36-40 36S0 202 0 182s18-36 40-36c10 0 18 2 24 6V78z"/>
</svg>


Pack 3 — Witchy Moods (12)
sticker_packs/witchy_moods/sticker-pack.json
{
  "id": "witchy_moods",
  "name": "Witchy Moods",
  "version": "1.0.0",
  "stickers": [
    { "id": "moon", "src": "stickers/moon.svg", "w": 256, "h": 256, "tags": ["moon","night"] },
    { "id": "candle", "src": "stickers/candle.svg", "w": 256, "h": 256, "tags": ["candle","spell"] },
    { "id": "crystal", "src": "stickers/crystal.svg", "w": 256, "h": 256, "tags": ["crystal"] },
    { "id": "star_charm", "src": "stickers/star_charm.svg", "w": 256, "h": 256, "tags": ["charm","star"] },
    { "id": "herb_bundle", "src": "stickers/herb_bundle.svg", "w": 256, "h": 256, "tags": ["herbs","sage"] },
    { "id": "cauldron", "src": "stickers/cauldron.svg", "w": 256, "h": 256, "tags": ["cauldron","brew"] },
    { "id": "eye", "src": "stickers/eye.svg", "w": 256, "h": 256, "tags": ["eye","protection"] },
    { "id": "sigil", "src": "stickers/sigil.svg", "w": 256, "h": 256, "tags": ["sigil","glyph"] },
    { "id": "spellbook", "src": "stickers/spellbook.svg", "w": 256, "h": 256, "tags": ["book","spell"] },
    { "id": "black_cat", "src": "stickers/black_cat.svg", "w": 256, "h": 256, "tags": ["cat","familiar"] },
    { "id": "broom", "src": "stickers/broom.svg", "w": 256, "h": 256, "tags": ["broom"] },
    { "id": "potion", "src": "stickers/potion.svg", "w": 256, "h": 256, "tags": ["potion"] }
  ]
}

Witchy SVGs (12) — all in one block for quick paste
<!-- moon.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#ffd54a" d="M166 44c-22 10-38 32-38 58 0 36 28 64 64 64 10 0 20-2 28-6-10 28-38 48-70 48-42 0-76-34-76-76 0-34 22-62 52-72z"/>
  <circle cx="184" cy="82" r="6" fill="#fff" opacity="0.7"/>
</svg>

<!-- candle.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#ff7ad9" d="M128 34c14 18 18 32 0 52-18-20-14-34 0-52z"/>
  <rect x="92" y="84" width="72" height="128" rx="20" fill="#101026"/>
  <path d="M106 120h44" stroke="#00e5ff" stroke-width="8" stroke-linecap="round" opacity="0.8"/>
</svg>

<!-- crystal.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#00e5ff" d="M128 30l54 64-22 128H96L74 94z"/>
  <path fill="#9b5cff" opacity="0.5" d="M128 30v192h32l22-128z"/>
  <path fill="none" stroke="#fff" stroke-width="6" opacity="0.6" d="M128 30l54 64-22 128H96L74 94z"/>
</svg>

<!-- star_charm.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#ffd54a" d="M128 34l20 56h58l-46 34 18 56-50-36-50 36 18-56-46-34h58z"/>
  <path fill="none" stroke="#00e5ff" stroke-width="8" opacity="0.6" d="M128 182v40"/>
  <circle cx="128" cy="232" r="8" fill="#00e5ff"/>
</svg>

<!-- herb_bundle.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#2ad37a" d="M78 170c24-26 36-54 36-88-28 10-46 36-56 64 6-34-2-64-22-88-10 34 0 74 18 100-14-12-34-18-60-16 26 20 54 32 84 28z"/>
  <path fill="#ff4fd8" d="M150 198l-14-10 26-36 14 10z"/>
  <path fill="#101026" opacity="0.5" d="M118 150l52 38 16-22-52-38z"/>
</svg>

<!-- cauldron.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#101026" d="M64 112h128c0 64-28 108-64 108s-64-44-64-108z"/>
  <path fill="#00e5ff" opacity="0.7" d="M80 112c6 22 18 36 48 36s42-14 48-36z"/>
  <path fill="#ff7ad9" opacity="0.6" d="M98 86c10 14 12 18 8 26-10-6-18-10-8-26zm46 0c10 14 12 18 8 26-10-6-18-10-8-26z"/>
</svg>

<!-- eye.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#101026" d="M128 74c56 0 96 54 96 54s-40 54-96 54S32 128 32 128s40-54 96-54z"/>
  <circle cx="128" cy="128" r="34" fill="#00e5ff"/>
  <circle cx="128" cy="128" r="14" fill="#0b0b12"/>
  <circle cx="142" cy="114" r="6" fill="#fff" opacity="0.8"/>
</svg>

<!-- sigil.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <circle cx="128" cy="128" r="86" fill="none" stroke="#9b5cff" stroke-width="10"/>
  <path fill="none" stroke="#00e5ff" stroke-width="8" stroke-linecap="round"
        d="M128 56v144M56 128h144M82 82l92 92M174 82l-92 92"/>
  <circle cx="128" cy="128" r="10" fill="#ffd54a"/>
</svg>

<!-- spellbook.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#101026" d="M72 54h112c14 0 26 12 26 26v132c-18-10-40-10-56 0-16-10-38-10-56 0-16-10-38-10-56 0V80c0-14 12-26 26-26z"/>
  <path d="M128 78h54" stroke="#00e5ff" stroke-width="8" stroke-linecap="round" opacity="0.8"/>
  <path fill="#ffd54a" d="M96 112l12 24 26 4-19 18 4 26-23-12-23 12 4-26-19-18 26-4z"/>
</svg>

<!-- black_cat.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#101026" d="M70 206c0-48 26-78 58-78s58 30 58 78c0 12-10 22-22 22H92c-12 0-22-10-22-22z"/>
  <path fill="#101026" d="M92 126l-18-26V72l26 18zm72 0l18-26V72l-26 18z"/>
  <circle cx="108" cy="166" r="10" fill="#7cff6b"/>
  <circle cx="148" cy="166" r="10" fill="#7cff6b"/>
  <path d="M128 174l-8 8h16z" fill="#ff4fd8"/>
</svg>

<!-- broom.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#cfd8dc" d="M56 192l136-136 12 12-136 136z"/>
  <path fill="#ffb300" d="M44 204c18 12 44 14 60 2l-20-20c-12 16-28 14-40 18z"/>
  <path fill="#ffd54a" d="M78 178l28 28c10-10 16-26 14-44z"/>
</svg>

<!-- potion.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <path fill="#101026" d="M106 40h44v20l-12 16v20c32 18 44 46 44 74 0 34-24 62-54 62s-54-28-54-62c0-28 12-56 44-74V76l-12-16z"/>
  <path fill="#00e5ff" opacity="0.75" d="M96 160c10 18 20 28 32 28s22-10 32-28c-8-10-18-14-32-14s-24 4-32 14z"/>
  <circle cx="156" cy="126" r="6" fill="#ff7ad9"/>
  <circle cx="108" cy="118" r="6" fill="#ffd54a"/>
</svg>

