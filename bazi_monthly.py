#!/usr/bin/env python3
"""
Bazi Monthly Comparison + Reminder
每月初一發送：
1. 月份運程提醒
2. Grok/DeepSeek monthly comparison
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
    """根據月份對應流月干支"""
    month_map = {
        1: "辛丑", 2: "庚寅", 3: "辛卯", 4: "壬辰",
        5: "癸巳", 6: "甲午", 7: "乙未", 8: "丙申",
        9: "丁酉", 10: "戊戌", 11: "己亥", 12: "庚子"
    }
    return month_map.get(date.month, "")

def generate_monthly_message(date):
    year = str(date.year)
    month_key = get_lunar_month_key(date)
    
    compare_data = load_json(COMPARE_FILE)
    
    greeting = "【每月運程提醒】大家好！隱姓埋名藏術數，又嚟同大家傾偈啦！"
    
    # 基本月份運勢
    if month_key:
        compare_text = ""
        if year in compare_data and month_key in compare_data[year]:
            info = compare_data[year][month_key]
            parts = info.split("。")
            if len(parts) >= 3:
                compare_text = f"""
📊 【Grok/DeepSeek 月份 Compare】
事業：{parts[0].strip()}
財運：{parts[1].strip()}
盲派斷：{parts[2].strip()}"""
        
        # 發送月度運程
        data = load_json(DATA_FILE)
        month_str = str(date.month)
        
        month_fortune = ""
        if year in data and month_str in data[year]:
            month_fortune = f"\n\n📅 【逐日運程精華】\n"
            for day in range(1, 32):
                day_str = str(day)
                if day_str in data[year][month_str]:
                    fortune = data[year][month_str][day_str].split("\n")[0]
                    month_fortune += f"{day}日：{fortune}\n"
        
        msg = f"""{greeting}

🌟 {date.year}年{date.month}月【{month_key}】運程

✅ 繼續跟住金水破火計劃，親水、戴金飾、行善。
✅ 事業/財運/感情關鍵月！{compare_text}

🔥 命硬靠心態，你一定得！

隱姓埋名，藏術數，學盲派8字，易經算股市——我哋下次見！"""
        
        return msg
    else:
        return f"{greeting}\n\n月份資料未找到。"

def main():
    date, now = get_hkt_date()
    message = generate_monthly_message(date)
    print(message)

if __name__ == "__main__":
    main()