#!/usr/bin/env python3
"""
OpenClaw Bazi Skill v2 - Workspace Version
"""
import datetime
import json
import os
import sys

DATA_FILE = "/home/node/.openclaw/workspace/bazi_fortune_data.json"

def get_hkt_date():
    try:
        import pytz
        hkt = pytz.timezone('Asia/Hong_Kong')
        now = datetime.datetime.now(hkt)
    except ImportError:
        now = datetime.datetime.now()
    return now.date(), now

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

def get_daily_bazi(date):
    """Calculate the daily 8-char (流日) for any given date."""
    ref_2026_05_14 = datetime.date(2026, 5, 14)
    ref_stem = 4  # 戊 (0-based)
    ref_branch = 0  # 子 (0-based)
    days_diff = (date - ref_2026_05_14).days
    stem_idx = (ref_stem + days_diff) % 10
    branch_idx = (ref_branch + days_diff) % 12
    return STEMS[stem_idx] + BRANCHES[branch_idx]

def get_year_bazi(year):
    """年柱: 天干地支 for the year."""
    offset = year - 2024
    stem_idx = offset % 10
    branch_idx = (4 + offset) % 12  # 辰=4 index
    return STEMS[stem_idx] + BRANCHES[branch_idx]

def get_month_bazi(year, month):
    """月柱: 天干地支 for the month."""
    # Accurate lookup for 2026 months
    # 2026=丙午年, stems/index: 甲=0,乙=1,丙=2,丁=3,戊=4,己=5,庚=6,辛=7,壬=8,癸=9
    # branches/index: 子=0,丑=1,寅=2,卯=3,辰=4,巳=5,午=6,未=7,申=8,酉=9,戌=10,亥=11
    month_calendar = {
        (2026, 1): (4, 2),   # 戊寅
        (2026, 2): (5, 3),   # 己卯
        (2026, 3): (6, 4),   # 庚辰
        (2026, 4): (7, 5),   # 辛巳
        (2026, 5): (8, 6),   # 壬午
        (2026, 6): (9, 7),   # 癸未
    }
    key = (year, month)
    if key in month_calendar:
        stem_idx, branch_idx = month_calendar[key]
    else:
        branch_idx = (2 + (month - 1)) % 12
        year_stem = (year - 2024) % 10
        stem_idx = (year_stem + (2 + (month - 1)) * 2) % 10
    return STEMS[stem_idx] + BRANCHES[branch_idx]

def generate_daily_alert(date, version="dual"):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    data = load_data()
    
    daily_bazi = get_daily_bazi(date)
    year_bazi = get_year_bazi(date.year)
    month_bazi = get_month_bazi(date.year, date.month)
    
    saba_bazi = """
【Saba 8字】
正四柱：乙亥 甲申 戊寅 甲子
隱藏四柱：身宮乙酉 胎息癸亥 胎元乙亥 命宮乙酉
日主戊土 • 最強五行水 • 庚運一代（1984-2044）

【當日8字】
{}年 {}月{}日 {}日
四柱：{} {} {} {}
""".format(
        date.year, date.month, date.day, daily_bazi,
        year_bazi, month_bazi, daily_bazi, daily_bazi[0] + '時'
    )
    
    greeting = "大家好！隱姓埋名藏術數，又嚟同大家傾偈啦！"
    date_str = "【{}年{}月{}日】".format(date.year, date.month, date.day)
    
    if version == "dual":
        grok_text = "事業：金水黏連繼續發力\n財運：守成避大動作\n盲派斷：隱藏雙劍鋒金伏吟大力劈甲！"
        if year in data and month in data[year] and day in data[year][month]:
            day_data = data[year][month][day]
            if isinstance(day_data, str):
                grok_text = day_data
            elif isinstance(day_data, dict) and "grok" in day_data:
                g = day_data["grok"]
                if isinstance(g, dict):
                    grok_text = "事業：{}\n財運：{}\n盲派斷：{}".format(
                        g.get('事業', ''), g.get('財運', ''), g.get('盲派斷', ''))
                elif isinstance(g, str):
                    grok_text = g
        
        deepseek_text = "事業：刑合困局 + 心魔誘惑\n財運：投機大忌\n盲派斷：巳申刑合 / 申子辰合水局"
        if year in data and month in data[year] and day in data[year][month]:
            day_data = data[year][month][day]
            if isinstance(day_data, str):
                deepseek_text = day_data
            elif isinstance(day_data, dict) and "deepseek" in day_data:
                d = day_data["deepseek"]
                if isinstance(d, dict):
                    deepseek_text = "事業：{}\n財運：{}\n盲派斷：{}".format(
                        d.get('事業', ''), d.get('財運', ''), d.get('盲派斷', ''))
                elif isinstance(d, str):
                    deepseek_text = d
        
        separator = "═" * 45
        alert = "{}{}\n【Grok 版】\n{}\n\n{}\n\n【DeepSeek 版】\n{}".format(
            date_str, saba_bazi, grok_text, separator, deepseek_text)
    else:
        alert = "單版模式"
    
    closing = "\n記住：命硬靠心態，你一定得！\n隱姓埋名，藏術數，學盲派8字，易經算股市——我哋下次見！🔥"
    return "{}\n\n{}\n{}".format(greeting, alert, closing)

def generate_daily_comparison(date):
    year = str(date.year)
    month = f"{date.month:02d}"
    day = f"{date.day:02d}"
    data = load_data()
    
    grok_content = None
    deepseek_content = None
    
    if year in data and month in data[year] and day in data[year][month]:
        day_data = data[year][month][day]
        if isinstance(day_data, dict):
            grok_content = day_data.get('grok')
            deepseek_content = day_data.get('deepseek')
    
    comparison_lines = [
        f"【OpenClaw AI 每日比較】{date.year}年{date.month}月{date.day}日",
        "",
    ]
    
    if grok_content:
        comparison_lines.append("【Grok 版】")
        comparison_lines.append(grok_content[:300] if len(grok_content) > 300 else grok_content)
        comparison_lines.append("")
    
    if deepseek_content:
        comparison_lines.append("【DeepSeek 版】")
        comparison_lines.append(deepseek_content[:300] if len(deepseek_content) > 300 else deepseek_content)
        comparison_lines.append("")
    
    if not grok_content and not deepseek_content:
        comparison_lines.append("今日數據載入中...")
        comparison_lines.append("")
    
    comparison_lines.extend([
        "【請手填 Rank Feedback 學習算法】",
        "1 = Grok 完勝",
        "2 = DeepSeek 完勝",
        "3 = 平手",
        "4 = Grok 微勝",
        "5 = DeepSeek 微勝",
        "",
        "記住：命硬靠心態，你一定得！",
        "隱姓埋名，藏術數，學盲派8字、易經算股市——我哋下次見！🔥"
    ])
    
    return "\n".join(comparison_lines)

def run_alert():
    date, _ = get_hkt_date()
    print("=== OpenClaw Daily Dual Alert ===")
    print(generate_daily_alert(date, "dual"))

def run_feedback():
    date, _ = get_hkt_date()
    print("=== OpenClaw Daily Feedback ===")
    print(generate_daily_comparison(date))

def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = "alert"
    
    if mode == "alert":
        run_alert()
    elif mode == "feedback":
        run_feedback()
    else:
        print("用法: python3 bazi_skill_v2.py [alert|feedback]")

if __name__ == "__main__":
    main()