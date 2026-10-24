---
name: paper-discussion-slides
description: Designs paper-discussion, journal-club and research-sharing slide decks (PPTX or Canva) that put audience understanding first. Use when asked to make paper discussion slides, a journal club deck, a reading-group presentation, a talk explaining a research paper, or 論文分享／論文討論／讀書會簡報. Defines the problem first, splits a concept into progressive build slides only when it needs step-by-step reasoning, aligns highlight frames precisely, connects callouts to what they explain with arrows, spells out every term on first use, and budgets time by key points and script length rather than page count.
---

# Paper Discussion Slides

For paper-discussion talks at meetups, reading groups, journal clubs and labs. Assume the audience is interested but not necessarily expert in the field (students and practitioners).

Write the slides and speaker notes in the language the user asks for (default: the language the user writes in).

## Overarching principle: everything serves audience understanding

Every rule below exists for this goal. When a situation is not covered, ask: "Does doing this make it easier for the audience to understand?" If not, do not do it, even if some rule seems to allow it. The rules are judgment tools, not a template to apply by default.

---

## 1. Workflow (in order; do not skip steps)

Material comes first: the slides are built from the paper's own assets, collected by `paper-project-setup`.

1. **Make sure the topic is set up.** If there is no project folder for this paper yet (a folder with a `manifest.json` listing the collected figures, videos and data), invoke the `paper-project-setup` skill first to create it and collect the source information and media files, then continue here. If the folder exists, read its `README.md` and `manifest.json`, and run setup again only for assets that are missing. Use the paper's own figures, videos and chart data; do not generate illustrations to stand in for them, and keep the source of every asset.
2. **Define the problem and the storyline.** First write down what question the paper answers and why it matters, then lay out the structure: problem → method → results → discussion (reasons / limitations, if they matter) → take-away + open question.
3. **Budget.** From the time the speaker has, decide how many key points fit (section 6). The budget is **key points and explanation time, not page count**. If over budget, cut key points first; never squeeze the explanation time of each point.
4. **Make every concept a complete single slide** and choose how to present it (section 3).
5. **Write the full speaker script for every slide** (about 1 minute; section 5).
6. **Decide slide by slide whether a concept needs a progressive build** (section 2). Split only when the concept needs detailed, step-by-step guidance, and split by subtraction.
7. **Re-estimate time from the script** (script length ÷ speaking rate, plus interaction time). If over, merge steps or cut key points. More pages because of builds is normal; never merge just to reduce page count.
8. **Check** (section 11): numbers against the source, frames zoomed in, full names on first use, callout size and arrows, script length, page numbers.

---

## 2. Progressive builds: the exception, not the default

### When to split
- **Core question: does this concept need detailed explanation that guides the audience's thinking step by step?**
  - Yes: the audience has to work through this step before the next one makes sense (e.g., start with a familiar example, then name the principle, then introduce the new idea) → split.
  - No: the point is a relationship that is understood at a glance → keep it together on one slide.
- Decide only by whether the point needs step-by-step explanation, not by page count. Splitting naturally adds pages; as long as every step has something to say (≥ 20 seconds), the time shows up in the script.
- **Do not split parallel lists, simple introductions, or relationships that are obvious at a glance.**

Read `references/examples.md` before building: it has the full positive and negative examples (an opening build, a composition relationship, an over-split parallel list).

### How to split: by subtraction
1. Build the complete slide first.
2. Duplicate it several times and, in each copy, delete what has not been explained yet. The first step is mostly empty; show only what has been said; the last step equals the complete slide.
   - **When the slide is one image whose parts are explained in turn** (a pipeline figure, a diagram), there is nothing separate to delete. Prefer cropping the image into its parts and placing them as separate pictures; if the parts cannot be separated cleanly, cover the parts not yet explained with `hide()` (an opaque white cover) and remove the cover on the step that explains that part.
   - `hide()` and `dim()` are opposites: `hide` covers what is **still to come**; `dim` fades what was **already discussed** so the current element stands out. Do not use one for the other.
3. All build steps of one concept share one page number, because logically they are one slide.
4. Every build step needs at least 20 seconds of script. If a step only gets one sentence, it is split too finely; merge it.

