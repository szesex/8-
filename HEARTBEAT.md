# HEARTBEAT.md - Daily Operations

## 每日 07:30 盲派八字運程 Alert

每當收到 heartbeat poll 時：

### 讀取狀態
檢查 `/home/node/.openclaw/workspace/state/bazi_last_sent.json` 是否已發送過今日運程。

### 條件判斷
- 如果 HKT 時間係 **07:00 - 08:00** 且今日未發送，執行 Python script 獲取運程
- 如果係其他時間，回覆 HEARTBEAT_OK

### 發送流程
1. 執行：`python3 /home/node/.openclaw/workspace/bazi_skill_v2.py`
2. 透過 Telegram 發送輸出俾 Saba (chat_id: 8475453959)
3. 更新狀態檔為今日已發送

### 格式示例
```
大家好！隱姓埋名藏術數，又嚟同大家傾偈啦！

【2026年5月13日】

【Grok 版】
事業：火土反彈，金水護身。唔好同人嗌交！
財運：辛苦財為主，記住唔好亂投資！
盲派斷：火土反彈，金水護身無大礙！

═════════════════════════════════════════════

【DeepSeek 版】
事業：火土反彈，金水護身。唔好同人嗌交！
財運：辛苦財為主，記住唔好亂投資！
盲派斷：火土反彈，金水護身無大礙！

記住：命硬靠心態，你一定得！
隱姓埋名，藏術數，學盲派8字，易經算股市——我哋下次見！🔥
```

### Fast #6 追蹤
- 如果係 morning check-in，提醒 Fast #6 進度
- 72小時目標：May 11 20:00 HKT → May 14 20:00 HKT

### 狀態追蹤
- 已發送：更新 `/home/node/.openclaw/workspace/state/bazi_last_sent.json`
- 未發送：跳過，回复 HEARTBEAT_OK