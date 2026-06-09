---
name: networking_followup
description: "Networking follow-up 追蹤 — 每日 09:00 HKT 提醒要 follow-up 嘅人 + auto-generate LinkedIn/email 草稿. Part of 翻身計劃."
user-invocable: true
---

# Networking Follow-up Reminder

_單打獨鬥翻身計劃 Skill 4 — Networking accountability_

## 功能

- **Add contact** — `add_contact.py <name> <company> [date] [follow_up] [topic] [next] [channel]`
- **Auto-generate 草稿** — LinkedIn / email 模板 (first follow-up vs subsequent)
- **Daily reminder** — Cron 每日 09:00 HKT 推送 due contacts 到 Telegram
- **Mark actions** — `mark.py followed_up <id>` (+7d) | `mark.py done <id>`
- **Query** — `query.py` (active / done / due)

## 用法

```bash
# 加 contact
python3 agent/add_contact.py "John Chan" "AECOM" "2026-06-05" "2026-06-12" "slope remedial 傾過" "Send resume" linkedin

# 即刻 check reminders
python3 agent/check_reminders.py

# Mark followed up (+7d bump)
python3 agent/mark.py followed_up 20260605120001

# Mark done
python3 agent/mark.py done 20260605120001

# Query
python3 agent/query.py                # Active
python3 agent/query.py due            # Due today
python3 agent/query.py done           # Done
```

## Cron

```
0 1 * * *  /usr/bin/python3 /home/node/.openclaw/workspace/skills/networking_followup/agent/check_reminders.py
# 每日 09:00 HKT (UTC 01:00)
```

## Channel 模板

- **LinkedIn** — 簡短 ping + 當初傾過嘅 topic
- **Email** — Subject + body (formal)
- **Other** — 通用短訊

**Subsequent follow-up** 自動 adapt (跟進次數 > 0)。

## 數據結構

`data/contacts.json`:
```json
[
  {
    "contact_id": "20260605120001",
    "name": "John Chan",
    "company": "AECOM",
    "contact_date": "2026-06-05",
    "follow_up_date": "2026-06-12",
    "topic": "slope remedial projects",
    "next_action": "Send resume + TCP cert",
    "channel": "linkedin",
    "done": false,
    "follow_up_count": 0,
    "added_at": "2026-06-05T12:00:00+08:00"
  }
]
```

## TODO
- [ ] Telegram inline command (`/followups`)
- [ ] 自動 import LinkedIn connections CSV
- [ ] Email integration (Gmail API)
- [ ] 智能建議 follow-up 時間 (per contact)
