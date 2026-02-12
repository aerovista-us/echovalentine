# EchoValentines — End-to-End Audit

**Date:** 2026-02-08  
**Scope:** Full user loop, polish, and consistency

---

## 1. Full User Loop (Verified)

### 1.1 Entry & Box Selection
| Step | Route / Action | Status |
|------|----------------|--------|
| App load | `index.html` → splash → `EV_APP.boot()` | ✅ |
| Default route | No hash → `#/boxes` | ✅ |
| Boxes page | `#/boxes` — hero, Shuffle a card, shelf of pack boxes | ✅ |
| Pack box click | → `#/box/{packId}` (card gallery) | ✅ |
| Shuffle (hero) | → `#/compose?pack=…&card=…&t=…` (random card + template) | ✅ |
| Shuffle (per box) | Same, from that pack | ✅ |
| Start (per box) | → last card compose if any, else `#/box/{packId}` | ✅ |
| Paste link (header) | → `#/open` (paste UI) | ✅ |
| Brand / Home | → `#/boxes` | ✅ |

### 1.2 Pick Card & Compose
| Step | Route / Action | Status |
|------|----------------|--------|
| Box gallery | `#/box/{packId}` — cards only (stickers filtered via `getLaunchCards`) | ✅ |
| Card thumb click | → `#/compose?pack=…&card=…` | ✅ |
| Compose form | To, From, Message, Track (optional), Seal (optional) | ✅ |
| Preview | Card art + message on card (live-updated) | ✅ |
| Punch & Copy | Encode payload → copy URL → toast + confetti, show Share link | ✅ |
| Payload | v, pack, card, to, from, msg (160), track, seal, ts | ✅ |

### 1.3 Open (Receiver)
| Step | Route / Action | Status |
|------|----------------|--------|
| Open with token | `#/open?token=…` → splash → load pack/card | ✅ |
| No token | Paste UI; Paste from clipboard → `pasteAndGo()` → `#/open?token=…` | ✅ |
| Invalid token | Decode throws → "Invalid link" (share.decode try/catch) | ✅ |
| Missing pack/card | renderNotFound | ✅ |
| Envelope | To/From on envelope; seal if present | ✅ |
| Open envelope | Flap animation, card revealed, message on card | ✅ |
| To/From panel | Below envelope; To/From only (message on card only) | ✅ |
| Punch one back | → `#/boxes` (box selection first) | ✅ |
| Browse boxes | → `#/boxes` | ✅ |
| Tracks | Player built from payload; optional track selection | ✅ |

### 1.4 Other Routes
| Route | Behavior | Status |
|-------|-----------|--------|
| `#/about` | About + Back → `#/boxes` | ✅ |
| Unknown | renderNotFound → Go home → `#/boxes` | ✅ |

---

## 2. Polish Checklist (Applied)

- **Message on card (viewer):** Message is on the card, visible only after "Open envelope". To/From stay in panel. ✅  
- **Message on card (compose):** Preview shows message on card; textarea updates it live. ✅  
- **Punch one back:** Goes to `#/boxes` (box selection), not same card. ✅  
- **Share link decode:** `EV_SHARE.decode` wrapped in try/catch; throws clear "Invalid or corrupted link". ✅  
- **Compose copy:** Preview text says "Message appears on the card after opening." ✅  
- **Receiving text:** openTextPanel enhanced (larger, weight, contrast); cardMessage styled (size, shadow). ✅  
- **Dropdowns:** select/option dark background and light text for contrast. ✅  
- **Pack boxes:** Taller min-height, description (tagline/description), actions not clipped. ✅  
- **Splash:** Full-screen (100vh/100dvh), black side bands on wide screens. ✅  
- **Viewer mobile:** envelopeWrapper/cardContainer sizing so card isn’t cut off. ✅  

---

## 3. Data & Config

- **Storage:** Prefs (to, from, lastPack, lastCard, tutorialDismissed), stats (punched), unlocks. ✅  
- **Loader:** manifest → packs; loadPack(packPath), loadPackData(packDir, pack); cards/stickers/tracks. ✅  
- **Share:** Base64url encode/decode; payload JSON; decode throws on invalid. ✅  
- **Config:** `EV_CONFIG.BASE_URL` for share URL; Umami optional. ✅  

---

## 4. Edge Cases

- **Empty packs / no cards:** shuffleAndCompose exits; gallery empty; compose not reachable without valid card. ✅  
- **Sticker cards filtered:** `getLaunchCards` excludes sticker cards from gallery and compose. ✅  
- **Missing pack or card in token:** renderNotFound. ✅  
- **Boot failure:** app_bootstrap catch shows "Crashed" and still marks splash content ready. ✅  
- **Route change during async:** renderSeq guards prevent stale appends. ✅  

---

## 5. Files Touched (Audits)

