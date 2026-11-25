---
name: paper-discussion-slides
description: Designs paper-discussion, journal-club and research-sharing slide decks (PPTX or Canva) that put audience understanding first, planning the storyline as a chain of questions before choosing material and layout. Use when asked to make paper discussion slides, a journal club deck, a reading-group presentation, a talk explaining a research paper, or 論文分享／論文討論／讀書會簡報. Defines the problem first, splits a concept into progressive build slides only when it needs step-by-step reasoning, aligns highlight frames precisely, connects callouts to what they explain with arrows, spells out every term on first use, and budgets time by key points and script length rather than page count.
---

# Paper Discussion Slides

For paper-discussion talks at meetups, reading groups, journal clubs and labs. Assume the audience is interested but not necessarily expert in the field (students and practitioners).

Write the slides and speaker notes in the language the user asks for (default: the language the user writes in).

## Overarching principle: everything serves audience understanding

Every rule below exists for this goal. When a situation is not covered, ask: "Does doing this make it easier for the audience to understand?" If not, do not do it, even if some rule seems to allow it. The rules are judgment tools, not a template to apply by default.

**Goals are the rules; specifics are examples.** Most rules below state a goal and then show one way that works (a style, a size, a number, a layout). Treat those specifics as illustrations of the goal, not as formats to reproduce exactly; choose what fits each slide. Only these are fixed: the template's measured header, footer, fonts and colours; minimum font sizes; callout arrows (section 2: they run from the element to its callout; a thick block arrow only in free space, a thin arrow when it has to cross a figure or pull out on a slant; one arrow style and colour per slide and its steps); and the checks (numbers against the source, zoomed frame checks, page numbers on build steps).

**Two questions behind every layout decision.** Most rules about callouts, arrows, masks and reveals below are cases of these two; when a situation is not covered, ask them directly:
1. **Is anything blocking what the audience needs to see?** A callout lying on the chart, a thick arrow over the data, a mask over the current point, text over text, a box running off the slide.
2. **Is anything interrupting the audience?** Anything that makes them stop and re-orient instead of following: an arrow that changes style between two steps, a callout that jumps to a new place, a straight line on a slant that looks like a mistake, an answer or hook shown before the speaker gets there, a symbol they have to decode.
The tools check what can be measured (`layout_check.py` for blocking, `audit_text.py` for text, `build_steps()` and `annotate()` for consistency); looking at every rendered step as an audience member catches the rest.

## Storyline first: design how the audience's question moves

The goal of a sharing talk is that the audience leaves understanding **the problem, the paper's one core idea, and a question worth thinking about**. It is not a walkthrough of the whole paper; a talk that reports every section and lists every finding is a talk nobody remembers.

**Design the movement between slides, not single slides.** A deck where every slide makes its point but nothing carries the audience from one slide to the next feels fragmented: each time the slide changes, the audience has to work out what this slide is about and how it relates to the last one. Plan the talk as a chain of beats instead. In each beat the audience arrives holding a question, sees something that answers it, and leaves with the next question. A slide is one step of that chain, not a self-contained unit.

- **One core question carries the whole talk.** Pose it early, ideally as a picture (for example the known pipeline drawn with the missing piece the paper fills), and keep it in view. Everything in the main story sets it up, explores it, or comes back to it; a slide that does none of these goes to backup.
- **Plan in this order: storyline, then material, then layout.** Do not pick figures or lay out slides until the chain of beats holds together. Material is chosen for what each beat must show; a good figure with no beat to serve is not used.
- **A useful backbone:** why the problem arises → where the idea comes from (the intuition behind the method) → what it achieves → reflection (limits, what it means, what is still open). Reorder or merge parts when the paper's story is clearer another way.
- **Ways to keep the chain moving** (examples in `references/storyline.md`):
  - *Keep the thread visible:* return to one map or key-idea picture at section boundaries with the current part highlighted, so the audience knows where they are; let a key-idea slide grow by one line each time it returns; open and close on the same image or definition.
  - *Let questions drive:* end a slide with the question the next one answers, revealed as its last step (section 2), never visible from the start; let each answer expose the next problem; name sub-problems as plain questions ("where to hang it? how to hang it?").
  - *Make each step graspable:* an everyday analogy or a person doing the same thing; one diagram built up step by step instead of a new picture each time; observation, then insight, then what it buys.
  - *Show the evidence:* let the audience see it (demos that accumulate, the same scene with and without the method) rather than only reading a number in a callout.
  - *Bring people in:* a short personal experience, the people behind the work, a moment of humour, when they serve the story.
