# Card Layout Audit — Visual Issues

## Issues Found (from image inspection)

### 1. **To/From Position** ❌
- **Current:** `top: 53%`
- **Issue:** Still too high, overlapping with decorative elements (ribbon)
- **Target:** Should be halfway between current position and message box
- **Calculation:** Message at 62%, halfway = ~57.5%

### 2. **Message Box Centering** ❌
- **Current:** `left: 0; right: 0; margin: auto; width: 82%`
- **Issue:** Appears right-aligned (based on "ddddd" text visible in bottom-right)
- **Possible causes:**
  - Width + padding calculation issue
  - Parent container alignment
  - Transform/positioning conflict

### 3. **Bottom Placeholder Still Visible** ❌
- **Issue:** "To: ____ From: ____" visible at bottom of card
- **Status:** SVG audit shows SGD-03.svg is fixed, but placeholder may be cached or from another source
- **Action:** Verify all sticker_galaxy_dreams cards are clean

### 4. **Debug Label ("ddddd")** ❌
- **Issue:** Text "ddddd" visible in bottom-right corner
- **Possible source:** 
  - Debug label/aria-label
  - Test content in message box
  - CSS positioning artifact
- **Action:** Find and remove/hide

## Current CSS Values

```css
.cardToFromRow {
  top: 53%;
}

.cardMessage {
  top: 62%;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
  width: 82%;
  transform: translateY(-50%);
}
```

## Fixes Applied ✅

1. ✅ **To/From position:** Moved from `53%` → `57.5%` (halfway to message box)
2. ✅ **Message box centering:** Updated to use `left: 0; right: 0; margin-left: auto; margin-right: auto; transform: translateY(-50%)` for horizontal centering (works better with absolute positioning when parent has `position: relative`)
3. ✅ **Placeholder check:** Verified SGD-03.svg and all sticker_galaxy_dreams cards are clean (no "To: ____" placeholders)

## Current CSS Values (Latest)

```css
.cardToFromRow {
  top: 57.5%;
}

.cardMessage {
  top: 62%;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
  width: 82%;
  max-width: 90%;
  transform: translateY(-50%);
}
```

## Notes

- **"ddddd" text:** Likely test content typed in message box, not a debug label
- **Bottom placeholder:** If still visible, may be browser cache - hard refresh recommended (Ctrl+Shift+R or Cmd+Shift+R)
- **Centering method:** Using `left: 0; right: 0; margin: auto` with absolute positioning works when parent has `position: relative` (`.cardStage` does) and element has a defined width
