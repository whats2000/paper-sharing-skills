# Template specification example

A template specification that was used in practice. It shows which values to measure when "the template constrains only the header, footer, fonts and text colours". For another template, measure the same items and put them in `TEMPLATE` in `scripts/slide_kit.py`; `chrome()` then draws them identically on every slide.

**Beamer Berlin theme + dolphin colour scheme, converted to PPTX (1920×1080 px canvas, 20 × 11.25 in slide, 1 px = 9525 EMU)**

This is the built-in default template: with no user template, use `new_deck()` and the default `TEMPLATE` as they are. Reference deck to look at (not to open and edit): `assets/sample-template.pptx` (built by `scripts/build_sample_template.py`; preview `assets/sample-template-preview.png`).

- **Header:** two full-width colour bands: 0–46 px `#4747BA`, 46–88 px `#8585D1`. No navigation text.
- **Slide title:** top left, x = 72, y = 120, height 78, 48 pt, `#3333B2`, regular weight, vertically centred in its box.
- **Footer:** 1040–1080 px (40 px band), split at x = 960:
  - left half `#4747BA`: short deck title, right-aligned, white, 18 pt;
  - right half `#8585D1`: the **source's** "authors / institution, year" (the work being discussed, not the presenter) on the left and "page / total" on the right, `#1F1F5C`, 18 pt;
  - 36 px padding from the band edges;
  - **each footer text box has exactly the band's top and height, zero insets, no autofit, and middle anchoring.** A text box that is taller than the band, starts above it, or is top-anchored with default insets renders the text too high (this happened in a real deck: the boxes were 44 px tall starting at 1036 px, 4 px above the band, top-anchored).
- **Cover:** no header or footer; title, original title, authors / source / date, a cover strip of source figures, logos bottom left, "Presented by …" bottom right.
- **Colours:**
  - accent `#3333B2`, second accent `#C83C3C`, secondary text `#5F5F6E`
  - blocks: title bar `#4747BA`, body `#EBEBF7` (a tint of the main colour)
  - callout text about `#FF5757` on a light grey box with a thin blue border (`#99BDD9`)
  - block arrows light grey-blue (about `#C8D0DA`)
- **Fonts:** Latin Arial; CJK Microsoft JhengHei / Noto Sans CJK TC.
- **Corners:** boxes may have rounded corners.

Everything else (block layouts, image grids, code boxes) is not part of the template and should be chosen per slide for its content.

## How to measure a template the user provides

1. Render one content slide of their file to PNG at 1920 px wide (`scripts/render_check.py`).
2. Read the band edges and colours from the pixels, and the title / footer text boxes, fonts and sizes from the PPTX XML.
3. Write the values into `TEMPLATE`, build one test slide with `chrome()`, render it, and compare `footers.png` with the user's original footer before building the deck.
