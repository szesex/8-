#!/usr/bin/env python3
"""
Targeted Job Alert - Send alert to Telegram
Cron: 0 0 * * 2,5 (週二、五 08:00 HKT)
"""
import sys
from datetime import datetime
from lib import (
    load_jobs,
    get_top_jobs,
    mark_notified,
    send_telegram,
    now_hkt,
    DEFAULT_KEYWORDS,
)


def build_alert(jobs):
    """Build markdown alert for top jobs."""
    today = now_hkt().strftime("%Y-%m-%d %a")
    if not jobs:
        text = (
            f"**🎯 Targeted Job Alert — {today}**\n\n"
            f"📭 暫時冇新 top-match 職位。\n\n"
            f"**提示：**\n"
            f"• 用 `add_job.py` 手動加新職位\n"
            f"• 或 search: https://hk.jobsdb.com/ ({', '.join(DEFAULT_KEYWORDS[:3])}...)\n"
            f"• Match 落 Skill 1 申請 (job_application_tracker)\n\n"
            f"---\n"
            f"💪 病好返就要 keep up 個 momentum。慢慢嚟。"
        )
        return text
    text = f"**🎯 Targeted Job Alert — {today}**\n\n"
    text += f"**Top {len(jobs)} 匹配職位：**\n"
    for j in jobs:
        score = j.get("match_score", 0)
        score_emoji = "🟢" if score >= 70 else "🟡" if score >= 40 else "🔴"
        text += f"\n{score_emoji} **[{score}] {j.get('company')}** — {j.get('title')}\n"
        if j.get("salary"):
            text += f"   💰 {j.get('salary')}\n"
        if j.get("matched_keywords"):
            text += f"   🔑 {', '.join(j.get('matched_keywords', []))}\n"
        text += f"   🔗 {j.get('url')}\n"
    text += (
        f"\n---\n"
        f"💡 申請後用 `Skill 1 (job_application_tracker)` 記低：\n"
        f"  `python3 ../../job_application_tracker/agent/add_application.py \"新增: {jobs[0].get('company')}, ..., deadline, notes\"`"
    )
    return text


def main():
    top = get_top_jobs(limit=5, min_score=30)
    alert = build_alert(top)
    print(alert)
    print()
    print("--- Sending to Telegram ---")
    result = send_telegram(alert)
    if result.get("ok"):
        print(f"✅ Sent. message_id = {result['result']['message_id']}")
        # Mark these as notified
        mark_notified([j["job_id"] for j in top])
        print(f"✓ Marked {len(top)} jobs as notified")
    else:
        print(f"❌ Telegram send failed: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
