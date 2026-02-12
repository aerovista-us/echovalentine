# Sticker Integration Summary — Audit & Changelog

**Last updated:** 2026-02-11  
**Scope:** Real-file audit of sticker usage in simp.v; where the feature was vs where it is now.

---

## Changelog — Where It Was vs Where It Is Now

### Before (earlier design / val.dev)

- **Stickers on the card:** Some builds (e.g. val.dev) had a **sticker-on-card** feature: users could pick stickers and place them on the card art (e.g. drag-and-drop), and the payload included a `sticker` field so the open view could render the sticker on the card.
- **Standalone sticker packs:** val.dev had a separate system: `packs/sticker_packs/` with multiple sticker packs (Neon Hearts, Arcade Icons, Witchy Moods), `loadStickerPacks()` in loader, and a **tabbed sticker picker** in the compose UI to choose from both pack stickers and standalone packs.
- **Payload:** Included sticker placement data (e.g. `payload.sticker` with packId/source for loading).
- **UI:** Sticker picker for “add sticker to card” plus envelope seal picker.

### Now (current simp.v)

- **Stickers on the card:** **Removed.** There is no UI to place stickers on the card, no `sticker` in the share payload, and no rendering of a sticker on the card in the open view. E2E_AUDIT explicitly states: *“Tutorial: Steps match current flow (message on card, **no stickers in this build**).”*
- **Standalone sticker packs:** **Not present.** simp.v has no `packs/sticker_packs/`, no `loadStickerPacks()`, and no tabbed sticker picker. VAL_DEV_FEATURES_COMPARISON.md describes these as “Not in Main.”
- **Pack stickers:** **Still loaded and used only for envelope seals.**  
  - Loader still fetches each pack’s `data.stickers` (e.g. `stickers.json`) and normalizes to `{ stickers: [...] }`.  
  - In compose, **only SVG stickers** are used: `sealOptions` is built from `data.stickers.stickers` filtered by `isSvgPath(src)`.  
  - The only sticker-related UI is the **seal picker** (optional envelope seal). Non-SVG stickers (e.g. .webp) in a pack’s stickers.json are **not** shown anywhere in the app.
- **Payload:** Share payload includes `to`, `from`, `msg`, `track`, `seal`, `ts` — **no `sticker` field.**
- **Sticker “cards”:** Cards that look like stickers (id/title/src containing “sticker”, “-st-”, etc.) are **filtered out** of the box gallery and compose card list via `getLaunchCards()` so they don’t appear as selectable cards.

So: **stickers were (in other builds) a full “stickers on the card” + optional standalone packs feature; in current simp.v they are only “envelope seal art” sourced from pack SVG stickers.**

---

## Real-File Audit (Current Codebase)

### 1. Loader — `assets/js/loader.js`

- **Lines 15, 19:** Loads `pack.data.stickers` (e.g. `stickers.json`) per pack; normalizes to `{ stickers: stickersRaw }` (handles both array and object format).
- **Exports:** `loadPackData` returns `{ cards, stickers, tracks }`. No `loadStickerPacks()`; no reference to `sticker_packs/`.

### 2. App — `assets/js/app.js`

| Location   | What it does |
|-----------|----------------|
| **6**     | `dataCache` holds `{ cards, stickers, tracks }` per pack. |
| **40–52** | `isStickerCard(card)` — detects “sticker” cards (by id/title/src) so they can be excluded from the card list. |
| **56**    | `getLaunchCards(cards)` — filters out sticker cards so gallery/compose only show launch cards. |
| **59–61** | `pickEnvelopeSeal(stickers)` — picks a random **SVG** sticker from the pack’s stickers array for default seal. |
| **235**   | Comment: “Gallery: launch cards only (sticker-cards removed).” |
| **329**   | Compose initial state: `seal: pickEnvelopeSeal(data.stickers?.stickers || [])`. |
| **331–335** | `sealOptions` = pack stickers **filtered to SVG paths only**; used to validate and default `state.seal`. |
| **539–601** | Seal picker UI: only rendered when `sealOptions.length > 0`; cycle/random/clear seal. |
| **361–370** | Punch payload: `to`, `from`, `msg`, `track`, `seal`, `ts` — **no `sticker`.** |
| **777–780** | Open view: uses `payload.seal` only for envelope image; **no use of `payload.sticker`.** |

