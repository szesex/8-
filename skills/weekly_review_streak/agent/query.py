#!/usr/bin/env python3
"""
Weekly Review - Query history
Usage:
    python3 query.py                       # Show last 4 weeks
    python3 query.py trend                 # 4-week trend table
    python3 query.py streaks               # Current streak status
    python3 query.py all                   # All weeks
"""
import sys
from lib import load_weeks, compute_streaks


def show_weeks(weeks, limit=None):
    if limit:
        weeks = weeks[-limit:]
    if not weeks:
        print("📭 No data. 用 log.py 開始記錄。")
        return
    for w in weeks:
        print(f"**{w.get('week')}**")
        print(f"  📚 Exam: {w.get('exam_hours', 0)}h")
        print(f"  📨 Job apps: {w.get('job_apps', 0)}")
        print(f"  💻 OpenClaw: {w.get('openclaw_hours', 0)}h")
        print(f"  🥊 MMA: {w.get('mma_hours', 0)}h")
        print(f"  💰 Debt: ${w.get('debt_repaid', 0):.0f}")
        if w.get("notes"):
            print(f"  📌 {w.get('notes')}")
        print()


def trend_table(weeks, limit=4):
    weeks = weeks[-limit:] if len(weeks) > limit else weeks
    if not weeks:
        print("📭 No data")
        return
    print(f"{'Week':<10} {'Exam':>6} {'Jobs':>6} {'OC':>6} {'MMA':>6} {'Debt':>8}")
    print("-" * 50)
    for w in weeks:
        print(
            f"{w.get('week'):<10} "
            f"{w.get('exam_hours', 0):>6.1f} "
            f"{w.get('job_apps', 0):>6} "
            f"{w.get('openclaw_hours', 0):>6.1f} "
            f"{w.get('mma_hours', 0):>6.1f} "
            f"${w.get('debt_repaid', 0):>7.0f}"
        )


def show_streaks():
    streaks, targets = compute_streaks()
    print("**🔥 Current Streaks (連續達標週數):**\n")
    labels = {
        "exam": ("📚 Exam", targets["exam"]),
        "job_apps": ("📨 Job apps", targets["job_apps"]),
        "openclaw": ("💻 OpenClaw", targets["openclaw"]),
        "mma": ("🥊 MMA", targets["mma"]),
    }
    for k, (label, target) in labels.items():
        s = streaks[k]
        emoji = "🔥" if s >= 3 else "🟡" if s >= 1 else "❄️"
        print(f"  {emoji} {label}: {s} 週 (目標: {target}h/{target} 個)")


def main():
    weeks = load_weeks()
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "recent"

    if cmd in ("recent", "latest", "list"):
        show_weeks(weeks, limit=4)
    elif cmd == "trend":
        trend_table(weeks)
    elif cmd == "streaks":
        show_streaks()
    elif cmd == "all":
        show_weeks(weeks)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
