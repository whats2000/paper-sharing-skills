---
name: paper-discussion-slides
description: Designs paper-discussion, journal-club and research-sharing slide decks (PPTX or Canva) that put audience understanding first. Use when asked to make paper discussion slides, a journal club deck, a reading-group presentation, a talk explaining a research paper, or 論文分享／論文討論／讀書會簡報. Defines the problem first, splits a concept into progressive build slides only when it needs step-by-step reasoning, aligns highlight frames precisely, connects callouts to what they explain with arrows, spells out every term on first use, and budgets time by key points and script length rather than page count.
---

# Paper Discussion Slides

For paper-discussion talks at meetups, reading groups, journal clubs and labs. Assume the audience is interested but not necessarily expert in the field (students and practitioners).

Write the slides and speaker notes in the language the user asks for (default: the language the user writes in).

## Overarching principle: everything serves audience understanding

Every rule below exists for this goal. When a situation is not covered, ask: "Does doing this make it easier for the audience to understand?" If not, do not do it, even if some rule seems to allow it. The rules are judgment tools, not a template to apply by default.

**Goals are the rules; specifics are examples.** Most rules below state a goal and then show one way that works (a style, a size, a number, a layout). Treat those specifics as illustrations of the goal, not as formats to reproduce exactly; choose what fits each slide. Only these are fixed: the template's measured header, footer, fonts and colours; minimum font sizes; and the checks (numbers against the source, zoomed frame checks, page numbers on build steps).

## Story first: convey the core idea and make people think

The goal of a sharing talk is that the audience leaves understanding **the problem, the paper's one core idea, and a question worth thinking about**. It is not a walkthrough of the whole paper; a talk that reports every section and lists every finding is a talk nobody remembers.

A useful backbone is: **why the problem arises → where the idea comes from (the intuition behind the method) → what it achieves → reflection** (limits, what it means, what is still open). This is not a fixed template; reorder or merge parts when the paper's story is clearer another way. What is not optional is a clear story the audience can follow from start to end.

Formulas, method details, architecture, training settings and full result tables are welcome **in backup slides** after the closing, ready for questions; they do not belong in the main story unless the audience cannot understand the idea without them.

- **Plan the narrative, not the page count.** Before any slide exists, write the story in a few lines: what problem (and why it is hard), what core idea solves it, which one or two pieces of evidence make it believable, and what question the audience should leave with. Pages follow from the story; never start from "N slides".
- **The see + hear test, slide by slide.** For each slide ask: someone who looks at this slide and hears its script once, without reading the paper, can they say the slide's point in one sentence? If not, the slide is doing too much or too little.
- **Know the venue.** A community or meetup talk is not a conference talk. The audience comes for the idea, not to check the method. Leave out formulas, loss functions, architecture diagrams, training tricks and full results tables in the main story; explain the mechanism with an everyday analogy instead (e.g. "it keeps a notebook of fixed size and rewrites it while working" rather than the update equation). Put the technical material in **backup slides after the closing**, for questions.
- **Each concept appears once.** Do not explain the same idea on two slides, and do not restate a contrast in every section. A recap of earlier work appears at the opening and at most once more at the close, not throughout. When reviewing, list each slide's point; any two that say the same thing → merge or cut one.
- **Plain names for the audience.** Call baselines and variants by what they are ("the same model, looking one frame back", "a memory that cannot learn"), not by their acronyms. Titles say the idea in everyday words. An abbreviation in a title is fine once the term has been introduced, or on the slide that introduces it (section 4).
- **Leave room to think.** Besides polls, give the audience at least one moment to think or discuss (e.g. a 60-second "talk to your neighbour: which would you choose?") about a question the talk has made concrete.

---

## 1. Workflow (in order; do not skip steps)

Material comes first: the slides are built from the paper's own assets, collected by `paper-project-setup`.

