"""
Targeted Job Alert - shared library
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# Paths
SKILL_DIR = Path("/home/node/.openclaw/workspace/skills/targeted_job_alert")
DATA_FILE = SKILL_DIR / "data" / "jobs.json"

# Telegram
TELEGRAM_BOT_TOKEN = "8775775652:AAEZCZo8aX0KCrQ0uHNZlIc8_bjTWVyoiw8"
TELEGRAM_CHAT_ID = "8475453959"

# Keywords (Saba's geotechnical / slope / AI focus)
DEFAULT_KEYWORDS = [
    "geotechnical",
    "slope remedial",
    "Assistant Engineer",
    "TCP",
    "Minor Works",
    "AI automation construction",
    "rock slope assessment",
    "tender preparation",
    "slope stability",
    "geotech",
]

HKT = ZoneInfo("Asia/Hong_Kong")


def now_hkt():
    return datetime.now(HKT)


def load_jobs():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        return []


def save_jobs(jobs):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(jobs, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def generate_job_id():
    return now_hkt().strftime("%Y%m%d%H%M%S")


def match_score(job, keywords=None):
    """
    Score 0-100 based on keyword overlap.
    Returns (score: int, matches: list[str]).
    """
    keywords = keywords or DEFAULT_KEYWORDS
    text = " ".join([
        job.get("title", ""),
        job.get("company", ""),
        job.get("description", ""),
    ]).lower()

    matches = [k for k in keywords if k.lower() in text]
    if not matches:
        return 0, []
    # Base score: 30 + 15 per match, capped at 100
    score = min(100, 30 + 15 * len(matches))
    # Boost if "AI" mentioned
    if "ai" in text or "automation" in text:
        score = min(100, score + 10)
    return score, matches


def add_job(company, title, url, salary="", description="", source="manual"):
    """Add a new job, return entry."""
    entry = {
        "job_id": generate_job_id(),
        "company": company,
        "title": title,
        "url": url,
        "salary": salary,
        "description": description,
        "source": source,
        "added_at": now_hkt().isoformat(timespec="seconds"),
        "notified": False,
    }
    score, matches = match_score(entry)
    entry["match_score"] = score
    entry["matched_keywords"] = matches

    jobs = load_jobs()
    # Dedup by URL
    if any(j.get("url") == url for j in jobs):
        return None, "URL already exists"
    jobs.append(entry)
    save_jobs(jobs)
    return entry, None


def is_seen(url):
    jobs = load_jobs()
    return any(j.get("url") == url for j in jobs)


def get_top_jobs(limit=5, min_score=30):
    """Get top scored, unnotified jobs."""
    jobs = load_jobs()
    seen_urls = {j.get("url") for j in jobs}
    candidates = [j for j in jobs if not j.get("notified") and j.get("match_score", 0) >= min_score]
    candidates.sort(key=lambda j: j.get("match_score", 0), reverse=True)
    return candidates[:limit]


def mark_notified(job_ids):
    jobs = load_jobs()
    for j in jobs:
        if j.get("job_id") in job_ids:
            j["notified"] = True
            j["notified_at"] = now_hkt().isoformat(timespec="seconds")
    save_jobs(jobs)


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
