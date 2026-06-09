"""
Weekly Review + Streak Tracker - shared library
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

# Paths
SKILL_DIR = Path("/home/node/.openclaw/workspace/skills/weekly_review_streak")
DATA_FILE = SKILL_DIR / "data" / "weeks.json"
JOB_DATA_FILE = Path("/home/node/.openclaw/workspace/skills/job_application_tracker/data/applications.json")

# Telegram
TELEGRAM_BOT_TOKEN = "8775775652:AAEZCZo8aX0KCrQ0uHNZlIc8_bjTWVyoiw8"
TELEGRAM_CHAT_ID = "8475453959"

HKT = ZoneInfo("Asia/Hong_Kong")


def now_hkt():
    return datetime.now(HKT)


def get_week_key(dt=None):
    """Get ISO week key like '2026-W23'."""
    dt = dt or now_hkt()
    year, week, _ = dt.isocalendar()
    return f"{year}-W{week:02d}"


def get_week_start_end(dt=None):
    """Get Monday-Sunday of the current week."""
    dt = dt or now_hkt()
    monday = dt - timedelta(days=dt.weekday())
    sunday = monday + timedelta(days=6)
    return monday.date(), sunday.date()


def load_weeks():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        return []


def save_weeks(weeks):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(weeks, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def get_week_entry(week_key=None):
    """Get the entry for a specific week, or None."""
    week_key = week_key or get_week_key()
    weeks = load_weeks()
    for w in weeks:
        if w.get("week") == week_key:
            return w
    return None


def log_week(stats):
    """
    Log a week's stats. stats dict with keys:
    - exam_hours (float)
    - job_apps (int)  [auto-filled from Skill 1 if None]
    - openclaw_hours (float)
    - mma_hours (float)
    - debt_repaid (float HKD)
    - notes (str)
    Returns the week entry.
    """
    week_key = get_week_key()
    weeks = load_weeks()

    # Auto-fill job_apps from Skill 1 if not provided
    if stats.get("job_apps") is None:
        stats["job_apps"] = get_job_app_count_this_week()

    entry = {
        "week": week_key,
        "exam_hours": stats.get("exam_hours", 0),
        "job_apps": stats.get("job_apps", 0),
        "openclaw_hours": stats.get("openclaw_hours", 0),
        "mma_hours": stats.get("mma_hours", 0),
        "debt_repaid": stats.get("debt_repaid", 0),
        "notes": stats.get("notes", ""),
        "logged_at": now_hkt().isoformat(timespec="seconds"),
    }
    # Remove existing
    weeks = [w for w in weeks if w.get("week") != week_key]
    weeks.append(entry)
    weeks.sort(key=lambda w: w.get("week", ""))
    save_weeks(weeks)
    return entry


def get_job_app_count_this_week():
    """Count job applications this week (auto from Skill 1)."""
    if not JOB_DATA_FILE.exists():
        return 0
    try:
        data = json.loads(JOB_DATA_FILE.read_text(encoding="utf-8"))
        today = now_hkt()
        week_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        return sum(1 for e in data if e.get("applied_date", "") >= week_ago)
    except:
        return 0


def get_rejected_count_this_month():
    """Count rejected applications this month."""
    if not JOB_DATA_FILE.exists():
        return 0
    try:
        data = json.loads(JOB_DATA_FILE.read_text(encoding="utf-8"))
        today = now_hkt()
        month_start = today.replace(day=1).strftime("%Y-%m-%d")
        return sum(1 for e in data if e.get("status") == "rejected" and e.get("applied_date", "") >= month_start)
    except:
        return 0


def compute_streaks():
    """
    Compute consecutive weeks meeting target.
    Targets: exam_hours >= 5, job_apps >= 2, openclaw_hours >= 3, mma_hours >= 2
    """
    targets = {
        "exam": 5,
        "job_apps": 2,
        "openclaw": 3,
        "mma": 2,
    }
    weeks = load_weeks()
    streaks = {k: 0 for k in targets}
    for w in reversed(weeks):
        if w.get("exam_hours", 0) >= targets["exam"]:
            streaks["exam"] += 1
        else:
            streaks["exam"] = 0
        if w.get("job_apps", 0) >= targets["job_apps"]:
            streaks["job_apps"] += 1
        else:
            streaks["job_apps"] = 0
        if w.get("openclaw_hours", 0) >= targets["openclaw"]:
            streaks["openclaw"] += 1
        else:
            streaks["openclaw"] = 0
        if w.get("mma_hours", 0) >= targets["mma"]:
            streaks["mma"] += 1
        else:
            streaks["mma"] = 0
    return streaks, targets


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