### Red frames and callouts
- A red frame marks only the part that is new or being discussed on this step; the callout states what that part means; the script explains it in detail.
- A frame lives only on the step that discusses it. When the focus moves on, remove the old frame so it does not distract.
- **Red frame vs. dimming:** use a red frame only to circle *a part of one image*. When the subject is a whole image or a whole element (e.g., the third of three pictures), do not frame it; dim the other (already discussed) elements instead.

### Arrows: connect what is being discussed to its callout
- Do not leave a callout floating in a corner. Draw an arrow from the element (or red frame) being discussed to its callout, so the audience sees at once what the sentence explains.
- **Curved arrow** (red, thick, round cap, arrowhead at the end): for "this leads to a question or idea", e.g., curving from a prompt box to a "can this work?" callout. The curve guides the eye and invites the next thought.
- **Solid block arrow** (light grey-blue, bold): for a direct "this → therefore", e.g., pointing straight down from two framed lines to the callout "this is the example".
- Arrows, like frames, exist only on the step that discusses them and leave with them.
- Start the arrow close to the element and end it close to the callout; do not cross other content; usually one arrow per slide.
- **When the target sits inside an image** (a label in the middle of a figure), the arrow cannot avoid the image. Then, in this order: (1) place the callout on an empty or already-hidden area of the image right next to the frame, so the arrow is short or unnecessary; (2) otherwise put the callout beside the image on the side nearest the frame and let the arrow run straight over the image along the shortest path, crossing only parts that are not being discussed; (3) never route an arrow over another framed or labelled element. A short arrow over the image is better than a long detour around it.

### Callouts: box fits the text, text is large
- Size the box to the text: about one line-height of padding around it. No large boxes with small text.
- Make the text readable from the back row: on a 1920×1080 slide, about 36 pt bold red (roughly 2/3 of the slide title), never below 28 pt.
- 1–3 lines per callout. If it does not fit, the content belongs in the script; do not shrink the font.

**Counter-example:** an 860×350 px callout with five lines of 20–24 pt text takes half the slide while the text is unreadable from the back; the audience sees a big grey block. Fix: cut to 2–3 lines, enlarge to 36 pt, shrink the box to fit, and connect it with an arrow to what it explains.

### One slide = one concept; the same figure may be reused
- The same figure can appear on several slides as long as each slide makes a different point (e.g., frame group A on one slide and group B on the next), letting the audience look at the same data from different angles.
- Never repeat a slide with the same content and the same point.
- If the script for one slide covers several concepts, split it or give each concept its own slide.

---

## 3. Decide what the slide must convey, then how to show it

Video, images and charts are not defaults; choose by condition:

| What the slide is about | Presentation |
|---|---|
| How a process or action happens (how a failure unfolds, how a robot moves its arm to get a view) | Video |
| A moment or a detail (a camera view, one instant on a timeline) | Image / screenshot, with a red frame if needed |
| Comparing numbers | Chart (may be redrawn; label "redrawn from the paper's Fig. N data") |
| Logic or a pipeline | Diagram |
| Parallel items | All laid out at once; no splitting |
| Composition or cause and effect (A + B ⇒ C) | Videos / images in one row joined by "+" and "⇒" (videos playing simultaneously); one slide |

- Having a video in the source does not mean it belongs on the slide; a video used for a single static point makes the audience look in the wrong place.
- **Visual first:** almost no text-only slides. Put only keywords and numbers on the slide and the full explanation in the speaker notes. With too much text, the audience reads instead of listening and thinking.

---

## 4. Terms: full name and plain explanation on first use

- On first use, write an abbreviation as "Full Name (ABBR) + one plain-language sentence", e.g., "In-Context Learning (ICL): the model learns a task from examples placed in its context, without changing its weights." Use the abbreviation alone only after that.
- Do this on the slide and in the script; never assume the audience already knows.
- Be especially careful not to open the talk with unexplained abbreviations.
- **No glossary slide.** A slide full of terms is forgotten by the time a term is used. Explain each term on the slide where it is first needed.

