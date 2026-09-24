---
name: ai-daily-news
description: Collect and aggregate daily AI news and industry news from global sources, covering large language models, AI products, industry trends, policy regulation, and research breakthroughs. Outputs a structured Markdown digest to a dated file and updates a daily index. Triggers include AI资讯日报, 每日AI资讯, 人工智能动态, AI行业日报, daily AI news, AI industry digest, 全网AI资讯, 科技资讯.
agent_created: true
version: 1.0.0
---

# AI Daily News Skill

Collect and aggregate daily AI news and industry news from global sources every day
and write a structured Markdown digest to a dated file.

---

## Overview

This skill:
1. Searches a curated list of sources (see `references/sources.md`) for today's AI news.
2. Deduplicates results and groups them by category.
3. Translates key English snippets into Chinese summaries when needed.
4. Writes the full digest to `<output_dir>/YYYY-MM-DD.md`.
5. Appends a one-line entry to `<output_dir>/index.md` for navigation.

---

## Trigger Detection

Activate this skill when the user mentions:
- AI资讯 / AI日报 / 人工智能动态 / AI行业日报
- 每日AI资讯 / 全网AI资讯 / 科技资讯
- daily AI news / AI industry digest / AI newsletter
- 大模型新闻 / 大模型资讯 / AI产品资讯
- 定时收集AI资讯 / 自动生成AI日报

---

## Execution Workflow

### Step 1 — Resolve Output Path

**Default output directory: `~/Documents/Daily news/AI资讯日报/`**

If the user specifies a different directory, use that instead.
Create the directory if it does not exist:

```bash
mkdir -p "<output_dir>"
```

### Step 2 — Determine Today's Date

```bash
date +%Y-%m-%d          # macOS / Linux
```

Use this value as the filename: `<output_dir>/全网资讯-YYYY-MM-DD.md`
(the file must be named `全网资讯-<date>.md`, not just `<date>.md`)

### Step 3 — Collect News

Use `WebSearch` and `WebFetch` to pull the latest content from the source list in
`references/sources.md`. For each source category, run targeted searches.

**Recommended WebSearch query patterns:**

| Category              | Query examples                                                   |
|-----------------------|------------------------------------------------------------------|
| 大模型&新发布         | `大模型 发布 {date}` / `LLM release {date}` / `GPT Claude Gemini 最新 {date}` |
| AI产品&应用           | `AI product launch {date}` / `AI应用 新产品 {date}` / `AI tools {date}` |
| 行业动态(国内)        | `AI 行业新闻 {date}` / `人工智能 产业 {date}` / `36氪 AI {date}` |
| 行业动态(国际)        | `AI industry news {date}` / `latest AI news {date}` |
| 政策&监管             | `AI regulation policy {date}` / `AI 监管 政策 {date}` / `人工智能 立法 {date}` |
| 研究突破              | `AI research breakthrough {date}` / `machine learning paper arxiv {date}` |
| 投资&融资             | `AI funding round {date}` / `AI startup investment {date}` / `AI 融资 {date}` |
| 芯片&算力             | `AI chip GPU {date}` / `算力 芯片 {date}` / `NVIDIA AMD 最新 {date}` |
| Newsletter精选        | `The Rundown AI {date}` / `TLDR AI {date}` / `Ben's Bites {date}` |

For **each category**, gather 3–8 items. Each item must include:
- Title (原文标题)
- Source name
- URL
- 1–2 sentence Chinese summary

### Step 3.5 — Deduplicate Against Yesterday's Report (mandatory)

