#!/usr/bin/env python3
"""
Job Application Tracker - Generate weekly dashboard
Cron: 0 21 * * 0  (every Sunday 21:00)
Pushes to Telegram.
"""
import sys
from datetime import datetime, timedelta
from collections import Counter
from lib import (
    load_applications,
    today_hkt,
    now_hkt,
    send_telegram,
)


ACTIVE_STATUSES = {"applied", "phone_screen", "interview"}


def compute_dashboard():
    """Compute dashboard stats + return markdown string."""
    data = load_applications()
    today = today_hkt()
    today_dt = datetime.strptime(today, "%Y-%m-%d")
    week_ago = (today_dt - timedelta(days=7)).strftime("%Y-%m-%d")

    # Status distribution
    status_counts = Counter(e.get("status", "unknown") for e in data)

    # This week new
    new_this_week = [e for e in data if e.get("applied_date", "") >= week_ago]

    # Active
    active = [e for e in data if e.get("status") in ACTIVE_STATUSES]

    # Replied = phone_screen + interview + offer
    replied = status_counts.get("phone_screen", 0) + status_counts.get("interview", 0) + status_counts.get("offer", 0)
    total = len(data)
    reply_rate = (replied / total * 100) if total > 0 else 0

    # Follow-up today
    follow_up_today = [
        e for e in data
        if e.get("follow_up_date", "") <= today
        and e.get("status") in {"applied", "phone_screen"}
    ]

    # 7-day trend (compare this week vs prev week)
    two_weeks_ago = (today_dt - timedelta(days=14)).strftime("%Y-%m-%d")
    prev_week = [
        e for e in data
        if two_weeks_ago <= e.get("applied_date", "") < week_ago
    ]
    if len(new_this_week) > len(prev_week):
        trend = f"📈 上升 ({len(prev_week)} → {len(new_this_week)})"
    elif len(new_this_week) < len(prev_week):
        trend = f"📉 下降 ({len(prev_week)} → {len(new_this_week)})"
    else:
        trend = f"➡️ 平 ({len(new_this_week)})"

    # Build markdown
    lines = []
    lines.append(f"**📊 Job Application Dashboard — {today}**")
    lines.append("")
    lines.append(f"- 總申請數：{total}")
    lines.append(f"- 本週新增：{len(new_this_week)}")
    lines.append(f"- 進行中：{len(active)} (applied + phone_screen + interview)")
    lines.append(f"- 回覆率：{reply_rate:.0f}% (phone_screen + interview + offer)")
    lines.append("")
    lines.append("**狀態分佈：**")
    for s in ["applied", "phone_screen", "interview", "offer", "rejected", "withdrawn"]:
        cnt = status_counts.get(s, 0)
        if cnt > 0:
            emoji = {"applied": "📨", "phone_screen": "📞", "interview": "🎤",
                     "offer": "🎉", "rejected": "❌", "withdrawn": "↩️"}.get(s, "•")
            lines.append(f"  {emoji} {s}: {cnt}")
    lines.append("")
    lines.append(f"**7 日趨勢：** {trend}")
    lines.append("")

    if follow_up_today:
        lines.append(f"**🔥 今日需要 follow-up ({len(follow_up_today)})：**")
        for e in follow_up_today[:5]:  # max 5
            lines.append(
                f"  • #{e.get('application_id')} {e.get('company')} — {e.get('position')}"
            )
        lines.append("")
    else:
        lines.append("✅ 今日冇 follow-up。")
        lines.append("")

    lines.append("---")
    lines.append("💪 單打獨鬥繼續 keep going。慢慢嚟，唔好急。")
    return "\n".join(lines)


def main():
    dashboard = compute_dashboard()
    print(dashboard)
    print()
    print("--- Sending to Telegram ---")
    result = send_telegram(dashboard)
    if result.get("ok"):
        print(f"✅ Sent. message_id = {result['result']['message_id']}")
    else:
        print(f"❌ Telegram send failed: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
