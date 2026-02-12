# Missing Assets — EchoValentines

**Generated:** 2026-02-08  
**Scope:** Packs in `packs/manifest.json` and static app assets.

---

## 1. Packs with no audio (no MP3 / no tracks)

These boxes have `data.tracks` pointing to `tracks.json`, but the tracks array is **empty**. The Track picker does not show for these packs (by design). To add music, add entries to each pack’s `tracks.json` with `id`, `title`, and `src` (e.g. `assets/audio/track.mp3`).

| Pack ID | Pack name (from pack.json) | tracks.json |
|---------|----------------------------|-------------|
| **noir_city_vigilante** | Noir City Vigilante | `{"tracks":[]}` |
| **dearest_mother** | Dearest Mother | `{"tracks":[]}` |
| **sample_love** | Sample Love | `{"tracks":[]}` |
| **found_family** | Found Family | `{"tracks":[]}` |
| **sticker_galaxy_dreams** | Sticker Galaxy Dreams | `{"tracks":[]}` |
| **yo_bro** | Yo Bro | `{"tracks":[]}` |

**Total: 6 packs** have no audio.

---

## 2. Packs that have audio (tracks with src)

These packs have at least one track in `tracks.json` with a `src` (mp3/m4a/etc.):

| Pack ID | Track count | Notes |
|---------|-------------|--------|
| alien_crush | 6 | .mp3 |
| love_spell | 5 | 4 .mp3 + 1 .mp4 (video) |
| arcade_love_90s | 2 | .mp3 |
| echo_reset | 2 | .mp3 |
| anti_love_blackpink | 7 | .mp3 |
| classic_sweet | 2 | .mp3 |
| neon_squad_heroes | 2 | .mp3 |
| sewer_ninja_neon | 8 | .mp3 |
| swamphop_sweetheart | 8 | .mp3 |
| timbr_founders_pack | 1 | .mp3 |

**Total: 10 packs** have at least one track. Actual file presence (e.g. under `packs/{id}/assets/audio/`) is not validated here; 404s can occur if a track’s `src` is missing on disk.

---

## 3. Static app assets

All referenced app assets are present:

- `assets/img/favicon.svg`
- `assets/img/logo-animated.svg`
- `assets/img/valentine-bg.svg`
- `assets/img/echovalentine_splash.mp4`
- `assets/css/main.css`
- `assets/js/*.js`

**Unused:** `assets/img/splash.2.svg` exists but is not referenced (splash uses video).

---

## 4. Design cues removed / corrected (this pass)

- **Compose form:** Placeholders updated from generic "Name" to **"Recipient's name"** (To) and **"Your name"** (From). Message placeholder set to **"Your message (appears on the card)"** so it’s clear where the text goes.
- **Envelope seal:** When a pack has no SVG seals (`sealOptions.length === 0`), the entire "Envelope seal (optional)" section is **hidden** (no "No SVG seals available in this pack." message).
- **Open (receiver) panel:** To/From show **"—"** when empty (no blank or "____" placeholders).

---

## 5. Optional next steps & launch decisions

- **6 packs with no audio:** Decide intentionally whether music is “core” (add at least one track to each of the 6 packs) or “optional” (leave as-is; track picker stays hidden by design).
- Verify that each `src` in `tracks.json` points to an existing file under the pack directory.
- **Unused asset:** Remove or repurpose `assets/img/splash.2.svg` if it’s no longer needed (splash uses video).