1. **Make sure the topic is set up.** If there is no project folder for this paper yet (a folder with a `manifest.json` listing the collected figures, videos and data), invoke the `paper-project-setup` skill first to create it and collect the source information and media files, then continue here. If the folder exists, read its `README.md` and `manifest.json`, and run setup again only for assets that are missing. Use the paper's own figures, videos and chart data; do not generate illustrations to stand in for them, and keep the source of every asset.
2. **Write the story before any slide** (see "Story first"): the problem and why it is hard → the one core idea, in plain words → the one or two pieces of evidence that make it believable → what it means and what is still open → the question the audience leaves with. Write it as a few spoken sentences; if it does not hold together as a story, slides will not fix it.
3. **Budget by points, not pages.** From the time the speaker has, decide how many key points fit (section 6). Prefer fewer points explained well. If over budget, cut key points (or move them to backup); never squeeze the explanation time of each point.
4. **Make every concept a complete single slide** and choose how to present it (section 3).
5. **Write a short spoken script for every slide** (section 5). Where a script grows long, split or cut that slide.
6. **Decide slide by slide whether a concept needs a progressive build** (section 2). Split only when the concept needs detailed, step-by-step guidance, and split by subtraction.
7. **Re-estimate time from the script** (script length ÷ speaking rate, plus interaction time). If over, merge steps or cut key points. More pages because of builds is normal; never merge just to reduce page count.
8. **Review the slide text from the audience's seat** (section 3a): read every slide as someone who has not heard the script, cut sentences down to keywords, then run `scripts/audit_text.py` and fix what it reports.
9. **Check** (section 11): numbers against the source, frames zoomed in, terms clear where first introduced, callout size and arrows, font sizes, script length, page numbers.

---

## 2. Progressive builds: the exception, not the default

### When to split
- **Core question: does this concept need detailed explanation that guides the audience's thinking step by step?**
  - Yes: the audience has to work through this step before the next one makes sense (e.g., start with a familiar example, then name the principle, then introduce the new idea) → split.
  - No: the point is a relationship that is understood at a glance → keep it together on one slide.
- Decide only by whether the point needs step-by-step explanation, not by page count. Splitting naturally adds pages; as long as every step has something to say (≥ 20 seconds), the time shows up in the script.
- **Do not split parallel lists, simple introductions, or relationships that are obvious at a glance.**
  - Exception: a list whose items each need their own explanation (≥ 20 seconds of script each) and point back to different earlier parts of the talk (e.g., "how reliable is each of the three results we saw?") may be revealed one item per step, dimming the items already discussed with `dim_area()`. The audience then looks at one item while the earlier ones stay visible for context.

Read `references/examples.md` before building: it has the full positive and negative examples (an opening build, a composition relationship, an over-split parallel list).

### How to split: by subtraction
1. Build the complete slide first.
2. Duplicate it several times and, in each copy, delete what has not been explained yet. The first step is mostly empty; show only what has been said; the last step equals the complete slide.
   - **When the slide is one image whose parts are explained in turn** (a pipeline figure, a diagram), there is nothing separate to delete. Prefer cropping the image into its parts and placing them as separate pictures; if the parts cannot be separated cleanly, cover the parts not yet explained with `hide()` (an opaque white cover) and remove the cover on the step that explains that part.
   - `hide()` and `dim_area()` / `dim()` are opposites: `hide` covers what is **still to come**; dimming fades what was **already discussed** so the current element stands out. Do not use one for the other.
   - **Goal of dimming: already-discussed content stays readable but quiet, so the eye goes to the current part.** One way that works well: lay `dim_area()` over it, a white rectangle at about 80% opacity (PowerPoint "transparency 20%"), no outline, no shadow, covering the whole group (picture, text and arrows of one row together). A mask is one shape the speaker can adjust in PowerPoint, and because every build step is its own slide (not an in-slide animation), the build survives export to PDF and handouts unchanged. Use `dim()` only to fade a single element in place.
3. All build steps of one concept share one page number, because logically they are one slide.
4. Every build step needs at least 20 seconds of script. If a step only gets one sentence, it is split too finely; merge it.

