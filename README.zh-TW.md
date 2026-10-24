<div align="center">

# 📑 paper-sharing-skills

**論文分享用的 Claude skill 集合：從收集論文素材，到站上台把它講清楚。**

專案資料夾與素材收集（附來源）· 以觀眾理解為核心的論文討論簡報（PPTX 或 Canva）· 只在需要分步推理時才拆頁 · 紅框精準對齊 · 每個說明框都有箭頭 · 用要點估時間，不用頁數。

![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-D97757?logo=claude&logoColor=white)
![Skills](https://img.shields.io/badge/skills-2-8A63D2)
![Python](https://img.shields.io/badge/python-3-3776AB?logo=python&logoColor=white)
![python-pptx](https://img.shields.io/badge/python--pptx-helpers-B7472A?logo=microsoftpowerpoint&logoColor=white)
![Version](https://img.shields.io/badge/release-v0.3.0-success)
![License](https://img.shields.io/badge/license-MIT-blue)

[English](README.md) · **繁體中文**

</div>

---

這個 repo 裡的每個 skill 都遵守同一個原則：**一切為了觀眾理解。** 遇到規則沒涵蓋的情況，Claude 會問自己「這樣做能讓觀眾更容易懂嗎？」——不能，就不做。規則是判斷工具，不是預設套用的模板。

可在 **Claude Code**、**claude.ai** 與 **Claude 桌面版**使用。

## ✨ 功能

📁 一篇論文一個資料夾 · 🔗 每個素材都有來源 · 🙋 真的抓不到才請你幫忙 · 🎯 先定義問題 · 🪜 必要時才分步 · 🟥 紅框精準 · ➡️ 箭頭連到說明 · 📖 專有名詞寫全稱 · ⏱️ 用要點估時間 · 🎬 影片與 QR code · 🌍 任何語言

<details>
<summary><b>各項說明 →</b></summary>

<br>

- **📁 一篇論文一個資料夾。** `paper-project-setup` 建立結構清楚的專案資料夾（`source/`、`figures/`、`videos/`、`posters/`、`data/`、`screenshots/`），附 README 與 `manifest.json`。
- **🔗 每個素材都有來源。** 每張圖、每段影片、圖表數據與截圖都記錄在 manifest 中（類型、標題、來源網址、取得方式），簡報圖說可以正確標註出處。
- **🙋 真的抓不到才請你幫忙。** Claude 會先嘗試直接下載、釋出檔案（GitHub / Hugging Face）與瀏覽器擷取；必須請你幫忙時，會把需求寫清楚到一次就能完成。抓不到的項目記在 `missing` 清單。
- **🎯 先定義問題。** 每份簡報都先講清楚論文要解決的問題，再談方法。
- **🪜 必要時才分步。** 只有需要一步步推理的概念才會用「減法」拆成多頁，不會預設拆頁。
- **🟥 紅框精準對齊。** 紅框對準圖中確切的區域，並用頁面渲染圖檢查。
- **➡️ 箭頭連到說明。** 每個說明框都用箭頭連到它在解釋的東西；框貼合文字，字夠大。
- **📖 專有名詞寫全稱。** 每個專有名詞第一次出現時寫出全稱並用白話解釋。
- **⏱️ 用要點估時間。** 時間預算依要點數量與每頁完整講稿長度估算，而不是頁數。
- **🎬 影片與 QR code。** 輔助函式可嵌入自動播放並循環的展示影片、QR code（例如 Slido）、真正的項目符號、雙向長條圖與置中說明框。
- **🌍 任何語言。** Skill 本身以英文撰寫；簡報與講稿可指定任何語言（例如繁體中文）。

</details>

---

## 🧩 Skills

| Skill | 功能 | 版本 |
| --- | --- | :---: |
| [`paper-project-setup`](skills/paper-project-setup/SKILL.md) | 為一篇論文或一個主題建立專案資料夾，收集 PDF、圖片、展示影片、圖表數據、截圖並記錄來源：能自動下載就自動（直接下載、釋出檔案、瀏覽器），真的抓不到才請使用者幫忙，並維護每個素材的 manifest 與缺漏清單。 | v0.2.1 |
| [`paper-discussion-slides`](skills/paper-discussion-slides/SKILL.md) | 製作以觀眾理解為核心的論文討論／讀書會簡報（PPTX 或 Canva）。附參考模板簡報、繪製模板頁首頁尾的 `chrome()`，以及產生頁面渲染、縮圖總覽與頁尾放大條的檢查工具。 | v0.2.0 |

之後會陸續加入更多論文分享相關的 skill。

### 兩者如何搭配

```mermaid
flowchart LR
    A["📄 論文連結<br/>或標題"] --> B["paper-project-setup<br/>資料夾 + 素材 + manifest"]
    B --> C["paper-discussion-slides"]
    C --> D1["定義問題"]
    D1 --> D2["規劃要點<br/>+ 時間預算"]
    D2 --> D3["一頁一個概念<br/>+ 完整講稿"]
    D3 --> D4["必要時<br/>分步呈現"]
    D4 --> D5["檢查紅框、名詞、<br/>說明框、時間"]
    D5 --> E["🎤 簡報 + 講稿"]
```

製作簡報前若論文還沒有專案資料夾，Claude 會先執行 `paper-project-setup`，再進入簡報流程。

---

## 📸 範例模板

簡報 skill 附一份參考簡報（[`sample-template.pptx`](skills/paper-discussion-slides/assets/sample-template.pptx)），示範版面規則：封面、附箭頭提問說明框的圖、精準對齊的紅框與說明、以及附 Slido QR 預留位的區塊元素。

[![四張範例投影片：封面、附箭頭說明框的圖、對齊的紅框、區塊元素](skills/paper-discussion-slides/assets/sample-template-preview.png)](skills/paper-discussion-slides/assets/sample-template-preview.png)

也可以使用你自己的模板——Claude 會讀取它的頁首頁尾版面，並用 `chrome()` 繪製。

---

## 🚀 安裝

### Claude Code

```bash
/plugin marketplace add whats2000/paper-sharing-skills
/plugin install paper-sharing-skills@paper-sharing-skills
```

### Claude 桌面版 / claude.ai

從 [Releases](../../releases) 下載 `paper-sharing-skills.plugin` 安裝到 Claude，或把 `skills/` 底下任一資料夾作為單獨的 skill 上傳。

> [!NOTE]
> 輔助腳本只需要 Python 標準函式庫，簡報另需 `python-pptx`。影片壓縮與擷取畫面使用 `ffmpeg`，圖片檢查可選用 Pillow。

---

## 💬 使用方式

直接描述你的需求即可：

- *「幫我做這篇論文的讀書會簡報，用繁體中文，20 分鐘。」*
- *「用我的模板（附件）做這篇論文的 journal club 簡報。」*
- *「幫這篇論文建立資料夾，並從專案頁面收集圖片和展示影片。」*
- *"Make a 30-minute discussion deck for this paper; the audience is students interested in robotics."*

---

## 🛠️ 新增 skill

1. 在 `skills/` 底下建立 kebab-case 命名的資料夾（例如 `paper-reading-notes`）。
2. 加入以 YAML frontmatter 開頭的 `SKILL.md`（`name` 與第三人稱撰寫的 `description`，包含使用者可能說的話）。
3. 內文寫成給 Claude 的指示；長範例與規格放 `references/`，程式碼放 `scripts/`。
4. 把 skill 加進上方表格，並更新 `.claude-plugin/plugin.json` 與 `marketplace.json` 的版本號。

> [!TIP]
> 新 skill 請維持同樣的原則：每條規則都要回答「這樣能讓觀眾或讀者更容易理解嗎？」

完整的目錄結構與輔助腳本說明請見 [English README](README.md)。

---

## 📚 引用

如果這些 skill 對你的演講或研究有幫助，歡迎引用：

```bibtex
@software{paper_sharing_skills,
  author  = {Ren-Di, Wu},
  title   = {{paper-sharing-skills: Audience-First Claude Skills for Sharing Research Papers}},
  year    = {2026},
  url     = {https://github.com/whats2000/paper-sharing-skills},
  version = {0.3.0}
}
```

---

## 📄 授權

[MIT](LICENSE) — © whats2000。
