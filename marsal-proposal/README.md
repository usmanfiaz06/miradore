# Marsal - Brand Evolution Proposal

HTML source for the Marsal branding proposal, rendered to print-ready PDF
through headless Chromium. Set in the Miradore design language.

## Build

```bash
python3 build.py              # -> ../Marsal_Brand_Evolution_Proposal_Miradore.pdf
python3 build.py --preview    # also writes page PNGs to preview/
```

Requires `playwright` (`pip install playwright`). Chromium is already present
at `/opt/pw-browsers` in this environment - do not run `playwright install`.

## Files

| Path | What it is |
|---|---|
| `proposal.html` | The whole document. One `<section class="page">` per A4 page. |
| `build.py` | Chromium print-to-PDF wrapper. |
| `fonts/fonts-inline.css` | Archivo, Inter, Inter Tight and IBM Plex Sans Arabic, base64 woff2. |
| `assets/` | Miradore logo (positive and reversed) and the cover image. |
| `assets/make_cover.py` | Regenerates `cover.jpg`. See below. |
| `preview/` | Rendered page PNGs (git-ignored). |

## Editing notes

- **Pages are fixed height** (`297mm`, `overflow:hidden`). Content that runs
  long is clipped rather than reflowed, so rebuild with `--preview` and check
  the pages after any copy change.
- **Type scale** lives in the `:root` block and the `Type scale` section. The
  document is set at `8.5pt / 1.56`; nudging the base size moves everything.
  Archivo carries all display type and numerals, Inter the body text.
- **The layout** is an asymmetric rail grid - a 30mm rail for section numbers
  and micro-labels, a 136mm main column. `.grid` gives you both; `.main-only`
  indents a single element to the main column. The recurring `.route` motif
  (node, orange leg, hairline, open node) sits under each section title.
- **Commercials** are in the page 08 table. SAR 14,000 total, quoted without
  VAT. If VAT ever needs showing, add the row back to the table and adjust the
  `.grand` band.
- **The schedule** is a CSS grid, 15 columns for 10-24 August. Bars are placed
  with inline `grid-column: <start> / span <n>`, where column 2 is Monday 10
  and column 16 is Monday 24. The two Kingdom weekends (14-15 and 21-22 Aug)
  are columns 6, 7 and 13, 14 - marked `class="we"` in both the header row and
  the `.g-grid` backing layer.
- **The cover image** is `assets/cover.jpg`, a generated night-highway scene
  (no third-party branding, no licence obligations). It is a placeholder:
  drop in a Marsal fleet photograph at the same path, portrait, at least
  1600 x 2200, and the cover picks it up with no CSS changes. The teal wash
  over it is the `.cover .wash` gradient - lighten or darken there if a
  replacement photo needs more or less scrim.
- **Arabic** renders through IBM Plex Sans Arabic. The mark itself is a dashed
  placeholder in the lockup diagrams - it is labelled as indicative, since the
  actual logomark is Phase 02 work.