- **The story wins over single-slide rules.** Returning to the map is not explaining a concept twice; the same layout with one part changed makes a new point; a `?` that marks the missing slot in a structure is the question itself, not a decorative symbol; a demo that needs the full screen may get its own slide even inside a parallel list; a quoted definition may stay whole with its key words highlighted.

Formulas, method details, architecture, training settings and full result tables are welcome **in backup slides** after the closing, ready for questions; they do not belong in the main story unless the audience cannot understand the idea without them.

- **Two tests, slide by slide.** *See + hear:* someone who looks at this slide and hears its script once, without reading the paper, can say the slide's point in one sentence. *Carry:* they know what question they take into the next slide. A slide that ends with no question while the next one starts a new topic is a seam: add a bridge question, reorder, or cut.
- **Know the venue.** A community or meetup talk is not a conference talk. The audience comes for the idea, not to check the method. Leave out formulas, loss functions, architecture diagrams, training tricks and full results tables in the main story; explain the mechanism with an everyday analogy instead (e.g. "it keeps a notebook of fixed size and rewrites it while working" rather than the update equation). Put the technical material in **backup slides after the closing**, for questions.
- **Each concept is explained once.** Do not explain the same idea on two slides, and do not restate a contrast in every section. Returning to the map or key idea to show where the talk is does not count as explaining again. When reviewing, list each slide's point; any two that say the same thing → merge or cut one.
- **Plain names for the audience.** Call baselines and variants by what they are ("the same model, looking one frame back", "a memory that cannot learn"), not by their acronyms. Titles use everyday words for the topic or the question (section 3a), never the answer. An abbreviation in a title is fine once the term has been introduced, or on the slide that introduces it (section 4).
- **Leave room to think.** Besides polls, give the audience at least one moment to think or discuss (e.g. a 60-second "talk to your neighbour: which would you choose?") about a question the talk has made concrete.

---

## 1. Workflow (in order; do not skip steps)

Plan first, then choose material, then lay out. Most of the quality of a talk is decided before the first slide exists.

**Plan (no slides yet)**

1. **Read the source and make sure the topic is set up.** If there is no project folder for this paper yet (a folder with a `manifest.json` listing the collected figures, videos and data), invoke the `paper-project-setup` skill first, then continue here. If the folder exists, read its `README.md`, `manifest.json` and `storyline_draft.md` (the rough beats and the asset each needs, written during setup). Steps 2–4 below refine that draft; when the refined chain needs material that was not collected, run setup again for just those assets.
2. **Find the core question and the one core idea:** what the audience should be wondering for the whole talk, what answers it, and what they leave with. Write it in two or three spoken sentences; if it does not hold together, slides will not fix it.
3. **Write the chain of beats** (read `references/storyline.md` first). One line per beat: the question the audience arrives with → what they see or hear that answers it (the evidence) → the question they leave with. Mark where the map or key idea returns, where a poll or discussion fits (a beat whose answer surprises), and where an everyday analogy is needed.
4. **Check the chain and budget it.** Read only the questions aloud, in order: each should follow from the one before; a beat with no incoming question is a seam. Budget time by beats (section 6); if over, cut beats or move them to backup, never squeeze the explanation of a beat.
5. **If the user is present, show the core question and the chain of beats before building.** It is the cheapest point to change direction.

