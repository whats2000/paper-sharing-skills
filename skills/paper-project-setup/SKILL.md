---
name: paper-project-setup
description: Sets up a project folder for one paper or topic and collects its media assets (paper PDF, figures, demo videos, chart data, screenshots) with source attribution, going to known sources first (arXiv source package via export.arxiv.org, the project page's GitHub repo, original pages by web search for non-paper topics) and asking the user to download only what truly cannot be fetched. Use before preparing a paper talk, or when asked to "set up a folder for this paper", "collect the figures and videos from the project page", "download the assets", or 建立論文資料夾／收集素材.
---

# Paper Project Setup

Create one tidy, self-describing folder per paper or topic and fill it with the original media the talk will need. This skill prepares material; designing the slides is the job of `paper-discussion-slides`.

Assets exist to let the talk get its concepts across, so **collect for the storyline, not for completeness**: sketch what the talk needs to say first, derive the asset list from it, then go and find those assets.

Principle: **collect what the story needs, collect originals, record where everything came from, and make the user do as little as possible.** Try every automatic route before asking the user to download anything, and when asking, make the request precise enough to finish in one pass.

---

## 1. Identify the sources

First decide what kind of topic this is, because each kind has its own fastest route to original media:

| Topic | Where the originals live | Go here first |
|---|---|---|
| **A paper on arXiv** | the arXiv source package (original figure files + `.tex` captions), then the project page | `export.arxiv.org` (section 4, route A) |
| **A paper with a project page** | the project page and its own source repository (images, videos, chart data) | the page's GitHub repo (section 4, route B) |
| **A paper not on arXiv** (publisher, OpenReview, tech report) | the publisher PDF / supplementary, the project page, the code repo | the project page and repo |
| **Not a paper** (a product, system, event, technique, a project without a paper) | the original pages: official site, announcement blog, docs, the original video upload | web search for the original pages (route E) |

Then find and record every place the material lives:

- the paper itself: arXiv ID (from the title by web search), publisher PDF, or technical report
- the **project page**: linked on the arXiv abstract page (comments / links), on the paper's first page or abstract, in the code repo's README, or as the repo's "homepage" field; very often `<owner>.github.io/<name>/`
- code and data (GitHub, Hugging Face) for released result tables and logs
- supplementary material and video hosts (YouTube, Vimeo, CDN links)

Note what kind of source each is (peer-reviewed paper and venue, preprint, technical report, blog, product page) and its date; the talk will need to say this.

## 2. Create the project folder

Ask where projects live if it is not known (e.g., a `Paper/` folder on the user's computer); otherwise use the location the user names. Create one folder per topic with a short kebab-case name, and run `scripts/asset_tools.py init <dir> --title "<paper title>" --url <each source page>` (the title is required; add `meta <dir> --source-type <type> --date <date>` too) to lay out:

```
<topic>/
  README.md          # what the paper is, links, source type, date, folder guide
  manifest.json      # one entry per asset (see section 6)
  storyline_draft.md # rough beats and the asset each one needs (section 3)
  source/            # paper PDF, saved page text / HTML, BibTeX
  figures/           # original images at full size (never only thumbnails)
  videos/            # original videos (+ compressed copies if needed)
  posters/           # still frames extracted from videos
  data/              # chart data (CSV / JSON) and tables
  screenshots/       # page or chart screenshots when no original exists
```

Keep originals untouched; write derived files (crops, compressed videos, redrawn charts) next to them with a suffix such as `_small.mp4` or `_redrawn.png`.

## 3. Draft the storyline, then derive the asset list

Read the paper before collecting media. Get the text sources first (route A's PDF and source package for an arXiv paper, the project page HTML, the publisher PDF, or the original pages for a non-paper topic) and read the abstract, introduction, figures and conclusion.

Then sketch the talk in `storyline_draft.md`, briefly (it is a draft for `paper-discussion-slides`, which refines it; see that skill's `references/storyline.md`):

1. **The core question and the one core idea**, in two or three spoken sentences: what the audience should wonder for the whole talk, and what answers it.
2. **The beats**, one line each: the question the audience arrives with → what they must see or hear to answer it → the question they leave with. A common backbone: why the problem arises → where the idea comes from → what it achieves → reflection.
3. **For each beat, the asset that shows it**: what kind (figure, video, chart data, screenshot, or a diagram to draw), which one if known ("Fig. 3, shortcut policy vs. SOTA"; "demo video of task X"), and where it probably lives (paper source, project page, code repo, another page).

The asset list is these per-beat needs. Look especially for what the paper itself does not supply but the story needs: what the audience must picture before the problem makes sense (e.g., what a benchmark task looks like, a real robot clip, the previous method's figure), usually found on the original pages of the related work, the dataset or the tool (route E). Add a few backup items for questions the audience will likely ask (the main results table, a key ablation). Leave out media no beat uses, however good it looks.

If the user is present, show the core question, the beats and the asset list in one short message before collecting; it is the cheapest point to redirect. Otherwise state it and continue.

## 4. Collect the assets: known routes first

Collect the asset list from section 3. Before downloading, say what you will collect (count, types, rough size) in one message; the user's request to collect assets is the go-ahead for that list. Ask again before anything outside it. If collecting turns up something that changes the story (a better figure, a demo video you did not know about), update `storyline_draft.md` and the list rather than collecting it on the side.

Work through the routes that fit the topic (section 1), in this order. When a host refuses, move to the **next route for that same material**; do not skip to the browser or to the user while a known route is untried.

**A. arXiv: `export.arxiv.org`, always first for an arXiv paper.** It is arXiv's official host for programmatic access and is often reachable when `arxiv.org` is not. Use the same paths with that host:

- `https://export.arxiv.org/e-print/<id>`: the **source package** (usually a gzipped tar). It holds the original figure files (PDF / PNG / JPG, full resolution, often vector) and the `.tex` with every caption. This is the best source of paper figures; take figures from here before screenshotting the PDF. Unpack into `source/arxiv_src/`, copy the figures used in the paper into `figures/` (convert vector PDFs to PNG at 300 dpi for slides, keep the PDF too), and map each file to its figure number using the `\includegraphics` and `\caption` lines.
- `https://export.arxiv.org/pdf/<id>`: the paper PDF into `source/`.
- `https://export.arxiv.org/abs/<id>`: the abstract page (comments field: venue, project page link); `https://export.arxiv.org/api/query?id_list=<id>`: metadata (title, authors, dates, versions) as Atom XML; BibTeX from `https://arxiv.org/bibtex/<id>` (if blocked, build it from the API metadata).

If the e-print is a single PDF (author uploaded no source), note it and rely on the project page for figures.

**B. Project page: get it from its source repository.** Project pages are usually static sites hosted on GitHub Pages, so the original media files sit in a public repository:

- `https://<owner>.github.io/<name>/` is served from `github.com/<owner>/<name>` (branch `gh-pages` or `main`, sometimes under `docs/`); `https://<owner>.github.io/` from `github.com/<owner>/<owner>.github.io`.
- When the page itself is blocked but GitHub is not, fetch the repo instead: `api.github.com/repos/<owner>/<name>` (default branch, `homepage` field), `api.github.com/repos/<owner>/<name>/git/trees/<branch>?recursive=1` (every file path), and `raw.githubusercontent.com/<owner>/<name>/<branch>/<path>` for each image, video and data file. Shallow-clone (`git clone --depth 1`) when there are many.
- Find the page's repo from the code repo README, the repo's `homepage` field, or by trying the `<owner>/<name>` that matches the URL path.
- Read the page's `index.html` from the repo to see which media it actually shows and in what order, and their captions; collect those, not every file in the repo.
- Videos embedded from YouTube / Vimeo are not in the repo; record their URLs (they can go on slides as links or QR codes) and add them to the user checklist only if a local copy is needed.

**C. Code and data repositories** (GitHub, Hugging Face datasets / Spaces) for the numbers behind the charts: result CSV / JSON, logs, released figures. Copy **only the files that back figures or tables in the talk** into `data/` (named after the figure they back); do not copy the whole repository into the project. Record the repo URL and commit in the manifest notes.

**D. Plain direct download** (`curl`, `wget`, Python `requests`) of any other public file URL found above.

**E. Topics that are not a paper**: web search for the original sources (the official site, the announcement post, the documentation, the original video upload, the maker's own GitHub) and collect media from those original pages, not from news reposts, aggregators or social media copies. Record each page as a source. Then apply routes B–D to them (official pages are often on GitHub too).

**F. A browser** (the built-in browser or Claude in Chrome, whichever is available) only when the routes above cannot reach a file, or the page builds its media with JavaScript:

- read the page and list every image, video and data URL with a script (see `references/browser-extraction.md`);
- let the browser download them (they land in the user's Downloads folder), then move them into the project folder;
- for interactive charts, read the underlying data from the page's scripts (often `data.js` or embedded JSON) and save it to `data/` instead of screenshotting the chart;
- screenshot only what has no downloadable original (e.g., an interactive figure), at full resolution, into `screenshots/`.

**G. Ask the user** only for what all routes above failed to fetch (section 5).

Practical notes:

- **Try every shell you have.** The cloud workspace and a shell on the user's computer can have different network allowlists (e.g., one reaches `export.arxiv.org`, the other only GitHub). Check which hosts each one reaches with one quick request per host before choosing where to download, and do not repeat a refused request with another command in the same shell.
- **Do not run `git clone` inside a folder synced from the user's computer** when file deletion there is restricted: git cannot remove its lock files and the clone fails half-way. Clone into a scratch directory, then copy the files you need into the project.
- Official alternative endpoints of the same site (`export.arxiv.org`, `raw.githubusercontent.com`, `api.github.com`, the page's own source repo) are fine to use. Never bypass a paywall, a login the user has not set up, or a site's refusal through third-party caches or mirrors. Download only publicly available material, for the user's own talk, and keep attribution.

## 5. When the user has to help

Ask once, with a complete checklist the user can finish in one pass:

- file name to save as, exact URL, and what it is (e.g., "Fig. 3, loss curves")
- where to put it (the exact project subfolder) or "anywhere, I'll move it"
- how to get it if not obvious (e.g., "right-click the video → Save video as")

Continue with everything else while waiting. When the files arrive, move them into place, rename them to the manifest names, and update the manifest.

## 6. Record every asset in the manifest

Add each asset with `scripts/asset_tools.py add` (or edit `manifest.json`). Each entry has:

| Field | Meaning |
|---|---|
| `file` | path inside the project folder |
| `type` | `pdf` (a PDF), `text` (saved page text or notes: .md / .txt / .bib), `page` (saved HTML / JS of a web page), `figure`, `video`, `poster`, `data`, `screenshot`; `add` refuses a type that does not match the file extension |
| `label` | what it is, e.g., "Fig. 1 benchmark results", "demo: pour bolts" |
| `source_url` | where it came from (page URL and, if different, the direct file URL) |
| `obtained` | `arxiv-source` (from the e-print package), `page-repo` (from the project page's source repo), `release` (code / data repo), `direct`, `browser`, `screenshot`, `user` |
| `notes` | which beat it serves (start with `beat N:` from `storyline_draft.md`, or `backup:`), caption, figure number, licence or attribution notes, anything odd |

Also record the assets you could not get and why with `asset_tools.py missing <dir> "what" --source URL --reason "why"`, so the gap is visible. `check` warns when the manifest has no title or sources, or an asset's type does not match its file.

## 7. Prepare assets for slides

- **Videos:** keep the original. If a file is too large for where it is going (e.g., an upload limit), make a compressed copy with `scripts/asset_tools.py shrink` (H.264, ~1280 px wide, CRF 28). Extract poster frames at a few points with `posters` so slides can show a still and highlight frames can be measured on it.
- **Figures:** keep full-size originals; highlight frames must be measured on the original, not on a thumbnail.
- **Charts:** prefer the underlying numbers in `data/` so charts can be redrawn cleanly and frames placed from exact coordinates.
- **Text:** save the page text or PDF so numbers can be checked against the source later.

## 8. Finish

1. Check every manifest file exists and opens (images load, videos play, data parses); `scripts/asset_tools.py check` does this.
2. Update the project `README.md`: paper title, authors, source type and date, links, and a short list of what was collected (by beat) and what is missing.
3. Tell the user in a few lines: where the folder is, what was collected, anything that still needs their help.

## Final checklist

- [ ] One folder per topic with the standard layout; originals untouched
- [ ] `storyline_draft.md` written (core question, beats, the asset each beat needs) before media was collected; every collected asset serves a beat or is marked backup
- [ ] Every source URL recorded; source type and date noted
- [ ] Topic type decided; for an arXiv paper the `export.arxiv.org` source package tried first; for a project page its source repo tried before the browser
- [ ] Every automatic route tried before asking the user; at most one consolidated request to the user
- [ ] Chart data saved as data where available, not only as screenshots
- [ ] Every asset in `manifest.json` with its source and how it was obtained; missing assets listed
- [ ] Large videos have compressed copies; poster frames extracted
- [ ] `check` passes
