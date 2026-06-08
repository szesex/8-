#!/usr/bin/env python3
"""
Side Income Report — MVP stub
Cron: 0 2 1 * * (每月 1 號 10:00 HKT)
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
DATA_FILE = Path("/home/node/.openclaw/workspace/skills/side_income_report/income.json")


def load_income():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        return []


def save_income(income):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(income, indent=2, ensure_ascii=False), encoding="utf-8")


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


def push_report():
    today = datetime.now(HKT)
    income = load_income()

    # This month
    this_month = today.strftime("%Y-%m")
    this_month_data = [e for e in income if e.get("date", "").startswith(this_month)]

    # Last month
    last_month = (today.replace(day=1)).strftime("%Y-%m")
    last_month_data = [e for e in income if e.get("date", "").startswith(last_month)]

    # Aggregate by source
    by_source = {}
    for e in this_month_data:
        src = e.get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + e.get("amount", 0)

    total = sum(by_source.values())

    text = (
        f"**💰 Side Income Report — {this_month}**\n\n"
        f"**本月總收入：** ${total:.0f}\n"
        f"**Entries：** {len(this_month_data)}\n\n"
    )
    if by_source:
        text += "**By source：**\n"
        for src, amt in sorted(by_source.items(), key=lambda x: -x[1]):
            text += f"  • {src}: ${amt:.0f}\n"
    else:
        text += "本月未記錄任何 income。\n"

    text += (
        f"\n**💡 還債金額建議：50% → 還債，30% → 投資自己，20% → 緩衝**\n"
        f"  → 還債：${total * 0.5:.0f}\n"
        f"\n---\n"
        f"🤒 病緊就慢慢嚟。記低收入先，計晒數再算。\n"
    )

    result = send_telegram(text)
    if result.get("ok"):
        print(f"✅ Pushed. message_id = {result['result']['message_id']}")
    else:
        print(f"❌ Failed: {result}")


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "add":
        if len(sys.argv) < 4:
            print("用法: python3 run.py add <amount> <source> [date] [hours] [notes]")
            return
        try:
            amount = float(sys.argv[2])
        except ValueError:
            print(f"❌ amount 必須係數字: {sys.argv[2]}")
            return
        source = sys.argv[3]
        date = sys.argv[4] if len(sys.argv) > 4 else datetime.now(HKT).strftime("%Y-%m-%d")
        hours = float(sys.argv[5]) if len(sys.argv) > 5 else 0
        notes = sys.argv[6] if len(sys.argv) > 6 else ""

        income = load_income()
        income.append({
            "date": date,
            "amount": amount,
            "source": source,
            "hours": hours,
            "notes": notes,
            "added_at": datetime.now(HKT).isoformat(timespec="seconds"),
        })
        save_income(income)
        print(f"✅ Added ${amount:.0f} from {source}")
    else:
        push_report()


if __name__ == "__main__":
    main()
