#!/usr/bin/env python3
"""
Networking - Query contacts
Usage:
    python3 query.py             # All active contacts
    python3 query.py done        # Done contacts
    python3 query.py due         # Due for follow-up
"""
import sys
from lib import load_contacts, get_due_contacts, today_hkt


def show(c, prefix=""):
    print(f"{prefix}**{c.get('name')}** ({c.get('company')})")
    print(f"{prefix}  ID: {c.get('contact_id')}")
    print(f"{prefix}  Contact: {c.get('contact_date')} → Follow-up: {c.get('follow_up_date')}")
    print(f"{prefix}  Topic: {c.get('topic', 'N/A')}")
    print(f"{prefix}  Next: {c.get('next_action', 'N/A')}")
    print(f"{prefix}  Channel: {c.get('channel', 'linkedin')}")
    print(f"{prefix}  Followed up: {c.get('follow_up_count', 0)} times")
    if c.get("done"):
        print(f"{prefix}  ✓ DONE")
    print()


def main():
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "active"
    contacts = load_contacts()

    if cmd in ("active", "all"):
        active = [c for c in contacts if not c.get("done")]
        print(f"🤝 Active contacts ({len(active)}):\n")
        for c in active:
            show(c)
    elif cmd == "done":
        done = [c for c in contacts if c.get("done")]
        print(f"✓ Done contacts ({len(done)}):\n")
        for c in done:
            show(c)
    elif cmd == "due":
        due = get_due_contacts()
        print(f"🔥 Due for follow-up ({len(due)}, today={today_hkt()}):\n")
        for c in due:
            show(c)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
