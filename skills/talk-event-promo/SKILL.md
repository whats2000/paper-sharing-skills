---
name: talk-event-promo
description: Makes the promotion for an upcoming paper or project talk, meaning a cover image for the event banner (Discord event, Meetup, slide-free announcement) and a short event title and description. Use when asked to choose or design an event cover, write an event intro, announce next week's sharing, 做活動封面、宣傳圖、活動簡介、下週分享的介紹, or when the topic of a scheduled talk changes and the promotion has to be redone.
---

# Talk Event Promo

A talk's promotion has one job: let someone scrolling past the event decide in a few seconds whether they want to come. The cover shows the idea and the text says why it is worth an hour. Neither tries to teach the topic. That is the talk's job.

Principle: **one glance, one idea.** If a picture or sentence makes people stop and decode it, it is not doing its job. Ask: "Would someone who has never heard of this topic get the point from the thumbnail and the first sentence?"

Write the title and description in the language the user asks for (default: the language the user writes in). Match the format of the group's earlier events when the user shows one (screenshot or text). Reuse its title prefix, its fixed lines and its tone.

---

## 1. Read the source first

Open the paper, project page or repo and find:

- **the one-sentence problem.** What was hard or annoying before this work?
- **the one-sentence answer.** What does this work do about it?
- **the honest limit.** What it still cannot do. A discussion event promises a discussion, so name one limit.
- **every image and video on the page**, with its URL and what it shows. List them with a script when the page builds itself with JavaScript (see `paper-project-setup`'s `references/browser-extraction.md`). If the topic already has a project folder, use its `manifest.json`.

If the shell cannot reach the host, use a browser (section 4).

## 2. Choose the cover

Pick the layout from what the work *does*, not from what images happen to look nicest:

| The work… | Layout | Example |
|---|---|---|
| turns an input into an output (video → 3D scene, sketch → app, photo → mesh) | **compare**: input on the left, output on the right, a centre badge naming the method | real room video ↔ simulated room, badge "Agent + 3D Tools" |
| improves something (before → after) | **compare** with "Before" / "After" labels | baseline vs. method on the same example |
| is a tool, workflow or process (a plugin, a pipeline, an agent loop) | **showcase**: title, the steps as a row of boxes with the key one highlighted, the tool's own UI cropped on the right | matt-flow: five steps, a dashed "skip" arc that gets blocked, the panel screenshot |

Rules for the pictures:

- **Use the work's own images.** Do not generate illustrations to stand in for them. The two halves of a compare cover should show *the same scene* so the difference is the method.
- **Prefer the pair whose difference shows at thumbnail size.** A subtle before/after (a few centimetres of misalignment) does not read on a 400 px card. Use it in the talk, not on the cover.
- **Crop screenshots to the part that matters.** A full terminal or full web page shrinks to unreadable text. Crop the panel, chart or result region, and give the crop at original resolution.
- **Drop overlays from the source.** Captions, progress bars and watermarks burned into a frame should be cropped out.
- **Few words on the cover.** A short title or two labels plus at most one badge or one warning line. No emoji in Pillow-rendered text (they draw as boxes). Labels are in English or the event language, consistently.

Size: 1600 × 640 (2.5 : 1, Discord's event banner ratio; it also crops sensibly for Meetup and social cards). Use another size only when the user names the platform and its size.

## 3. Render the cover

Write a spec next to the images and run `scripts/make_cover.py` (Pillow; finds a CJK font automatically, or pass `--font`):

```bash
python3 scripts/make_cover.py cover.json cover.jpg --preview cover_thumb.png
```

`compare` spec keys: `left` / `right` (`image`, optional `crop` [x, y, w, h], `label`), `center` (badge text, `\n` for a line break).
`showcase` spec keys: `title`, `subtitle`, `steps`, `highlight` (index), optional `skip` (`from`, `to`, `label`), `footer`, `image` (`path`, `crop`), `accent` colour.
The script's docstring has complete examples.

Then **look at both files** (open them with Read):

- the full cover: labels sit on calm areas of the picture, the badge does not hide the key object, nothing is cut at the edges;
- the 400 px preview: every word still reads, and the idea still comes across. If not, cut words or choose a bigger crop.

When neither layout fits, draw the cover in a browser canvas or with Pillow by hand, and keep the same rules.

## 4. When the shell cannot fetch the images

Many hosts are blocked for the workspace shell. In a browser (built-in browser or Claude in Chrome), open a page **on the image's own origin** (e.g., the project site, or the raw image URL), draw the images onto a `<canvas>` there (same origin, so the canvas is not tainted), and export `canvas.toDataURL('image/jpeg', 0.85)`. A long data URL comes back in pieces. Read it with `slice()` in chunks of about 70,000 characters, join them and decode them in the shell. Do not set `crossOrigin` on images that are already same-origin, because a redirect can then hang the load.

## 5. Write the title and description

**Title:** `<group prefix>｜<what it does, in plain words>`. Lead with the outcome a newcomer understands ("一支影片變成模擬房間"), not the paper's acronym. Put the acronym in the description or leave it out.

**Description:** short. Users cut long ones. Aim for **two or three sentences, about 80–150 Chinese characters or 50–90 English words**, then the group's fixed lines:

1. the problem or the hook, in one sentence
2. what the work does about it, and the key idea in a few words
3. the invitation, which says what we will look at *and* one limit or open question to discuss

Then the fixed lines the group always uses (e.g., `📱 現場有 Slido 投票，請帶手機`, `📄 原文：<link>` or `🔗 專案：<link>`). Emoji are fine in the text. They just do not belong in the rendered cover.

Do not list every tool or component, do not repeat the title, and do not promise results the source does not show. A link to the previous session ("this continues last week's…") is worth one clause only if it is true and helps newcomers too.

Read `references/examples.md` for two finished examples (a compare cover and a showcase cover) and their text.

## 6. Deliver

Send the cover file and give the title and description in a code block, ready to paste. If the topic changes (speakers swap, a talk moves), redo the cover and text for the new topic and say which week the old set now belongs to.

## Final checklist

- [ ] Layout chosen from what the work does (input→output, before→after, or process)
- [ ] The work's own images; same scene on both halves of a compare cover
- [ ] Screenshots cropped to the part that matters; burned-in captions removed
- [ ] Full cover and 400 px preview both checked by looking at them
- [ ] No emoji in the rendered cover
- [ ] Title leads with the plain-language outcome
- [ ] Description is two or three sentences plus the group's fixed lines, and names one limit or open question
