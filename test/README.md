# Pack Overlay Audit Testing

This directory contains Playwright scripts for systematically auditing card pack overlays.

## Prerequisites

1. Install Node.js (if not already installed)
2. Install Playwright:
   ```bash
   npm install playwright
   ```

## Running the Audit

1. **Start a local server** in the project root:
   ```bash
   # Option 1: Python
   python -m http.server 8765
   
   # Option 2: Node.js serve
   npx serve -p 8765
   ```

2. **Run the audit script**:
   ```bash
   node test/audit-packs.js
   ```

   Or set a custom base URL:
   ```bash
   BASE_URL=http://localhost:8765 node test/audit-packs.js
   ```

## Output

The audit generates:
- **Screenshots**: `test/audit-results/{packId}_{cardId}.png` - Full page screenshots of each tested card
- **JSON Report**: `test/audit-results/audit-report.json` - Detailed findings in JSON format
- **Markdown Report**: `test/audit-results/audit-report.md` - Human-readable summary

## What the Audit Checks

1. **Placeholder Detection**: Scans SVG files for "To: ____" or "From: ____" placeholder text
2. **Overlay Visibility**: Verifies To/From row and message box are visible
3. **Overlay Positioning**: Captures computed CSS styles for positioning analysis
4. **Visual Issues**: Screenshots help identify alignment, sizing, and readability problems

## Using Results to Adjust Overlays

1. Review screenshots in `test/audit-results/`
2. Identify packs with positioning issues
3. Update `overlay` section in `packs/{packId}/pack.json`
4. Re-run audit to verify fixes
5. Iterate until all packs look correct

## Example Overlay Adjustment

If a pack's To/From is too high, adjust in `pack.json`:

```json
{
  "overlay": {
    "toFrom": {
      "top": "60%"
    }
  }
}
```

See `PACK_OVERLAY_SCHEMA.md` for all available properties.