### Red frames and callouts
- A red frame marks only the part that is new or being discussed on this step; the callout states what that part means; the script explains it in detail.
- A frame lives only on the step that discusses it. When the focus moves on, remove the old frame so it does not distract.
- **Red frame vs. dimming:** use a red frame only to circle *a part of one image*. When the subject is a whole image or a whole element (e.g., the third of three pictures), do not frame it; dim the other (already discussed) elements instead (`dim_area()` over them).

### Arrows: connect what is being discussed to its callout
- **Goal: the eye goes from the element to its explanation.** Do not leave a callout floating in a corner. Draw an arrow from the element (or red frame) being discussed to its callout, so the audience sees at once what the sentence explains.
- Choose the arrow's style per slide for what the link means. For example: a **curved red arrow** (thick, round cap) suggests "this leads to a question or idea", such as curving from a prompt box to a "can this work?" callout, because the curve guides the eye and invites the next thought; a **solid light grey-blue block arrow** suggests a direct "this, therefore", such as pointing straight down from two framed lines to the callout "this is the example".
- Arrows, like frames, exist only on the step that discusses them and leave with them.
- Start the arrow close to the element and end it close to the callout; do not cross other content; usually one arrow per slide.
- **When the target sits inside an image** (a label in the middle of a figure), the arrow cannot avoid the image. Then, in this order: (1) place the callout on an empty or already-hidden area of the image right next to the frame, so the arrow is short or unnecessary; (2) otherwise put the callout beside the image on the side nearest the frame and let the arrow run straight over the image along the shortest path, crossing only parts that are not being discussed; (3) never route an arrow over another framed or labelled element. A short arrow over the image is better than a long detour around it.

### Callouts: box fits the text, text is large
- Size the box to the text: about one line-height of padding around it. No large boxes with small text.
- **Goal: readable from the back row; never below 28 pt.** For example, 36 pt bold red on a 1920×1080 slide (about 3/4 of the default 48 pt title) works well.
- Keep a callout to one to three short lines. If it does not fit, the content belongs in the script; do not shrink the font.

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

### 3a. On-slide text: keywords that anchor the script

The words on a slide are anchors: they let the audience follow the speaker and later recap the talk from the slides alone, and they let the speaker find their place in the script. Sentences belong in the notes.

- **Goal: the audience reads each line in about three seconds and knows what it means.** One idea per line, as keywords or numbers (roughly 12–15 CJK characters or 6–8 English words; a guide, not a limit). Choose the form that reads most naturally: `label: keyword`, "A vs B" or a number with its unit usually read at a glance, while a typed `A → B` makes people stop to work out what the arrow means.
- **No sentence punctuation** on the slide: no full stops, semicolons, dashes, or chains of commas. If a line needs them, it is a sentence; move it to the notes.
- **Definitions on first use stay short** (section 4), e.g. "In-Context Learning (ICL): weights fixed, learns from examples". The plain-language explanation is spoken, and written in the notes.
- **Poll questions fit one line** on the slide; the set-up sentence is spoken.
- Callouts: one to three short lines; block items: a few short lines.
- **Font sizes** (1920 × 1080 canvas, 20-inch slide; these floors are fixed): body text, labels, table cells and chart axes at least **24 pt** (26–30 pt typical); source credits and figure captions at least **22 pt**; callouts at least 28 pt (36 pt typical). When a paper figure's own labels are too small to read from the back row, enlarge the figure, crop it, or redraw it.
- **Review pass:** after the deck is built, read each rendered slide as an audience member who has not heard the script. What do they read first? Can they read every line in about three seconds? Then run `scripts/audit_text.py deck.pptx`: it lists runs below the size floors and paragraphs that read as sentences. Fix every `SMALL`, `LONG` and `ARROW` line except author lists and source credits.

