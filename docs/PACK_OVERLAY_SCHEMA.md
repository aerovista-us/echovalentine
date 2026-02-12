# Pack Overlay Schema

## Overview
Each `pack.json` file can include an optional `overlay` section that defines pack-specific CSS overrides for the To/From row and message box overlays. These styles are applied dynamically via JavaScript, allowing each card pack to have custom positioning, sizing, fonts, and colors without modifying CSS files.

## Schema Structure

```json
{
  "overlay": {
    "toFrom": {
      // Optional: Override To/From row styles
    },
    "message": {
      // Optional: Override message box styles
    }
  }
}
```

## To/From Row Properties (`toFrom`)

All properties are optional. If not specified, CSS defaults from `main.css` are used.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `top` | string | `"57.5%"` | Vertical position from top of card (percentage) |
| `gap` | string | `"2em"` | Gap between "To:" and "From:" text |
| `fontSize` | string | `"clamp(14px, 3vw, 20px)"` | Font size for To/From text |
| `color` | string | `"rgba(255,252,248,.98)"` | Text color |
| `textShadow` | string | `"0 1px 2px rgba(0,0,0,.9), 0 2px 4px rgba(0,0,0,.7)"` | Text shadow CSS value |
| `padding` | string | `"0 5%"` | Padding around To/From row |

## Message Box Properties (`message`)

All properties are optional. If not specified, CSS defaults from `main.css` are used.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `top` | string | `"62%"` | Vertical position from top of card (percentage) |
| `width` | string | `"82%"` | Width of message box |
| `maxWidth` | string | `"90%"` | Maximum width of message box |
| `padding` | string | `"5% 6%"` | Padding inside message box |
| `fontSize` | string | `"clamp(17px, 4vw, 26px)"` | Font size for message text |
| `color` | string | `"rgba(255,252,248,.98)"` | Text color |
| `textShadow` | string | `"0 1px 2px rgba(0,0,0,.9), 0 2px 6px rgba(0,0,0,.75), 0 0 20px rgba(0,0,0,.5)"` | Text shadow CSS value |
| `lineHeight` | string | `"1.45"` | Line height for message text |

## Example

```json
{
  "id": "arcade_love_90s",
  "name": "90s Arcade Love",
  "overlay": {
    "toFrom": {
      "top": "60%",
      "gap": "3em",
      "fontSize": "clamp(16px, 3.5vw, 22px)",
      "color": "#00ff41"
    },
    "message": {
      "top": "65%",
      "width": "75%",
      "maxWidth": "85%",
      "fontSize": "clamp(18px, 4.5vw, 28px)",
      "color": "#00ffff"
    }
  }
}
```

## Implementation Notes

- Styles are applied via inline `style` attributes on the overlay elements
- Only specified properties override defaults; unspecified properties use CSS defaults
- Values should be valid CSS values (strings with units, colors, etc.)
- Percentage values for `top` are relative to the card container height
- The overlay system works in both compose (`#/compose`) and open (`#/open`) views

## Best Practices

1. **Start with defaults**: Test with default CSS values first, then adjust only what's needed
2. **Use responsive units**: Prefer `clamp()` for font sizes, percentages for positioning
3. **Test multiple cards**: Some packs may have cards with different layouts; test representative samples
4. **Consider readability**: Ensure text colors contrast well with card backgrounds
5. **Document special cases**: If a pack needs unusual values, add comments in pack.json
