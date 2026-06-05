"""
yinyiming-iching Backtesting Module
隱姓埋名易經卦爻 BTC 5m 歷史回測
使用 pandas 進行數據處理與績效計算
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from .iching import YinyimingIChing

class Backtester:
    def __init__(self, df: pd.DataFrame, prediction_func=None):
        """
        df: DataFrame with columns ['timestamp', 'close'] 
            timestamp 可為 datetime 或 string
        prediction_func: 自訂預測函數（可選），默認使用 YinyimingIChing
        """
        self.df = df.copy()
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df = self.df.sort_values('timestamp').reset_index(drop=True)
        self.prediction_func = prediction_func or self._default_predict

    def _default_predict(self, dt_str: str) -> str:
        """默認使用 YinyimingIChing 預測"""
        try:
            predictor = YinyimingIChing(dt_str)
            result = predictor.predict_btc_5m()
            direction = result['prediction']['direction']
            if 'UP' in direction:
                return 'UP'
            elif 'DOWN' in direction:
                return 'DOWN'
            else:
                return 'HOLD'
        except:
            return 'HOLD'

    def run_backtest(self, forward_minutes: int = 5) -> Dict:
        """
        執行回測
        forward_minutes: 預測後多少分鐘的實際漲跌（默認5m）
        """
        results = []
        for i in range(len(self.df) - 1):
            row = self.df.iloc[i]
            dt_str = row['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            pred = self.prediction_func(dt_str)

            # 實際未來漲跌
            current_price = row['close']
            future_idx = min(i + forward_minutes, len(self.df) - 1)
            future_price = self.df.iloc[future_idx]['close']
            actual_change = (future_price - current_price) / current_price * 100

            actual = 'UP' if actual_change > 0.05 else ('DOWN' if actual_change < -0.05 else 'HOLD')

            results.append({
                'timestamp': row['timestamp'],
                'prediction': pred,
                'actual': actual,
                'actual_change_pct': round(actual_change, 4)
            })

        result_df = pd.DataFrame(results)

        # 計算績效
        total = len(result_df)
        correct = len(result_df[result_df['prediction'] == result_df['actual']])
        accuracy = correct / total if total > 0 else 0

        up_preds = result_df[result_df['prediction'] == 'UP']
        up_correct = len(up_preds[up_preds['actual'] == 'UP'])
        up_precision = up_correct / len(up_preds) if len(up_preds) > 0 else 0

        down_preds = result_df[result_df['prediction'] == 'DOWN']
        down_correct = len(down_preds[down_preds['actual'] == 'DOWN'])
        down_precision = down_correct / len(down_preds) if len(down_preds) > 0 else 0

        metrics = {
            'total_signals': total,
            'accuracy': round(accuracy, 4),
            'up_precision': round(up_precision, 4),
            'down_precision': round(down_precision, 4),
            'up_signals': len(up_preds),
            'down_signals': len(down_preds)
        }

        return {
            'detailed_results': result_df,
            'metrics': metrics
        }

    def improve_rules(self, result_df: pd.DataFrame) -> str:
        """
        簡單規則優化建議（可擴充機器學習）
        """
        # 分析錯誤案例
        errors = result_df[result_df['prediction'] != result_df['actual']]
        suggestions = []
        if len(errors) > 0:
            suggestions.append(f"發現 {len(errors)} 個錯誤預測，建議檢查動爻納音與實際波動相關性")
            suggestions.append("可嘗試調整：妻財權重閾值、或加入奇門吉門過濾")
        else:
            suggestions.append("目前規則表現不錯，可繼續累積更多數據優化")
        return "\n".join(suggestions)


# 使用示例
if __name__ == "__main__":
    # 模擬歷史數據（實際請換成真實 BTC 5m CSV）
    dates = pd.date_range(start="2026-06-01", periods=100, freq="5min")
    np.random.seed(42)
    prices = 100000 + np.cumsum(np.random.randn(100) * 50)
    sample_df = pd.DataFrame({
        'timestamp': dates,
        'close': prices
    })

    bt = Backtester(sample_df)
    backtest_output = bt.run_backtest()

    print("=== 回測績效 ===")
    print(backtest_output['metrics'])
    print("\n=== 優化建議 ===")
    print(bt.improve_rules(backtest_output['detailed_results']))