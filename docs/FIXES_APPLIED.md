# Fixes Applied - User Feedback

## ✅ Fixed Issues

### 1. Track Playback - Auto-progression Disabled
**Issue**: Tracks auto-progress and continue playing through playlist  
**Fix**: Modified `assets/js/player.js` to stop after selected track ends instead of auto-playing next track  
**File**: `assets/js/player.js` line 71-76  
**Change**: Removed `playNext()` call, now just calls `stop()` when track ends

### 2. Demo Text Removed from Dearest Mother Pack ✅
**Issue**: Demo text ("Inside message goes here", "User-customizable in composer") visible in message box when card is sent  
**Fix**: Removed demo text lines from all 24 `mom_*.svg` files in `packs/dearest_mother/assets/cards/`  
**Files**: All `mom_01.svg` through `mom_24.svg`  
**Change**: Removed the two text elements containing demo text, kept the message box rectangle  
**Status**: ✅ Complete - All 24 files updated, verified no demo text remains

### 3. Button Order Swapped on Receiver Side
**Issue**: "Open envelope" button is at bottom, "Punch one back"/"Browse boxes" at top - users leave before opening  
**Fix**: Swapped button positions so "Open envelope" appears at top  
**File**: `assets/js/app.js` line 863-895  
**Change**: Moved "Open envelope" button to `topActions` (top), moved "Punch one back"/"Browse boxes" to bottom

## ⚠️ Issues Requiring Further Investigation

### 4. Envelope Seal Issue
**Issue**: 
- Only one seal per set
- Seal does not apply
- No way to add seal
- Seal does not appear on envelope

**Current Implementation**:
- Seal picker exists in compose view (`app.js` lines 588-616)
- Seals are loaded from `pack.data.stickers.stickers` filtered for SVG paths
- Seal is passed to `EV_ENVELOPE.create()` which should display it
- Some packs may only have one SVG seal (e.g., arcade_love_90s has one SVG seal)

**Possible Issues**:
1. Seal picker may not be visible/working properly
2. Seal may not be saving to payload correctly
3. Seal may not be displaying on envelope preview
4. Packs may need more seal options added

**Next Steps**:
- Test seal picker UI visibility and functionality
- Verify seal is being saved in `punchAndCopy()` payload
- Check envelope preview shows selected seal
- Consider adding more seal options to packs that only have one

### 5. Card Design Quality Issues
**Issue**: 
- 90s Arcade Love: Design is generic, stars don't connect to arcade theme, needs high-quality arcade-themed SVGs
- Anti Love: Colors are good but images/SVGs are too generic

**Status**: These require new SVG assets to be created/commissioned  
**Action**: Documented for asset update - not a code fix but an asset quality issue

## Summary

**Fixed**: 3 issues (track playback, demo text, button order)  
**Needs Investigation**: 1 issue (envelope seal)  
**Asset Updates Needed**: 2 packs (arcade_love_90s, anti_love) - requires new SVG designs