**Counter-example:** a poll slide whose options read "ICL", "SOTA", "VLA", "harness", "System 2" when the audience has never seen these terms explained; nobody can answer it. Fix: on the slide where each term first appears, write it in full (e.g., State-of-the-Art (SOTA): the best published result; Vision-Language-Action model (VLA): a model that maps images and instructions directly to robot actions).

---

## 5. Speaker notes

- Every slide has a full spoken script: what the slide says, what the paper says, the numbers.
- **Length = time.** A normal slide is about 1 minute (English ≈ 130–150 words; Chinese ≈ 200–250 characters). Each build step is at least 20 seconds (English ≈ 45–50 words; Chinese ≈ 70–90 characters).
- Exact numbers that do not fit on the slide go into the notes.
- Flag limitations the authors admit and the strength of their wording (e.g., if the paper says "in some cases", remind the audience it is not yet reliable).
- On the source slide, state what kind of source it is (e.g., "a research blog, not a peer-reviewed paper").
- **Poll slides:** the question slide's script is only what the speaker says while the room votes: read the question, explain each option in one sentence, say how to join (about 30–60 seconds; Chinese ≈ 100–200 characters). The reveal slide gets a normal script (about 1 minute: the answer, the evidence, one follow-up question). The waiting time is not scripted; it is already inside the 3 minutes counted for the interaction (section 6).
- End the last slide with an open question and mark the pause.

---

## 6. Time budget: set by key points and script, not by page count

- **Length is decided by the key points.** Decide how many points to make and how long each needs; some points naturally take several build slides, so the page count grows. **Page count is not a rule, and estimating time from page count is inaccurate.**
- Estimate time like this:
  1. List the key points and estimate each one's explanation time (usually 1–1.5 minutes; a point that needs step-by-step guidance may take 2–3 minutes spread over several build slides).
  2. After writing the script, convert its length to minutes with the speaking rate above and add interaction time.
  3. If over time, cut key points first; do not compress the explanation of each point, and do not cram a point that needs a build back into one slide.
- Count each interaction as at least 3 minutes (joining, waiting for votes, revealing, follow-up), covering both its question and reveal slides, and take it out of the time budget, not add it on top. At most 2–3 interactions per 30 minutes.
- Reference, with the arithmetic: a 30-minute talk **without interactions** fits roughly 15–17 key points (about 1.5–2 minutes each, including the opening and closing). Each interaction removes about 3 minutes, i.e. about 2 key points: with 2 interactions, 24 minutes ≈ 12–14 key points; with 3 interactions, 21 minutes ≈ 11–13 key points. The poll's question and reveal slides belong to the interaction, not to the key-point count. The number of physical slides varies with builds; 20 or 30 slides can both be right.

**Counter-example (badly over time):** a talk planned for 30 minutes packed 23 key points and 10 interactions, and split parallel lists into many one-sentence slides (74 physical slides). It ran 90 minutes, three times over. The problem was too many points and interactions and splitting without reason, not "more than 20 pages".

**Counter-example (treating page count as a rule):** to stay under 20 slides, a point that needs step-by-step guidance is crammed into one slide, or its build steps are removed. Fewer pages, but the audience can no longer follow.

---

## 7. Interaction (Slido or similar)

The goal is for the room to think together, not one person talking while everyone else does something else.

- Put a QR code and the event code near the start; put a small QR code in the corner of poll slides. Draw it with `qr()` from `slide_kit.py`.
- If the user has not given the event link or code, ask once when they are present; otherwise use `qr()` with empty data (it draws a labelled placeholder), write "event code to be filled in" in the notes, and list every placeholder in the handoff.
- Use "guess, then reveal": a question slide (options + a related image, no answer) → a reveal slide (red callout with the answer + the evidence).
- Formats: the same question as a pre-test and post-test (to see whether opinions changed), predict a number, guess the best / worst, word cloud, a 60-second discuss-with-your-neighbour open question.
- Terms in poll options follow section 4 as well.
- In the notes, write how to set up the tool, the expected answers, and follow-up questions after the reveal.

---

## 8. Layout and template

