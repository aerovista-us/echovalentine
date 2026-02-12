# Card overlay standard — EchoValentines

All card sets use the **same overlay positions**: **To and From side-by-side** at the top, **message below**.

## Reserved zones (app-drawn)

The app draws overlays on top of the card image:

| Zone        | Position        | Content        | CSS class       |
|-------------|-----------------|----------------|-----------------|
| **To / From** | Top row (~14%)  | `To: [name]` and `From: [name]` next to each other | `.cardToFromRow` (contains `.cardTo`, `.cardFrom`) |
| **Message** | Below (~52%)    | User message   | `.cardMessage`  |

- **To and From:** One row near the top, side-by-side with a gap; left-aligned within each half.
- **Message:** Centered block below the To/From row, multi-line.

All use the same serif font, warm white color, and text-shadow for readability on any background.

## For pack / card authors

When designing card art (SVG or images):

- Reserve the **top ~18%** for the To/From row (one horizontal line).
- Reserve the **middle band** (roughly 30–70% from top) for the message so it doesn’t clash with art.

See **packs/_template_pack/assets/cards/tpl-01.svg** and **packs/neon_squad_heroes/assets/cards/nsh-05.svg** for examples with `zone-tofrom` and `zone-message` groups. The app overlays draw the actual text; the SVG can show placeholder lines or a dashed message area for layout reference.
