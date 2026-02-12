# Comprehensive Pack Audit Report

**Generated:** $(date)  
**Total Packs Audited:** 16

## Executive Summary

- **Total Packs:** 16
- **Packs with Errors:** 0
- **Packs with Warnings:** 3
- **Packs with Dummy Data:** 2
- **V2 Compliant Packs:** 0
- **Total Dummy/Placeholder Items:** 14
- **Total File Issues:** 27

## Critical Issues

### 1. Dummy/Placeholder Data Found

#### sample_love
- **Pack ID/Name:** Contains "sample" keyword (intentional sample pack)
- **Card Titles:** Generic "Card 1", "Card 2", etc. (6 cards)
- **Track:** Empty src field with placeholder name "(optional) dreamy loop"

#### love_spell
- **Card IDs:** Generic "card_01", "card_02" format
- **Card Titles:** Generic "Card 01", "Card 02" format
- **Sticker Titles:** Generic "Sticker 01" format

### 2. Missing Files

#### alien_crush
- Missing 6 sticker files referenced in stickers.json:
  - AC-ST-01.svg
  - AC-ST-02.svg
  - AC-ST-03.svg
  - AC-ST-04.svg
  - AC-ST-05.svg
  - AC-ST-06.svg

#### anti_love_blackpink
- Missing 6 sticker files referenced in stickers.json:
  - albp-st-01.svg
  - albp-st-02.svg
  - albp-st-03.svg
  - albp-st-04.svg
  - albp-st-05.svg
  - albp-st-06.svg

#### neon_squad_heroes
- **12 cards with extremely long filenames** (175+ characters) - DALLE-generated names
- Missing 4 sticker files with extremely long filenames (175+ characters)

### 3. V2 Structure Compliance

**Packs NOT matching v2 folder structure:**
- `sample_love` - Missing covers directory
- `yo_bro` - Missing covers directory
- `dearest_mother` - Missing covers directory

**Packs with missing stickers directory (but have stickers in JSON):**
- `echo_reset` - Has 12 stickers in JSON but no stickers directory
- `found_family` - Has 0 stickers (OK)
- `noir_city_vigilante` - Has 12 stickers in JSON but no stickers directory
- `swamphop_sweetheart` - Has 6 stickers in JSON but no stickers directory
- `timbr_founders_pack` - Has 8 stickers in JSON but no stickers directory
- `sticker_galaxy_dreams` - Has 12 stickers in JSON but no stickers directory

## Detailed Pack Reports

### sample_love
**Status:** ⚠️ Sample Pack (Intentional)

**Issues:**
- Missing cover.svg/cover.webp
- Track t1 has empty src field
- Generic card titles ("Card 1", "Card 2", etc.)
- Contains "sample" keyword in pack metadata

**Structure:**
- Cards: 6
- Stickers: 6
- Tracks: 1 (placeholder)

**Recommendation:** This is a sample pack - consider keeping it separate or clearly marking it as demo content.

---

### alien_crush
**Status:** ⚠️ Missing Files

**Issues:**
- 6 missing sticker files referenced in stickers.json

**Structure:**
- Cards: 32
- Stickers: 8 (6 missing files)
- Tracks: 6

**Recommendation:** Remove references to missing stickers or add the missing files.

---

### anti_love_blackpink
**Status:** ⚠️ Missing Files

**Issues:**
- 6 missing sticker files referenced in stickers.json

**Structure:**
- Cards: 24
- Stickers: 16 (6 missing files)
- Tracks: 7

**Recommendation:** Remove references to missing stickers or add the missing files.

---

### neon_squad_heroes
**Status:** ⚠️ Critical - Long Filenames

**Issues:**
- **12 cards with filenames >175 characters** (DALLE-generated names)
- 4 missing sticker files with extremely long filenames

**Examples of problematic filenames:**
- `dalle-2025-01-31-160816-a-cinematic-cyberpunk-city-at-night-for-neon-echoes-scene-1-a-lone-figure-walks-down-an-empty-neon-lit-street-bathed-in-glowing-lights-of-blue-pi.svg`

**Structure:**
- Cards: 35
- Stickers: 16 (4 missing files)
- Tracks: 2

