# Worked examples

Two promotions made for the same weekly reading group (Discord event, title prefix `討論分享｜`, fixed lines for Slido and the source link). The previous event, which set the format, used a cartoon "Model-Based ↔ Model-Free" comparison image and a three-line description.

---

## 1. Compare cover: AHa-3D (video → interactive 3D scene)

**Source:** a project blog, <https://kevinxu02.github.io/real2sim-indoor-site/>. GPT-6 Astra plus a harness of 3D tools (camera estimation, measurement, X-Ray outline overlay, physics checks) turns an ordinary room video into a Blender scene a robot can interact with.

**Why compare:** the work turns an input (a real video) into an output (a simulated room). The page has a frame of the source video and a render of the reconstruction **from the same room** (`media/scene-sync/open_concept_g0034/source.jpg` and `media/interactions/scene-interactions.jpg`), so the difference is the method.

**Rejected candidates:**
- the motivation strip (source / without harness / with harness). It is a good talk slide, but the three-way difference is too subtle at thumbnail size;
- X-Ray before/after. The outline moves by a few pixels, which is invisible on a card.

**Spec:**
```json
{
  "layout": "compare",
  "left":  {"image": "figures/source.jpg", "label": "Real Video"},
  "right": {"image": "figures/scene-interactions.jpg", "crop": [0, 0, 1920, 960], "label": "Simulation"},
  "center": "Agent +\n3D Tools"
}
```
The `crop` drops the caption bar burned into the bottom of the render.

Result: `../assets/example-compare.jpg`

**Text:**
```
討論分享｜一支影片變成模擬房間：AI Agent 自己蓋 Real2Sim 場景

只給 GPT-6 Astra 一支室內影片，它就能自己寫 Blender 程式，把房間重建成機器人可以互動的模擬場景。關鍵在於一套「建模 → 檢查 → 修正」的流程和 3D 工具。一起看它怎麼做到，也聊聊還做不好的地方。

📱 現場有 Slido 投票，請帶手機
📄 原文：https://kevinxu02.github.io/real2sim-indoor-site/
```
A first draft had four paragraphs (every tool named, the authors, all three limitations) and the user cut it. That is too long for an event card.

---

## 2. Showcase cover: matt-flow (a workflow tool)

**Source:** a GitHub repo, <https://github.com/kevin801221/matt-flow-mods>. A Claude Code mod that keeps Claude on Matt Pocock's development flow: it blocks code edits until the right step, and hands the next command to the user when a step finishes.

**Why showcase:** the work is a process, not an input→output transform. The idea is "steps in order, skipping is blocked", which a row of steps with a blocked dashed arc shows directly.

**Picture choice:** the README's screenshots are full terminal windows, and their text is unreadable at card size. Only the side panel (level, step list, next-step card) is cropped from `docs/images/pane.png`, and it is placed on the right as proof that the tool is real.

**Spec:**
```json
{
  "layout": "showcase",
  "title": "matt-flow",
  "subtitle": "讓 Claude Code 照流程走",
  "steps": ["問清楚", "寫規格", "動手做", "檢查", "複盤"],
  "highlight": 2,
  "skip": {"from": 0, "to": 2, "label": "想跳步？擋下來"},
  "footer": "每一步做完，把下一步指令交給你",
  "image": {"path": "figures/pane.png", "crop": [792, 18, 640, 500]}
}
```

Result: `../assets/example-showcase.jpg`

**Text:**
```
討論分享｜matt-flow：讓 Claude Code 乖乖照開發流程走

用 Claude Code 寫程式，常常需求還沒問清楚它就開始改程式。matt-flow 把 Matt Pocock 的開發流程（問清楚 → 寫規格 → 動手做 → 檢查 → 複盤）變成一條軌道：Claude 想跳步會被擋下來，每一步做完就把下一步交給你。一起看它怎麼做，也聊聊這種護欄適不適合你。

📱 現場有 Slido 投票，請帶手機
🔗 專案：https://github.com/kevin801221/matt-flow-mods
```

This topic replaced AHa-3D when the speakers swapped weeks. The AHa-3D set was kept for the later week rather than thrown away.
