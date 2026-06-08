---
name: job_application_tracker
description: "Track job applications — add, update status, query, weekly dashboard. Auto-pushes Telegram summary every Sunday 21:00 HKT. Part of 單打獨鬥翻身計劃."
user-invocable: true
---

# Job Application Tracker

_單打獨鬥翻身計劃 Skill 1 — 組織化 + 數據驅動 job search_

## 功能

- **新增申請** — 一句 command 記錄晒公司/職位/薪金/deadline
- **更新狀態** — applied / phone_screen / interview / offer / rejected / withdrawn
- **週日 Dashboard** — 自動 cron 21:00 HKT 推送 Telegram
- **查詢** — dashboard / follow-up / active / rejected / 全部

## 用法

```bash
# 新增
python3 agent/add_application.py "新增: ABC Engineering, Assistant Engineer (Geotechnical), 18-22k, 2026-06-10, 2026-06-30, 有 slope remedial 經驗"

# 更新狀態
python3 agent/update_status.py 20260609123456 interview "明天 10am 電話面試"

# 查詢
python3 agent/query.py dashboard
python3 agent/query.py status 20260609123456
python3 agent/query.py follow_up_today
python3 agent/query.py active
python3 agent/query.py rejected_recent 30
python3 agent/query.py all

# 觸發 dashboard (test)
python3 agent/generate_dashboard.py
```

## Cron 設定

```bash
# 每週日 21:00 HKT (UTC 13:00) 推送 dashboard
0 13 * * 0 /usr/bin/python3 /home/node/.openclaw/workspace/skills/job_application_tracker/agent/generate_dashboard.py >> /home/node/.openclaw/workspace/logs/job_tracker_dashboard.log 2>&1
```

## 數據結構

`data/applications.json`:
```json
[
  {
    "application_id": "20260609123456",
    "company": "ABC Engineering",
    "position": "Assistant Engineer (Geotechnical)",
    "salary_range": "18-22k",
    "applied_date": "2026-06-10",
    "deadline": "2026-06-30",
    "status": "applied",
    "follow_up_date": "2026-06-17",
    "notes": "有 slope remedial 經驗",
    "created_at": "2026-06-09T12:34:56+08:00",
    "updated_at": "2026-06-09T14:00:00+08:00"
  }
]
```

## Status 規則

| Status | 意思 | 跟進 default |
|--------|------|-------------|
| `applied` | 已申請 | +7 日 follow-up |
| `phone_screen` | 電話面試 | +3 日 follow-up |
| `interview` | 面試 | +1 日 follow-up |
| `offer` | 獲 offer | - |
| `rejected` | 被拒 | - |
| `withdrawn` | 自己撤回 | - |

## 提示

- `follow_up_date` 只 auto-set 喺新增時，更新 status 唔會 auto-adjust
- 如果想改 follow_up_date，手動 edit `data/applications.json`
- Dashboard 默認 push 去 Saba Telegram (chat_id 8475453959)
