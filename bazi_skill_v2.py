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

def get_daily_bazi(date):
    """Calculate the daily 8-char (流日) for any given date."""
    # Reference: 2024-01-01 is 乙丑日
    stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # Known reference points for accuracy
    # 2026-05-14 = 戊子日
    # Using solar term boundaries for accuracy
    ref_2026_05_14 = datetime.date(2026, 5, 14)
    ref_stem = 4  # 戊 (0-based)
    ref_branch = 0  # 子 (0-based)
    
    days_diff = (date - ref_2026_05_14).days
    stem_idx = (ref_stem + days_diff) % 10
    branch_idx = (ref_branch + days_diff) % 12
    
    return stems[stem_idx] + branches[branch_idx]

def generate_daily_alert(date, version="dual"):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    data = load_data()
    
    daily_bazi = get_daily_bazi(date)
    
    saba_bazi = """
【Saba 8字】
正四柱：乙亥 甲申 戊寅 甲子
隱藏四柱：身宮乙酉 胎息癸亥 胎元乙亥 命宮乙酉
日主戊土 • 最強五行水 • 庚運一代（1984-2044）

【當日8字】
{}年{}月{}日 {}日
""".format(date.year, date.month, date.day, daily_bazi)
    
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
    comparison = """
【OpenClaw AI 每日比較】{}年{}月{}日

Grok 版風格：重「金水黏連 + 隱藏雙劍鋒金 + 技術變現」
DeepSeek 版風格：重「刑合困局 + 心魔誘惑 + 老千局心理戰」

今日建議：
- 事業：兩版都話今日有打硬仗機會，建議主動出擊
- 財運：小心心魔（子水）引誘，專注正財辛苦錢
- 盲派斷：金水黏連繼續鎖死，火土反彈已被壓制

【請手填 Rank Feedback 學習算法】
1 = Grok 完勝
2 = DeepSeek 完勝
3 = 平手
4 = Grok 微勝
5 = DeepSeek 微勝

記住：命硬靠心態，你一定得！
隱姓埋名，藏術數，學盲派8字，易經算股市——我哋下次見！🔥
""".format(date.year, date.month, date.day)
    return comparison

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