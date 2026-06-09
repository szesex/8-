#!/usr/bin/env python3
"""
Networking - Mark follow-up actions
Usage:
    python3 mark.py followed_up <contact_id>     # Bump follow_up_date +7d
    python3 mark.py done <contact_id>            # Mark as done (no more follow-ups)
"""
import sys
from lib import mark_followed_up, mark_done, load_contacts


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 mark.py followed_up <contact_id>")
        print("  python3 mark.py done <contact_id>")
        sys.exit(1)
    action = sys.argv[1].lower()
    contact_id = sys.argv[2]

    if action == "followed_up":
        mark_followed_up(contact_id)
        # Show updated
        for c in load_contacts():
            if c.get("contact_id") == contact_id:
                print(f"✅ {c.get('name')} followed up. Next follow-up: {c.get('follow_up_date')} (count: {c.get('follow_up_count')})")
                return
        print(f"❌ Contact not found: {contact_id}")
    elif action == "done":
        mark_done(contact_id)
        for c in load_contacts():
            if c.get("contact_id") == contact_id:
                print(f"✅ {c.get('name')} marked done.")
                return
        print(f"❌ Contact not found: {contact_id}")
    else:
        print(f"❌ Unknown action: {action}")


if __name__ == "__main__":
    main()
