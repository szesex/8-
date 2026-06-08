---
name: side_income_report
description: "Side Income 月報 — 每月 1 號 10:00 HKT 自動生成報告 (woodworking / freelance / 其他). Part of 翻身計劃."
user-invocable: true
---

# Monthly Side Income Report (Stub)

_單打獨鬥翻身計劃 Skill 5_

## 功能（MVP）
- 記錄 side income (woodworking PT @ 活木生活, freelance, 其他)
- 每月 1 號 10:00 HKT 自動生成上個月報告
- 比較、還債金額

## Cron
```
0 2 1 * *  # 每月 1 號 10:00 HKT (UTC 02:00)
```

## 用法
```bash
python3 run.py                  # 推送本月報告
python3 run.py add AMOUNT SOURCE  # 加新 entry
```

## Files
- `SKILL.md`
- `run.py` (MVP)
