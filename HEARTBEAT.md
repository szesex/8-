# HEARTBEAT.md - Daily Operations (Auto 07:30 + 23:00)

## 任務觸發條件

每當收到 heartbeat poll 時，根據 HKT 時間執行對應任務：

- **HKT 07:00-08:00** → 07:30 盲派八字運程 Alert
- **HKT 15:00-16:00 (23:00 HKT)** → 23:00 Daily Feedback 比較

其他時間回覆 HEARTBEAT_OK。

---

## 任務一：07:30 盲派八字運程 Alert

### 發送流程
1. 執行：`python3 /home/node/.openclaw/workspace/bazi_skill_v2.py alert`
2. 透過 Telegram 發送輸出俾 Saba (chat_id: 8475453959)
3. 更新狀態：`/home/node/.openclaw/workspace/state/bazi_last_sent.json`

### 格式
```
大家好！隱姓埋名藏術數，又嚟同大家傾偈啦！

【2026年5月14日】
【Saba 8字】
正四柱：乙亥 甲申 戊寅 甲子
隱藏四柱：身宮乙酉 胎息癸亥 胎元乙亥 命宮乙酉
日主戊土 • 最強五行水 • 庚運一代（1984-2044）

【當日8字】
2026年 5月14日 戊子日
四柱：丙午 壬午 戊子 戊時

【Grok 版】
事業：土水黏連，ICE pathway穩陣前進！
財運：辛苦財為主，穩陣收成！
盲派斷：金水黏連力度加強，死結繼續破！

═════════════════════════════════════════════

【DeepSeek 版】
事業：穩固成果。唔好衝動！
財運：累積財富，記住唔好亂買！
盲派斷：金水黏連過渡，養精蓄銳！

記住：命硬靠心態，你一定得！
隱姓埋名，藏術數，學盲派8字、易經算股市——我哋下次見！🔥
```

---

## 任務二：23:00 Daily Feedback 比較

### 發送流程
1. 執行：`python3 /home/node/.openclaw/workspace/bazi_skill_v2.py feedback`
2. 透過 Telegram 發送輸出俾 Saba (chat_id: 8475453959)
3. 更新狀態：`/home/node/.openclaw/workspace/state/feedback_last_sent.json`

### 格式
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

## 自動 Git Push Backup

當收到 Saba 嘅 Rank 回覆（1-5）時：
1. 將 Rank 寫入 `/home/node/.openclaw/workspace/bazi_user_rank_feedback.json`
2. 自動執行 Git commit + push：
   ```bash
   cd /home/node/.openclaw/workspace && git add -A && git commit -m "Auto backup $(date +%Y-%m-%d_%H:%M)" && git push
   ```

---

## 狀態追蹤

- `/home/node/.openclaw/workspace/state/bazi_last_sent.json` - 最后發送 alert 時間
- `/home/node/.openclaw/workspace/state/feedback_last_sent.json` - 最后發送 feedback 時間
- `/home/node/.openclaw/workspace/bazi_user_rank_feedback.json` - 用戶 Rank 記錄

---

## Fast #6 追蹤（可選）

72小時目標：May 11 20:00 HKT → May 14 20:00 HKT
（斷食完成後無需特別提示，正常作息即可）