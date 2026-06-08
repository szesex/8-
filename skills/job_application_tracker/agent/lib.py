"""
Job Application Tracker - shared library
Single source of truth for applications data + Telegram send
"""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

# Paths
SKILL_DIR = Path("/home/node/.openclaw/workspace/skills/job_application_tracker")
DATA_FILE = SKILL_DIR / "data" / "applications.json"

# Telegram (for cron pushes)
TELEGRAM_BOT_TOKEN = "8775775652:AAEZCZo8aX0KCrQ0uHNZlIc8_bjTWVyoiw8"
TELEGRAM_CHAT_ID = "8475453959"

# Status enum
VALID_STATUSES = {"applied", "phone_screen", "interview", "offer", "rejected", "withdrawn"}

# HKT timezone
HKT = ZoneInfo("Asia/Hong_Kong")


def now_hkt():
    """Return current datetime in HKT."""
    return datetime.now(HKT)


def today_hkt():
    """Return today's date string in HKT (YYYY-MM-DD)."""
    return now_hkt().strftime("%Y-%m-%d")


def load_applications():
    """Load all applications from JSON. Returns list (empty if file missing)."""
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_applications(data):
    """Save applications list to JSON."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def generate_application_id():
    """Generate application_id from current timestamp (YYYYMMDDHHMMSS)."""
    return now_hkt().strftime("%Y%m%d%H%M%S")


def parse_add_input(user_input: str):
    """
    Parse "新增：company, position, salary, applied_date, deadline, notes"
    Returns dict with parsed fields or raises ValueError.
    """
    # Strip leading "新增：" or "add:" prefix
    s = user_input.strip()
    for prefix in ("新增：", "新增:", "add:", "add："):
        if s.lower().startswith(prefix.lower()):
            s = s[len(prefix):].strip()
            break

    parts = [p.strip() for p in s.split(",")]
    if len(parts) < 5:
        raise ValueError(
            f"需要至少 5 個欄位 (公司, 職位, 薪金, 申請日期, deadline)，"
            f"收到 {len(parts)} 個: {parts}"
        )

    company, position, salary, applied_date, deadline = parts[:5]
    notes = ",".join(parts[5:]).strip() if len(parts) > 5 else ""

    # Validate dates (YYYY-MM-DD)
    for label, val in [("申請日期", applied_date), ("deadline", deadline)]:
        try:
            datetime.strptime(val.strip(), "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"{label} 格式錯誤，要 YYYY-MM-DD: '{val}'")

    # Auto-generate follow_up_date = applied + 7 days
    applied_dt = datetime.strptime(applied_date.strip(), "%Y-%m-%d")
    follow_up = (applied_dt + timedelta(days=7)).strftime("%Y-%m-%d")

    return {
        "company": company,
        "position": position,
        "salary_range": salary,
        "applied_date": applied_date.strip(),
        "deadline": deadline.strip(),
        "notes": notes,
        "status": "applied",
        "follow_up_date": follow_up,
    }


def add_application(user_input: str):
    """Parse user input, build new entry, save, return new entry."""
    fields = parse_add_input(user_input)
    app_id = generate_application_id()
    entry = {
        "application_id": app_id,
        **fields,
        "created_at": now_hkt().isoformat(timespec="seconds"),
    }
    data = load_applications()
    data.append(entry)
    save_applications(data)
    return entry


def find_by_id(application_id: str):
    """Find application by ID, return (index, entry) or (None, None)."""
    data = load_applications()
    for i, e in enumerate(data):
        if e.get("application_id") == application_id:
            return i, e
    return None, None


def update_status(application_id: str, new_status: str, notes: str = ""):
    """
    Update application status + notes.
    Returns (old_entry, new_entry) or (None, None) if not found.
    """
    if new_status not in VALID_STATUSES:
        raise ValueError(
            f"status 必須係 {VALID_STATUSES} 之一，收到: '{new_status}'"
        )
    data = load_applications()
    idx, entry = find_by_id(application_id)
    if entry is None:
        return None, None
    old = dict(entry)
    entry["status"] = new_status
    if notes:
        # Append to existing notes
        existing = entry.get("notes", "")
        entry["notes"] = f"{existing} | {notes}" if existing else notes
    entry["updated_at"] = now_hkt().isoformat(timespec="seconds")
    data[idx] = entry
    save_applications(data)
    return old, entry


def send_telegram(text: str):
    """Send message to Saba's Telegram chat."""
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