**Counter-example:** a recap slide carried "In-Context Learning (ICL): without changing the model's weights, it learns a new task only from examples placed in its context, just like giving a language model one worked example". The audience reads instead of listening, and the line wraps across the slide. Fix: "In-Context Learning (ICL): weights fixed, learns from examples" on the slide, the full sentence in the notes. See `references/examples.md` for more before / after pairs.

- **No typed arrows (→, ⇒) in normal slide text.** In a sentence or keyword line, a typed arrow belongs to notes and chat, not to finished slides; it looks like a draft and the audience has to decode it. Arrows inside an equation or formula (a mapping, a transition such as `s_t → s_{t+1}`) are notation and stay. Write the connecting word a person would say: "塞進更多畫面，反而學到假線索" rather than "塞進更多畫面 → 學到假線索". When a relationship really needs an arrow, draw it as a shape (`arc_arrow()`, `block_arrow()`).

---

## 4. Terms: make the meaning clear where they first appear

- **Goal: on the slide where an abbreviation or term first appears, the design lets the audience see what it stands for and what it means**, without relying on the script alone. How to show it is a layout choice, for example a line in the body ("In-Context Learning (ICL): weights fixed, learns from examples"), a label next to the figure or element it names, or the full name in a smaller line under the abbreviation.
- The title of that slide may already use the abbreviation. After the first introduction, use the abbreviation alone, in titles and body text.
- The script explains the term once in plain words; never assume the audience already knows.
- Be especially careful not to open the talk with unexplained abbreviations.
- **No glossary slide.** A slide full of terms is forgotten by the time a term is used. Explain each term on the slide where it is first needed.

**Counter-example:** a poll slide whose options read "ICL", "SOTA", "VLA", "harness", "System 2" when the audience has never seen these terms explained; nobody can answer it. Fix: make each term clear on the slide where it first appears (e.g., "State-of-the-Art (SOTA): best published result"; "Vision-Language-Action model (VLA): images and instructions in, robot actions out").

---

## 5. Speaker notes

- Every slide has a script the speaker can say out loud: what the slide shows and why it matters, with the numbers.
- **Write it as one person talking to a room**, not as written notes: short sentences, spoken connectives ("so", "here's the surprise"), questions to the room. No parentheses, no abbreviation glosses in brackets, no stage directions (pause, click, "set up Slido") and no citations inside the script. Operational notes (tool setup, placeholders to fill) go in the handoff, not in the notes.
- **Keep it short.** As a rough reference, a typical slide is about 30–60 seconds of speech and a build step about 20–30 seconds. At a speaking rate of roughly 120 English words or 180–200 Chinese characters per minute, that is about 60–120 words (100–180 characters) per slide and 40–70 words (60–120 characters) per build step.
- **A long note is a signal to split or cut the slide.** When a slide's script runs well past these lengths, the slide carries more than one point: split it into build steps or separate slides, or move the extra detail to backup. Do not keep a long note and simply talk faster.
- Exact numbers that do not fit on the slide go into the notes.
- Flag limitations the authors admit and the strength of their wording (e.g., if the paper says "in some cases", remind the audience it is not yet reliable).
- On the source slide, state what kind of source it is (e.g., "a research blog, not a peer-reviewed paper").
- **Poll slides:** the question slide's script is only what the speaker says while the room votes: read the question, explain each option in one sentence, say how to join (about 30–45 seconds). The reveal slide gets a normal script: the answer, the evidence, one follow-up question. The waiting time is not scripted; it is already inside the 3 minutes counted for the interaction (section 6).
- End the last slide with an open question for the room.

---

## 6. Time budget: set by key points and script, not by page count

- **Length is decided by the key points.** Decide how many points to make and how long each needs; some points naturally take several build slides, so the page count grows. **Page count is not a rule, and estimating time from page count is inaccurate.**
- Estimate time like this:
  1. List the key points and estimate each one's explanation time (roughly 1–1.5 minutes for a simple point, 2–3 minutes for one that needs step-by-step guidance spread over several build slides).
  2. After writing the script, convert its length to minutes with the speaking rate above and add interaction time.
  3. If over time, cut key points first; do not compress the explanation of each point, and do not cram a point that needs a build back into one slide.
