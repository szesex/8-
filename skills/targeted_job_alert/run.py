#!/usr/bin/env python3
"""
Targeted Job Alert — MVP stub
Cron: 0 0 * * 2,5 (週二、五 08:00 HKT)

Currently a stub that pushes a static prompt.
TODO: integrate with real job search API.
"""
import sys
import json
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TELEGRAM_BOT_TOKEN = "8775775652:AAEZCZo8aX0KCrQ0uHNZlIc8_bjTWVyoiw8"
TELEGRAM_CHAT_ID = "8475453959"
HKT = ZoneInfo("Asia/Hong_Kong")
DATA_FILE = Path("/home/node/.openclaw/workspace/skills/targeted_job_alert/jobs.json")

KEYWORDS = [
    "geotechnical engineer",
    "slope stability",
    "Assistant Engineer",
    "TCP",
    "Minor Works Class 1",
    "rock slope",
    "tender preparation",
]


def load_jobs():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        return []


def save_jobs(jobs):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(jobs, indent=2, ensure_ascii=False), encoding="utf-8")


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": "true",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"ok": False, "error": str(e)}


def push_alert():
    """Push a static reminder — TODO replace with real search."""
    today = datetime.now(HKT).strftime("%Y-%m-%d %a")
    keywords_str = ", ".join(KEYWORDS)
    text = (
        f"**🎯 Targeted Job Alert — {today}**\n\n"
        f"⏰ 週二、五 自動提醒你去 check 新職位\n\n"
        f"**搜尋關鍵字：**\n{keywords_str}\n\n"
        f"**建議 sources：**\n"
        f"• JobsDB: https://hk.jobsdb.com/\n"
        f"• CTgoodjobs: https://www.ctgoodjobs.hk/\n"
        f"• LinkedIn: https://www.linkedin.com/jobs/\n\n"
        f"💡 提示：搜完之後用 Skill 1 (job_application_tracker) 記低。\n"
        f"---\n"
        f"⚠️ MVP stub — TODO: 接入真實 API 自動 scrape"
    )
    result = send_telegram(text)
    if result.get("ok"):
        print(f"✅ Pushed. message_id = {result['result']['message_id']}")
    else:
        print(f"❌ Failed: {result}")


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "add":
        # Manual add
        if len(sys.argv) < 3:
            print("用法: python3 run.py add <URL> [notes]")
            return
        url = sys.argv[2]
        notes = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        jobs = load_jobs()
        jobs.append({
            "url": url,
            "notes": notes,
            "added_at": datetime.now(HKT).isoformat(timespec="seconds"),
        })
        save_jobs(jobs)
        print(f"✅ Added job: {url}")
    else:
        push_alert()


if __name__ == "__main__":
    main()
