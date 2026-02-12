# Overlay Adjustments Summary

## Initial Adjustments Made

### 1. arcade_love_90s ✅
**Layout Analysis:**
- Main text at y=280 (top)
- Hearts graphics at y=380-500 (middle-bottom)
- Footer text at y=550 (bottom)

**Adjustments:**
- To/From: `top: 50%` (moved up to avoid hearts)
- Message: `top: 70%` (moved down to clear hearts area)
- Colors: Using theme colors (#00ff41 for To/From, #00ffff for message)
- Added glow effects matching arcade aesthetic

### 2. sticker_galaxy_dreams ✅
**Layout Analysis:**
- Title at y=200 (top)
- Main text "Starbright" at y=350 (middle)
- No bottom text

**Adjustments:**
- To/From: `top: 60%` (slightly higher than default)
- Message: `top: 65%` (positioned below main text)
- Width: `80%` (slightly narrower for better fit)

## Packs Needing Visual Testing

All other packs currently use baseline defaults. They should be tested visually and adjusted as needed:

### Packs with Similar Layouts (may share similar adjustments):

**Top + Middle Text Pattern:**
- love_spell (y=148 top, y=220 middle)
- neon_squad_heroes (y=200 top, y=350 middle)
- echo_reset (likely similar)
- noir_city_vigilante (likely similar)

**Recommendation:** Test these together, may need similar To/From at 60% and Message at 65%

**Bottom Footer Pattern:**
- found_family (has bottom text)
- classic_sweet (has bottom text)

**Recommendation:** May need To/From higher (50-55%) to avoid footer overlap

## Testing Workflow

1. **Start local server:**
   ```bash
   python -m http.server 8765
   ```

2. **Test each pack visually:**
   - Navigate to `http://localhost:8765/#/compose?pack={packId}&card={firstCard}`
   - Fill in test data: "To: Test", "From: Me", "Message: Testing overlay positioning"
   - Take screenshots or note issues

3. **Adjust overlay config:**
   - Edit `packs/{packId}/pack.json`
   - Modify `overlay.toFrom.top` and `overlay.message.top` values
   - Adjust colors if needed for readability
   - Re-test until visually correct

4. **Common Adjustments:**
   - **Too high:** Increase `top` percentage (e.g., 57.5% → 60%)
   - **Too low:** Decrease `top` percentage (e.g., 62% → 58%)
   - **Overlapping graphics:** Move up or down by 5-10%
   - **Not readable:** Adjust `color` to match theme or increase contrast

## Placeholder Status

✅ All packs verified clean (except template pack and nsh-05 which has hidden zones)

## Next Steps

1. Test remaining 15 packs visually
2. Adjust overlay configs based on findings
3. Document final values in this file
4. Consider creating overlay presets for common patterns
