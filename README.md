# Daily Skill Hub

一套「日报类」AI Agent Skills 合集 —— 每个技能负责一个领域，每天自动收集全球最新资讯，产出结构化 Markdown 日报。

**每个技能一个独立目录**，互不依赖、可单独安装使用。

---

## 技能清单

| 技能目录 | 领域 | 每日产出文件 | 输出目录 |
|---------|------|-------------|---------|
| [`skills/ai-daily-news`](./skills/ai-daily-news) | AI 与科技行业资讯 | `全网资讯-YYYY-MM-DD.md` | `~/Documents/Daily news/AI资讯日报/` |
| [`skills/pm-daily-news`](./skills/pm-daily-news) | 产品经理资讯 | `YYYY-MM-DD-每日资讯.md` | `~/Documents/Daily news/产品经理日报/` |
| [`skills/daily-hot-topics`](./skills/daily-hot-topics) | 泛娱乐热点与平台热榜 | `每日热门_YYYY-MM-DD.md` | `~/Documents/Daily news/每日热门/` |
| [`skills/daily-story`](./skills/daily-story) | 全领域知识（文史地理典故） | `每日story_YYYY-MM-DD.md` | `~/Documents/Daily news/story/` |
| [`skills/daily-vocab-collect`](./skills/daily-vocab-collect) | 知识收纳（热词/金句/行业名词） | `多看YYYY-MM-DD.md` | `~/Documents/Daily news/知识收纳/` |
| [`skills/daily-tools-digest`](./skills/daily-tools-digest) | 全球热门工具（数字 + 实体） | `热门工具YYYY-MM-DD.md` | `~/Documents/Daily news/全网全球工具日报/` |
| [`skills/daily-creative-digest`](./skills/daily-creative-digest) | 全领域创意灵感与赚钱思路 | `每日创意_YYYY-MM-DD.md` | `~/Documents/Daily news/每日创意/` |
| [`skills/daily-skill-digest`](./skills/daily-skill-digest) | 热门 AI Agent Skills | `热门 skillYYYY-MM-DD.md` | `~/Documents/Daily news/热门Skill日报/` |

---

## 目录结构

```
Daily-skill-hub/
├── README.md
└── skills/
    ├── ai-daily-news/
    │   ├── SKILL.md
    │   └── references/
    │       ├── sources.md          # 信息来源清单
    │       └── report_template.md  # 报告模板
    ├── pm-daily-news/
    │   ├── SKILL.md
    │   ├── references/…            # 来源清单 + 报告模板
    │   └── scripts/
    │       └── collect_news.py     # 抓取脚本
    ├── daily-hot-topics/
    │   ├── SKILL.md
    │   ├── manifest.yaml           # 技能元数据
    │   ├── assets/report_template.md
    │   └── references/search_guide.md
    ├── daily-story/
    ├── daily-vocab-collect/
    ├── daily-tools-digest/
    ├── daily-creative-digest/
    └── daily-skill-digest/
```

每个技能内部结构：

- **`SKILL.md`** — 技能主体，含 frontmatter（`name` / `description` / `version` / 触发词）与执行流程
- **`references/`** — 信息来源清单、搜索维度、报告模板
- **`scripts/`** — 可选，辅助脚本
- **`assets/`** — 可选，报告模板等静态资源
- **`manifest.yaml`** — 可选，市场发布用的元数据

---

## 安装

把需要的技能目录整个复制到你的 Agent 技能目录即可，例如 WorkBuddy / Claude Code：

```bash
# 单个技能
cp -r skills/ai-daily-news ~/.workbuddy/skills/

# 全部
cp -r skills/* ~/.workbuddy/skills/
```

安装后在对话里说出该技能的触发词（写在各技能 `SKILL.md` 的 `description` 里）即可调用，例如「每日热门」「知识收纳」「今日 AI 资讯」。

需要定时运行时，新建一个每日自动化任务，在 prompt 开头写上：

```
加载并严格遵循技能 `<技能名>`，按该技能定义执行。
```

---

## 通用设计约定

- **语言**：报告统一使用简体中文
- **时效性**：搜索词必须带具体日期；优先收录 24–48 小时内的内容
- **来源可溯**：每条资讯包含标题、来源、链接、中文摘要
- **索引维护**：多数技能会同时更新所在输出目录的 `index.md`
- **输出路径**：所有报告写入 `~/Documents/Daily news/<主题>/`，不写进技能目录
- **配色（仅行情类）**：遵循中国股市习惯，涨 🔴 / 跌 🟢

---

## 许可

MIT
