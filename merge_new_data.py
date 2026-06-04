#!/usr/bin/env python3
"""
Smart parser: section-based year detection.
Each section in source files has a title like "2026年5月（巳月）" or "2026年丑月".
The 干支月 (stem-branch month) doesn't align with Gregorian year boundaries.
- 丑月 = 12th lunar month = Jan of next Gregorian year
- We map based on the section title's 干支月 + Gregorian year context.
"""

import re
import json
from pathlib import Path
from collections import defaultdict

WORKSPACE = "/home/node/.openclaw/workspace"
JSON_FILE = f"{WORKSPACE}/bazi_fortune_data.json"
GROK_FILE = "/home/node/.openclaw/media/inbound/grok_分析---b834df51-f3b5-4553-9ab0-83a3b8498e45.txt"
DEEPSEEK_FILE = "/home/node/.openclaw/media/inbound/deepseek逐日data---faeab2c2-5653-4ee8-bdd2-3ce261c16b81.txt"

# Map 干支月 to Gregorian month (rough: 干支月 starts ~5-7 days into Gregorian month)
# 寅月 (Feb) = Feb 4 - Mar 5
# 卯月 (Mar) = Mar 6 - Apr 4
# ...
# 丑月 (Jan) = Jan 5 - Feb 3
STEM_BRANCH_MONTHS = {
    '寅': (2, 4),   # Feb
    '卯': (3, 6),   # Mar
    '辰': (4, 5),   # Apr
    '巳': (5, 6),   # May
    '午': (6, 6),   # Jun
    '未': (7, 7),   # Jul
    '申': (8, 7),   # Aug
    '酉': (9, 8),   # Sep
    '戌': (10, 8),  # Oct
    '亥': (11, 7),  # Nov
    '子': (12, 7),  # Dec
    '丑': (1, 5),   # Jan (next year)
}

# Load JSON
with open(JSON_FILE) as f:
    data = json.load(f)

# Remove any 2028/2029 entries (those were from bad year detection)
for bad_year in list(data.keys()):
    if int(bad_year) > 2027:
        del data[bad_year]

# ---------- Section-based parser ----------
def parse_file_sections(path, daily_pattern):
    """
    Parse a file by sections. Each section has a title like "2026年5月（巳月）" 
    that tells us the (gregorian_year, gregorian_month) context.
    """
    with open(path) as f:
        content = f.read()

    # Find all section titles - they look like "2026年5月（巳月）..." or "2026年丑月..."
    # Pattern: "YYYY年N月（STEM月）" or "YYYY年STEM月"
    section_pattern = re.compile(
        r'^(202[67])年\s*'
        r'(?:(\d+)月|([丑寅卯辰巳午未申酉戌亥])月)',
        re.MULTILINE
    )

    sections = []
    for m in section_pattern.finditer(content):
        greg_year = int(m.group(1))
        if m.group(2):  # "5月" form
            greg_month = int(m.group(2))
        else:  # "丑月" form
            stem = m.group(3)
            greg_month, _ = STEM_BRANCH_MONTHS[stem]
            # 丑月 falls in next Gregorian year
            if stem == '丑':
                greg_year += 1
        sections.append((m.start(), greg_year, greg_month))

    # Find all daily entries
    daily_entries = []
    for m in daily_pattern.finditer(content):
        month = int(m.group(1))
        day = int(m.group(2))
        pos = m.start()
        daily_entries.append((pos, month, day, m.group(3), m.group(4), m.group(5), m.group(6)))

    # For each daily entry, find the most recent section header
    # If a section says "2026年5月" and entry is "5月5日", it's 2026/5/5
    # If a section says "2026年12月" with range "12月7日 → 1月5日", 
    # entries from 12月X日 are 2026, entries from 1月Y日 are 2027
    entries_with_year = []
    section_idx = 0
    current_section = None  # (greg_year, greg_month, end_month)
    sorted_sections = sorted(sections)
    sorted_daily = sorted(daily_entries)

    for pos, month, day, stema, career, fortune, judgment in sorted_daily:
        # Find the most recent section
        while section_idx < len(sorted_sections) and sorted_sections[section_idx][0] <= pos:
            current_section = sorted_sections[section_idx]
            section_idx += 1

        if current_section is None:
            continue

        sec_year, sec_month = current_section[1], current_section[2]

        # Determine year for this entry
        if month >= sec_month:
            year = sec_year
        else:
            year = sec_year + 1

        if year > 2027:
            continue

        entries_with_year.append((year, month, day, stema, career, fortune, judgment))

    return entries_with_year

