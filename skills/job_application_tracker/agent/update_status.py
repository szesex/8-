#!/usr/bin/env python3
"""
Job Application Tracker - Update status
Usage:
    python3 update_status.py "20260609123456" "interview" "明天 10am 電話面試"
"""
import sys
from lib import update_status, VALID_STATUSES


def main():
    if len(sys.argv) < 3:
        print(f"用法: python3 update_status.py <application_id> <new_status> [notes]")
        print(f"status enum: {', '.join(sorted(VALID_STATUSES))}")
        sys.exit(1)
    app_id = sys.argv[1].lstrip("#")
    new_status = sys.argv[2]
    notes = sys.argv[3] if len(sys.argv) > 3 else ""
    try:
        old, new = update_status(app_id, new_status, notes)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    if old is None:
        print(f"❌ 搵唔到 application_id = '{app_id}'")
        sys.exit(1)
    print(f"✅ Updated #{app_id}")
    print()
    print("--- Before ---")
    print(f"  status: {old.get('status')}")
    print(f"  notes:  {old.get('notes', '')}")
    print()
    print("--- After ---")
    print(f"  status: {new.get('status')}")
    print(f"  notes:  {new.get('notes', '')}")


if __name__ == "__main__":
    main()