- **The template constrains only the header, footer, fonts and text colours.** Lay out everything else to fit the content.
- Do not copy a layout from an example slide without asking why it looks that way. For instance, an example slide may use a grey monospace code box because it shows a language-model prompt; when the content is not a prompt, that style does not apply.
- **Which template to use, decided in this order:**
  1. The user supplied a template (PPTX, a theme name, or a deck to match): measure its header, footer, title position, colours and fonts, set them in `TEMPLATE` in `scripts/slide_kit.py`, and build with `new_deck('their-template.pptx')` so its masters and fonts come along. Copy slides from it only if it contains slides whose content should be reused (a fixed cover, a logo slide).
  2. The user or the project notes say no template was supplied, or the user says to use the default: use the built-in default without asking: `new_deck()` with the default `TEMPLATE` (Beamer Berlin + dolphin). Say in the handoff that the default was used.
  3. Nothing is known about a template and the user is present: ask once whether they have one; if they have none, use the default.
- `assets/sample-template.pptx` (preview: `assets/sample-template-preview.png`, built by `scripts/build_sample_template.py`) is a **reference deck to look at, not a file to open and edit**: it shows the default template's elements (cover, callout, arrows, frame, two build steps sharing a page number, a block), not slide types to copy. `references/template-example.md` lists the default's measured values and how to measure another template.
- **Footer credit** (`chrome(..., credit=...)`) names the **source being discussed**: its authors or institution and year (e.g. "Ken Goldberg / UC Berkeley, 2026"). The presenter's name and affiliation go on the cover, not in the footer.
- **Draw the header and footer with `chrome()` from `scripts/slide_kit.py`, never by hand.** Hand-drawn footers drift: a text box taller than its band, starting above it, or anchored to the top with default insets puts the footer text too high. `chrome()` makes every footer text box exactly the band, with zero insets, no autofit, and middle anchoring. For another template, measure it and change `TEMPLATE` in `slide_kit.py` once, rather than adjusting slides one by one.

---

## 9. Red frames must be aligned precisely

- Measure frame positions on the **full-size asset**: for charts, convert from plotting coordinates (export element coordinates when redrawing a chart); for screenshots, measure the target's pixel range on the original image. Never estimate proportions from a thumbnail.
- When an image is cover-cropped into a box, convert coordinates using the cropped range, or every frame will be offset.
- **Zoom in on every slide with a frame:** crop and enlarge the area to confirm the frame fully encloses the target, is not offset, and does not cut into neighbouring content. A full-deck thumbnail sheet shows layout only; it cannot confirm frame positions.

---

## 10. Building PPTX files

When building with python-pptx, read `references/pptx-techniques.md` first and use the helpers in this skill's `scripts/slide_kit.py` (template header / title / footer, callouts that fit their text and can be centred, curved and block arrows, red frames, dimming and hiding, native bar charts with negative values, real bullet lists, titled blocks in the template's colours, autoplaying and looping videos, QR codes, coordinate conversion). Use `bullets()` for lists instead of typing '•' (a typed bullet has different widths in CJK and Latin text, so wrapped lines misalign). Check the result with `scripts/render_check.py`: it renders every page, a thumbnail sheet for layout, and `footers.png`, a full-resolution strip of every footer.

## 11. Final checklist

- [ ] The talk opens by defining the problem
- [ ] Total time estimated from script length + interaction time is within budget (not estimated from page count)
- [ ] Builds are used only for points that need step-by-step guidance; parallel lists and at-a-glance relationships are not split; points that need a build were not crammed into one slide to save pages
- [ ] Each slide's presentation was chosen for the point it makes
- [ ] Every term has its full name + plain explanation on first use; no glossary slide
- [ ] Red frames appear only on their own step and were zoom-checked for alignment; whole elements are dimmed, not framed
- [ ] Every callout is connected by an arrow to what it explains; boxes fit the text; text is about 36 pt
- [ ] About 1 minute of script per slide; at least 20 seconds per build step
- [ ] Template chosen in the order of section 8; footer credit names the source, presenter is on the cover
- [ ] Header and footer drawn with `chrome()`; `footers.png` from `render_check.py` shows footer text vertically centred inside its band on every page
- [ ] Numbers match the source; build steps share page numbers
- [ ] Videos embedded with `video()` and a poster frame; playback tested in PowerPoint, or the handoff says it was not tested
- [ ] Lists use `bullets()` (no typed '•'); every QR or event-code placeholder is listed in the handoff
