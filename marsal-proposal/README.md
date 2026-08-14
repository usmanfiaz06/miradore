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
| `fonts/fonts-inline.css` | Inter, Inter Tight and IBM Plex Sans Arabic, base64 woff2. |
| `assets/` | Miradore logo, positive and reversed. |
| `preview/` | Rendered page PNGs (git-ignored). |

## Editing notes

- **Pages are fixed height** (`297mm`, `overflow:hidden`). Content that runs
  long is clipped rather than reflowed, so rebuild with `--preview` and check
  the pages after any copy change.
- **Type scale** lives in the `:root` block and the `Type scale` section. The
  document is set at `8.5pt / 1.55`; nudging the base size moves everything.
- **Commercials** are in the page 08 table. The headline fee is SAR 24,000
  with 15% VAT shown separately, matching the convention used in the other
  Miradore quotations in this repo.
- **The schedule** is a CSS grid, 9 columns for 16-24 August. Bars are placed
  with inline `grid-column: <start> / span <n>`, where column 2 is Sunday 16.
  The Kingdom weekend (Fri 21, Sat 22) is columns 7 and 8.
- **Arabic** renders through IBM Plex Sans Arabic. The mark itself is a dashed
  placeholder in the lockup diagrams - it is labelled as indicative, since the
  actual logomark is Phase 02 work.
