#!/usr/bin/env python3
"""
Bazi Monthly Comparison + Reminder
每月初一發送：
1. 月份運程提醒
2. Grok + DeepSeek monthly comparison
"""

import datetime
import json
import os

DATA_FILE = "/home/workdir/artifacts/bazi_fortune_data.json"
COMPARE_FILE = "/home/workdir/artifacts/bazi_monthly_comparison.json"

def get_hkt_date():
    try:
        import pytz
        hkt = pytz.timezone('Asia/Hong_Kong')
        now = datetime.datetime.now(hkt)
    except ImportError:
        now = datetime.datetime.now()
    return now.date(), now

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_lunar_month_key(date):
    month_map = {
        1: "辛丑", 2: "庚寅", 3: "辛卯", 4: "壬辰",
        5: "癸巳", 6: "甲午", 7: "乙未", 8: "丙申",
        9: "丁酉", 10: "戊戌", 11: "己亥", 12: "庚子"
    }
    return month_map.get(date.month, "")

def format_comparison(comparison):
    """Format Grok vs DeepSeek as plain text"""
    grok = comparison.get("grok", "")
    deepseek = comparison.get("deepseek", "")
    
    result = "━━━━━━━━━━━━━━\n"
    result += "🟢 GROK 分析\n"
    result += "━━━━━━━━━━━━━━\n"
    if grok:
        result += grok.strip() + "\n"
    else:
        result += "（無資料）\n"
    
    result += "\n━━━━━━━━━━━━━━\n"
    result += "🔵 DEEPSEEK 分析\n"
    result += "━━━━━━━━━━━━━━\n"
    if deepseek:
        result += deepseek.strip() + "\n"
    else:
        result += "（無資料）\n"
    
    return result

def generate_monthly_message(date):
    year = str(date.year)
    month_key = get_lunar_month_key(date)
    
    compare_data = load_json(COMPARE_FILE)
    
    greeting = "【每月初一運程 Compare】"
    
    if not month_key:
        return f"{greeting}\n\n月份資料未找到。"
    
    comparison_text = ""
    if year in compare_data and month_key in compare_data[year]:
        comparison = compare_data[year][month_key]
        comparison_text = format_comparison(comparison)
    
    msg = f"""{greeting}
🌟 {date.year}年{date.month}月【{month_key}】

✅ 繼續跟住金水破火計劃，親水、戴金飾、行善。

{comparison_text}
🔥 命硬靠心態，你一定得！"""
    
    return msg

def main():
    date, now = get_hkt_date()
    message = generate_monthly_message(date)
    print(message)

if __name__ == "__main__":
    main()