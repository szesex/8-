#!/usr/bin/env python3
"""
Job Application Tracker - Add new application
Usage:
    python3 add_application.py "新增: ABC Engineering, Assistant Engineer, 18-22k, 2026-06-10, 2026-06-30, slope remedial 經驗"
"""
import sys
from lib import add_application


def main():
    if len(sys.argv) < 2:
        print("用法: python3 add_application.py \"新增: 公司, 職位, 薪金, 申請日期, deadline, 備註\"")
        print("範例: python3 add_application.py \"新增: ABC Eng, Asst Eng, 18-22k, 2026-06-10, 2026-06-30, slope remedial\"")
        sys.exit(1)
    user_input = sys.argv[1]
    try:
        entry = add_application(user_input)
    except ValueError as e:
        print(f"❌ Parse error: {e}")
        sys.exit(1)
    print(f"✅ Added new application #{entry['application_id']}")
    print()
    for k, v in entry.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
