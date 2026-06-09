# 8- · 隱姓埋名 AI 工具箱 🐉

[![Saba](https://img.shields.io/badge/Saba-30%20歲%20廢青-blueviolet)](https://t.me/saba)
[![Bazi](https://img.shields.io/badge/八字-乙亥甲申戊寅甲子-crimson)](#-bazi-盲派8字)
[![Status](https://img.shields.io/badge/status-5%20翻身%20skills%20%7C%20daily%20alerts-brightgreen)](#-翻身計劃-5-skills)
[![Model](https://img.shields.io/badge/MiniMax--M3-active-orange)](https://minimax.io)

> 隱姓埋名，藏術數，學盲派8字、易經算股市 — 同時 build 翻身計劃

## 📦 內容

### 🔮 Bazi 盲派8字 (Daily Fortune)
- **自動 cron** — HKT 07:30 daily alert + 23:00 feedback
- **Grok vs DeepSeek** — 兩版本 8 字分析比較
- **Rank 反饋** — 學習算法 (1=Grok完勝 2=DeepSeek完勝 3=平手 4=Grok微勝 5=DeepSeek微勝 6=兩個都唔得)
- **JSON data** — `bazi_fortune_data.json` 覆蓋 2026 5月 — 2027 12月
- **核心脚本** — `bazi_skill_v2.py`, `bazi_cron_daemon.py`, `merge_new_data.py`
- **日主戊土 · 庚運一代 (1984-2044)** — 金水黏連為主軸

### 💪 翻身計劃 — 5 Skills (Single-fighter Recovery)
| # | Skill | Cron HKT | 用途 |
|---|-------|----------|------|
| 1 | [job_application_tracker](./skills/job_application_tracker/) | 週日 21:00 | 求職申請 dashboard (6 status enum) |
| 2 | [targeted_job_alert](./skills/targeted_job_alert/) | 週二、五 08:00 | 目標職位 + match score (auto Telegram push) |
| 3 | [weekly_review_streak](./skills/weekly_review_streak/) | 週日 20:00 | 每週數據 + 連續 streak (exam/jobs/OC/MMA) |
| 4 | [networking_followup](./skills/networking_followup/) | 每日 09:00 | 人脈跟進 + LinkedIn/email 草稿生成 |
| 5 | [side_income_report](./skills/side_income_report/) | 每月 1 號 10:00 | Side income 月報 + 50/30/20 還債建議 |

每個 skill：
- `agent/lib.py` + 2-4 sub-scripts (add/update/query/generate)
- `data/*.json` (mock entries 可立即用)
- `SKILL.md` 完整文檔
- `.gitignore` (Python cache)

### 🧠 記憶系統
- **Memanto** (moorcheh.ai cloud) — 173+ 永久 memories
- **Memanto sync** — HKT 04:00 daily auto sync
- **Files tracked** — `MEMORY.md` + `memory/YYYY-MM-DD.md`

### 🤖 InterClaw Multi-Agent
- 5 workers online (Zeabur + same container)
- Coordinator + worker pattern
- Cloudflare Quick Tunnel gateway

### 📜 yinyiming-iching
- 隱姓埋名 易經卦爻 BTC 5m 預測工具
- Repo: https://github.com/yip-lgtm/yinyiming-iching (also `szesex/8-/yinyiming-iching/`)
- v0.1.0 MIT license

---

## 🔮 Bazi 盲派8字

### 用法
```bash
# 7:30 daily alert
python3 bazi_skill_v2.py alert

# 23:00 daily feedback
python3 bazi_skill_v2.py feedback

# 更新 JSON data
python3 merge_new_data.py
```

### Cron 設定
| Task | Time | Type |
|------|------|------|
| Daily alert | HKT 07:30 | Python daemon (PID 353) |
| Daily feedback | HKT 23:00 | Python daemon |
| Memanto sync | HKT 04:00 | System cron |
| Job tracker dashboard | 週日 21:00 HKT | System cron |
| Job alert | 週二、五 08:00 HKT | System cron |
| Weekly review | 週日 20:00 HKT | System cron |
| Networking | 每日 09:00 HKT | System cron |
| Side income | 每月 1 號 10:00 HKT | System cron |

### Rank 評分
1 = Grok 完勝
2 = DeepSeek 完勝
3 = 平手
4 = Grok 微勝
5 = DeepSeek 微勝
6 = 兩個都唔得

數據喺 `bazi_user_rank_feedback.json`。

---

## 💪 翻身計劃 5 Skills

### 1. Job Application Tracker
追蹤求職進度，6 個 status (applied/phone_screen/interview/offer/rejected/withdrawn)。
**自動生成 dashboard 推送 Telegram 週日 21:00。**
```bash
python3 skills/job_application_tracker/agent/add_application.py "AECOM" "Geotechnical Engineer" "applied" "2026-06-08" "Indeed"
python3 skills/job_application_tracker/agent/update_status.py 20260608001 interview "2026-06-15 10:00"
python3 skills/job_application_tracker/agent/generate_dashboard.py
```

### 2. Targeted Job Alert
目標職位 + match score (30 base + 15 per keyword + AI/automation boost)。
**自動推送 Top 5 高度匹配職位到 Telegram 週二、五 08:00。**
```bash
python3 skills/targeted_job_alert/agent/add_job.py "Geotechnical Eng" "AECOM" "https://..." 85
python3 skills/targeted_job_alert/agent/send_alert.py
```

### 3. Weekly Review + Streak
每週日 20:00 HKT 推送 review 到 Telegram。
**Auto-pull 本週 job apps 從 Skill 1。**
**3 個下週建議自動生成。**
```bash
python3 skills/weekly_review_streak/agent/log.py 5 2 4 2 2500 "病好返第二日"
python3 skills/weekly_review_streak/agent/query.py streaks
```

### 4. Networking Follow-up
**每日 09:00 HKT 提醒 follow-up 嘅人 + auto-generate LinkedIn/email 草稿。**
- First follow-up vs subsequent (adapt based on count)
- `mark.py followed_up <id>` (+7d bump)
- `mark.py done <id>`
```bash
python3 skills/networking_followup/agent/add_contact.py "John Chan" "AECOM" "2026-06-05" "2026-06-12" "slope remedial" "Send resume" linkedin
python3 skills/networking_followup/agent/check_reminders.py
```

### 5. Side Income Report
**每月 1 號 10:00 HKT 推送月報到 Telegram。**
- By source 細分 + 比較上個月 (delta %)
- 智能建議 (concentration / rate / hours)
- 50/30/20 還債分配 (還債 / 投資自己 / 緩衝)
- YTD 累計
```bash
python3 skills/side_income_report/agent/add_income.py 800 "活木生活木工" "2026-06-09" 8 "整 layer 板"
python3 skills/side_income_report/agent/generate_monthly_report.py
```

---

## 🧠 記憶系統 (Memanto)

永久記憶喺 moorcheh.ai 雲端 (不受 OpenClaw session 重啟影響)。
```bash
# Manual sync
python3 skills/memanto_sync/memanto_sync.py sync

# Recall via query
python3 skills/memanto_sync/memanto_sync.py recall "八字"

# Status
python3 skills/memanto_sync/memanto_sync.py status
```

**Agent name:** `saba_bazi`
**API key:** env var `MOORCHEH_API_KEY`

---

## 🤖 InterClaw Multi-Agent

5 workers (Zeabur + container-beijing):
- 1 coordinator
- 4 workers (PIDs 168, 225-228)

Gateway URL: Cloudflare Quick Tunnel (changes on restart)

---

## 📜 8字 速覽

```
正四柱：乙亥 甲申 戊寅 甲子
隱藏四柱：身宮乙酉 胎息癸亥 胎元乙亥 命宮乙酉
日主戊土 • 最強五行水 • 庚運一代（1984-2044）
```

---

## 🔧 安裝

```bash
# 一次性 setup
cd /home/node/.openclaw/workspace
python3 bazi_skill_v2.py  # 確認 timezone 正常
crontab -e                # 確認 cron 排好

# Memanto
pip3 install memanto --break-system-packages
export MOORCHEH_API_KEY="..."
python3 skills/memanto_sync/run.sh sync
```

---

## 📊 GitHub Commits (最近)

```
dc26de3  Skill 5 完整版 (side_income_report)
47ba9da  Skill 4 完整版 (networking_followup)
a006b72  Skill 3 完整版 (weekly_review_streak)
79c4880  Skill 2 完整版 (targeted_job_alert)
e32999b  Skill 1 完整版 (job_application_tracker)
8448152  Skills 2-5 stubs
93344ac  Rank 2 (6/8 DeepSeek完勝)
ca84064  Rank 6 (6/5 兩個都唔得)
c411872  Rank 6 (6/5)
1d8f1be  Rank 6 option added
31414c7  JSON data rebuild (year detection fix)
```

---

## 💡 信念

> **命硬靠心態，你一定得！**
> **隱姓埋名，藏術數，學盲派8字、易經算股市——我哋下次見！🔥**

---

_Last updated: 2026-06-09 — 5 個翻身 skills 全部完整 + tested + cron 排好_
