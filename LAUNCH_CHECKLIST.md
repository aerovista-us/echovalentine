# EchoValentines — Launch Checklist

**From review (2026-02-11):** “Ship it / watch it” items and what was done.

---

## Deployment target

| Field | Value |
|-------|--------|
| **Deployment target** | Firebase / Cloudflare / GitHub Pages *(circle one)* |
| **Deployed URL** | |
| **Expected BASE_URL** | |

---

## Done (implemented)

1. **Cache:** Removed 1-year `Cache-Control` meta from `index.html`. Caching should be controlled at host/CDN: index.html = no-cache or short TTL; assets/ = hashed or longer TTL.
2. **BASE_URL:** Comment in `config.js` clarified: must match exact deployed origin; set before launch.
3. **packPath validation:** `loader.js` now validates `packPath` (no `..`, no unsafe chars, must end in `.json`) before fetching.
4. **Seal src:** `envelope.js` restricts envelope seal image `src` to same-origin relative paths or `https:` URLs (blocks `javascript:`, `data:`, etc.).
5. **a11y:** Focus moves to `#app` after route change; `#app` has `tabindex="-1"`; open-view panel has `aria-live="polite"` and `aria-atomic="true"`.
6. **Landing:** “Open the app” nav CTA emphasized (font-weight, subtle glow); “Box → Card → Message → Link” added to landing section for copy consistency with howto.
7. **STICKER_INTEGRATION_SUMMARY.md:** Changelog tightened; obsolete “sticker picker / add to cards” steps labeled; mini “Current simp.v only” table added.
8. **MISSING_ASSETS.md:** Section 5 updated with intentional “music core vs optional” decision for 6 no-audio packs and unused `splash.2.svg` note.

---

## Before go-live (verify)

- [ ] **BASE_URL** in `config.js` points at the exact production URL (e.g. GitHub Pages or final host path).
- [ ] **Caching:** Host/CDN serves `index.html` with no-cache or short TTL; static assets (e.g. under `assets/`) with long TTL or hashed filenames.
- [ ] **Analytics:** If using Umami, set `EV_CONFIG.UMAMI_*` in production.
- [ ] **6 no-audio packs:** Confirm decision (leave as-is vs add at least one track each).
- [ ] **Unused asset:** Remove or repurpose `assets/img/splash.2.svg` if not needed.

---

## Final verification steps (go-live)

### A) Confirm BASE_URL is correct in the deployed build

**Goal:** Share links open on the same deployed origin/path.

**Quick checks:**

- On the live site, create a link → paste it into a new browser or incognito tab.
- Confirm the generated URL’s **origin** matches your deployed domain exactly (including any subpath).
- If you host under a subpath (e.g. `/echo-valentine/`), BASE_URL must include it.

**Pass if:** A copied share link opens the app on the same domain (and same subpath if used) in incognito, and renders the intended content without redirecting to a different origin.

**If this fails:** Set `EV_CONFIG.BASE_URL` to the exact deployed origin + subpath, rebuild, and redeploy.

### B) Confirm caching behavior (index vs assets)

**Goal:** `index.html` updates immediately after a deploy; assets can cache longer.

**Quick checks (DevTools → Network):**

- Reload the app and inspect the **document** request (index.html or the main doc):
  - Should show no-cache / revalidate behavior (short TTL is fine).
- Static assets (CSS, JS, images):
  - Ideally hashed filenames or longer TTL.
- **If you ever see “old UI after deploy,”** it’s almost always index caching.

**Pass if:** After a redeploy, a hard refresh shows the new UI immediately; DevTools shows the document request revalidated / no-cache.

**If this fails:** Bypass cache for `/index.html` (or lower TTL) at your host/CDN, and ensure assets are fingerprinted/hashed so they can stay cached.

---

## Host/CDN header examples

Pick what you’re using and set headers accordingly.

### Firebase Hosting (`firebase.json`)

```json
{
  "hosting": {
    "public": "public",
    "headers": [
      {
        "source": "/index.html",
        "headers": [
          { "key": "Cache-Control", "value": "no-cache" }
        ]
      },
      {
        "source": "/**",
        "headers": [
          { "key": "Cache-Control", "value": "public, max-age=3600" }
        ]
      }
    ]
  }
}
```

(If your assets are fingerprinted/hashed, you can safely bump their `max-age` way up.)

### Cloudflare (CDN layer)

Set a **Cache Rule**:

- If URL equals `/index.html` → **Bypass cache**
- If URL matches `/assets/*` → **Cache longer**

### GitHub Pages

You don’t get strong header control. If you’re on GitHub Pages and want reliable updates:

- Prefer **hashed asset filenames** (so you can keep assets cached).
- Accept that `index.html` caching may vary by browser/CDN path.

---

## Optional “nice-to-have” checks (not blockers)

- **Security:** Try a malicious/odd `packPath` manually (e.g. `../x.json`, `http://x`, `data:`) → confirm the app rejects it cleanly.
- **Seals:** Confirm seals reject `http:` and `data:` (and silently fall back to no seal).
- **Keyboard / a11y:** Route change shifts focus to the app container; open-view announcements don’t get spammy (`aria-live` is polite).

---

## Optional follow-up (non-blocking)

- innerHTML / `html` helper: keep using `esc()` for any user content; consider migrating to text nodes or a single sanitization path (see production audit).
- Tutorial steps: ensure they match current flow (message on card, no stickers in this build).
