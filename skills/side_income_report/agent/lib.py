"""
Side Income Report - shared library
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

# Paths
SKILL_DIR = Path("/home/node/.openclaw/workspace/skills/side_income_report")
DATA_FILE = SKILL_DIR / "data" / "income.json"

# Telegram
TELEGRAM_BOT_TOKEN = "8775775652:AAEZCZo8aX0KCrQ0uHNZlIc8_bjTWVyoiw8"
TELEGRAM_CHAT_ID = "8475453959"

HKT = ZoneInfo("Asia/Hong_Kong")


def now_hkt():
    return datetime.now(HKT)


def this_month():
    return now_hkt().strftime("%Y-%m")


def last_month():
    last = now_hkt().replace(day=1) - timedelta(days=1)
    return last.strftime("%Y-%m")


def load_income():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        return []


def save_income(income):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(income, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def add_income(amount, source, date=None, hours=0, notes=""):
    """Add new income entry."""
    date = date or now_hkt().strftime("%Y-%m-%d")
    entry = {
        "entry_id": now_hkt().strftime("%Y%m%d%H%M%S"),
        "date": date,
        "amount": float(amount),
        "source": source,
        "hours": float(hours),
        "notes": notes,
        "added_at": now_hkt().isoformat(timespec="seconds"),
    }
    income = load_income()
    income.append(entry)
    save_income(income)
    return entry


def get_month_data(month=None):
    """Get all income entries for a given month (YYYY-MM)."""
    month = month or this_month()
    income = load_income()
    return [e for e in income if e.get("date", "").startswith(month)]


def aggregate_by_source(entries):
    """Sum amounts grouped by source."""
    out = {}
    for e in entries:
        src = e.get("source", "unknown")
        out[src] = out.get(src, 0) + e.get("amount", 0)
    return out


def compute_stats(entries):
    """Compute total, hours, hourly rate."""
    total = sum(e.get("amount", 0) for e in entries)
    hours = sum(e.get("hours", 0) for e in entries)
    rate = total / hours if hours > 0 else 0
    return total, hours, rate


def compare_to_last_month(current_month=None):
    """Compare current month to last month. Returns dict with delta."""
    current_month = current_month or this_month()
    curr_entries = get_month_data(current_month)
    last_entries = get_month_data(last_month())

    curr_total, _, _ = compute_stats(curr_entries)
    last_total, _, _ = compute_stats(last_entries)

    if last_total > 0:
        delta_pct = ((curr_total - last_total) / last_total) * 100
    else:
        delta_pct = 100 if curr_total > 0 else 0

    return {
        "current_total": curr_total,
        "last_total": last_total,
        "delta_pct": delta_pct,
        "current_entries": len(curr_entries),
        "last_entries": len(last_entries),
    }


def debt_split(total):
    """Suggest 50/30/20 split: debt, self-invest, buffer."""
    return {
        "debt": total * 0.5,
        "self_invest": total * 0.3,
        "buffer": total * 0.2,
    }


def generate_recommendations(by_source, total, hours, rate):
    """Generate recommendations based on data."""
    recs = []
    # Source concentration
    if by_source:
        top_src = max(by_source, key=by_source.get)
        top_pct = by_source[top_src] / total * 100 if total > 0 else 0
        if top_pct > 80:
            recs.append(f"⚠️ {top_src} 佔 {top_pct:.0f}%，過度集中。考慮加多一個 source 分散風險。")
        if top_pct < 60:
            recs.append(f"💡 {top_src} 主力 ({top_pct:.0f}%)，可以試下加價 10-20% 測試市場。")
    # Hourly rate
    if rate > 0 and rate < 100:
        recs.append(f"💰 現時時薪 ${rate:.0f} 偏低。可考慮加價或轉更高 value 工作。")
    elif rate >= 150:
        recs.append(f"🔥 現時時薪 ${rate:.0f} 唔錯！Keep 住呢個 rate。")
    # Hours
    if hours < 10:
        recs.append(f"⏰ 本月工時 {hours:.1f}h 偏少。可嘗試搵多啲 freelance 機會。")
    elif hours > 60:
        recs.append(f"⚠️ 本月工時 {hours:.1f}h 過多，小心 burnout。")
    return recs


def build_report():
    """Build monthly report markdown."""
    this = this_month()
    last = last_month()

    this_entries = get_month_data(this)
    last_entries = get_month_data(last)
    by_source = aggregate_by_source(this_entries)
    total, hours, rate = compute_stats(this_entries)
    cmp = compare_to_last_month(this)
    split = debt_split(total)
    recs = generate_recommendations(by_source, total, hours, rate)

    text = f"**💰 Side Income Report — {this}**\n\n"
    text += f"**本月總收入：** ${total:.0f}\n"
    text += f"**Entries：** {len(this_entries)}  |  **工時：** {hours:.1f}h  |  **時薪：** ${rate:.0f}/h\n\n"

    if by_source:
        text += "**By source：**\n"
        for src, amt in sorted(by_source.items(), key=lambda x: -x[1]):
            pct = amt / total * 100 if total > 0 else 0
            text += f"  • {src}: ${amt:.0f} ({pct:.0f}%)\n"
        text += "\n"
    else:
        text += "本月未記錄任何 income。\n\n"

    # Comparison
    if cmp["last_total"] > 0:
        delta_emoji = "📈" if cmp["delta_pct"] > 0 else "📉" if cmp["delta_pct"] < 0 else "➡️"
        text += f"**比較上個月 ({last})：** {delta_emoji} {cmp['delta_pct']:+.1f}%\n"
        text += f"  (${cmp['last_total']:.0f} → ${cmp['current_total']:.0f})\n\n"
    elif cmp["current_total"] > 0:
        text += f"🆕 上個月冇記錄，呢個係新開始！\n\n"

    # Recommendations
    if recs:
        text += "**💡 建議：**\n"
        for r in recs:
            text += f"  {r}\n"
        text += "\n"

    # Debt split
    if total > 0:
        text += f"**💸 還債金額建議 (50/30/20)：**\n"
        text += f"  • 還債：${split['debt']:.0f} (50%)\n"
        text += f"  • 投資自己：${split['self_invest']:.0f} (30%)\n"
        text += f"  • 緩衝：${split['buffer']:.0f} (20%)\n\n"

    # YTD
    ytd_total = sum(
        e.get("amount", 0)
        for e in load_income()
        if e.get("date", "").startswith(now_hkt().strftime("%Y"))
    )
    text += f"**📊 Year-to-Date：** ${ytd_total:.0f}\n"
    text += "\n---\n"
    text += "💪 Side income 慢慢儲，都係單打獨鬥嘅底氣。\n"
    text += "🤒 病好咗第一週 keep 住記低。"
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
