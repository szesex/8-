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

def generate_daily_alert(date, version="dual"):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    data = load_data()
    
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
        alert = "{}\n\n【Grok 版】\n{}\n\n{}\n\n【DeepSeek 版】\n{}".format(
            date_str, grok_text, separator, deepseek_text)
    else:
        alert = "單版模式"
    
    closing = "\n記住：命硬靠心態，你一定得！\n隱姓埋名，藏術數，學盲派8字，易經算股市——我哋下次見！🔥"
    return "{}\n\n{}\n{}".format(greeting, alert, closing)

def run_alert():
    date, _ = get_hkt_date()
    print("=== OpenClaw Daily Dual Alert ===")
    print(generate_daily_alert(date, "dual"))

if __name__ == "__main__":
    run_alert()