| File | Changes |
|------|--------|
| `assets/js/app.js` | Message on card; panel To/From only; compose copy; textarea preview; **placeholders** (Recipient's name, Your name, Your message…); **seal section hidden** when no seals. |
| `assets/css/main.css` | .cardMessage; composeStage; visual polish; **contain** (app, card, shelf, gallery); **prefers-reduced-motion**; **focus-visible**; smooth scroll. |
| `assets/js/share.js` | decode() try/catch. |
| `E2E_AUDIT.md` | This audit; assets; packs with no audio; design cues; performance. |
| `MISSING_ASSETS.md` | **New.** Packs with no MP3 (6); packs with audio (10); static assets; design-cue fixes. |

---

## 6. Assets & Links Audit

### 6.1 Static assets (all present)
| Asset | Referenced in | Status |
|-------|----------------|--------|
| `assets/img/favicon.svg` | index.html (link rel="icon") | ✅ |
| `assets/img/logo-animated.svg` | index.html (brand) | ✅ |
| `assets/img/valentine-bg.svg` | main.css (.valentine-bg) | ✅ |
| `assets/img/echovalentine_splash.mp4` | splash.js (video src) | ✅ |
| `assets/css/main.css` | index.html | ✅ |
| All `assets/js/*.js` | index.html (script order) | ✅ |

**Unused:** `assets/img/splash.2.svg` exists but is not referenced (splash uses video). Safe to keep or remove.

### 6.2 Hash / in-app links (no broken links)
| Link | Target | Status |
|------|--------|--------|
| `#/boxes` | Box selection | ✅ |
| `#/box/{id}` | Pack gallery | ✅ |
| `#/compose?pack=…&card=…` | Compose | ✅ |
| `#/open` | Paste link | ✅ |
| `#/open?token=…` | Open card | ✅ |
| `#/about` | About | ✅ |

### 6.3 Packs & loader
- **manifest.json:** Lists 16 packs. Each has a matching directory under `packs/` with `pack.json`. ✅  
- **Loader:** Fetches `packs/manifest.json`, then `packs/{packPath}` per entry. Pack path is e.g. `love_spell/pack.json`; directory name must match. Boot catches per-pack load errors and continues, so missing or invalid packs are skipped and do not crash the app. ✅  
- **Dynamic assets:** Card images, stickers, tracks, box_art, and seal SVGs are resolved from pack data (e.g. `packs/{packDir}/{path}`). 404s for missing files can occur if a pack references a file that does not exist; app does not validate presence of every asset up front.

### 6.4 Packs with no audio (no MP3)
These **6 boxes** have `tracks.json` with an empty `tracks` array — no music in the app for these packs:

- **noir_city_vigilante** (Noir City Vigilante)
- **dearest_mother** (Dearest Mother)
- **sample_love** (Sample Love)
- **found_family** (Found Family)
- **sticker_galaxy_dreams** (Sticker Galaxy Dreams)
- **yo_bro** (Yo Bro)

See **MISSING_ASSETS.md** for the full list and for packs that do have tracks.

### 6.5 Recommendations
- Keep `EV_CONFIG.BASE_URL` correct for production so shared links use the right origin.  
- If adding packs, ensure `pack.json`, `data.cards`, and `data.stickers` (and optional `data.tracks`) exist and paths point to real files.

---

## 7. Design cues & placeholders (this pass)

- **Compose placeholders:** "To" → placeholder **"Recipient's name"**; "From" → **"Your name"**; "Message" → **"Your message (appears on the card)"** (no generic "Name" or "text goes here").
- **Envelope seal:** When the pack has no SVG seals, the entire seal picker section is **hidden** (no "No SVG seals available" text).
- **Open panel:** To/From show **"—"** when empty (no blank or underscore placeholders).

---

## 8. Visual Polish & Performance (This Pass)

- **Primary buttons:** Stronger hover glow (box-shadow + brightness).  
- **Ghost buttons:** Hover background.  
- **Open text panel:** Subtle pink glow in shadow.  
- **Links:** Hover color to accent, transition.  
- **Card thumbs:** Deeper hover lift, accent border/shadow.  
- **Pack boxes:** Hover accent glow in shadow.  
- **Card stage:** Inset border + subtle pink glow.  
- **Toasts:** Stronger shadow; success toast green glow.  
- **Topbar:** Gradient background, softer inset border.  
- **Envelope shell:** Inset border + deeper shadow.  
- **Brand logo:** Hover glow on logo.  
- **Performance:** `contain: layout` on `.app`, `.shelf`, `.gallery`; `contain: layout style` on `.card`. Smooth scroll on `html`.  
- **Reduced motion:** `@media (prefers-reduced-motion: reduce)` shortens animations/transitions.  
- **Focus visible:** Accent outline on `.btn`, `.input`, `.link`, `select.input` for keyboard/a11y.  

No layout or behavior changes beyond placeholder text and hiding the empty seal section.

---

## 9. Suggested Follow-Ups (Optional)

- **Analytics:** Ensure `EV_CONFIG` (e.g. Umami) is set in production if desired.  
- **BASE_URL:** Confirm `config.js` BASE_URL for production share links.  
- **Tutorial:** Steps match current flow (message on card, no stickers in this build).  
- **a11y:** Consider aria-live for dynamic content (e.g. open panel) and focus after route change.  

---

*End of E2E Audit*
