---
name: weekly_review_streak
description: "每週日 20:00 HKT 自動 review — 追蹤 streak (study / 申請 / OpenClaw dev / MMA / 還債). 3 個下週建議. 單打獨鬥風格鼓勵. Part of 翻身計劃."
user-invocable: true
---

# Weekly Review + Streak Tracker (Stub)

_單打獨鬥翻身計劃 Skill 3 — 保持動力_

## 功能（MVP）
- 每週日 20:00 HKT 自動 review
- 追蹤 streak：
  - Exam study hours
  - Job applications submitted
  - OpenClaw development hours
  - Exercise / MMA training
  - Debt repayment amount
- 3 個下週建議
- 單打獨鬥風格鼓勵

## Cron
```
0 12 * * 0  # 週日 20:00 HKT (UTC 12:00)
```

## 用法
```bash
python3 run.py              # 推送 review
python3 run.py log          # log 本週數據 (互動)
```

## TODO
- [ ] 互動式 log prompt
- [ ] 趨勢圖
- [ ] 自動從 Skill 1 (job_tracker) 讀取本週申請數
- [ ] streak 自動計算

## Files
- `SKILL.md`
- `run.py` (MVP)
