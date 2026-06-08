#!/usr/bin/env python3
"""
Targeted Job Alert - Search jobs
Currently a stub that loads from data/jobs.json (manual entries).
TODO: integrate with real API (JobsDB / LinkedIn / Indeed).
"""
import sys
import json
from lib import load_jobs, match_score, DEFAULT_KEYWORDS


def search_keyword(keyword):
    """Return jobs that match the given keyword (case-insensitive)."""
    jobs = load_jobs()
    matches = []
    for j in jobs:
        text = " ".join([j.get("title", ""), j.get("company", ""), j.get("description", "")]).lower()
        if keyword.lower() in text:
            matches.append(j)
    return matches


def search_all():
    """Show all jobs with match scores."""
    jobs = load_jobs()
    if not jobs:
        print("📭 No jobs in database. Use add_job.py to add some.")
        return
    print(f"📋 {len(jobs)} jobs total:\n")
    for j in sorted(jobs, key=lambda x: x.get("match_score", 0), reverse=True):
        score = j.get("match_score", 0)
        score_emoji = "🟢" if score >= 70 else "🟡" if score >= 40 else "🔴"
        print(f"{score_emoji} [{score}] {j.get('company')} — {j.get('title')}")
        if j.get("salary"):
            print(f"    💰 {j.get('salary')}")
        if j.get("matched_keywords"):
            print(f"    🔑 {', '.join(j.get('matched_keywords', []))}")
        print(f"    🔗 {j.get('url')}")
        if j.get("notified"):
            print(f"    ✓ Notified")
        print()


def main():
    if len(sys.argv) < 2:
        search_all()
        return
    keyword = sys.argv[1]
    matches = search_keyword(keyword)
    print(f"🔍 {len(matches)} jobs matching '{keyword}':\n")
    for j in matches:
        print(f"  • {j.get('company')} — {j.get('title')}")
        print(f"    {j.get('url')}")


if __name__ == "__main__":
    main()
