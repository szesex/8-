---
name: side_income_report
description: "Side Income 月報 — 每月 1 號 10:00 HKT 自動生成報告 (woodworking / freelance / 其他). 包括 by-source 細分 + 比較上個月 + 50/30/20 還債建議 + YTD. Part of 翻身計劃."
user-invocable: true
---

# Monthly Side Income Report

_單打獨鬥翻身計劃 Skill 5 — 還債 + 投資自己_

## 功能

- **Add income** — `add_income.py <amount> <source> [date] [hours] [notes...]`
- **Monthly report** — Cron 每月 1 號 10:00 HKT 推送 Telegram
  - 本月總收入 + 工時 + 時薪
  - By source 細分 + 百分比
  - 比較上個月 (delta %)
  - 💡 智能建議 (concentration / rate / hours)
  - 50/30/20 還債分配
  - YTD 累計
- **Query** — current / ytd / all / specific month / sources

## 用法

```bash
# 加 income
python3 agent/add_income.py 800 "活木生活木工" "2026-06-09" 8 "整 layer 板"
python3 agent/add_income.py 1500 "Freelance - Resume" "2026-06-09" 3 "幫同事改"

# 即刻推送本月 report
python3 agent/generate_monthly_report.py

# Query
python3 agent/query.py              # 本月
python3 agent/query.py 2026-05      # 指定月份
python3 agent/query.py ytd          # YTD
python3 agent/query.py all          # 全部
python3 agent/query.py sources      # 所有 source
```

## Cron

```
0 2 1 * *  /usr/bin/python3 /home/node/.openclaw/workspace/skills/side_income_report/agent/generate_monthly_report.py
# 每月 1 號 10:00 HKT (UTC 02:00)
```

## 50/30/20 還債規則

| Bucket | % | 用法 |
|--------|---|------|
| 還債 | 50% | 加速清 debt |
| 投資自己 | 30% | Exam / 工具 / 課程 |
| 緩衝 | 20% | 應急 / 獎勵自己 |

## 智能建議邏輯

- **Source 集中度 >80%** → 建議加新 source 分散風險
- **Source 集中度 <60%** → 建議加價 10-20%
- **時薪 <$100** → 偏低，可加價
- **時薪 ≥$150** → 唔錯，keep
- **工時 <10h** → 太少，搵多啲機會
- **工時 >60h** → 太多，小心 burnout

## 數據結構

`data/income.json`:
```json
[
  {
    "entry_id": "20260520100000",
    "date": "2026-05-20",
    "amount": 800,
    "source": "活木生活木工",
    "hours": 8,
    "notes": "整 layer 板",
    "added_at": "2026-05-20T10:00:00+08:00"
  }
]
```

## 整合

- **Skill 3 (weekly_review_streak)** — 未來 debt_repaid auto-pull from 此 skill

## TODO
- [ ] Telegram inline command (`/income`)
- [ ] 自動 import CSV (bank statement)
- [ ] 圖表 (monthly bar chart)
- [ ] 預測功能 (基於過往 3 個月 trend)