**Choose material**

6. **For each beat, choose what lets the audience see the answer** (section 3): a video, a figure, a chart, an illustration, or the returning map. Use the paper's own figures, videos and chart data; do not generate illustrations to stand in for them, and keep the source of every asset. Choose anchor visuals that can return and change one part at a time.

**Lay out and write**

7. **Write the reveal order of every slide, then build it** (section 2): the complete slide first, then one slide per step with `build_steps()`, masking what was already discussed. The hook question is always the last step.
8. **Write a short spoken script for every slide** (section 5). Each script ends by handing the audience the next question. Where a script grows long, split or cut that slide.
9. **Re-estimate real time from the script** (read-aloud minutes × 2–3, plus video and interaction time; section 6). If over, merge steps or cut beats. More pages because of builds is normal; never merge just to reduce page count.
10. **Review the slide text from the audience's seat** (section 3a): read every slide as someone who has not heard the script, cut sentences down to keywords, then run `scripts/audit_text.py` and fix what it reports.
11. **Check** (section 11): first click through the rendered deck looking only at the transitions (does every slide hand over to the next?), then the single-slide checks: numbers against the source, frames zoomed in, terms clear where first introduced, callout size, arrow direction (element to callout) and colour, font sizes, script length, page numbers.

---

## 2. Reveal in the order you speak: builds are the default

**Nothing appears before the speaker reaches it.** A slide whose question, answer and next hook are all visible from the start gives the story away: the audience reads ahead, the answer lands before the question has been felt, and the hook to the next slide is spent before the speaker gets there. Models tend to put everything on one slide at once; this section exists to counter that, so treat revealing as the default and showing everything at once as the exception.

### When to reveal
- **Reveal whenever a slide has an order to it:** a question and its answer, a prediction and the result, a set-up and its punchline, a problem and its fix, the parts of a diagram explained in turn, and the hook question for the next slide, which always comes last. Example from an experienced lecturer: "Who annotates the data?" → "Me?" → a big "NO" → "We hired 'expert' annotators" → the photo of an annotation floor: four reveals on one slide, each a beat of a few seconds.
- **Show everything at once only** when the point is a relationship understood at a glance (A + B ⇒ C with three videos playing side by side), or a parallel set with no tension in it: items the audience does not need to see one by one (eight test platforms do not need eight steps).
- **Many pages are fine.** Every step is its own slide so the build survives export to PDF and handouts; a 20-slide talk can easily become 50 physical slides.

Read `references/examples.md` before building: it has positive and negative examples (an opening build, a composition relationship, an over-split parallel list).

### Two kinds of steps
- **Explanation steps** carry part of the reasoning (a familiar example, then the principle, then the new idea). Each needs something real to say, about 20 seconds of script or more; if a step only gets one throwaway sentence, merge it.
- **Reveal beats** release something the audience was waiting for: the answer, the punchline, the result, the hook. They may last a few seconds. Their justification is the tension they release, not their length.

### Plan the reveal order before building
For every slide, write its reveal order next to the beat it belongs to: step 1 shows…, step 2 adds…, …, last step shows the hook. A slide for which no order can be written is one of the "at once" cases above. Writing the order first is what makes the build happen; deciding afterwards usually ends with everything on one slide.

