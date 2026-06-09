#!/usr/bin/env python3
"""
Networking - Add contact
Usage:
    python3 add_contact.py "John Chan" "AECOM" "2026-06-08" "2026-06-15" "slope remedial 傾過" "Send 完整 resume" linkedin
"""
import sys
from lib import add_contact


def main():
    if len(sys.argv) < 3:
        print("用法: python3 add_contact.py <name> <company> [contact_date] [follow_up_date] [topic] [next_action] [channel]")
        print("channel: linkedin (default) | email | other")
        sys.exit(1)
    name = sys.argv[1]
    company = sys.argv[2]
    contact_date = sys.argv[3] if len(sys.argv) > 3 else None
    follow_up_date = sys.argv[4] if len(sys.argv) > 4 else None
    topic = sys.argv[5] if len(sys.argv) > 5 else ""
    next_action = sys.argv[6] if len(sys.argv) > 6 else ""
    channel = sys.argv[7] if len(sys.argv) > 7 else "linkedin"
    entry = add_contact(name, company, contact_date, follow_up_date, topic, next_action, channel)
    print(f"✅ Added #{entry['contact_id']}: {entry['name']} ({entry['company']})")
    print(f"   Contact: {entry['contact_date']}")
    print(f"   Follow-up: {entry['follow_up_date']}")
    print(f"   Topic: {entry['topic']}")
    print(f"   Channel: {entry['channel']}")


if __name__ == "__main__":
    main()