- Count each poll as about 3 minutes (joining, waiting for votes, showing the answer) and a discussion moment as about 2 minutes, and take them out of the time budget, not add them on top. Explaining the answer after a reveal belongs to the next key point's time. At most 2–3 interactions (polls and discussion moments together) per 30 minutes.
- For a community or meetup talk, aim lower: about 6–10 key points for 30–45 minutes, plus 2 polls and one discussion moment, is usually right; the rest goes to backup.
- Rough reference, with the arithmetic: 30 minutes with 2 polls (about 6 minutes) and one discussion moment (about 2 minutes) leaves about 22 minutes; at 2–3 minutes per point that is about 7–10 key points, including the opening and closing. These numbers only check the estimate; the script decides. The number of physical slides varies with builds; 20 or 30 slides can both be right.

**Counter-example (badly over time):** a talk planned for 30 minutes packed 23 key points and 10 interactions, and split parallel lists into many one-sentence slides (74 physical slides). It ran 90 minutes, three times over. The problem was too many points and interactions and splitting without reason, not "more than 20 pages".

**Counter-example (treating page count as a rule):** to stay under 20 slides, a point that needs step-by-step guidance is crammed into one slide, or its build steps are removed. Fewer pages, but the audience can no longer follow.

---

## 7. Interaction (Slido or similar)

The goal is for the room to think together, not one person talking while everyone else does something else.

- Put a QR code and the event code near the start; put a small QR code in the corner of poll slides. Draw it with `qr()` from `slide_kit.py`.
- If the user has not given the event link or code, ask once when they are present; otherwise use `qr()` with empty data (it draws a labelled placeholder), write "event code to be filled in" in the notes, and list every placeholder in the handoff.
- **Goal: the room thinks before hearing the answer.** The format is open. One that works well is "guess, then reveal": a question slide (options and a related image, no answer), then a reveal slide (a red callout with the answer and the evidence).

### Choosing a poll question

A poll costs about three minutes, so it earns its place only if the room learns something from the reveal. Pick a question that:

1. **has an answer in the source**: a number, a comparison, a result, not only an opinion;
2. **most people will guess wrong, or split on**: the surprise is what makes the point stick;
3. **is not given away** by the talk title, the event description, or the slide just before it (asking "does longer context help?" in a talk titled "Context Scaling" teaches nothing);
4. **opens the next key point**: the reveal slide is the first slide of that point, so the answer leads straight into the explanation.

- Good sources: a naive baseline that backfires ("add one past frame: better or worse?"), a threshold ("how long / how many before X beats Y?"), which of several methods fails, a surprising cost.
- An opinion poll (e.g. the same open question as pre-test and post-test) is worth it only when the talk changes the evidence the audience has. If the event description or the storyline already answers it, replace it.
- Options use units the audience can feel (seconds, minutes, dollars), with the technical unit only in backup or notes if needed ("about 1 minute", not "2K steps").
- When a poll is judged weak, **replace it with a better question**; do not drop the interaction unless the user asks to remove it.
- In the notes, write the correct answer and the wrong answer most people are expected to pick, so the speaker can contrast them at the reveal.
- Other formats, for example: the same question as a pre-test and post-test (to see whether opinions changed), predict a number, guess the best / worst, word cloud, a 60-second discuss-with-your-neighbour open question.
- Terms in poll options follow section 4 as well.
- In the notes, write how to set up the tool, the expected answers, and follow-up questions after the reveal.

---

## 8. Layout and template