### How to build: the complete slide, then subtract, then mask
This is how a designer does it by hand, and `build_steps()` in `scripts/slide_kit.py` does it for you: draw the complete slide once, tag each part with the step it appears on and the last step it is the focus, and the helper makes one slide per step.
1. Build the complete slide first.
2. Copy it once per step and, in each copy, delete what has not been said yet. The first step is mostly empty; the last step equals the complete slide.
3. **When the focus moves on, annotations leave and content is masked.**
   - *Annotations* (a callout with its arrow and red frame) belong to the step that discusses them. On the next step they are gone, not faded: an old callout on screen competes with the new one.
   - *Content* already discussed (a picture, a list item, a block, one row of a comparison) stays for context under `dim_area()`: one white mask at about 80% opacity (PowerPoint "transparency 20%"), no outline, no shadow, so it stays readable but quiet while the eye goes to the current point. The mask covers the whole section block (its title bar, body, text and pictures together), never just the text, and masks never stack: two overlapping masks turn a section almost opaque.
   - `build_steps()` does both: give an annotation part the box `'remove'` and a content part the box `'auto'` (one part per section block). It draws one mask over each part's full extent, merges masks that overlap, measures everything from the real elements, never estimates, and keeps the current part on top of any mask. Use `dim()` only to fade a single element in place.
   - **When the slide is one image whose parts are explained in turn** (a pipeline figure, a diagram), there is nothing separate to delete. Prefer cropping the image into its parts and placing them as separate pictures; if the parts cannot be separated cleanly, cover the parts not yet explained with `hide()` (an opaque white cover) and remove the cover on the step that explains that part.
   - `hide()` and `dim_area()` / `dim()` are opposites: `hide` covers what is **still to come**; dimming fades what was **already discussed**. Do not use one for the other.
4. All build steps of one slide share one page number, because logically they are one slide.
5. Each step has its own script; the script of the step before a reveal ends where the reveal begins.

### Red frames and callouts
- A red frame marks only the part that is new or being discussed on this step; the callout states what that part means; the script explains it in detail.
- A frame lives only on the step that discusses it. When the focus moves on, remove the old frame so it does not distract.
- **Red frame vs. dimming:** use a red frame only to circle *a part of one image*. When the subject is a whole image or a whole element (e.g., the third of three pictures), do not frame it; dim the other (already discussed) elements instead (`dim_area()` over them).

### Arrows: connect what is being discussed to its callout
- **Goal: the eye goes from the element to its explanation.** Do not leave a callout floating in a corner. Draw an arrow from the element (or red frame) being discussed to its callout, so the audience sees at once what the sentence explains.
- **Direction is fixed: a callout arrow starts at the element (or red frame) and ends at the callout**, with the arrowhead on the callout. The arrow sets the reading order: the audience looks at the figure first, then follows the arrow to the callout that says what it means. An arrow pointing from the callout back into the figure makes them read the callout first and look for the evidence afterwards, which reverses the explanation.
- **Arrow form follows the two questions** (nothing blocked, nothing interrupting):
  - A *thick block arrow* has a wide body, so it may only run through free space, and straight: on a picture or chart it blocks the very thing being explained. Over a figure, use a *thin arrow* (a line with an arrowhead).
  - A thin arrow is straight when the callout lines up with what it explains and curved when the callout is pulled out on a slant: a straight line on a slant looks like a mistake and stops the eye.
  - Keep one arrow style and colour, and where possible one callout place, for a slide and all its build steps; only the text changes. An arrow that switches form or colour between two steps on the same figure makes the audience re-orient. `annotate()` keeps the first callout's style for the rest of the slide and says when it had to fall back.
  - Colour is a choice: usually a muted red (about `#FF5757`) or a muted grey-blue (`#C8D0DA` for block arrows, a darker `#8FA3B8` for thin lines). Avoid saturated colours.
