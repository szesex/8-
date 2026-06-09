#!/usr/bin/env python3
"""
Weekly Review - Generate review
Cron: 0 12 * * 0 (週日 20:00 HKT)
"""
import sys
from lib import (
    get_week_key,
    get_week_start_end,
    get_week_entry,
    compute_streaks,
    get_rejected_count_this_month,
    send_telegram,
    now_hkt,
)


def build_review():
    """Build markdown review for current week."""
    week_key = get_week_key()
    monday, sunday = get_week_start_end()
    today = now_hkt().strftime("%Y-%m-%d")

    entry = get_week_entry(week_key)
    streaks, targets = compute_streaks()
    rejected = get_rejected_count_this_month()

    text = f"**📅 Weekly Review — {today} (Week {week_key.split('W')[1]})**\n"
    text += f"📆 Period: {monday} → {sunday}\n\n"

    if not entry:
        text += "⚠️ 本週未 log 數據。\n"
        text += "用 `python3 agent/log.py` 記錄。\n\n"
    else:
        # Stats
        text += "**本週數據：**\n"
        text += f"📚 Exam: {entry.get('exam_hours', 0)}h "
        text += f"{'✅' if entry.get('exam_hours', 0) >= targets['exam'] else '⚠️'}\n"
        text += f"📨 Job apps: {entry.get('job_apps', 0)} "
        text += f"{'✅' if entry.get('job_apps', 0) >= targets['job_apps'] else '⚠️'}\n"
        text += f"💻 OpenClaw: {entry.get('openclaw_hours', 0)}h "
        text += f"{'✅' if entry.get('openclaw_hours', 0) >= targets['openclaw'] else '⚠️'}\n"
        text += f"🥊 MMA: {entry.get('mma_hours', 0)}h "
        text += f"{'✅' if entry.get('mma_hours', 0) >= targets['mma'] else '⚠️'}\n"
        text += f"💰 Debt repaid: ${entry.get('debt_repaid', 0):.0f}\n"
        if entry.get("notes"):
            text += f"📌 備註: {entry.get('notes')}\n"
        text += "\n"

    # Streaks
    text += "**🔥 Streak 狀況：**\n"
    text += f"📚 Exam: {streaks['exam']} 週連續\n"
    text += f"📨 Job apps: {streaks['job_apps']} 週連續\n"
    text += f"💻 OpenClaw: {streaks['openclaw']} 週連續\n"
    text += f"🥊 MMA: {streaks['mma']} 週連續\n"
    text += "\n"

    # Highlights
    if entry:
        good = []
        improve = []
        if entry.get("exam_hours", 0) >= targets["exam"]:
            good.append(f"Exam 達標 {entry.get('exam_hours', 0)}h")
        else:
            improve.append(f"Exam 差 {targets['exam'] - entry.get('exam_hours', 0)}h 至達標")
        if entry.get("job_apps", 0) >= targets["job_apps"]:
            good.append(f"申請達標 {entry.get('job_apps', 0)} 個")
        else:
            improve.append(f"申請差 {targets['job_apps'] - entry.get('job_apps', 0)} 個至達標")
        if entry.get("openclaw_hours", 0) >= targets["openclaw"]:
            good.append(f"OpenClaw 達標 {entry.get('openclaw_hours', 0)}h")
        if entry.get("mma_hours", 0) >= targets["mma"]:
            good.append(f"MMA 達標 {entry.get('mma_hours', 0)}h")

        if good:
            text += f"**💪 做得好：**\n" + "\n".join(f"  • {g}" for g in good[:2]) + "\n\n"
        if improve:
            text += f"**🎯 要改進：**\n" + "\n".join(f"  • {i}" for i in improve[:1]) + "\n\n"

    if rejected > 0:
        text += f"❌ 本月 rejected: {rejected} 個申請。\n"
        text += "💡 Adjust keywords / 重新審視 resume 強項。\n\n"

    # 3 next-week suggestions
    text += "**📋 下週 3 個建議行動：**\n"
    text += "1. 至少 2 個新申請 (用 Skill 1 記低)\n"
    text += "2. Exam study 至少 5h (block calendar)\n"
    text += "3. MMA / 運動至少 2 次 (1 對 1 減壓)\n\n"

    text += "---\n"
    text += "💪 單打獨鬥，keep going。\n"
    text += "病好返就要 keep up 個 momentum。\n"
    text += "你係自己嘅最強後盾。"
    return text


def main():
    review = build_review()
    print(review)
    print()
    print("--- Sending to Telegram ---")
    result = send_telegram(review)
    if result.get("ok"):
        print(f"✅ Sent. message_id = {result['result']['message_id']}")
    else:
        print(f"❌ Telegram send failed: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
