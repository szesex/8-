#!/usr/bin/env python3
"""
Weekly Review - Log this week's stats
Usage:
    python3 log.py                                # Interactive mode
    python3 log.py <exam_h> <job_apps> <openclaw_h> <mma_h> <debt_repaid> [notes...]
    python3 log.py --auto                        # Auto-pull job_apps from Skill 1
"""
import sys
from lib import log_week


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--auto":
        # Auto: only fill job_apps from Skill 1, rest = 0
        entry = log_week({
            "exam_hours": 0,
            "job_apps": None,  # auto-fill
            "openclaw_hours": 0,
            "mma_hours": 0,
            "debt_repaid": 0,
            "notes": "auto log (manual fill later)",
        })
        print(f"✅ Auto-logged week {entry['week']}")
        print(f"   job_apps (auto from Skill 1): {entry['job_apps']}")
        print(f"   其他欄位: 0 (請用 log.py 手動 update)")
        return

    if len(sys.argv) < 2:
        # Interactive mode
        print("📝 Weekly Review — Interactive Log")
        print()
        try:
            exam = float(input("📚 Exam study hours: ") or 0)
            job_input = input("📨 Job applications (Enter = auto from Skill 1): ").strip()
            job_apps = int(job_input) if job_input else None
            openclaw = float(input("💻 OpenClaw dev hours: ") or 0)
            mma = float(input("🥊 MMA / exercise hours: ") or 0)
            debt = float(input("💰 Debt repaid (HKD): ") or 0)
            notes = input("📌 Notes (optional): ").strip()
        except (ValueError, EOFError):
            print("❌ Invalid input")
            sys.exit(1)
        entry = log_week({
            "exam_hours": exam,
            "job_apps": job_apps,
            "openclaw_hours": openclaw,
            "mma_hours": mma,
            "debt_repaid": debt,
            "notes": notes,
        })
    else:
        # CLI mode
        if len(sys.argv) < 6:
            print("用法: python3 log.py <exam_h> <job_apps> <openclaw_h> <mma_h> <debt_repaid> [notes...]")
            print("      python3 log.py --auto")
            sys.exit(1)
        try:
            entry = log_week({
                "exam_hours": float(sys.argv[1]),
                "job_apps": int(sys.argv[2]),
                "openclaw_hours": float(sys.argv[3]),
                "mma_hours": float(sys.argv[4]),
                "debt_repaid": float(sys.argv[5]),
                "notes": " ".join(sys.argv[6:]) if len(sys.argv) > 6 else "",
            })
        except ValueError as e:
            print(f"❌ Invalid number: {e}")
            sys.exit(1)

    print(f"\n✅ Logged week {entry['week']}:")
    for k, v in entry.items():
        if k not in ("week", "logged_at"):
            print(f"   {k}: {v}")


if __name__ == "__main__":
    main()