- Arrows that show a flow inside the content (input to model, one picture to the next, before to after) are grey-blue block arrows in the free space between the pieces.
- Arrows, like frames, exist only on the step that discusses them and leave with them.
- **A callout needs its own free space, away from the figure.** It never lies on a picture, chart, table or text, and it sits far enough from what it explains that the arrow is clearly visible (about 90 px or more): the arrow's job is to lead the eye from the figure to the thought, and a callout pressed against the figure leaves no arrow to follow. The one exception is an area of the image that is already hidden with `hide()`. If no free space exists, shrink the figure, shorten the callout or move content; do not accept an overlap.
- **Draw a callout with `annotate()`, never by placing the callout and the arrow separately.** It takes the box of what is being explained, searches the slide for free space (preferred side first, then the others; the place whose arrow crosses the least content wins), draws the arrow from the target's edge to the callout (a block arrow only when it is lined up and crosses no figure, otherwise a thin arrow), and warns when no free space exists. Positions are computed from real boxes (`picture()`, `hbars()`, `sub()` and `box_of()` return them), not guessed.
- Start the arrow close to the element and end it on the callout; do not cross other content; usually one arrow per slide.
- **When the target sits inside an image** (a label in the middle of a figure), the arrow cannot avoid the image. Then, in this order: (1) put the callout beside the image on the side nearest the target (or on an area of the image already hidden with `hide()`), still with a clearly visible arrow; (2) let the arrow run over the image along the shortest path, crossing only parts that are not being discussed; (3) never route an arrow over another framed or labelled element.

### Callouts: box fits the text, text is large
- Size the box to the text: about one line-height of padding around it. No large boxes with small text.
- **Goal: readable from the back row; never below 28 pt.** For example, 36 pt bold on a 1920×1080 slide (about 3/4 of the default 48 pt title) works well. The callout is red when it is the key point of the slide (which is often); a supporting remark is dark or blue with only its key word in red (section 3a).
- Keep a callout to one to three short lines. If it does not fit, the content belongs in the script; do not shrink the font.

**Counter-example:** an 860×350 px callout with five lines of 20–24 pt text takes half the slide while the text is unreadable from the back; the audience sees a big grey block. Fix: cut to 2–3 lines, enlarge to 36 pt, shrink the box to fit, and connect it with an arrow to what it explains.

### One slide = one concept; the same figure may be reused
- The same figure can appear on several slides as long as each slide makes a different point (e.g., frame group A on one slide and group B on the next), letting the audience look at the same data from different angles.
- Never repeat a slide with the same content and the same point. Reusing the same layout with one part changed (a new highlight, one more line, one swapped element) makes a new point and is encouraged.
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
| Parallel items | All laid out at once; no splitting (except demos that each need the full screen) |
| Composition or cause and effect (A + B ⇒ C) | Videos / images in one row joined by "+" and "⇒" (videos playing simultaneously); one slide |

- Having a video in the source does not mean it belongs on the slide; a video used for a single static point makes the audience look in the wrong place.
- **Visual first:** almost no text-only slides. Put only keywords and numbers on the slide and the full explanation in the speaker notes. With too much text, the audience reads instead of listening and thinking.

### 3a. On-slide text: keywords that anchor the script

The words on a slide are anchors: they let the audience follow the speaker and later recap the talk from the slides alone, and they let the speaker find their place in the script. Sentences belong in the notes.

