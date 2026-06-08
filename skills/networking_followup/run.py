#!/usr/bin/env python3
"""
Networking Follow-up — MVP stub
Cron: 0 1 * * * (每日 09:00 HKT)
"""
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TELEGRAM_BOT_TOKEN = "8775775652:AAEZCZo8aX0KCrQ0uHNZlIc8_bjTWVyoiw8"
TELEGRAM_CHAT_ID = "8475453959"
HKT = ZoneInfo("Asia/Hong_Kong")
DATA_FILE = Path("/home/node/.openclaw/workspace/skills/networking_followup/contacts.json")


def load_contacts():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        return []


def save_contacts(contacts):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(contacts, indent=2, ensure_ascii=False), encoding="utf-8")


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


def push_reminder():
    today = datetime.now(HKT).strftime("%Y-%m-%d")
    contacts = load_contacts()
    due = [c for c in contacts if c.get("follow_up_date", "") <= today and not c.get("done")]

    if not due:
        text = f"✅ **{today} 冇 follow-up。**\n繼續 keep 住 networking ✊"
    else:
        text = f"**🤝 今日 follow-up ({len(due)})：**\n"
        for c in due:
            text += f"\n• **{c.get('name')}** ({c.get('company')})\n"
            text += f"  接觸：{c.get('contact_date')} → Follow-up：{c.get('follow_up_date')}\n"
            text += f"  討論：{c.get('topic', 'N/A')}\n"
            text += f"  Next action: {c.get('next_action', 'N/A')}\n"
        text += "\n---\n💡 提示：Send 訊息前先睇返當初 discussion context。"

    result = send_telegram(text)
    if result.get("ok"):
        print(f"✅ Pushed. message_id = {result['result']['message_id']}")
    else:
        print(f"❌ Failed: {result}")


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "add":
        if len(sys.argv) < 4:
            print("用法: python3 run.py add <name> <company> [contact_date] [follow_up_date] [topic] [next_action]")
            return
        name = sys.argv[2]
        company = sys.argv[3]
        contact_date = sys.argv[4] if len(sys.argv) > 4 else datetime.now(HKT).strftime("%Y-%m-%d")
        follow_up_date = sys.argv[5] if len(sys.argv) > 5 else contact_date
        topic = sys.argv[6] if len(sys.argv) > 6 else ""
        next_action = sys.argv[7] if len(sys.argv) > 7 else ""

        contacts = load_contacts()
        contacts.append({
            "name": name,
            "company": company,
            "contact_date": contact_date,
            "follow_up_date": follow_up_date,
            "topic": topic,
            "next_action": next_action,
            "done": False,
            "added_at": datetime.now(HKT).isoformat(timespec="seconds"),
        })
        save_contacts(contacts)
        print(f"✅ Added: {name} ({company})")
    else:
        push_reminder()


if __name__ == "__main__":
    main()
