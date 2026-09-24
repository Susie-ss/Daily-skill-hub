---
name: pm-daily-news
description: Collect and aggregate daily product manager news from global sources (domestic and international blogs, newsletters, communities) and write a structured Markdown digest to a dated file. Triggers include 产品资讯日报, 每日PM资讯, product news digest, daily PM update, 产品经理动态汇总.
agent_created: true
version: 1.0.0
---

# PM Daily News Skill

Collect product manager news from global sources every day and write a structured
Markdown digest to a dated file.

---

## Overview

This skill:
1. Searches a curated list of sources (see `references/sources.md`) for today's PM news.
2. Deduplicates results and groups them by category.
3. Translates key English snippets into Chinese summaries when needed.
4. Writes the full digest to `<output_dir>/YYYY-MM-DD-每日资讯.md`.
5. Optionally appends a one-line entry to `<output_dir>/index.md` for navigation.

---

## Trigger Detection

Activate this skill when the user mentions:
- 产品资讯 / 产品经理资讯 / PM资讯 / 产品动态
- daily product news / PM digest / product manager news
- 每日资讯 / 每日更新 / 今日资讯
- 定时收集资讯 / 自动生成日报

---

## Execution Workflow

### Step 1 — Resolve Output Path

Default output directory: `~/Documents/Daily news/产品经理日报/`

If the user specifies a different directory, use that instead.
Create the directory if it does not exist:

```bash
mkdir -p <output_dir>
```

### Step 2 — Determine Today's Date

```bash
date +%Y-%m-%d          # macOS / Linux
```

Use this value as the filename: `<output_dir>/YYYY-MM-DD-每日资讯.md`

### Step 3 — Collect News

Use `WebSearch` and `WebFetch` to pull the latest content from the source list in
`references/sources.md`. For each source category, run targeted searches:

**Recommended WebSearch query patterns:**

| Category              | Query examples                                                   |
|-----------------------|------------------------------------------------------------------|
| 产品设计              | `site:sspai.com 产品 OR 设计` / `少数派 产品经理 {date}`        |
| 产品思维/方法论        | `product management best practices {date}` / `PM methodology`   |
| 行业动态(国内)         | `产品经理 行业资讯 {date}` / `人人都是产品经理 最新`             |
| 行业动态(国际)         | `ProductHunt today` / `Hacker News product {date}`              |
| AI & 技术趋势         | `AI product news {date}` / `AI工具 产品 {date}`                 |
| 创业 & 增长            | `startup growth hacking {date}` / `增长 产品 {date}`            |
| 用户研究 & UX          | `UX research news {date}` / `用户体验 {date}`                   |
| Newsletter精选        | `Lenny's Newsletter` / `FirstRound Review latest`               |

For **each category**, gather 3–8 items. Each item must include:
- Title (原文标题)
- Source name
- URL
- 1–2 sentence Chinese summary

**Always check the previous run date first.** Read the most recent report filename in
`<output_dir>` (or the automation memory file) and, if there is a gap of more than
one day, explicitly cover the whole uncovered window in this run — search with
`freshness` set to span the gap and label items with their actual publication date.
Skipped runs are normal (automation pauses, weekends); do not silently drop news.

**Recommended `freshness` values:** `d7` for a normal daily run, `d1`/`d2` if you
already covered yesterday, wider spans only when filling a multi-day gap.

### Step 4 — Run the Aggregation Script (Optional Enhancement)

The script `scripts/collect_news.py` can be used to do additional post-processing
(deduplication, sorting by relevance). Run it if the manual search yields >30 raw items:

```bash
python3 scripts/collect_news.py --date YYYY-MM-DD --output <output_dir>
```

The script reads from stdin (pipe JSON) or uses a cached `_raw_YYYY-MM-DD.json` file.

### Step 5 — Write the Markdown Report

Use `Write` tool to create `<output_dir>/YYYY-MM-DD-每日资讯.md` using the template in
`references/report_template.md`.

**Important: the live format has drifted from the older template — follow the most
recent report in `<output_dir>` as the source of truth.** Current established format:

- Title: `# 产品经理日报 · YYYY-MM-DD`
- Blockquote line: item count + category breakdown + 25+ 来源 + the day's 关键词 list
- `## 今日精选 Top 5` numbered `### 1. 标题` entries, placed at the top and NOT
  duplicated in the categories below
