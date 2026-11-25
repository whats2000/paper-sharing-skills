---
name: paper-slides-revision
description: Revises a finished paper-discussion deck slide by slide with the user in the loop, proposing fixes for known problems for the user to approve and applying their page-by-page feedback, without changing the storyline. Use after paper-discussion-slides has built a deck, or when asked to revise, polish, check or fix slides (修改簡報、修正第 N 頁、檢查簡報、改投影片), including decks made by hand or with other tools.
---

# Paper Slides Revision

The deck's storyline is already decided. This skill finds what goes wrong on individual slides and, with the user deciding what to change, fixes it so the audience can see and follow each slide, without changing what the talk says or the order it says it in. Work in the language of the deck.

## The storyline is fixed

- **Do not add, cut, merge or reorder beats.** Do not remove a return of the map (a recurring table or diagram), move content to backup, or replace a picture or diagram with text.
- **Fix locally:** the same point on the same slide, shown so the audience can read it.
- **When a fix seems to need a story change, do not make it.** List it for the user as a suggestion, with the reason.
- **Time is a rough guide to size only.** Never cut content to fit a time estimate.
- **Tool warnings are prompts to look, not gates.** Judge each one with two questions: is anything blocking what the audience needs to see, and is anything interrupting them? Leave a warning when fixing it would make the slide worse, for example a summary table the audience reads as one structure.

## Workflow

1. **Find the sources:** the deck, the script that builds it, the storyline file and the speaker notes. When a build script exists, edit the script and rebuild; do not hand-edit the PPTX, or the next rebuild loses the fix.
2. **Look at every build step as an audience member.** Render the deck with `render_check.py` from the `paper-discussion-slides` skill's `scripts/` folder.
3. **Run the checks** from the same folder: `layout_check.py deck.pptx` and `audit_text.py deck.pptx`.
4. **Go through the known problems below.** Note each finding with the page number in the footer and the physical slide number, because builds make them differ.
5. **Let the user decide before changing anything.** What you observe is a candidate, not a verdict: the presenter may want that heading, that text or that layout, for reasons you cannot see.
   - Show the findings first: the rendered pages (open the PDF beside the conversation), and a short list with the page, the problem and the fix you propose for each.
   - Ask which to fix. A multiple-choice question works well where the session has one; group findings of the same kind so the user decides once per kind.
   - Fix only what the user approves. Anything they decline stays as it is; do not raise it again.
   - The user's own feedback ("page 12: the arrow is wrong") is already a decision: apply it without asking again, and ask only when it is unclear which slide or what change they mean.
   - When the user is not there to answer, change nothing. Deliver the findings and the proposed fixes as a list for them to decide on later.
6. **Fix one approved item at a time** in the build script, rebuild, and re-render the slides you changed. An approved fix applies to every slide with the same problem; say which slides changed.
7. **Show the result:** render the deck to a PDF and open it beside the conversation where the session can (for example `SendUserFile` with `display: 'render'`). Add a short list of what changed, then ask whether anything else needs changing.

## Known problems

Each item gives what to look for and the fix to propose. Propose; the user decides (workflow step 5).

1. **Callout arrows.**
   - **A curved arrow that leaves its element or enters its callout at a slant** (`layout_check` reports `BEND`). Redraw it with `annotate()`, or with `curve_arrow()` when the layout is placed by hand. The curve goes straight out of the middle of one edge of the element and straight into one edge of the callout. For example: right edge into the top of a callout below and to the right, or bottom edge into its left edge.
   - **The arrow sets the reading order.** It starts at the middle of the element (or red frame) being discussed and ends on the callout, so the audience looks at the evidence first and then reads what it means. Never the other way round, and never a callout floating with no arrow.
   - **It neither blocks nor interrupts.** No callout or thick arrow lying on the figure. One arrow style and colour for a slide and all its build steps. Callout, arrow and frame leave with their step.
   - **When `annotate()` finds no free space,** change the layout of that slide: shrink the figure, shorten the callout, or move content. Do not place the callout by hand to force a fit.
2. **Text inside a figure too small to read from the back:** pie-chart labels, small panels, axis numbers.
   - Enlarge the figure, crop it to the part being discussed, or redraw the chart natively with larger labels.
   - Do not shrink anything else on the slide to make room.
3. **An analogy given only as text** when it maps onto the paper (a written test and real driving, compared with a benchmark score and real manipulation).
   - Draw the mapping as a small diagram with the same structure in both rows: what is tested, then what it is taken to prove.
   - The audience then sees how the analogy carries over. Same content, drawn.
4. **A results table that has to be read cell by cell.**
   - Colour each cell's background by its verdict.
   - Keep the evidence in the cell (the number or the drop, not only "fail").
   - Tie the rows to what the audience saw earlier (for example a thumbnail of each benchmark).
   - Frame the column or row being discussed on that step.
