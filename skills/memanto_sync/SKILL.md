---
name: memanto_sync
description: "Sync OpenClaw workspace memory (MEMORY.md + memory/*.md) to Memanto cloud for unlimited long-term memory. Also exposes recall/status commands."
user-invocable: true
---

# Memanto Sync Skill

_無限記憶 · Cloud-backed agent memory_

## 功能

- **`sync`** — 將 `MEMORY.md` + `memory/*.md` 自動 chunk + store 落 Memanto
- **`recall Q`** — 查詢 Memanto 記憶
- **`status`** — 顯示 Memanto agent / API 狀態
- **`watch`** — Watch mode，文件改動自動 sync

## 設定

1. 攞 Moorcheh API key：https://console.moorcheh.ai/api-keys
2. `memanto config set-key <key>` （或 `export MOORCHEH_API_KEY=...`）
3. `memanto agent create <name>` （例如 `saba_bazi`）

## Cron 設定（每日 sync）

```bash
# Add to bazi_daemon_supervisor.sh or as standalone cron:
0 4 * * * cd /home/node/.openclaw/workspace && python3 skills/memanto_sync/memanto_sync.py sync >> logs/memanto_sync.log 2>&1
```

或者用 OpenClaw cron job：
```json
{
  "name": "memanto-daily-sync",
  "schedule": "0 4 * * *",
  "command": "python3 /home/node/.openclaw/workspace/skills/memanto_sync/memanto_sync.py sync"
}
```

## Memory Types

Memanto 支援 13 個 built-in types：fact / instruction / decision / goal / preference / relationship / etc.

`remember` 會 auto-detect type，或用 `--type <type>` 指定。

## 用法

```bash
# 單次 sync
python3 skills/memanto_sync/memanto_sync.py sync

# Query
python3 skills/memanto_sync/memanto_sync.py recall "Saba八字"

# Status
python3 skills/memanto_sync/memanto_sync.py status

# Watch (real-time)
python3 skills/memanto_sync/memanto_sync.py watch
```

## Memory chunking

- 預設每 chunk 500 chars（可調）
- 標記 `[<file>#<chunk_idx>/<total>]` 前綴方便 recall 知道 source
- 已存在嘅 memory 會 deduplicate（same content 不重複 store）

## 13 Built-in Memory Types

| Type | 用法 |
|------|------|
| `fact` | 客觀事實 (e.g. "Saba八字是...") |
| `instruction` | 行為指引 (e.g. "Reply in Cantonese") |
| `decision` | 決定 (e.g. "Use M3 model") |
| `goal` | 目標 (e.g. "考 MICE/CEng 認證") |
| `preference` | 喜好 (e.g. "Lihkg 仔風格") |
| `relationship` | 人際關係 |
| ... | |

## Files

- `memanto_sync.py` — Main skill script
- `SKILL.md` — This file