- **Goal: the audience reads each line in about three seconds and knows what it means.** One idea per line, as keywords or numbers (roughly 12–15 CJK characters or 6–8 English words; a guide, not a limit). Choose the form that reads most naturally: `label: keyword`, "A vs B" or a number with its unit usually read at a glance, while a typed `A → B` makes people stop to work out what the arrow means.
- **Red marks the key point, wherever it is.** Red is not the colour of callouts and black is not the colour of body text: red is emphasis. Mark the one or two words or numbers the audience must take from the slide in red, whether they sit in a callout, a bullet, a label, a table cell or a caption ("only **19.8%** can be called a win", with just "19.8%" red). A callout is often red because it is often the key point; a callout that only supports the point stays dark or blue with its key word in red. Keep red rare, one or two marks per slide or build step: when everything is red, nothing is.
- **No sentence punctuation** on the slide: no full stops, semicolons, dashes, or chains of commas. If a line needs them, it is a sentence; move it to the notes. A quoted definition may stay whole, with its key words highlighted.
- **Definitions on first use stay short** (section 4), e.g. "In-Context Learning (ICL): weights fixed, learns from examples". The plain-language explanation is spoken, and written in the notes.
- **Poll questions fit one line** on the slide; the set-up sentence is spoken.
- Callouts: one to three short lines; block items: a few short lines.
- **Font sizes** (1920 × 1080 canvas, 20-inch slide; these floors are fixed): body text, labels, table cells and chart axes at least **24 pt** (26–30 pt typical); source credits and figure captions at least **22 pt**; callouts at least 28 pt (36 pt typical). When a paper figure's own labels are too small to read from the back row, enlarge the figure, crop it, or redraw it.
- **Titles: the topic or the audience's question, never the answer.** A title names what the slide is about ("Data collection pipeline", "Cognitive map", "Observation") or asks the question the audience is holding ("Who annotates the data?", "How large?", "What is missing?"). It never states the result the slide is about to reveal: the title is visible from the first step, so a title like "Answer: it got worse" or "The learned notebook wins" gives the reveal away. Keep titles short (about 12 CJK characters or 6 English words), keep the same title on every build step and on consecutive slides about the same topic (an experienced lecturer kept "Changing reference frames" for seven slides), and do not use a "label: sentence" formula on slide after slide ("Recap: …", "Task: …", "Answer: …") or labels that name the slide's function ("Answer", "Poll", "Takeaways"). A full-screen demo needs one word or no title.
- **Review pass:** after the deck is built, read each rendered slide as an audience member who has not heard the script. What do they read first? Can they read every line in about three seconds? Then run `scripts/audit_text.py deck.pptx`: it lists runs below the size floors and paragraphs that read as sentences. Fix every `SMALL`, `LONG`, `ARROW` and `HOOK` line except author lists and source credits.

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
- **The script carries the transitions.** End it with the hand-over: the question, or the "so…", that the next slide answers. The slide does not have to spell out the transition; the speaker does.
- **Write it as one person talking to a room**, not as written notes: short sentences, spoken connectives ("so", "here's the surprise"), questions to the room. No parentheses, no abbreviation glosses in brackets, no stage directions (pause, click, "set up Slido") and no citations inside the script. Operational notes (tool setup, placeholders to fill) go in the handoff, not in the notes.
- **Keep it short.** As a rough reference, a typical slide is about 30–60 seconds of speech, an explanation step about 20–30 seconds, and a reveal beat (an answer, a punchline, a hook) can be a few seconds. At a speaking rate of roughly 120 English words or 180–200 Chinese characters per minute, that is about 60–120 words (100–180 characters) per slide and 40–70 words (60–120 characters) per build step.
- Short notes matter more than they seem: in the room every note grows to 2–3 times its read-aloud length (section 6).
- **A long note is a signal to split or cut the slide.** When a slide's script runs well past these lengths, the slide carries more than one point: split it into build steps or separate slides, or move the extra detail to backup. Do not keep a long note and simply talk faster.
- Exact numbers that do not fit on the slide go into the notes.
- Flag limitations the authors admit and the strength of their wording (e.g., if the paper says "in some cases", remind the audience it is not yet reliable).
- On the source slide, state what kind of source it is (e.g., "a research blog, not a peer-reviewed paper").
- **Poll slides:** the question slide's script is only what the speaker says while the room votes: read the question, explain each option in one sentence, say how to join (about 30–45 seconds). The reveal slide gets a normal script: the answer, the evidence, one follow-up question. The waiting time is not scripted; it is already inside the 3 minutes counted for the interaction (section 6).
- End the last slide with an open question for the room.

---

## 6. Time budget: set by key points and script, not by page count

