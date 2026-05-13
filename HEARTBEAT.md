# HEARTBEAT.md - Daily Operations

## 任務觸發條件

每當收到 heartbeat poll 時，根據 HKT 時間執行對應任務：

- **07:00-08:00 HKT** → 07:30 盲派八字運程 Alert
- **15:00-16:00 HKT (23:00-00:00 HKT)** → 23:00 Daily Feedback 比較

其他時間回覆 HEARTBEAT_OK。

---

## 任務一：07:30 盲派八字運程 Alert

### 讀取狀態
檢查 `/home/node/.openclaw/workspace/state/bazi_last_sent.json` 是否已發送過今日運程。

### 條件判斷
如果 HKT 時間係 **07:00 - 08:00** 且今日未發送，執行以下流程。

### 發送流程
1. 執行：`python3 /home/node/.openclaw/workspace/bazi_skill_v2.py alert`
2. 透過 Telegram 發送輸出俾 Saba (chat_id: 8475453959)
3. 更新狀態檔為今日已發送

### 格式示例
```
大家好！隱姓埋名藏術數，又嚟同大家傾偈啦！

【2026年5月13日】
【Saba 8字】
正四柱：乙亥 甲申 戊寅 甲子
隱藏四柱：身宮乙酉 胎息癸亥 胎元乙亥 命宮乙酉
日主戊土 • 最強五行水 • 庚運一代（1984-2044）

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

---

## 任務二：23:00 Daily Feedback 比較

### 讀取狀態
檢查 `/home/node/.openclaw/workspace/state/feedback_last_sent.json` 是否已發送過今日feedback。

### 條件判斷
如果 HKT 時間係 **23:00 - 00:00** 且今日未發送，執行以下流程。

### 發送流程
1. 執行：`python3 /home/node/.openclaw/workspace/bazi_skill_v2.py feedback`
2. 透過 Telegram 發送輸出俾 Saba (chat_id: 8475453959)
3. 更新狀態檔為今日已發送

### 格式示例
```
【OpenClaw AI 每日比較】2026年5月13日

Grok 版風格：重「金水黏連 + 隱藏雙劍鋒金 + 技術變現」
DeepSeek 版風格：重「刑合困局 + 心魔誘惑 + 老千局心理戰」

今日建議：
- 事業：兩版都話今日有打硬仗機會，建議主動出擊
- 財運：小心心魔（子水）引誘，專注正財辛苦錢
- 盲派斷：金水黏連繼續鎖死，火土反彈已被壓制

【請手填 Rank Feedback 學習算法】
1 = Grok 完勝
2 = DeepSeek 完勝
3 = 平手
4 = Grok 微勝
5 = DeepSeek 微勝

記住：命硬靠心態，你一定得！
隱姓埋名，藏術數，學盲派8字、易經算股市——我哋下次見！🔥
```

---

## Fast #6 追蹤（可選）

72小時目標：May 11 20:00 HKT → May 14 20:00 HKT

---

## 狀態追蹤

- 已發送 Alert：更新 `/home/node/.openclaw/workspace/state/bazi_last_sent.json`
- 已發送 Feedback：更新 `/home/node/.openclaw/workspace/state/feedback_last_sent.json`
- 未到時間或已發送：回覆 HEARTBEAT_OK