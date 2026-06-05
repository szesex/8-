# yinyiming-iching

**隱姓埋名易經卦爻 Polymarket BTC 5m 預測工具**

一個參考 `kentang2017/kinqimen` 結構，結合**盲派八字 + 納音 + 六爻分輕重 + 合沖**心法的 Python 易經卦爻預測庫。

專為 **Polymarket BTC 5分鐘升跌** 設計，實戰驗證為主。

## 理念（隱姓埋名風格）
- 唔係神秘，而是**時間能量 + 線與線關係 + 納音五行**嘅實證系統。
- 重點：**選關鍵爻**（分輕重） + **合沖分析** + **納音加持**。
- 用嚟輔助短線 timing（5m BTC Yes/No 市場），**千祈唔好亂入市**，只係驗證同學習工具。
- 結合之前教學：易經六爻 + 盲派納音 + 奇門思維，一齊用會更有層次。

## 功能
- 時間起卦（梅花易數風格 + 時間柱納音）
- 自動生成六爻 + 動爻識別
- **分輕重選關鍵爻**（位置 + 動 + 納音旺衰 + 對用神影響）
- 合沖分析（兄弟妻財關係）
- 納音五行整合（參考玄真《盲派納音算命學》）
- BTC 5m UP/DOWN 預測邏輯（妻財強動 = UP；兄弟強沖 = DOWN/波動）
- Streamlit Web Demo
- 支援 Polymarket Yes/No 市場建議
- **歷史回測 + 規則優化**（pandas-based）

## 安裝

```bash
# 開發模式（推薦）
git clone https://github.com/szesex/8-.git
cd 8-/yinyiming-iching
pip install -r requirements.txt
pip install -e .

# 或直接安裝依賴
pip install sxtwl pendulum streamlit pandas numpy
```

## 快速開始

### 基本起卦
```python
from src.yinyiming_iching import YinyimingIChing

# 輸入時間（UTC or HKT）
dt = "2026-06-05 15:30:00"  # 5m 預測用呢個時間

predictor = YinyimingIChing(dt)
result = predictor.predict_btc_5m()

print(result)
# 輸出示例：
# 卦象：...
# 關鍵爻：妻財（第五爻動） - 重
# 納音：...
# 合沖：...
# 預測：UP (信心 65%) - Polymarket Yes 建議
# 理由：妻財得令動 + 兄弟被合，資金流入機會較大
```

### Streamlit Web Demo
```bash
streamlit run app.py
# 開 http://localhost:8501
```

## 核心心法（對應之前教學）
1. **選關鍵爻**：只睇真正動 + 影響用神（妻財）的線
2. **分輕重**：位置高 + 納音旺 = 重
3. **合沖**：兄弟被合 = 搶奪力減 = 利升
4. **納音**：用玄真老師方法加強判斷
5. **驗證**：事後對比 Polymarket 實際結果，不斷優化規則

## 結構
```
yinyiming-iching/
├── README.md
├── LICENSE (MIT)
├── requirements.txt
├── app.py                           # Streamlit Demo
├── src/
│   └── yinyiming_iching/
│       ├── __init__.py
│       ├── iching.py                # 核心起卦 + 分析
│       ├── backtest.py              # ★ 歷史回測 + 規則優化
│       └── (nayin.py - 可擴充)
├── examples/
│   ├── btc_5m_example.py
│   └── backtest_example.py          # ★ 回測使用示例
└── data/
    └── (歷史 BTC 5m 數據 CSV)
```

## 歷史回測與規則優化
使用 `backtest.py` 進行歷史數據回測，驗證並優化預測規則。

### 快速回測
```python
import pandas as pd
from src.yinyiming_iching.backtest import Backtester

# 載入你的 BTC 5m 歷史數據（timestamp, close）
df = pd.read_csv("data/btc_5m_history.csv")

bt = Backtester(df)
output = bt.run_backtest(forward_minutes=5)

print(output['metrics'])  # accuracy, precision 等
print(bt.improve_rules(output['detailed_results']))  # 優化建議
```

**回測指標包括：**
- Overall Accuracy
- UP / DOWN Precision
- Signal 數量
- 簡單規則優化建議（可進一步加 ML 模型）

### 優化思路（隱姓埋名風格）
- 如果 UP precision 低 → 提高妻財權重閾值或加納音過濾
- 如果 DOWN 常錯 → 檢查兄弟沖妻財時是否真的利淡
- 建議累積至少 1000+ 個 5m bar 再優化
- 可結合奇門吉門（生門、開門）做多層過濾

## 未來方向
- 整合 kinqimen 奇門（時空 + 門星神）
- 歷史回測 BTC 5m 數據（已支援）
- 多時間框架（1m / 15m / 1h）
- Discord/Telegram bot 推送
- 真實數據源整合（ccxt 等）

## 免責
呢個只係學習同驗證工具。加密貨幣高風險，**唔係投資建議**。請自己驗證 + 風險管理。

## 貢獻
歡迎 PR！特別係：
- 優化預測規則
- 加更多納音/盲派心法
- 歷史數據回測

一起將「隱姓埋名」嘅實戰心法變成工具，幫助更多人自學易經算 crypto。

---

**隱姓埋名**
「知之為知之，不知為不知」
繼續驗證，繼續進步。

如果想即刻用或者改規則，話我知，我哋一齊整！