- **Length is decided by the key points.** Decide how many points to make and how long each needs; some points naturally take several build slides, so the page count grows. **Page count is not a rule, and estimating time from page count is inaccurate.**
- **A talk takes 2–3 times as long as reading its script aloud.** Reading the notes is only part of delivering them: the speaker expands on what is written, pauses for the room, lets a video make its point, takes a question mid-talk, and loses time on clicks, links and demos. Estimates made from script length alone come out 2–3 times too short, so always estimate the real time in the room, never the read-aloud time.
- Estimate time like this:
  1. List the beats and estimate each one's real time (roughly 2–3 minutes for a simple point, 4–6 minutes for one that needs step-by-step guidance spread over several build slides).
  2. After writing the script, compute the real time: read-aloud minutes (speaking rate in section 5) × 2.5 (range 2–3), plus the full length of every video the audience has to watch, plus interaction time. If the speaker knows their own ratio from an earlier talk (script length against the actual duration), use it instead of 2.5.
  3. If over time, cut beats first (or move them to backup); do not compress the explanation of each point, and do not cram a point that needs a build back into one slide.
- Count each poll as about 4 minutes (joining, waiting for votes, showing the answer, the reactions) and a discussion moment as about 3 minutes, and take them out of the time budget, not add them on top. Explaining the answer after a reveal belongs to the next beat's time. At most 2–3 interactions (polls and discussion moments together) per 30 minutes.
- For a community or meetup talk, aim lower than feels natural: about 5–8 key points for 30 minutes, plus 2 polls and one discussion moment; the rest goes to backup.
- Rough reference, with the arithmetic: 30 minutes with 2 polls (about 8 minutes) and one discussion moment (about 3 minutes) leaves about 19 minutes of real explaining time. Divided by 2.5, that is under 8 minutes of script read aloud (about 900 English words or 1,400 Chinese characters for the whole main story), and about 5–8 key points including the opening and closing. These numbers only check the estimate; the script decides. The number of physical slides varies with builds; 20 or 30 slides can both be right.

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
- **Use the space the content needs, no more and no less.** A box much bigger than its text, or a slide that looks half finished, signals that the layout needs work: shrink the box to fit, or enlarge the text and chart to use the space (staying within one idea). Empty space is a signal to look again, not a quota to fill; a short, clean list with room around it is often the easiest slide to read.
- **A good visual lets the audience understand the point by looking at it.** That means an illustration that shows the idea itself, not a symbol placed next to it. For example, for "tested on only one robot", one robot drawn in colour beside several greyed-out robot outlines; for "only 2 of 10 runs finished", ten small task icons with two complete and eight stopped part-way. Someone who sees only the picture should already grasp the point; the words confirm it. A thumbnail of an earlier figure or result the point refers to also works, because the audience recognises it at once.
- **Simple symbols are not visuals.** A `?`, `≈`, a generic icon or a big standalone number does not show the idea (the exception is a `?` marking the missing slot in a structure, which shows the question); the audience has to decode it, which makes the slide harder. Do not add them to decorate or to fill space. If no illustration genuinely shows the point, a clean text slide is better than a decorated one. Never invent stand-ins for the paper's own figures or results.
- **One reading path.** The audience should know where to start and in which order to read: the largest text is the point itself, not a decoration, and items run in one direction in the order the speaker talks about them. A grid of cards where each card has several entry points (a big symbol, a heading, a detail line) makes people jump around and tires them out.
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

When building with python-pptx, read `references/pptx-techniques.md` first and use the helpers in this skill's `scripts/slide_kit.py` (template header / title / footer, callouts that fit their text and can be centred, curved and block arrows, red frames, dimming masks and hiding, native bar charts with negative values, real bullet lists, titled blocks in the template's colours, autoplaying and looping videos, QR codes, coordinate conversion). Use `bullets()` for lists instead of typing '•' (a typed bullet has different widths in CJK and Latin text, so wrapped lines misalign). Check the result with `scripts/render_check.py`: it renders every page, a thumbnail sheet for layout, and `footers.png`, a full-resolution strip of every footer. Then run `scripts/audit_text.py` for font sizes and sentence-like text (section 3a), and `scripts/layout_check.py` for elements off the slide, overlapping text, arrows that land on nothing, callouts lying on content, arrows too short to follow, block arrows lying on a figure, straight arrows on a slant and curved arrows that leave or enter at a slant; `--list` prints every element's real box, so query positions there instead of guessing them.

