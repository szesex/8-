---
name: targeted_job_alert
description: "自動搵工 — 根據 geotechnical/slope keywords 搜尋職位 (MVP stub). Cron 週二+五 08:00 HKT. Part of 單打獨鬥翻身計劃."
user-invocable: true
---

# Targeted Job Alert (Stub)

_單打獨鬥翻身計劃 Skill 2 — 自動搵工_

## 功能（MVP）
- 根據設定關鍵字 list 標記已知職位來源
- 每週二、五 08:00 HKT 自動推送提示
- 未來：scrape JobsDB / CTgoodjobs / LinkedIn

## 關鍵字
geotechnical engineer, slope stability, Assistant Engineer, TCP, Minor Works Class 1, rock slope, tender preparation

## Cron
```
0 0 * * 2,5  # 週二、五 08:00 HKT (UTC 00:00)
```

## 用法（MVP）
```bash
python3 run.py              # 推送今日提示
python3 run.py add URL      # 手動加職位 link
```

## TODO
- [ ] 接入真實 jobs API (JobsDB, CTgoodjobs, LinkedIn)
- [ ] dedup 已推介
- [ ] 智能匹配 (skills 評分)

## Files
- `SKILL.md` (本檔)
- `run.py` (MVP script — 暫時只 push 提示)
