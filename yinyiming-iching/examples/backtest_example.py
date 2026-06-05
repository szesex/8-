"""
yinyiming-iching 回測示例
隱姓埋名易經卦爻 BTC 5m 歷史回測
"""

import pandas as pd
import numpy as np
from src.yinyiming_iching.backtest import Backtester

# 模擬 BTC 5m 歷史數據（實際請換成真實 CSV）
np.random.seed(42)
dates = pd.date_range(start="2026-06-01 00:00", periods=500, freq="5min")
prices = 100000 + np.cumsum(np.random.randn(500) * 30)
sample_df = pd.DataFrame({
    'timestamp': dates,
    'close': prices
})

print("=== 隱姓埋名易經卦爻 BTC 5m 回測 ===")
bt = Backtester(sample_df)
output = bt.run_backtest(forward_minutes=5)

print("\n回測績效：")
print(output['metrics'])

print("\n優化建議：")
print(bt.improve_rules(output['detailed_results']))

print("\n詳細結果前5筆：")
print(output['detailed_results'].head())