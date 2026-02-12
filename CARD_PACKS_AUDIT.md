# Card packs audit — To/From placeholder

All note (card) packs are checked so that **only the app overlay** shows To/From and message; card SVGs should not contain visible "To: ____ From: ____" placeholder text.

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
