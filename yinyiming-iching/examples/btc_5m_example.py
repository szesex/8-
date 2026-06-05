"""
yinyiming-iching 示例
隱姓埋名易經卦爻 BTC 5m 預測
"""

from src.yinyiming_iching.iching import YinyimingIChing

# 示例：2026年6月5日 15:30 HKT 起卦
dt = "2026-06-05 15:30:00"
predictor = YinyimingIChing(dt)
result = predictor.predict_btc_5m()

print("=== 隱姓埋名易經卦爻 BTC 5m 預測 ===")
print(f"時間: {result['datetime']}")
print(f"卦爻: {result['hexagram_lines']}")
print(f"動爻: {result['moving_lines']}")
print(f"納音: {result['nayin']}")
print(f"合沖: {result['he_chong']}")
print("\n關鍵爻分析:")
for idx, info in result['key_lines_analysis'].items():
    print(f"  第{info['position']}爻 ({info['type']}) - 權重 {info['weight']}")

print("\n=== 預測結果 ===")
print(f"方向: {result['prediction']['direction']}")
print(f"信心: {result['prediction']['confidence']}%")
print(f"理由: {result['prediction']['reason']}")
print(f"Polymarket 建議: {result['prediction']['polymarket_suggestion']}")