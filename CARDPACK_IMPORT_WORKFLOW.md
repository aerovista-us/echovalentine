# Cardpack Import Workflow

Based on analysis of the codebase structure, here are the steps required to import a new cardpack:

## 📋 Overview

A cardpack consists of:
- **Pack metadata** (`pack.json`)
- **Cards data** (`cards.json`)
- **Stickers data** (`stickers.json`)
- **Tracks data** (`tracks.json`) - optional
- **Asset files** (SVG images, MP3 audio files)

---

## 🔄 Import Workflow Steps

### Step 1: Create Pack Directory Structure
Create a new directory under `packs/` with your pack ID (e.g., `packs/my_new_pack/`)

```
packs/
  └── my_new_pack/
      ├── pack.json
      ├── cards.json
      ├── stickers.json
      ├── tracks.json (optional)
      └── assets/
          ├── cards/
          │   ├── card-01.svg
          │   ├── card-02.svg
          │   └── ...
          ├── stickers/
          │   ├── sticker-01.svg
          │   └── ...
          ├── covers/
          │   └── cover.svg
          └── audio/ (optional)
              ├── track-01.mp3
              └── ...
```

---

### Step 2: Create `pack.json`
Create the pack metadata file with the following structure:

```json
{
  "id": "my_new_pack",
  "name": "My New Pack",
  "tagline": "A brief description of the pack",
  "cards_count": 10,
  "data": {
    "cards": "cards.json",
    "stickers": "stickers.json",
    "tracks": "tracks.json"
  }
}
```

**Fields:**
- `id`: Unique identifier (must match directory name, lowercase with underscores)
- `name`: Display name for the pack
- `tagline`: Short description shown in UI
- `cards_count`: Number of cards (optional, can be auto-calculated)
- `data`: References to JSON data files

---

### Step 3: Create `cards.json`
Define all cards in the pack:

```json
{
  "cards": [
    {
      "id": "c1",
      "title": "Card Title",
      "front_svg": "assets/cards/card-01.svg"
    },
    {
      "id": "c2",
      "title": "Another Card",
      "src": "assets/cards/card-02.svg"
    }
  ]
}
```

**Note:** The code supports both `front_svg` (old format) and `src` (new format) fields.

**Fields:**
- `id`: Unique card identifier
- `title`: Card title/name
- `front_svg` or `src`: Path to card image (relative to pack directory)

---

### Step 4: Create `stickers.json`
Define all stickers available in the pack:

```json
{
  "stickers": [
    {
      "id": "s1",
      "name": "Heart",
      "src": "assets/stickers/heart.svg"
    },
    {
      "id": "s2",
      "name": "Star",
      "src": "assets/stickers/star.svg"
    }
  ]
}
```

**Fields:**
- `id`: Unique sticker identifier
- `name`: Sticker name (optional)
- `src`: Path to sticker image (relative to pack directory)

---

### Step 5: Create `tracks.json` (Optional)
Define audio tracks for the pack:

```json
{
  "tracks": [
    {
      "id": "t1",
      "name": "Track Name",
      "title": "Display Title",
      "src": "assets/audio/track-01.mp3"
    }
  ]
}
```

**Fields:**
- `id`: Unique track identifier
- `name` or `title`: Track display name
- `src`: Path to audio file (relative to pack directory)

**Note:** If no tracks, use empty array or omit the file.

---

### Step 6: Add Assets
Place all asset files in the appropriate directories:

- **Card images**: `assets/cards/*.svg` (or `.png`)
- **Sticker images**: `assets/stickers/*.svg` (or `.png`)
- **Cover image**: `assets/covers/cover.svg`
- **Audio files**: `assets/audio/*.mp3`

**Supported formats:**
- Images: SVG (preferred), PNG
- Audio: MP3

---

### Step 7: Register Pack in Manifest
Add the new pack to `packs/manifest.json`:

```json
{
  "packs": [
    {
      "id": "my_new_pack",
      "packPath": "my_new_pack/pack.json"
    },
    // ... existing packs
  ]
}
```

**Important:**
- `id` must match the pack directory name
- `packPath` must be relative to `packs/` directory
- Format: `{pack_id}/pack.json`

---

## ✅ Validation Checklist

Before considering the pack complete, verify:

- [ ] Pack directory exists: `packs/{pack_id}/`
- [ ] `pack.json` exists and is valid JSON
- [ ] `cards.json` exists and contains at least one card
- [ ] `stickers.json` exists (can be empty array)
- [ ] `tracks.json` exists (optional, can be empty array)
- [ ] All card images referenced in `cards.json` exist
- [ ] All sticker images referenced in `stickers.json` exist
- [ ] All audio files referenced in `tracks.json` exist (if tracks provided)
- [ ] Pack is registered in `packs/manifest.json`
- [ ] Pack ID is unique (no duplicates in manifest)
- [ ] All file paths are relative to pack directory
- [ ] Image paths use forward slashes (`/`)

---

## 🔍 Code Reference

The import workflow is handled by:

1. **`assets/js/loader.js`** - Loads manifest and pack data
   - `loadManifest()` - Loads `packs/manifest.json`
   - `loadPack(packPath)` - Loads individual pack metadata
   - `loadPackData(packId, pack)` - Loads cards, stickers, tracks

2. **`assets/js/app.js`** - Boot process (lines 646-684)
   - Loads manifest
   - Iterates through packs
   - Loads each pack metadata
   - Extracts pack directory from packPath

---

## 📝 Example: Complete Pack Structure

```
packs/
  └── sample_love/
      ├── pack.json
      ├── cards.json
      ├── stickers.json
      ├── tracks.json
      └── assets/
          ├── cards/
          │   ├── c1.svg
          │   ├── c2.svg
          │   └── ...
          ├── stickers/
          │   ├── s1.svg
          │   ├── s2.svg
          │   └── ...
          ├── covers/
          │   └── cover.svg
          └── audio/
              └── track-01.mp3
```

---

## 🚨 Common Issues & Solutions

### Issue: Pack not showing up
**Solution:** 
- Verify pack is in `manifest.json`
- Check pack ID matches directory name
- Ensure `pack.json` is valid JSON

### Issue: Cards not loading
**Solution:**
- Verify `cards.json` path in `pack.json` data field
- Check image paths are relative to pack directory
- Ensure image files exist

### Issue: Images not displaying
**Solution:**
- Verify image paths use forward slashes
- Check paths are relative to pack directory (not absolute)
- Ensure file extensions match (`.svg` vs `.png`)

### Issue: Stickers not appearing
**Solution:**
- Verify `stickers.json` exists (can be empty array)
- Check sticker image paths
- Ensure images are in `assets/stickers/` directory

---

## 🔧 Automated Import Script (Future Enhancement)

A potential `tools/import_pack.py` script could:

1. Validate pack structure
2. Check all referenced files exist
3. Validate JSON syntax
4. Add pack to manifest automatically
5. Generate pack ID from directory name
6. Verify no duplicate IDs

---

## 📚 Related Files

- `packs/manifest.json` - Pack registry
- `packs/_template_pack/` - Template structure reference
- `assets/js/loader.js` - Pack loading logic
- `assets/js/app.js` - Pack initialization

---

*Last updated: Based on codebase analysis*
