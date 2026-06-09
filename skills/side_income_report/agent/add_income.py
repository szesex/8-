#!/usr/bin/env python3
"""
Side Income - Add entry
Usage:
    python3 add_income.py <amount> <source> [date] [hours] [notes...]
"""
import sys
from lib import add_income


def main():
    if len(sys.argv) < 3:
        print("用法: python3 add_income.py <amount> <source> [date] [hours] [notes...]")
        print("範例: amount=800 source=活木生活木工 date=2026-06-09 hours=8")
        sys.exit(1)
    try:
        amount = float(sys.argv[1])
    except ValueError:
        print(f"❌ amount 必須係數字: {sys.argv[1]}")
        sys.exit(1)
    source = sys.argv[2]
    date = sys.argv[3] if len(sys.argv) > 3 else None
    hours = float(sys.argv[4]) if len(sys.argv) > 4 else 0
    notes = " ".join(sys.argv[5:]) if len(sys.argv) > 5 else ""
    entry = add_income(amount, source, date, hours, notes)
    print(f"✅ Added #{entry['entry_id']}: ${entry['amount']:.0f} from {entry['source']}")
    print(f"   Date: {entry['date']}  Hours: {entry['hours']}h")
    if entry["notes"]:
        print(f"   Notes: {entry['notes']}")


if __name__ == "__main__":
    main()
