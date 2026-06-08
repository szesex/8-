#!/usr/bin/env python3
"""
Weekly Review + Streak Tracker — MVP stub
Cron: 0 12 * * 0 (週日 20:00 HKT)
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TELEGRAM_BOT_TOKEN = "8775775652:AAEZCZo8aX0KCrQ0uHNZlIc8_bjTWVyoiw8"
TELEGRAM_CHAT_ID = "8475453959"
HKT = ZoneInfo("Asia/Hong_Kong")
DATA_FILE = Path("/home/node/.openclaw/workspace/skills/weekly_review_streak/weeks.json")


def load_weeks():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        return []


def save_weeks(weeks):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(weeks, indent=2, ensure_ascii=False), encoding="utf-8")


def get_job_app_count_this_week():
    """Read job_application_tracker data for this week's count."""
    job_file = Path("/home/node/.openclaw/workspace/skills/job_application_tracker/data/applications.json")
    if not job_file.exists():
        return 0
    try:
        from datetime import timedelta
        data = json.loads(job_file.read_text(encoding="utf-8"))
        today = datetime.now(HKT)
        week_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        return sum(1 for e in data if e.get("applied_date", "") >= week_ago)
    except:
        return 0


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


def push_review():
    """Push weekly review."""
    today = datetime.now(HKT)
    week = today.strftime("%Y-W%V")
    job_count = get_job_app_count_this_week()

    text = (
        f"**📅 Weekly Review — {today.strftime('%Y-%m-%d')} (Week {week.split('W')[1]})**\n\n"
        f"**本週數據：**\n"
        f"📨 Job applications this week: **{job_count}**\n"
        f"📚 Exam study: (手動 log)\n"
        f"💻 OpenClaw dev: (手動 log)\n"
        f"🥊 MMA: (手動 log)\n"
        f"💰 Debt repaid: (手動 log)\n\n"
        f"**下週 3 個建議行動：**\n"
        f"1. 至少 2 個新申請 (用 Skill 1 記低)\n"
        f"2. Exam study 至少 5 hrs\n"
        f"3. MMA / Exercise 至少 2 次\n\n"
        f"---\n"
        f"💪 單打獨鬥第 {week.split('W')[1]} 週。Keep going，慢慢嚟唔好急。\n"
        f"你係自己嘅最強後盾。"
    )
    result = send_telegram(text)
    if result.get("ok"):
        print(f"✅ Pushed. message_id = {result['result']['message_id']}")
    else:
        print(f"❌ Failed: {result}")


def main():
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "log":
        print("TODO: Interactive log prompt")
    else:
        push_review()


if __name__ == "__main__":
    main()
