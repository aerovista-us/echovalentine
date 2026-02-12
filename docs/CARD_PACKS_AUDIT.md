# Card packs audit — To/From placeholder & Overlay Configuration

All note (card) packs are checked so that **only the app overlay** shows To/From and message; card SVGs should not contain visible "To: ____ From: ____" placeholder text.

Each pack now includes an `overlay` configuration section in `pack.json` for pack-specific CSS overrides. See `PACK_OVERLAY_SCHEMA.md` for details.

## Status by pack

| Pack | Cards with placeholder (before fix) | Status |
|------|-------------------------------------|--------|
| **_template_pack** | tpl-01 has hidden zone only | OK (template) |
| **love_spell** | ls-001–ls-068 | ✅ Fixed |
| **neon_squad_heroes** | nsh-01–04, nsh-06–24 (nsh-05 has zone hidden) | ✅ Fixed |
| **echo_reset** | nsh-01–nsh-24 | ✅ Fixed |
| **noir_city_vigilante** | ncv-01–ncv-24 | ✅ Fixed |
| **sticker_galaxy_dreams** | sgd-01–sgd-24 | ✅ Fixed |
| **sewer_ninja_neon** | snn-01–snn-24 | ✅ Fixed |
| **found_family** | ff-005–ff-031 | ✅ Fixed |
| **timbr_founders_pack** | tfp-01–tfp-12 | ✅ Fixed |
| **classic_sweet** | cs-01–cs-12 | ✅ Fixed |

## Placeholder formats found

1. **Single line (centered)**  
   `<text x="450" y="430" ...>To: ________   From: ________</text>`  
   Used in: echo_reset, neon_squad_heroes, noir_city_vigilante, sticker_galaxy_dreams.

2. **Single line (sewer_ninja_neon)**  
   `y="436.67"`, `fill="rgba(255,255,255,0.75)"`.

3. **Bottom line (love_spell / found_family style)**  
   `<!-- To/From hints at bottom -->` + `<text x="92" y="532" ...>To: ________   From: ________</text>`.

4. **Classic_sweet**  
   `<!-- To/From line hints -->` + `<text x="92" y="532" font-family="Arial" ...>`.

5. **Timbr (two lines)**  
   `<text ...>To: ____________</text>` and `<text ...>From: __________</text>`.

After fix: card art has no visible To/From; app draws them via `.cardToFromRow` and `.cardMessage` in `main.css` / `app.js`.

## Overlay Configuration Status

All packs now have baseline `overlay` configurations in their `pack.json` files. These use default positioning values and should be adjusted per-pack based on visual testing with Playwright.

**Baseline values:**
- To/From: `top: 57.5%`
- Message: `top: 62%`, `width: 82%`, `maxWidth: 90%`

**Next steps:**
1. Run Playwright audit (`test/audit-packs.js`) to identify packs needing adjustment
2. Review screenshots in `test/audit-results/`
3. Adjust overlay values in `pack.json` files as needed
4. Re-test until all packs are visually correct

See `test/README.md` for instructions on running the audit.
