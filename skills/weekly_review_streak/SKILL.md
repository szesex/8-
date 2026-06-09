---
name: weekly_review_streak
description: "每週日 20:00 HKT 自動 review — 追蹤 streak (exam 5h / job apps 2 / OpenClaw 3h / MMA 2h / debt repaid). 3 個下週建議. 單打獨鬥風格鼓勵. Part of 翻身計劃."
user-invocable: true
---

# Weekly Review + Streak Tracker

_單打獨鬥翻身計劃 Skill 3 — 保持動力 + 數據驅動_

## 功能

- **Log 數據** — CLI 輸入 / 互動 prompt / `--auto` (auto-pull job_apps from Skill 1)
- **Generate review** — 週日 20:00 HKT 自動 cron 推送 Telegram
- **Streak 追蹤** — 連續達標週數 (target: exam 5h / job 2 / OC 3h / MMA 2h)
- **Trend table** — 4-week 比較
- **3 個下週建議** — 自動生成
- **Rejected counter** — 本月 rejected 申請數 (from Skill 1)

## 用法

```bash
# Log (CLI mode)
python3 agent/log.py <exam_h> <job_apps> <openclaw_h> <mma_h> <debt_repaid> [notes...]

# Log (interactive)
python3 agent/log.py

# Log (auto: only job_apps from Skill 1)
python3 agent/log.py --auto

# Generate review (manual)
python3 agent/generate_review.py

# Query
python3 agent/query.py              # 最近 4 週
python3 agent/query.py trend        # 4-week 表格
python3 agent/query.py streaks      # 連續 streak 狀態
python3 agent/query.py all          # 全部
```

## Cron

```
0 12 * * 0  /usr/bin/python3 /home/node/.openclaw/workspace/skills/weekly_review_streak/agent/generate_review.py
# 週日 20:00 HKT (UTC 12:00)
```

## Streak 規則

| Metric | Target |
|--------|--------|
| 📚 Exam study | ≥ 5 hrs/week |
| 📨 Job apps | ≥ 2 submitted/week |
| 💻 OpenClaw dev | ≥ 3 hrs/week |
| 🥊 MMA / exercise | ≥ 2 hrs/week |

## 數據結構

`data/weeks.json`:
```json
[
  {
    "week": "2026-W23",
    "exam_hours": 6,
    "job_apps": 3,
    "openclaw_hours": 5,
    "mma_hours": 2,
    "debt_repaid": 3000,
    "notes": "...",
    "logged_at": "2026-06-08T20:00:00+08:00"
  }
]
```

## 整合

- **Skill 1 (job_application_tracker)** — auto-pull 本週申請數
- **未來** — 整合 Skill 5 (side_income) debt repaid

## TODO
- [ ] Telegram inline command (`/review`)
- [ ] 自動 generate review 用 OpenClaw model
- [ ] 圖表 (monthly heatmap)
