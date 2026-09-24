#!/usr/bin/env python3
"""
pm-daily-news · collect_news.py
--------------------------------
Post-processing helper for the PM Daily News skill.

Usage:
    python3 collect_news.py --date 2026-06-30 --output ~/Documents/pm-daily-news/

What it does:
1. Reads raw news items from a JSON file (_raw_YYYY-MM-DD.json) or stdin.
2. Deduplicates by URL and title similarity.
3. Sorts by category and relevance score.
4. Writes a clean JSON file (_clean_YYYY-MM-DD.json) for the report step.
5. Optionally prints a summary table to stdout.

JSON input format (array of objects):
    [
        {
            "title": "Article Title",
            "url": "https://...",
            "source": "Source Name",
            "category": "产品思维",   // see CATEGORIES below
            "language": "zh" | "en",
            "date": "2026-06-30",
            "summary_zh": "中文摘要",
            "relevance": 0.85        // 0.0 – 1.0, optional
        },
        ...
    ]
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

# ─── Constants ────────────────────────────────────────────────────────────────

CATEGORIES = [
    "🔥 今日精选",
    "🧠 产品思维 & 方法论",
    "🚀 行业动态（国内）",
    "🌏 行业动态（国际）",
    "🤖 AI 产品 & 技术趋势",
    "🎨 用户体验 & 设计",
    "📈 增长 & 商业策略",
    "🏢 B端 & 企服产品",
    "🛠️ 工具 & 资源",
]

CATEGORY_KEYWORDS = {
    "🧠 产品思维 & 方法论": ["方法论", "framework", "roadmap", "strategy", "思维", "process", "pm"],
    "🤖 AI 产品 & 技术趋势": ["ai", "gpt", "llm", "人工智能", "大模型", "machine learning", "automation"],
    "🎨 用户体验 & 设计": ["ux", "ui", "design", "设计", "用户体验", "用户研究", "交互"],
    "📈 增长 & 商业策略": ["growth", "增长", "revenue", "monetize", "营销", "marketing", "saas metrics"],
    "🏢 B端 & 企服产品": ["b2b", "enterprise", "saas", "b端", "企服", "tob", "crm", "erp"],
    "🚀 行业动态（国内）": [],   # fallback for zh items without other matches
    "🌏 行业动态（国际）": [],   # fallback for en items without other matches
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lower-case and strip punctuation for comparison."""
    return re.sub(r"[^\w\s]", "", text.lower())


def is_duplicate(item: dict, seen: list[dict], threshold: float = 0.7) -> bool:
    """Check if item is a duplicate by URL or title similarity."""
    for seen_item in seen:
        if item["url"] == seen_item["url"]:
            return True
        title_a = normalize(item.get("title", ""))
        title_b = normalize(seen_item.get("title", ""))
        if title_a and title_b:
            # Jaccard similarity on word sets
            a_words = set(title_a.split())
            b_words = set(title_b.split())
            if len(a_words | b_words) == 0:
                continue
            sim = len(a_words & b_words) / len(a_words | b_words)
            if sim >= threshold:
                return True
    return False


def infer_category(item: dict) -> str:
    """Infer category from title + summary keywords if not already set."""
    existing = item.get("category", "")
    if existing and existing in CATEGORIES:
        return existing

    text = (item.get("title", "") + " " + item.get("summary_zh", "")).lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return cat

    # Language-based fallback
    if item.get("language", "en") == "zh":
        return "🚀 行业动态（国内）"
    return "🌏 行业动态（国际）"


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="PM Daily News — news post-processor")
    parser.add_argument("--date", default=date.today().isoformat(), help="Date (YYYY-MM-DD)")
    parser.add_argument("--output", default=os.path.expanduser("~/Documents/pm-daily-news/"),
                        help="Output directory")
    parser.add_argument("--max-per-category", type=int, default=8,
                        help="Max items per category (default: 8)")
    parser.add_argument("--top-n", type=int, default=5,
                        help="Number of top picks (default: 5)")
    args = parser.parse_args()

    output_dir = Path(os.path.expanduser(args.output))
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_path = output_dir / f"_raw_{args.date}.json"

    # ── Load raw data ──────────────────────────────────────────────────────────
    if not sys.stdin.isatty():
        print("[collect_news] Reading from stdin ...", file=sys.stderr)
        try:
            raw_items = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"[collect_news] ERROR: Invalid JSON from stdin: {e}", file=sys.stderr)
            sys.exit(1)
    elif raw_path.exists():
        print(f"[collect_news] Reading {raw_path} ...", file=sys.stderr)
        raw_items = json.loads(raw_path.read_text(encoding="utf-8"))
    else:
        print(f"[collect_news] No input found (stdin or {raw_path}). Exiting.", file=sys.stderr)
        sys.exit(1)

    print(f"[collect_news] Loaded {len(raw_items)} raw items.", file=sys.stderr)

    # ── Deduplicate ────────────────────────────────────────────────────────────
    deduped: list[dict] = []
    for item in raw_items:
        if not is_duplicate(item, deduped):
            deduped.append(item)

    print(f"[collect_news] After dedup: {len(deduped)} items.", file=sys.stderr)

    # ── Infer categories & sort ────────────────────────────────────────────────
    for item in deduped:
        item["category"] = infer_category(item)
        if "relevance" not in item:
            item["relevance"] = 0.5  # neutral default

    deduped.sort(key=lambda x: x.get("relevance", 0.5), reverse=True)

    # ── Group by category, cap per category ───────────────────────────────────
    grouped: dict[str, list] = {cat: [] for cat in CATEGORIES}
    for item in deduped:
        cat = item["category"]
        if cat in grouped and len(grouped[cat]) < args.max_per_category:
            grouped[cat].append(item)
        elif cat not in grouped:
            # Put uncategorized into most-fitting fallback
            fallback = "🌏 行业动态（国际）" if item.get("language") == "en" else "🚀 行业动态（国内）"
            if len(grouped[fallback]) < args.max_per_category:
                grouped[fallback].append(item)

    # ── Build top picks ────────────────────────────────────────────────────────
    all_sorted = sorted(deduped, key=lambda x: x.get("relevance", 0.5), reverse=True)
    top_picks = all_sorted[: args.top_n]
    grouped["🔥 今日精选"] = top_picks

    # ── Write clean JSON ───────────────────────────────────────────────────────
    clean_path = output_dir / f"_clean_{args.date}.json"
    output_data = {
        "date": args.date,
        "generated_at": datetime.now().isoformat(),
        "total": len(deduped),
        "grouped": {cat: items for cat, items in grouped.items() if items},
    }
    clean_path.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[collect_news] Clean data written to {clean_path}", file=sys.stderr)

    # ── Print summary to stdout ────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  PM Daily News · {args.date}")
    print(f"  Total: {len(deduped)} items (from {len(raw_items)} raw)")
    print(f"{'='*60}")
    for cat, items in grouped.items():
        if items:
            print(f"  {cat}: {len(items)} items")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
