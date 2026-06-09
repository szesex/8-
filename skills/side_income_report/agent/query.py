#!/usr/bin/env python3
"""
Side Income - Query
Usage:
    python3 query.py                       # Current month
    python3 query.py 2026-05               # Specific month
    python3 query.py ytd                   # Year-to-date
    python3 query.py all                   # All entries
    python3 query.py sources               # All unique sources
"""
import sys
from lib import (
    load_income, get_month_data, aggregate_by_source, compute_stats,
    this_month, now_hkt
)


def show(entries, header=""):
    if not entries:
        print("📭 No data.")
        return
    if header:
        print(header)
    total, hours, rate = compute_stats(entries)
    by_source = aggregate_by_source(entries)
    print(f"  Entries: {len(entries)}  Total: ${total:.0f}  Hours: {hours:.1f}  Rate: ${rate:.0f}/h")
    print()
    print("  By source:")
    for src, amt in sorted(by_source.items(), key=lambda x: -x[1]):
        pct = amt / total * 100 if total > 0 else 0
        print(f"    {src}: ${amt:.0f} ({pct:.0f}%)")
    print()
    print("  Recent entries:")
    for e in sorted(entries, key=lambda x: x.get("date", ""), reverse=True)[:10]:
        notes = f" — {e.get('notes')}" if e.get("notes") else ""
        print(f"    {e.get('date')} | ${e.get('amount'):.0f} | {e.get('source')} | {e.get('hours')}h{notes}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "current"

    if cmd == "current":
        m = this_month()
        show(get_month_data(m), f"💰 Current month ({m}):")
    elif cmd == "ytd":
        year = now_hkt().strftime("%Y")
        all_data = load_income()
        ytd = [e for e in all_data if e.get("date", "").startswith(year)]
        show(ytd, f"💰 Year-to-Date ({year}):")
    elif cmd == "all":
        all_data = load_income()
        show(all_data, f"💰 All entries ({len(all_data)}):")
    elif cmd == "sources":
        all_data = load_income()
        sources = sorted({e.get("source", "?") for e in all_data})
        print(f"📋 Known sources ({len(sources)}):")
        for s in sources:
            print(f"  • {s}")
    else:
        # Specific month
        show(get_month_data(cmd), f"💰 {cmd}:")


if __name__ == "__main__":
    main()