There is no drag-drop module, no sticker-on-card layer, and no `payload.sticker` encode/decode.

### 3. Pack data (examples)

- **alien_crush/stickers.json:** `{ "version": 1, "stickers": [ seal_launch.svg, ac-st-07.webp, ac-st-08.webp ] }`. Only `seal_launch.svg` is eligible for the seal picker (SVG-only in app).
- **anti_love_blackpink, arcade_love_90s, dearest_mother, found_family, yo_bro, etc.:** Various packs have `stickers.json` and many reference `assets/stickers/seal_launch.svg` plus other assets. Only `.svg` entries appear in the compose seal picker.
- **pack.json:** Many packs have `"data": { "stickers": "stickers.json" }`. Loader uses this to load stickers; app uses them only for `sealOptions`.

### 4. Directories

- **simp.v:** No `packs/sticker_packs/` directory. No `dragdrop.js` or equivalent in `assets/js/`.

---

## Why the Doc Said “Sticker Picker” and “Add to Cards”

This summary originally described fixing **alien_crush** `stickers.json` (structure, paths, IDs) and “test that stickers appear in the sticker picker” and “stickers can be added to cards.” That matched a **planned or previous** build where:

- A “sticker picker” let users choose stickers to put **on the card**.
- Sticker assets (including Alien Crush SVGs) would be used for that picker.

In the **current** simp.v build:

- The only picker that uses pack stickers is the **seal picker** (envelope seal).
- “Sticker picker” in the sense of “add sticker to card” does not exist. The previous doc’s “Next Steps”—**copy files, test stickers in picker, add to cards**—are **obsolete** and not applicable to current behavior.

---

## Summary Table (before vs now)

| Feature / artifact              | Where it was (or planned)     | Where it is now (simp.v)        |
|---------------------------------|------------------------------|----------------------------------|
| Stickers on the card            | Yes (e.g. val.dev)           | **No** — removed / not in build  |
| Payload `sticker` field         | Yes                          | **No** — payload has `seal` only |
| Standalone sticker packs        | val.dev: `sticker_packs/`    | **No** — not in simp.v           |
| loadStickerPacks()              | val.dev loader               | **No** — not in simp.v loader    |
| Tabbed sticker picker UI        | val.dev compose              | **No**                           |
| Pack stickers loaded            | Yes                          | **Yes** — loader + dataCache     |
| Envelope seal from pack stickers| Yes                          | **Yes** — SVG only → seal picker |
| Seal in payload                 | Yes                          | **Yes** — `payload.seal`         |
| Sticker cards hidden from gallery| Yes                          | **Yes** — getLaunchCards()        |

### Current simp.v only (quick reference)

| Feature / artifact       | Current simp.v |
|--------------------------|----------------|
| Sticker-on-card UI       | No             |
| payload.sticker          | No             |
| Standalone sticker_packs/| No             |
| loadStickerPacks()       | No             |
| Tabbed sticker picker    | No             |
| Pack stickers loaded     | Yes            |
| Envelope seal picker uses stickers | Yes (SVG only) |
| payload.seal supported   | Yes            |

---

## If You Re-Enable “Stickers on the Card” Later

- You’d need to restore or add: UI to pick/place stickers on the card, a `sticker` (or equivalent) field in the share payload, and open-view logic to render that sticker on the card.
- Pack sticker files (e.g. alien_crush `stickers.json` and assets) are already loaded; you’d add a second use (card stickers) alongside the existing seal use.
- The alien_crush structure fix described in the original summary (object with `version` + `stickers` array, correct paths/IDs) remains valid for pack authors; only the “sticker picker” and “add to cards” steps are obsolete in the current app.

---

*Audit completed from real files in simp.v; changelog reflects removal of sticker-on-card and standalone sticker packs in favor of envelope-seal-only usage.*