- **The template constrains only the header, footer, fonts and text colours.** Lay out everything else to fit the content.
- **Fill the space the content is given.** Large empty areas on a slide, or a box much bigger than its text, signal that the layout needs work. Fix it the way a designer would: shrink the box to fit, or enlarge the text and chart to use the space (staying within one idea), and for a conceptual point (a limitation, a trade-off, a comparison of two ideas) add a simple drawn illustration or the paper's own image as a visual anchor (for example dots for "2 of 10" or a stopwatch with "?" for "not measured"; choose whatever fits the point). Simple icons like these are fine; never invent stand-ins for the paper's own figures or results. Where the slide still feels thin, add the one key point it is missing, not filler. A text-only bullet list that leaves half the slide blank should usually become cards, each with its own small visual.
- **Text beside a picture, video or chart is vertically centred on it.** When text and media share a row, give the text box the media's top and height (use the box `picture()` / `video()` return, not the requested box, since media are fitted) and anchor it to the middle (`anchor='m'`); a side block (`block()`) is centred the same way. Text stuck to the top edge of a row while the image is taller looks unfinished.
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

When building with python-pptx, read `references/pptx-techniques.md` first and use the helpers in this skill's `scripts/slide_kit.py` (template header / title / footer, callouts that fit their text and can be centred, curved and block arrows, red frames, dimming masks and hiding, native bar charts with negative values, real bullet lists, titled blocks in the template's colours, autoplaying and looping videos, QR codes, coordinate conversion). Use `bullets()` for lists instead of typing '•' (a typed bullet has different widths in CJK and Latin text, so wrapped lines misalign). Check the result with `scripts/render_check.py`: it renders every page, a thumbnail sheet for layout, and `footers.png`, a full-resolution strip of every footer. Then run `scripts/audit_text.py` for font sizes and sentence-like text (section 3a).

## 11. Final checklist

- [ ] The story was written before the slides: problem → core idea → evidence → open question; the audience can retell the core idea in one sentence
- [ ] Every slide passes the see + hear test; no concept is explained on two slides
- [ ] No formulas, architecture or training details in the main story of a community talk; they sit in backup slides after the closing
- [ ] Baselines use plain words, not acronyms; titles use everyday words (an abbreviation only once introduced); at least one think/discuss moment
- [ ] The talk opens by defining the problem
- [ ] Total time estimated from script length + interaction time is within budget (not estimated from page count)
- [ ] Builds are used only for points that need step-by-step guidance; parallel lists and at-a-glance relationships are not split; points that need a build were not crammed into one slide to save pages
- [ ] Each slide's presentation was chosen for the point it makes
- [ ] Every term's meaning is clear on the slide that first introduces it; no glossary slide
- [ ] Red frames appear only on their own step and were zoom-checked for alignment; whole elements are dimmed, not framed; dimming masks have no outline or shadow
- [ ] Every callout is connected by an arrow to what it explains; boxes fit the text; text readable from the back row (≥ 28 pt)
- [ ] Notes are short and spoken (no parentheses, glosses or stage directions); every long note led to a split, a cut or a move to backup
- [ ] Template chosen in the order of section 8; footer credit names the source, presenter is on the cover
- [ ] Header and footer drawn with `chrome()`; `footers.png` from `render_check.py` shows footer text vertically centred inside its band on every page
- [ ] Numbers match the source; build steps share page numbers
- [ ] Videos embedded with `video()` and a poster frame; playback tested in PowerPoint, or the handoff says it was not tested
- [ ] Lists use `bullets()` (no typed '•'); every QR or event-code placeholder is listed in the handoff
- [ ] Every on-slide line is a keyword or number, not a sentence; every slide re-read from the audience's seat; `audit_text.py` reports no `SMALL`, `LONG` or `ARROW` lines except author lists and source credits
- [ ] Body text ≥ 24 pt, captions ≥ 22 pt, callouts ≥ 28 pt
- [ ] Text and blocks beside media are vertically centred on the media, not stuck to the top
- [ ] No slide has a large blank area or a box much larger than its text; conceptual slides have a visual anchor
- [ ] No typed arrows in normal slide text (equations excepted); every line reads naturally in about three seconds
- [ ] Every poll has an answer in the source, is not given away by the title or description, is likely to be guessed wrong, and its reveal opens the next key point
