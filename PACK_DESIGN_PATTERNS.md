# Pack Design Patterns

This document tracks shared design patterns across card packs that may benefit from similar overlay configurations.

## Overview

Some card packs share similar design layouts or visual structures. Identifying these patterns helps:
- Apply consistent overlay adjustments
- Create shared overlay presets
- Understand which packs need similar positioning tweaks

## Known Patterns

### Pattern: Bottom Footer Text
**Packs**: love_spell, found_family, classic_sweet
**Description**: Cards have footer text or decorative elements at the bottom (y ~530-550)
**Overlay Impact**: To/From row may need to be positioned higher to avoid footer overlap
**Status**: To be verified via Playwright audit

### Pattern: Center-Heavy Design
**Packs**: arcade_love_90s, neon_squad_heroes
**Description**: Main content/graphics concentrated in center-middle area
**Overlay Impact**: Message box may need vertical adjustment to avoid center graphics
**Status**: To be verified via Playwright audit

### Pattern: Top Title Area
**Packs**: sticker_galaxy_dreams, echo_reset
**Description**: Card titles or main text in upper third of card
**Overlay Impact**: To/From row positioning may need to account for title area
**Status**: To be verified via Playwright audit

### Pattern: 90s Arcade Love 3-Star Design
**Packs**: (To be identified)
**Description**: User mentioned finding a "3 star design" pattern across multiple sets
**Overlay Impact**: Unknown - needs investigation
**Status**: **Needs investigation via SVG comparison**

## Investigation Method

1. **SVG Structure Analysis**: Compare SVG element structures across packs
2. **Visual Pattern Matching**: Use Playwright screenshots to identify similar layouts
3. **Overlay Position Clustering**: Group packs with similar optimal overlay positions

## Next Steps

1. Run Playwright audit on all packs
2. Analyze screenshots for visual patterns
3. Compare SVG structures programmatically
4. Document shared patterns and create overlay presets if beneficial

## Notes

- Patterns are preliminary and need verification
- Some packs may have unique requirements despite similar designs
- Overlay adjustments should prioritize readability and visual balance over strict pattern matching