Before writing, **always** diff today's findings against the most recent existing
report in `<output_dir>` (usually yesterday's). Skipping this produces a report
that repeats items the user already read.

Fast two-pass procedure:

```bash
# Pass 1 — blind keyword sweep: which candidate topics are already in yesterday's file?
cd "<output_dir>" && for k in "关键词1" "关键词2" ... ; do
  printf "%-16s " "$k"; grep -c "$k" "全网资讯-<yesterday>.md"
done

# Pass 2 — list yesterday's headlines for the ambiguous ones, then compare by hand
grep -n "^### \[" "全网资讯-<yesterday>.md" | grep -E "关键词A|关键词B"
```

Rules:
- Any item whose keyword hits yesterday's report → **skip it**, unless today brings a
  genuinely new development (then re-frame the summary around today's delta and add
  a `[延续报道]` tag).
- Items from a date earlier than yesterday → label `[本周]`.
- This is cheap: one `grep` sweep over 80+ keywords takes seconds and reliably catches
  repeats that eyeballing misses.

### Step 4 — Write the Markdown Report

Use `Write` tool to create `<output_dir>/全网资讯-YYYY-MM-DD.md` using the template in
`references/report_template.md`.

Key rules:
- Always include the date header and generation timestamp, plus the coverage window
  (e.g. `覆盖窗口: 9/17 – 9/18`).
- Group items under the category headings defined in the template.
- Each item: `### [Title](url)` → `> **Source:** xxx` → summary paragraph.
- Add a `## 🔥 今日精选` section at the top with the 3–5 most insightful/important items
  (5 is the norm), each with a substantive 2–4 sentence summary — not a one-liner.
- Use emoji section headers as defined in the template.
- End with a `## 📌 延伸阅读` section linking to evergreen resources.

### Step 5 — Update Index

Append one line to `<output_dir>/index.md` (matching the existing file's format exactly):

```markdown
- [全网资讯-YYYY-MM-DD](./全网资讯-YYYY-MM-DD.md) — {item_count} 条资讯
```

If the day had a mid-day follow-up pass, annotate it in the same line, e.g.
`— 170 条资讯（含晨间增量 16 条）`.

If `index.md` does not exist, create it with a header first:

```markdown
# 🤖 AI 全网资讯日报索引

> 🧠 每日自动汇聚全球AI与科技行业资讯，持续更新。

---
```

### Step 6 — Confirm to User

After writing, report:
- File path created
- Total item count
- Category breakdown
- Brief top-3 highlights inline in chat

---

## Automation Setup (Scheduled Daily Run)

This skill is driven by a daily automation scheduled at **14:45**. The schedule must stay
inside the 09:20–17:00 window (the user's machine is off in the evening, and may not be on
before 09:20).

```
Name: AI全网资讯日报
Schedule: RRULE:FREQ=DAILY;BYHOUR=14;BYMINUTE=45  (runs at 14:45 every day)
Prompt: 帮我收集今天的全网AI资讯和行业资讯，生成日报到 ~/Documents/Daily news/AI资讯日报/ 目录
```

The automation prompt must be self-contained — no follow-up questions. For an unattended
run, state assumptions inline rather than asking; never block on user input.

If the automation fires a **second time on the same day** (mid-day follow-up), do not
regenerate the whole report: read the existing file, collect only the new time window,
dedupe by keyword, and insert an increment block labelled
`## 🌅 晨间增量更新（HH:MM–HH:MM 补采）` before the 延伸阅读 section. Then update the
index line's item count.

---

## Source Coverage

Full source list with URLs, language, and update frequency is in `references/sources.md`.

Summary of coverage:
- **大模型厂商**: OpenAI, Google DeepMind, Anthropic, Meta AI, xAI, Microsoft, 百度, 阿里巴巴, 字节跳动, 智谱AI, 月之暗面, 百川智能, DeepSeek
- **AI新闻媒体(国际)**: The Verge AI, TechCrunch AI, MIT Technology Review AI, ArsTechnica AI, The Rundown AI, TLDR AI, Ben's Bites, AI Breakfast
- **AI新闻媒体(国内)**: 量子位, 机器之心, 36氪 AI, 虎嗅 AI, 雷锋网 AI科技评论, 钛媒体, AI科技评论
- **研究出版**: arXiv (cs.AI, cs.CL, cs.LG), Papers With Code, Hugging Face Daily Papers
- **行业分析**: a16z AI, Sequoia AI, Lightspeed AI, CB Insights AI, 爱分析
- **开发者社区**: Hacker News, GitHub Trending, Reddit r/MachineLearning, 知乎AI话题
- **政策伦理**: 国家网信办, 工信部, 欧洲AI法案, White House AI, Stanford HAI

---

## Notes

- If a source is behind a paywall, fetch what is publicly accessible (headline + intro).
- Prefer items published within the last 24–48 hours; label older items with `[本周]`.
- Translate English titles into Chinese in brackets when the item is English-only;
  when the report is being written in Chinese, just write the Chinese headline directly.
- **Length target: 100–130 items per day.** Counting convention: `item_count` in the index
  line = 精选条目 + 8 大分类条目；工具推荐表的行数**不**计入（在文件头单独标注「工具推荐表 N 项」）。
  Empirically, a **single-day window lands at ~100 items**, while a multi-day catch-up window
  (e.g. Sat+Sun) naturally inflates to 130+. If the count climbs past ~140, compress
  国际行业动态 and 投资&融资 by 3–5 items each. Every item needs a real URL — do not pad
  with linkless entries.
- **Dedup keyword sweep (build the list from today's candidates, not from memory).** After
  collecting, run `grep -c` for every distinct entity/proper noun you plan to write (product
  names, company names, people, benchmark names, policy documents) against the most recent
  report, then `grep "^### \["` on the hits to read the actual yesterday headlines. Blind-sweep
  with a fixed 60–80 keyword list alone is not enough — the list must be regenerated each day
  from that day's candidate items, otherwise new entities slip through.
- The 8 categories are: 大模型&新发布 / AI产品&应用 / 国内行业动态 / 国际行业动态 /
  政策&监管 / 研究突破 / 投资&融资 / 芯片&算力.
- Prioritize items about major model releases, product launches, regulatory changes, and
  high-impact research. For a Chinese reader, lead with 国内 news where possible.
- Note: this skill's automation runs at 14:45 daily; any schedule change must stay inside
  the 09:20–17:00 window (user's machine is off outside it).
