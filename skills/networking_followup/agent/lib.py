"""
Networking Follow-up - shared library
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

# Paths
SKILL_DIR = Path("/home/node/.openclaw/workspace/skills/networking_followup")
DATA_FILE = SKILL_DIR / "data" / "contacts.json"

# Telegram
TELEGRAM_BOT_TOKEN = "8775775652:AAEZCZo8aX0KCrQ0uHNZlIc8_bjTWVyoiw8"
TELEGRAM_CHAT_ID = "8475453959"

HKT = ZoneInfo("Asia/Hong_Kong")


def now_hkt():
    return datetime.now(HKT)


def today_hkt():
    return now_hkt().strftime("%Y-%m-%d")


def load_contacts():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        return []


def save_contacts(contacts):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(contacts, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def add_contact(name, company, contact_date=None, follow_up_date=None,
                topic="", next_action="", channel="linkedin"):
    """Add new contact."""
    contact_date = contact_date or today_hkt()
    follow_up_date = follow_up_date or (
        datetime.now(HKT) + timedelta(days=7)
    ).strftime("%Y-%m-%d")

    entry = {
        "contact_id": now_hkt().strftime("%Y%m%d%H%M%S"),
        "name": name,
        "company": company,
        "contact_date": contact_date,
        "follow_up_date": follow_up_date,
        "topic": topic,
        "next_action": next_action,
        "channel": channel,
        "done": False,
        "follow_up_count": 0,
        "added_at": now_hkt().isoformat(timespec="seconds"),
    }
    contacts = load_contacts()
    contacts.append(entry)
    save_contacts(contacts)
    return entry


def get_due_contacts(today=None):
    """Get contacts due for follow-up (and not done)."""
    today = today or today_hkt()
    contacts = load_contacts()
    return [
        c for c in contacts
        if c.get("follow_up_date", "") <= today and not c.get("done")
    ]


def mark_followed_up(contact_id):
    """Mark as followed up + bump follow_up_date by 7 days."""
    contacts = load_contacts()
    for c in contacts:
        if c.get("contact_id") == contact_id:
            c["done"] = False  # Keep active for future
            c["follow_up_count"] = c.get("follow_up_count", 0) + 1
            c["last_followed_up_at"] = now_hkt().isoformat(timespec="seconds")
            # Bump follow_up_date by 7 days
            old = datetime.strptime(c["follow_up_date"], "%Y-%m-%d")
            c["follow_up_date"] = (old + timedelta(days=7)).strftime("%Y-%m-%d")
            break
    save_contacts(contacts)


def mark_done(contact_id):
    """Mark contact as done (no more follow-ups)."""
    contacts = load_contacts()
    for c in contacts:
        if c.get("contact_id") == contact_id:
            c["done"] = True
            c["done_at"] = now_hkt().isoformat(timespec="seconds")
            break
    save_contacts(contacts)


def generate_followup_draft(contact):
    """Generate LinkedIn / email follow-up message draft."""
    name = contact.get("name", "")
    company = contact.get("company", "")
    topic = contact.get("topic", "")
    next_action = contact.get("next_action", "")
    channel = contact.get("channel", "linkedin").lower()
    last_count = contact.get("follow_up_count", 0)

    if channel == "linkedin":
        if last_count == 0:
            # First follow-up
            message = (
                f"Hi {name},\n\n"
                f"Hope you're doing well! It was great connecting with you at "
                f"{company} on {contact.get('contact_date')}. "
                f"我哋傾過「{topic}」呢個 topic，我諗咗一陣覺得非常有 value。\n\n"
                f"{f'我想 follow up 下次：{next_action}。你 ok 嗎？' if next_action else '我諗住繼續 explore 呢個方向，有咩 update 你想 share?'}\n\n"
                f"Best,\nSaba"
            )
        else:
            # Subsequent follow-up
            message = (
                f"Hi {name},\n\n"
                f"想再 ping 你下 — 上次傾過「{topic}」之後我繼續有 progress。\n\n"
                f"{f'Next step: {next_action}' if next_action else '你覺得下一步可以點?'}\n\n"
                f"Thanks,\nSaba"
            )
    elif channel == "email":
        subject = f"Following up: {topic}" if topic else "Following up"
        message = (
            f"Subject: {subject}\n\n"
            f"Hi {name},\n\n"
            f"Hope this finds you well. I'm following up on our conversation from "
            f"{contact.get('contact_date')} about {topic}.\n\n"
            f"{f'As discussed, the next step would be: {next_action}.' if next_action else 'I wanted to check in and see if there are any updates on your end.'}\n\n"
            f"Looking forward to hearing from you.\n\n"
            f"Best regards,\nSaba"
        )
    else:
        # Generic
        message = (
            f"Hi {name}, 跟進一下我哋 {contact.get('contact_date')} 嘅傾偈 (關於 {topic})。"
            f"{f' Next: {next_action}。' if next_action else ''}"
        )
    return message


def build_reminder():
    """Build reminder markdown for today's due contacts."""
    today = today_hkt()
    due = get_due_contacts(today)
    if not due:
        return (
            f"✅ **{today} 冇 follow-up。**\n"
            f"繼續 keep 住 networking ✊"
        )

    text = f"**🤝 今日 follow-up ({len(due)})：**\n\n"
    for c in due:
        text += f"**{c.get('name')}** ({c.get('company')})\n"
        text += f"  📅 接觸：{c.get('contact_date')} → 跟進：{c.get('follow_up_date')}\n"
        text += f"  💬 Topic: {c.get('topic', 'N/A')}\n"
        text += f"  🎯 Next: {c.get('next_action', 'N/A')}\n"
        text += f"  📡 Channel: {c.get('channel', 'linkedin')}\n"
        # Generate draft
        draft = generate_followup_draft(c)
        text += f"\n  ✍️ **草稿 ({c.get('channel')})：**\n"
        # Indent
        for line in draft.split("\n"):
            text += f"  > {line}\n"
        text += "\n"
    text += (
        "---\n"
        "💡 Send 完之後用 `done.py` mark done, 或者 `mark_followed_up.py` 推遲 7 日。\n"
        "🤝 Networking 係長線投資。Keep it up."
    )
    return text


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
