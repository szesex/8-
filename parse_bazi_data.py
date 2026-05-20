#!/usr/bin/env python3
"""Parse Grok + DeepSeek bazi data into bazi_fortune_data.json"""

import json
import re
from pathlib import Path

GROK_FILE = "/home/node/.openclaw/media/inbound/grok_分析---a75c9f62-bc71-4e26-8dcd-3cacee772209.txt"
DEEPSEEK_FILE = "/home/node/.openclaw/media/inbound/deepseek逐日data---f39ae0c6-606b-414b-af73-2fa053881ec6.txt"
OUTPUT_FILE = "/home/node/.openclaw/workspace/bazi_fortune_data.json"

def parse_grok_file(filepath):
    """Parse Grok file into dict: {(year, month, day): grok_text}"""
    data = {}
    current_year = None
    current_month = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: 年 month (月) complete Lihkg仔逐日運程（示範，其餘6-12月一樣已生成好）
    # OR: 年月 完整 Lihkg仔潮文逐日運程（X日YYY → Z日AAA）
    
    # Find year markers: "2026年5月", "2027年2月", etc.
    year_pattern = r'(202[6-9])年(\d+)月'
    # Find date entries: "5月5日 己卯" or "5月6日 丙辰"
    date_pattern = r'(\d+)月(\d+)日\s+([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])\s*\n事業：(.*?)\n財運：(.*?)\n盲派斷：(.*?)(?=\n\d+月\d+日|\n(?:202[6-9]年|$))'
    
    # Split by year sections
    year_sections = re.split(r'(202[6-9]年\d+月)', content)
    
    for i, section in enumerate(year_sections):
        if not section.strip():
            continue
        
        # Check if this is a year header
        year_match = re.match(r'(202[6-9])年(\d+)月', section)
        if year_match:
            current_year = year_match.group(1)
            current_month = year_match.group(2)
            continue
        
        # If we have current year/month, parse dates in this section
        if current_year and current_month:
            # Find all date entries in this section
            matches = re.findall(
                r'(\d+)月(\d+)日\s+([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])\s*\n事業：(.*?)\n財運：(.*?)\n盲派斷：(.*?)(?=\n\d+月\d+日|\Z)',
                section,
                re.DOTALL
            )
            for match in matches:
                month, day, ganzi, career, money, mangpai = match
                key = f"{current_year}-{int(current_month):02d}-{int(month):02d}"
                data[key] = {
                    "grok": f"事業：{career.strip()}\n財運：{money.strip()}\n盲派斷：{mangpai.strip()}"
                }
    
    return data

def parse_deepseek_file(filepath):
    """Parse DeepSeek file - this is narrative format, harder to parse"""
    data = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The DeepSeek content is a large narrative grouped by year/month
    # We need to extract narrative sections for each day
    
    # Pattern to find date ranges like "5月5日 至 5月6日 (己卯、庚辰)"
    # OR single dates like "5月10日 (甲申)"
    
    # Let's find year sections first
    year_matches = list(re.finditer(r'(202[6-9])\s*丙午年', content))
    
    current_pos = 0
    for idx, year_match in enumerate(year_matches):
        year = year_match.group(1)
        year_start = year_match.start()
        
        # Get section until next year or end
        if idx + 1 < len(year_matches):
            year_end = year_matches[idx + 1].start()
        else:
            year_end = len(content)
        
        section = content[year_start:year_end]
        
        # Parse month sections within this year
        month_pattern = r'(\d+)月\s*\(?([^\)]+)\)?.*?(?=\d+月\s*\(|$)'
        month_matches = list(re.finditer(r'(\d+)月\s*\(?([^\)]+)\)?', section))
        
        for midx, month_match in enumerate(month_matches):
            month = month_match.group(1)
            month_start = month_match.start()
            
            # Get section until next month or end
            if midx + 1 < len(month_matches):
                month_end = month_matches[midx + 1].start()
            else:
                month_end = len(section)
            
            month_section = section[month_start:month_end]
            
            # Now find day entries within month section
            # Pattern: "5月5日 至 5月6日 (己卯、庚辰)" or "5月10日 (甲申)"
            day_entries = re.findall(
                r'(\d+)月(\d+)日\s*(?:至\s*\d+月(\d+)日)?\s*(?:\(([^)]+)\))?',
                month_section
            )
            
            for entry in day_entries:
                if len(entry) >= 4:
                    start_day = entry[1]
                    end_day = entry[2] if entry[2] else entry[1]
                    ganzi = entry[3] if entry[3] else ""
                    
                    # Extract narrative for this day range
                    # Look for content between this date and next date
                    date_key_pattern = rf'{month}月{start_day}日'
                    if end_day != start_day:
                        date_key_pattern += rf'(?:\s*至\s*{month}月{end_day}日)?'
                    
                    # Find the narrative section
                    narrative_match = re.search(
                        rf'{month}月{start_day}日[^財運]*財運[：:]\s*(.*?)(?={month}月\d+日|\Z)',
                        month_section,
                        re.DOTALL
                    )
                    
                    if narrative_match:
                        narrative = narrative_match.group(1).strip()
                        # Clean up formatting
                        narrative = re.sub(r'\s+', ' ', narrative)
                        narrative = narrative.replace('事業： ', '事業：').replace('財運： ', '財運：').replace('盲派斷： ', '盲派斷：')
                        
                        for day in range(int(start_day), int(end_day) + 1):
                            key = f"{year}-05-{int(day):02d}"  # Default to May, need to fix
                            # Actually need to track month better
    
    return data

def main():
    print("Reading Grok file...")
    grok_data = parse_grok_file(GROK_FILE)
    print(f"Parsed {len(grok_data)} grok entries")
    
    # Load existing JSON
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        existing = json.load(f)
    
    # Start with existing data, add grok entries
    for key, value in grok_data.items():
        parts = key.split('-')
        if len(parts) == 3:
            year, month, day = parts
            if year not in existing:
                existing[year] = {}
            if month not in existing[year]:
                existing[year][month] = {}
            if day not in existing[year][month]:
                existing[year][month][day] = {}
            existing[year][month][day]['grok'] = value['grok']
    
    # Write back
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    
    print(f"Written to {OUTPUT_FILE}")
    print(f"Total entries: {sum(len(m) for y in existing.values() for m in y.values())}")

if __name__ == "__main__":
    main()