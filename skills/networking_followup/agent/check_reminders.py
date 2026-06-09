#!/usr/bin/env python3
"""
Networking - Check reminders and push to Telegram
Cron: 0 1 * * * (每日 09:00 HKT)
"""
import sys
from lib import build_reminder, send_telegram


def main():
    text = build_reminder()
    print(text)
    print()
    print("--- Sending to Telegram ---")
    result = send_telegram(text)
    if result.get("ok"):
        print(f"✅ Sent. message_id = {result['result']['message_id']}")
    else:
        print(f"❌ Telegram send failed: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