5. **A defined set that changes size or names**, such as four checks shown later as three cards or under new names. Restore the same count and names everywhere.
6. **An assumption and the twist that overturns it shown on the same step.** Give the assumption its own step and put the twist on the next, so the audience holds the belief before it breaks.
7. **Something that appears later drawn early under a white cover.** Give it the step it appears on instead. A cover is only for parts of one image that cannot be cropped apart; then check every step it is on, because it must not cut through a callout, an arrow or any other element of that step.
8. **Mask or annotation errors:**
   - a dimming mask that cuts through an element or covers the current point;
   - a mask with an outline or shadow;
   - a callout, arrow or frame left over from the previous step.

   Fix the parts given to `build_steps()`: annotations use `'remove'`, and content uses one mask per section block.
9. **A supporting item taking up the main space:** a QR code, a logo or a credit. Make it small and put it in a corner.
10. **Takeaways the audience must remember shown all at once:** the questions to ask, the rules, the conclusions.
    - Reveal them one per step, each with its own line of script, even when they are parallel.
    - Show a set at once only when it is a relationship understood at a glance, or a parallel set with no tension that nobody needs to remember item by item (eight test platforms do not need eight steps).
    - Reveal the items as they are. Do not turn a diagram or table into a bullet list to do it.
11. **Too much on a slide's last build step.**
    - Builds accumulate: each step adds a little, and the last step can still hold far more than anyone can read (a root-cause bar, four cards and two bullet blocks is seven text boxes on one screen).
    - Count the separate text boxes and blocks on the final step. A table or diagram the audience reads as one structure counts as one, so a returning map is never crowding.
    - When the audience could not take the final step in at a glance, move a group to its own slide right after it, so each slide makes one point. The order stays the same.
12. **Sub-headings nobody needs.** A small heading over a chart, block or list that repeats the slide title, names what is obviously there ("Results", "Overview"), or labels a single item.
    - Remove it.
    - Keep a heading only when the audience needs it to read what is under it: the axis or unit of a chart that has none ("success rate, %"), or the names of two columns being compared.
    - When a removed heading carried something worth saying, put it in the speaker notes.
13. **Text the speaker says, not text the audience needs to see.** Every line on a slide competes with the speaker for attention, so a slide shows only what the audience must look at to follow: the point, the evidence (the numbers they compare), the terms being introduced, the labels needed to read a figure, and the hand-over question.
    - Explanation, background, reasons, caveats, examples and asides go in the speaker notes, not on the slide.
    - Moving text to the notes deletes nothing: check that the script still says it, in spoken words.
    - Source captions under figures stay (small and grey), because they credit the source.
14. **Supplementary illustrations.** Check each item the audience must picture: would a small drawing of that item's own idea let them grasp it at a glance? Add one only then; if nothing qualifies, add nothing.
    - **The test is understanding, not space.** A diagram that carries the explanation is content and belongs to the slide already (see item 3). A supplementary illustration is a small drawing added for one reason only: it shows that item's own idea. For example, for "tested on one robot", one robot drawn among greyed-out outlines; or one small sketch per item in a list explained item by item.
    - **Blank space is never the reason.** Empty space is a signal to look again, not a quota to fill. A picture that only decorates fails the test.
    - **It changes nothing planned.** Never move, shrink, split or delay planned content for it. It uses only space that is empty on that step, and it leaves on the step before planned content (a summary, a conclusion) takes that space.
    - **Simple in style, specific in content.** All illustrations in the deck share one style that matches the template's tone; for a clean, formal template that means simple line drawings with an even stroke and a transparent background, not hand-drawn or realistic pictures. Each one shows its item's own idea, never a generic icon (a gear for "method", a light bulb for "idea") that the audience would have to decode. Simple symbols (`?`, `≈`, a big standalone number) are not illustrations.
    - **Only colours already in the deck.** List the colours the deck uses and what each one means (template colour, body and secondary text, the key-point red, chart colours). Add none: draw in a neutral already in the deck (for example the secondary-text grey), and use the key-point colour only on the one element that carries the point, so it means the same there as everywhere else.
15. **A conclusion or hand-over line under the content placed by eye** (`layout_check` reports `BOTTOM`: too high or too low in the free space), **or left small when there is room.** Text size steers attention: the audience reads the largest text first, so the point should stand out.
    - Redraw it with `bottom_line()` from `slide_kit.py`, called last on the slide (inside `draw()` for a build, given its own part). It measures the free space under the content across all build steps, ignoring a QR code off to the side, sizes the line to stand out (up to just below the title size), and centres it vertically in that space. It warns when the space is too small.
    - Look at the rendered result: the line sits in the middle of the space under the content.
    - Give lines of the same kind the same treatment across the deck. Supporting lines keep their size.

## Working from the user's feedback

- **Match the page they name to a slide.** The footer page number and the physical slide differ because of builds. When what they describe does not match the slide you found, say which slide you think they mean before you edit.
- **When they correct a rule** ("arrows should…"), apply it to every slide with the same problem and say which slides changed.
- **Keep one live file.** When the original is locked (open in PowerPoint), save under a new name and tell the user. Once the original can be written, update it and move the extra copy aside.
- **Build every language version from one source,** through a translation table, so later edits reach all of them. Check each version's layout on its own, because text length differs between languages.
- **Show the result after every change,** as in step 7 of the workflow.

The fixes collected here are candidates for the slide-making skill later. Keep them here until a test run shows that adding one there does not hurt the story.
