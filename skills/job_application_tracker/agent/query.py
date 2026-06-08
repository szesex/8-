#!/usr/bin/env python3
"""
Job Application Tracker - Query
Usage:
    python3 query.py dashboard
    python3 query.py status 20260609123456
    python3 query.py follow_up_today
    python3 query.py rejected_recent 30
    python3 query.py active
    python3 query.py all
"""
import sys
from datetime import datetime, timedelta
from lib import load_applications, today_hkt
from generate_dashboard import compute_dashboard as _dashboard_func

ACTIVE_STATUSES = {"applied", "phone_screen", "interview"}


def show_entry(e):
    """Pretty-print a single application entry."""
    print(f"#{e.get('application_id')} — {e.get('company')}")
    print(f"  職位: {e.get('position')}")
    print(f"  薪金: {e.get('salary_range')}")
    print(f"  申請: {e.get('applied_date')}  |  Deadline: {e.get('deadline')}")
    print(f"  Status: {e.get('status')}  |  Follow-up: {e.get('follow_up_date')}")
    if e.get("notes"):
        print(f"  備註: {e.get('notes')}")


def cmd_dashboard():
    print(_dashboard_func())


def cmd_status(app_id):
    app_id = app_id.lstrip("#")
    data = load_applications()
    for e in data:
        if e.get("application_id") == app_id:
            show_entry(e)
            return
    print(f"❌ 搵唔到 #{app_id}")


def cmd_follow_up_today():
    today = today_hkt()
    data = load_applications()
    items = [
        e for e in data
        if e.get("follow_up_date", "") <= today
        and e.get("status") in {"applied", "phone_screen"}
    ]
    if not items:
        print("✅ 今日冇 follow-up。")
        return
    print(f"🔥 今日需要 follow-up ({len(items)})：")
    for e in items:
        show_entry(e)
        print()


def cmd_rejected_recent(days=30):
    data = load_applications()
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    items = [
        e for e in data
        if e.get("status") == "rejected"
        and e.get("applied_date", "") >= cutoff
    ]
    print(f"❌ 過去 {days} 日 rejected ({len(items)})：")
    for e in items:
        show_entry(e)
        print()


def cmd_active():
    data = load_applications()
    items = [e for e in data if e.get("status") in ACTIVE_STATUSES]
    print(f"🔄 進行中 ({len(items)})：")
    for e in items:
        show_entry(e)
        print()


def cmd_all():
    data = load_applications()
    print(f"📋 所有申請 ({len(data)})：")
    for e in data:
        show_entry(e)
        print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1].lower().replace("-", "_")

    if cmd == "dashboard":
        cmd_dashboard()
    elif cmd == "status":
        if len(sys.argv) < 3:
            print("用法: python3 query.py status <application_id>")
            sys.exit(1)
        cmd_status(sys.argv[2])
    elif cmd == "follow_up_today":
        cmd_follow_up_today()
    elif cmd == "rejected_recent":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        cmd_rejected_recent(days)
    elif cmd == "active":
        cmd_active()
    elif cmd == "all":
        cmd_all()
    else:
        print(f"❌ Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
