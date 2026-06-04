#!/usr/bin/env python3
"""
Parse the new Grok + DeepSeek source files and merge into bazi_fortune_data.json.
Format: "N月D日 STEM-BRANCH" followed by 3 lines 事業/財運/盲派斷
"""

import re
import json
from pathlib import Path

WORKSPACE = "/home/node/.openclaw/workspace"
JSON_FILE = f"{WORKSPACE}/bazi_fortune_data.json"
GROK_FILE = "/home/node/.openclaw/media/inbound/grok_分析---b834df51-f3b5-4553-9ab0-83a3b8498e45.txt"
DEEPSEEK_FILE = "/home/node/.openclaw/media/inbound/deepseek逐日data---faeab2c2-5653-4ee8-bdd2-3ce261c16b81.txt"

# Load JSON
with open(JSON_FILE) as f:
    data = json.load(f)

# ---------- Parser for Grok file (N月D日 STEM-BRANCH) ----------
def parse_grok_file(path):
    """Parse Grok source: 'N月D日 STEM-BRANCH' + 3 lines."""
    with open(path) as f:
        content = f.read()

    # Pattern: "5月5日 己卯" (N月D日 STEM-BRANCH, optional time component)
    # May also see "5月20日 庚辰\n" with extra stuff between
    pattern = re.compile(
        r'(\d+)月(\d+)日\s+'
        r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])(?:\s+[\u4e00-\u9fff]+)?\s*\n'
        r'事業：([^\n]+)\n'
        r'財運：([^\n]+)\n'
        r'盲派斷：([^\n]+)',
        re.MULTILINE
    )

    results = []
    for m in pattern.finditer(content):
        month = int(m.group(1))
        day = int(m.group(2))
        stema = m.group(3)
        career = m.group(4).strip()
        fortune = m.group(5).strip()
        judgment = m.group(6).strip()
        # Filter: only 2026 and 2027
        results.append((month, day, stema, career, fortune, judgment))

    return results

# ---------- Parser for DeepSeek file ----------
# DeepSeek has TWO formats:
# 1) "5/5 (己卯)" in table
# 2) Markdown table with date (5月5日) and content
# 3) "流日實戰手冊" table with "5/5 (己卯)" and tab-separated 3 columns

def parse_deepseek_file(path):
    """Parse DeepSeek source. Multiple formats possible."""
    with open(path) as f:
        content = f.read()

    results = []

    # Format A: "5/5 (己卯)" with tab-separated 3 columns
    # e.g., "5/5 (己卯)  月頭...    屌，呢兩日唔好同人講錢...    卯酉沖..."
    pattern_a = re.compile(
        r'(\d+)/(\d+)\s*\(([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])\)\s*'
        r'([^\t\n]+?)(?:\n|\t)\s*'
        r'([^\t\n]+?)(?:\n|\t)\s*'
        r'([^\t\n]+)',
        re.MULTILINE
    )

    for m in pattern_a.finditer(content):
        month = int(m.group(1))
        day = int(m.group(2))
        stema = m.group(3)
        career = m.group(4).strip()
        fortune = m.group(5).strip()
        judgment = m.group(6).strip()
        # Skip if too long (means we matched a paragraph, not a daily entry)
        if len(career) < 200 and len(fortune) < 200 and len(judgment) < 200:
            results.append((month, day, stema, career, fortune, judgment))

    return results

# Parse both files
grok_entries = parse_grok_file(GROK_FILE)
deepseek_entries = parse_deepseek_file(DEEPSEEK_FILE)

print(f"Parsed {len(grok_entries)} Grok entries")
print(f"Parsed {len(deepseek_entries)} DeepSeek entries")

# Show some samples
print("\n=== Grok samples (first 3) ===")
for m, d, s, c, f, j in grok_entries[:3]:
    print(f"  {m}/{d} ({s}):")
    print(f"    事業: {c[:50]}")
    print(f"    財運: {f[:50]}")
    print(f"    盲派: {j[:50]}")

print("\n=== DeepSeek samples (first 3) ===")
for m, d, s, c, f, j in deepseek_entries[:3]:
    print(f"  {m}/{d} ({s}):")
    print(f"    事業: {c[:50]}")
    print(f"    財運: {f[:50]}")
    print(f"    盲派: {j[:50]}")
