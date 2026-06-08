---
name: targeted_job_alert
description: "自動搵工 — 根據 geotechnical/slope/AI keywords 評分職位匹配度 (0-100)。Cron 週二+五 08:00 HKT 自動推送 Top 5 職位。Part of 單打獨鬥翻身計劃."
user-invocable: true
---

# Targeted Job Alert

_單打獨鬥翻身計劃 Skill 2 — 自動搵工 + 智能匹配_

## 功能

- **手動加職位** — `add_job.py <公司> <職位> <URL> [salary] [description]`
- **搜尋職位** — `search_jobs.py [keyword]`，按 match score 排序
- **Match 評分** — 0-100 分，根據 10 個 keywords 重疊度 + AI/automation boost
- **自動推送** — Cron 週二、五 08:00 HKT 推送 Top 5 匹配職位到 Telegram
- **Dedup** — 自動跳過已見 URL
- **一鍵跳 Skill 1** — Alert 提示用戶用 `job_application_tracker` 記低申請

## 用法

```bash
# 加職位
python3 agent/add_job.py "AECOM" "Assistant Engineer (Geotech)" "https://..." "20-25k" "slope + AI"

# 搜尋
python3 agent/search_jobs.py
python3 agent/search_jobs.py slope

# 即刻推送 alert
python3 agent/send_alert.py

# 簡化模式 (預設 stub)
python3 run.py
```

## Match Score 規則

| 分數 | Emoji | 意思 |
|------|-------|------|
| 70+ | 🟢 | 高度匹配 — 強烈建議申請 |
| 40-69 | 🟡 | 中度匹配 — 可以考慮 |
| <40 | 🔴 | 低度匹配 — 唔好嘥時間 |

**計分公式：**
- Base: 30 + 15 × matched keywords (cap 100)
- AI/automation mention: +10 boost

**10 個 keywords:**
geotechnical, slope remedial, Assistant Engineer, TCP, Minor Works, AI automation construction, rock slope assessment, tender preparation, slope stability, geotech

## Cron

```
0 0 * * 2,5  /usr/bin/python3 /home/node/.openclaw/workspace/skills/targeted_job_alert/agent/send_alert.py
# 週二、五 08:00 HKT (UTC 00:00)
```

## 數據結構

`data/jobs.json`:
```json
[
  {
    "job_id": "20260608120001",
    "company": "AECOM Asia",
    "title": "Assistant Engineer (Geotechnical)",
    "url": "https://...",
    "salary": "20-25k",
    "description": "Slope remedial + AI",
    "source": "manual",
    "added_at": "2026-06-08T12:00:00+08:00",
    "notified": false,
    "match_score": 85,
    "matched_keywords": ["geotechnical", "slope remedial", ...]
  }
]
```

## TODO
- [ ] 接入真實 jobs API (JobsDB scrape / LinkedIn / Indeed)
- [ ] 自動 dedup + cross-reference 已申請
- [ ] Telegram inline command (`/jobs`)
- [ ] 週日 weekly summary 整合去 Skill 3 review