**Show the result when the deck is done**, and again after every revision the user asks for: render it to a PDF and open it beside the conversation where the session can (for example `SendUserFile` with `display: 'render'` opens it in the side panel), so the user looks at the deck itself instead of reading a description of it.

## 11. Final checklist

- [ ] The core question and the chain of beats were written and checked before material was chosen; the audience can retell the core idea in one sentence
- [ ] Click-through check: every slide hands over to the next with a question or a "so…"; no seams where a new topic starts cold
- [ ] Every slide passes the see + hear and carry tests; no concept is explained on two slides (returning to the map does not count)
- [ ] No formulas, architecture or training details in the main story of a community talk; they sit in backup slides after the closing
- [ ] Baselines use plain words, not acronyms; titles are short topics or questions, never the answer a slide reveals, the same across build steps, with no repeated "label: sentence" formula; at least one think/discuss moment
- [ ] The talk opens by defining the problem
- [ ] Real time estimated as read-aloud script time × 2–3, plus videos and interactions, is within budget (not estimated from page count or from read-aloud time alone)
- [ ] Every slide with an order to it (question and answer, prediction and result, set-up and punchline, hook) reveals in the order it is spoken; no answer or hook is visible before the speaker reaches it; only at-a-glance relationships and tension-free parallel sets appear at once
- [ ] Each slide's presentation was chosen for the point it makes
- [ ] Every term's meaning is clear on the slide that first introduces it; no glossary slide
- [ ] Red frames, arrows and callouts appear only on their own step and are gone on the next; discussed content is masked, every build step zoom-checked so no mask cuts through an element or covers the current one; dimming masks have no outline or shadow
- [ ] Every callout drawn with `annotate()`, its arrow landing on the callout and nothing running off the slide (`scripts/layout_check.py` reports no `OFF`, `OVERLAP`, `ARROW`, `CROWD`, `SHORT`, `BLOCK` or `SLANT`); every callout arrow starts at what it explains and ends at the callout; no thick block arrow lies on a picture, chart or table (thin arrows there), no straight arrow runs on a slant (curves there); one arrow style and colour per slide and its steps; boxes fit the text; text readable from the back row (≥ 28 pt)
- [ ] Notes are short and spoken (no parentheses, glosses or stage directions); every long note led to a split, a cut or a move to backup
- [ ] Template chosen in the order of section 8; footer credit names the source, presenter is on the cover
- [ ] Header and footer drawn with `chrome()`; `footers.png` from `render_check.py` shows footer text vertically centred inside its band on every page
- [ ] Numbers match the source; build steps share page numbers
- [ ] Videos embedded with `video()` and a poster frame; playback tested in PowerPoint, or the handoff says it was not tested
- [ ] Lists use `bullets()` (no typed '•'); every QR or event-code placeholder is listed in the handoff
- [ ] Every on-slide line is a keyword or number, not a sentence; every slide re-read from the audience's seat; `audit_text.py` reports no `SMALL`, `LONG`, `ARROW` or `HOOK` lines except author lists and source credits
- [ ] Body text ≥ 24 pt, captions ≥ 22 pt, callouts ≥ 28 pt
- [ ] Red marks the key point wherever it is (callout, bullet, label, cell), one or two marks per slide; key words inside body text are marked too; supporting callouts are not all red
- [ ] Text and blocks beside media are vertically centred on the media, not stuck to the top
- [ ] No box much larger than its text; every visual shows the idea itself (illustrations the point can be understood from, not decorative icons or symbols to decode); each slide has one clear reading path with the point as the largest text
- [ ] No typed arrows in normal slide text (equations excepted); every line reads naturally in about three seconds
- [ ] Every poll has an answer in the source, is not given away by the title or description, is likely to be guessed wrong, and its reveal opens the next key point
