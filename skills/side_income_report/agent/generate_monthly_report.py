#!/usr/bin/env python3
"""
Side Income - Generate monthly report
Cron: 0 2 1 * * (每月 1 號 10:00 HKT)
"""
import sys
from lib import build_report, send_telegram


def main():
    text = build_report()
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