# ---------- Grok pattern ----------
grok_pattern = re.compile(
    r'^(\d+)月(\d+)日\s+'
    r'([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])(?:\s+[\u4e00-\u9fff]+)?\s*\n'
    r'事業：([^\n]+)\n'
    r'財運：([^\n]+)\n'
    r'盲派斷：([^\n]+)',
    re.MULTILINE
)

grok_raw = parse_file_sections(GROK_FILE, grok_pattern)

grok_by_date = defaultdict(list)
# grok_raw entries: (year, month, day, stema, career, fortune, judgment)
for year, month, day, stema, career, fortune, judgment in grok_raw:
    total_len = len(career) + len(fortune) + len(judgment)
    grok_by_date[(year, month, day)].append((total_len, stema, career, fortune, judgment))

grok_entries = []
for (year, month, day), occurrences in grok_by_date.items():
    occurrences.sort()
    _, stema, career, fortune, judgment = occurrences[0]
    grok_entries.append((year, month, day, stema, career, fortune, judgment))

# ---------- DeepSeek pattern ----------
ds_pattern = re.compile(
    r'^(\d+)/(\d+)\s*\(([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])\)\s*'
    r'([^\t\n]+?)(?:\n|\t)\s*'
    r'([^\t\n]+?)(?:\n|\t)\s*'
    r'([^\t\n]+)',
    re.MULTILINE
)

ds_raw = parse_file_sections(DEEPSEEK_FILE, ds_pattern)
ds_raw = [e for e in ds_raw if len(e[4]) < 200 and len(e[5]) < 200 and len(e[6]) < 200]  # year, month, day, stema, career, fortune, judgment

ds_by_date = defaultdict(list)
# ds_raw entries: (year, month, day, stema, career, fortune, judgment)
for year, month, day, stema, career, fortune, judgment in ds_raw:
    total_len = len(career) + len(fortune) + len(judgment)
    ds_by_date[(year, month, day)].append((total_len, stema, career, fortune, judgment))

ds_entries = []
for (year, month, day), occurrences in ds_by_date.items():
    occurrences.sort()
    _, stema, career, fortune, judgment = occurrences[0]
    ds_entries.append((year, month, day, stema, career, fortune, judgment))

from collections import Counter
print("=== Grok by year ===")
print(Counter(y for y, m, d, s, c, f, j in grok_entries))
print("=== DeepSeek by year ===")
print(Counter(y for y, m, d, s, c, f, j in ds_entries))

# Build combined text
def combine(career, fortune, judgment):
    return f"事業：{career}\n財運：{fortune}\n盲派斷：{judgment}"

# Merge Grok
updates_grok = 0
new_grok = 0
for year, month, day, stema, career, fortune, judgment in grok_entries:
    year_str = str(year)
    month_str = f"{month:02d}"
    day_str = f"{day:02d}"
    if year_str not in data:
        data[year_str] = {}
    if month_str not in data[year_str]:
        data[year_str][month_str] = {}
    entry_text = combine(career, fortune, judgment)
    old = data[year_str][month_str].get(day_str, {})
    if old.get('grok') != entry_text:
        data[year_str][month_str][day_str] = {
            'grok': entry_text,
            'deepseek': old.get('deepseek', '')
        }
        if old.get('grok'):
            updates_grok += 1
        else:
            new_grok += 1

# Merge DeepSeek
updates_ds = 0
new_ds = 0
for year, month, day, stema, career, fortune, judgment in ds_entries:
    year_str = str(year)
    month_str = f"{month:02d}"
    day_str = f"{day:02d}"
    if year_str not in data:
        data[year_str] = {}
    if month_str not in data[year_str]:
        data[year_str][month_str] = {}
    entry_text = combine(career, fortune, judgment)
    if day_str in data[year_str][month_str]:
        old_ds = data[year_str][month_str][day_str].get('deepseek', '')
        if old_ds != entry_text:
            data[year_str][month_str][day_str]['deepseek'] = entry_text
            if old_ds:
                updates_ds += 1
            else:
                new_ds += 1
    else:
        data[year_str][month_str][day_str] = {
            'grok': '',
            'deepseek': entry_text
        }
        new_ds += 1

# Save
with open(JSON_FILE, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n=== Grok: {len(grok_entries)} unique dates, updated {updates_grok}, new {new_grok} ===")
print(f"=== DeepSeek: {len(ds_entries)} unique dates, updated {updates_ds}, new {new_ds} ===")
print(f"2026 total days: {sum(len(data.get('2026', {}).get(f'{m:02d}', {})) for m in range(1, 13))}")
print(f"2027 total days: {sum(len(data.get('2027', {}).get(f'{m:02d}', {})) for m in range(1, 13))}")