**Recommendation:** **URGENT** - Rename all files to short format (card_001.svg, sticker_001.webp, etc.) and update JSON references.

---

### love_spell
**Status:** ⚠️ Generic Naming

**Issues:**
- Generic card IDs ("card_01", "card_02")
- Generic card titles ("Card 01", "Card 02")
- Generic sticker titles ("Sticker 01")

**Structure:**
- Cards: 71
- Stickers: 3
- Tracks: 5

**Recommendation:** Update card/sticker IDs and titles to be more descriptive.

---

### yo_bro
**Status:** ⚠️ Missing Covers

**Issues:**
- Missing cover.svg/cover.webp
- Missing covers directory

**Structure:**
- Cards: 24
- Stickers: 0
- Tracks: 0

**Recommendation:** Add cover.svg (800×520) to assets/covers/

---

### dearest_mother
**Status:** ⚠️ Missing Covers

**Issues:**
- Missing cover.svg/cover.webp
- Missing covers directory

**Structure:**
- Cards: 24
- Stickers: 0
- Tracks: 0

**Recommendation:** Add cover.svg (800×520) to assets/covers/

---

### Other Packs (Clean)

The following packs have no critical issues:
- `arcade_love_90s` ✅
- `classic_sweet` ✅
- `echo_reset` ✅ (but missing stickers directory)
- `found_family` ✅
- `noir_city_vigilante` ✅ (but missing stickers directory)
- `sewer_ninja_neon` ✅
- `sticker_galaxy_dreams` ✅ (but missing stickers directory)
- `swamphop_sweetheart` ✅ (but missing stickers directory)
- `timbr_founders_pack` ✅ (but missing stickers directory)

## V2 Standard Compliance

### Current Status: 0% Compliant

**None of the packs fully comply with v2 standards** due to:
1. File naming conventions (long DALLE names)
2. Missing folder structure (covers directories)
3. Format inconsistencies

### Required Changes for V2 Compliance

1. **File Naming:**
   - Cards: `card_001.svg`, `card_002.svg`, etc.
   - Stickers: `sticker_001.svg`, `sticker_002.svg`, etc.
   - Tracks: `t01_intro.mp3`, `t02_spell.mp3`, etc.
   - Max filename length: 50 characters

2. **Folder Structure:**
   ```
   packs/<pack_id>/
     pack.json
     assets/
       covers/
         cover.svg (800×520)
       cards/
         card_001.svg
       stickers/
         sticker_001.svg
     audio/
       tracks.json
       tracks/
         t01_intro.mp3
   ```

3. **pack.json Format:**
   ```json
   {
     "id": "pack_id",
     "name": "Pack Name",
     "version": "2.0.0",
     "cards": { "dir": "assets/cards", "default_format": "svg" },
     "stickers": { "dir": "assets/stickers", "default_format": "svg" },
     "audio": { "tracks_json": "audio/tracks.json" }
   }
   ```

## Recommendations

### Priority 1 (Critical)
1. **neon_squad_heroes:** Rename all long filenames immediately
2. **Missing sticker files:** Remove references or add files for alien_crush and anti_love_blackpink
3. **Missing covers:** Add cover.svg to yo_bro and dearest_mother

### Priority 2 (High)
1. **Generic naming:** Update love_spell card/sticker IDs and titles
2. **Missing stickers directories:** Create directories for packs that have stickers in JSON but no directory

### Priority 3 (Medium)
1. **Sample pack:** Consider removing or clearly marking sample_love
2. **Track placeholders:** Remove empty track entries from sample_love

### Priority 4 (Low)
1. **V2 migration:** Plan gradual migration to v2 standard
2. **File format standardization:** Ensure all cards/stickers use SVG or WebP consistently

## Next Steps

1. Run `tools/pack_normalize.py` (to be created) to rename files and fix structure
2. Run `tools/pack_validate.py` (to be created) to verify fixes
3. Update pack.json files to v2 format
4. Create missing cover files
5. Fix missing file references

---

**Report Generated By:** pack_audit.py  
**Full JSON Report:** pack_audit_report.json