- Category headings, in this order:
  `## 产品思维` / `## 行业动态（国内）` / `## 行业动态（国际）` /
  `## AI 技术趋势` / `## UX 设计` / `## 增长策略` / `## 工具推荐`（表格）/ `## 延伸阅读`
- Each item is plain `### 标题` followed by bullet lines, in this exact shape:

```markdown
### 标题
- **来源：** 来源名（可多个，用 / 分隔）
- **链接：** https://...
- **摘要：** 中文摘要，2–5 句；关键判断用 **粗体** 标出「对产品经理意味着什么」
- **关键日期：** YYYY-MM-DD
```

- 工具推荐 is a Markdown table: `| 工具 | 简介 | 链接 |`
- Footer: `*报告由 WorkBuddy pm-daily-news skill 自动生成 · 部分内容基于搜索快照聚合，请以原文链接为准*`

**Style rules (user preference — do not deviate):**
- **No emoji anywhere, especially not in headings.** Headings are plain text.
- Use full-width Chinese punctuation (`：` `（）` `——` `「」`), not half-width, in
  the `**来源：**` / `**链接：**` / `**摘要：**` / `**关键日期：**` labels.
- Aim for 38–48 items per day.
- Keep every item's 摘要 focused on "so what" — what it means for a PM, not just what
  happened. Causal/interpretive framing is preferred over data listing.

### Step 6 — Update Index

**Insert** (do not append) one line at the **top** of the list in
`<output_dir>/index.md` — newest entry first:

```markdown
- [YYYY-MM-DD 产品资讯日报](./YYYY-MM-DD-每日资讯.md) — {item_count} 条资讯
```

If `index.md` does not exist, create it with a header first:

```markdown
# 产品经理日报索引

> 每日自动汇聚全球产品相关资讯，持续更新。

---
```

### Step 7 — Confirm to User

After writing, report:
- File path created
- Total item count
- Category breakdown
- Brief top-3 highlights inline in chat

### Step 8 — Call `present_files`

This is a scheduled automation by default. The user may be reading the output on a
different client and will **not** receive the file unless you explicitly deliver it.
Pass the newly written `.md` file (and `index.md` if useful) to `present_files`
before ending the turn.

---

## Automation Setup (Scheduled Daily Run)

To schedule this skill to run automatically every day, create an automation:

```
Name: PM Daily News
Schedule: RRULE:FREQ=DAILY;BYHOUR=13;BYMINUTE=15  (runs at 13:15 every day)
Prompt: 帮我收集今天的产品经理相关资讯，生成日报到 ~/Documents/Daily news/ 目录
```

The automation prompt must be self-contained — no follow-up questions.

---

## Source Coverage

Full source list with URLs, language, and update frequency is in `references/sources.md`.

Summary of coverage:
- **国内**: 人人都是产品经理、少数派、36氪、产品壹佰、ToB产品汇、PMCAFF
- **国际**: Product Hunt, Hacker News, Lenny's Newsletter, First Round Review, Mind the Product, UX Collective, Product Coalition (Medium), a16z blog, Y Combinator blog
- **AI/Tech**: The Rundown AI, Ben's Bites, TLDR Tech, MIT Technology Review
- **设计**: Nielsen Norman Group, UX Planet, Smashing Magazine
- **增长/营销**: GrowthHackers, Andrew Chen's blog, Reforge blog

---

## Notes

- If a source is behind a paywall, fetch what is publicly accessible (headline + intro).
- Prefer items published within the last 24–48 hours; label older items with `[本周]`.
- Keep the original title as-is when it is already Chinese; for English titles use
  `原文标题 [中文标题]`.
- Aim for 38–48 items per day (recent runs: 38–47).
- **Always check the automation memory file before starting** (path pattern:
  `.workbuddy/memory/automations/automation-*/memory.md`) — it records the last run
  date and the previous run's 关键词, which tells you the gap to fill and prevents
  repeating yesterday's stories.
- **After finishing, append a brief summary to that same memory file** (run date,
  file path, item count, and 4–8 关键词). Do NOT paste the full report into memory.
- **Also append a short entry to the workspace daily log**
  `.workbuddy/memory/YYYY-MM-DD.md` (create it if missing; logs are append-only).
