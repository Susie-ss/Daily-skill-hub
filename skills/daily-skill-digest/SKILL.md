---
name: daily-skill-digest
description: 每日收集全网最热门的 AI Agent Skills（skills.sh 排行榜、GitHub Trending、社区推荐等），生成标题为「热门 AI Agent Skills + 日期」的 Markdown 日报并更新索引，每天收录 8-15 个。当用户要求生成热门 Skill 日报、AI Agent 技能收集、Skill 排行榜汇总，或引用「热门Skill日报」「热门 skill」时使用。
version: 1.0.0
agent_created: true
---

# Daily Skill Digest（热门 Skill 日报）

## Overview

每天收集全网最热门、使用频率高的 AI Agent Skills，整合成一份结构化 Markdown 日报。每个 Skill 都要讲清「是什么 / 怎么用 / 为什么值得装」。

## 输出文件

- 保存路径：`~/Documents/Daily news/热门Skill日报/热门 skillYYYY-MM-DD.md`
- 文件名：`热门 skill` + 当天日期（如 `热门 skill2026-09-17.md`）
- 索引文件：`~/Documents/Daily news/热门Skill日报/index.md`
- 保存目录不存在时先创建（`mkdir -p`）

## 执行流程

### Step 1: 确认日期

用 `date +%Y-%m-%d` 获取当天日期，不要自己推算。

### Step 2: 搜索素材

用 WebSearch 搜索以下关键词（或类似变体），并用 WebFetch 对重要信息取详情：

- `hot AI agent skills today` / `trending agent skills`
- `skills.sh popular skills` / `skills.sh leaderboard`
- `最热门 AI Agent Skill` / `AI技能 排行榜`
- `best agent skills to install` / `top agent skills 2026`
- `new AI agent skills this week`

可交叉验证的来源：skills.sh 排行榜、GitHub Trending、掘金、知乎、Reddit r/AI_Agents。

### Step 3: 整合生成报告

**文件顶部**：

```markdown
# 🔥 热门 AI Agent Skills · {YYYY-MM-DD}

> 每日自动汇聚全网最热门的 AI Agent Skills | 生成时间: {当前时间}
> 共收录 **{N}** 个热门 Skills
```

**每个 Skill 输出四个板块**：

```markdown
## {Skill 名称}

### 1. 基本信息
- **名称**: （中英文名称）
- **开发者**: （作者/组织）
- **安装量/热度**: （如有排行榜数据）
- **GitHub**: （链接）
- **安装命令**: `npx skills add ...`

### 2. 📖 介绍
用 2-3 段话介绍这个 Skill 是什么、解决了什么问题、核心功能特点。
语言通俗易懂，让不熟悉该领域的读者也能理解。

### 3. 🎯 场景
- 场景一：具体场景 + 用户痛点 + Skill 如何解决
- 场景二：...
- 场景三：...

### 4. 💡 价值
用 2-3 句话总结核心价值：为什么受欢迎、带来什么实际收益、相比同类有什么独特优势。
```

**文章底部**：

```markdown
---
> 📌 数据来源：skills.sh / GitHub / 社区推荐 | 自动生成，仅供参考
```

**质量要求**：

| 项 | 要求 |
|----|------|
| 数量 | 每天 **8-15 个**，保证质量 |
| 信息 | 优先用 skills.sh 官方排行榜数据，多来源交叉验证 |
| 内容 | 介绍必须有实质内容，不能泛泛而谈 |
| 分类 | 可按类别分组（浏览器自动化、开发工具、内容创作、金融投资等） |
| 时效 | 优先收录近期发布或近期热度攀升的 Skills |
| 语言 | 中文撰写，专业但不晦涩，标题可适度用 emoji |

### Step 4: 更新索引

`index.md` 不存在时先创建：

```markdown
# 热门 AI Agent Skills 日报索引

> 每日自动汇聚全网最热门的 AI Agent Skills，持续更新。

---
```

追加一行：

```markdown
- [{YYYY-MM-DD} 热门Skill日报](./热门%20skill{YYYY-MM-DD}.md) — {N} 个 Skills
```

### Step 5: 保存并展示

写入文件后，向用户简要汇报今日收录数量与 3 个最值得装的 Skill。

## 注意事项

- **只用真实搜索结果，禁止编造 Skill 名称、安装量、GitHub 链接或安装命令**
- 安装命令必须来自官方说明，不要自己拼
- 同一 Skill 在多个榜单出现时合并为一条，标注多来源热度
- 报告全文使用简体中文
- 不收录违规、低俗内容
