#!/usr/bin/env python3
"""
Targeted Job Alert - Add a job manually
Usage:
    python3 add_job.py "ABC Engineering" "Assistant Engineer (Geotechnical)" "https://..." "20-25k" "slope remedial + AI work"
"""
import sys
from lib import add_job


def main():
    if len(sys.argv) < 4:
        print("用法: python3 add_job.py <company> <title> <url> [salary] [description]")
        print("範例: python3 add_job.py \"AECOM\" \"Assistant Engineer (Geotech)\" \"https://jobsdb.com/123\" \"20-25k\" \"slope remedial\"")
        sys.exit(1)
    company = sys.argv[1]
    title = sys.argv[2]
    url = sys.argv[3]
    salary = sys.argv[4] if len(sys.argv) > 4 else ""
    description = " ".join(sys.argv[5:]) if len(sys.argv) > 5 else ""
    entry, err = add_job(company, title, url, salary, description)
    if err:
        print(f"❌ {err}")
        sys.exit(1)
    print(f"✅ Added #{entry['job_id']} (match: {entry['match_score']})")
    print(f"  Company: {entry['company']}")
    print(f"  Title:   {entry['title']}")
    print(f"  URL:     {entry['url']}")
    if entry.get("matched_keywords"):
        print(f"  Matched: {', '.join(entry['matched_keywords'])}")


if __name__ == "__main__":
    main()
