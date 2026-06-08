---
name: networking_followup
description: "Networking follow-up 追蹤 — 每日 09:00 HKT 提醒要 follow-up 嘅人 + 生成 message 草稿. Part of 翻身計劃."
user-invocable: true
---

# Networking Follow-up Reminder (Stub)

_單打獨鬥翻身計劃 Skill 4_

## 功能（MVP）
- 記錄 networking 過嘅人
- 每日 09:00 HKT 自動提醒要 follow-up
- 自動生成 LinkedIn / email 草稿

## Cron
```
0 1 * * *  # 每日 09:00 HKT (UTC 01:00)
```

## 用法
```bash
python3 run.py                          # 推送今日提醒
python3 run.py add NAME COMPANY DATE    # 加新 contact
```

## Files
- `SKILL.md`
- `run.py` (MVP)
