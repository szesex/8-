"""
yinyiming-iching
隱姓埋名易經卦爻核心模組
參考 kinqimen 結構 + 盲派分輕重 + 納音 + 合沖心法
專為 Polymarket BTC 5m UP/DOWN 設計
"""

from datetime import datetime
import hashlib
from typing import Dict, List, Tuple

# 簡單六十四卦名稱（完整版可擴充）
HEXAGRAM_NAMES = {
    (1,1,1,1,1,1): "乾為天",
    (0,0,0,0,0,0): "坤為地",
    # ... 可擴充其餘62卦
}

# 納音簡化對應（實際可用完整六十甲子納音表）
NAYIN_SIMPLE = {
    "甲子": "海中金", "乙丑": "海中金",
    # ... 完整表可從之前玄真書數據加
}

class YinyimingIChing:
    def __init__(self, dt_str: str, tz: str = "Asia/Hong_Kong"):
        """
        dt_str: "2026-06-05 15:30:00"
        """
        self.dt = datetime.fromisoformat(dt_str)
        self.pillars = self._get_pillars()  # 簡化：年月日時
        self.hexagram = self._generate_hexagram()
        self.moving_lines = self._identify_moving_lines()
        self.nayin = self._get_nayin()

    def _get_pillars(self) -> Dict:
        # 簡化版：實際可用 sxtwl 取真太陽時 + 八字
        # 這裡用簡單 hash 模擬
        ymdh = f"{self.dt.year}{self.dt.month}{self.dt.day}{self.dt.hour}"
        seed = int(hashlib.md5(ymdh.encode()).hexdigest()[:8], 16)
        return {
            "year": seed % 10,
            "month": (seed // 10) % 12,
            "day": (seed // 100) % 30,
            "hour": (seed // 1000) % 12
        }

    def _generate_hexagram(self) -> List[int]:
        """
        簡化起卦：用時間數字生成六爻（陽1/陰0）
        實際可用梅花易數或時間柱轉爻
        """
        seed = sum(self.pillars.values())
        lines = []
        for i in range(6):
            val = (seed + i * 7) % 6
            lines.append(1 if val > 2 else 0)  # 簡化陽陰
        return lines  # 下到上：初爻到上爻

    def _identify_moving_lines(self) -> List[int]:
        """
        識別動爻（簡化：隨機或規則）
        實際用時間或特定條件決定哪爻動
        """
        moving = []
        for i, line in enumerate(self.hexagram):
            if (sum(self.pillars.values()) + i) % 3 == 0:  # 簡化規則
                moving.append(i)
        return moving

    def _get_nayin(self) -> str:
        # 簡化，返回示例
        return "海中金"  # 實際用完整表

    def analyze_key_lines(self) -> Dict:
        """
        核心：分輕重選關鍵爻
        用神 = 妻財（BTC資金/升勢）
        忌神 = 兄弟（波動/搶奪）
        """
        key_lines = {}
        for idx in self.moving_lines:
            line_pos = idx + 1  # 1=初爻 ... 6=上爻
            weight = 0
            # 分輕重規則（對應之前教學）
            if line_pos >= 5:  # 第五、六爻位置高 = 重
                weight += 3
            if idx in self.moving_lines:
                weight += 2
            # 納音加持（簡化）
            if "金" in self.nayin or "水" in self.nayin:
                weight += 1

            key_lines[idx] = {
                "position": line_pos,
                "weight": weight,
                "type": "妻財" if line_pos in [2,5] else "兄弟" if line_pos in [1,3] else "其他"
            }
        return key_lines

    def analyze_he_chong(self) -> str:
        """
        簡化合沖分析
        """
        if len(self.moving_lines) >= 2:
            return "有合有沖，波動較大"
        return "相對穩定"

    def predict_btc_5m(self) -> Dict:
        """
        核心預測邏輯（隱姓埋名風格）
        """
        key_lines = self.analyze_key_lines()
        hechong = self.analyze_he_chong()

        # 簡單規則（可擴充歷史回測優化）
        wealth_strong = any(
            l["type"] == "妻財" and l["weight"] >= 4 
            for l in key_lines.values()
        )
        brothers_strong = any(
            l["type"] == "兄弟" and l["weight"] >= 4 
            for l in key_lines.values()
        )

        if wealth_strong and not brothers_strong:
            direction = "UP"
            confidence = 65
            reason = "妻財關鍵爻重 + 得令動，資金流入機會較大"
        elif brothers_strong and not wealth_strong:
            direction = "DOWN"
            confidence = 55
            reason = "兄弟強 + 沖妻財，搶奪/波動壓力大"
        else:
            direction = "VOLATILE / SIDEWAYS"
            confidence = 50
            reason = f"{hechong}，方向不明確，建議觀望"

        return {
            "datetime": self.dt.isoformat(),
            "hexagram_lines": self.hexagram,
            "moving_lines": self.moving_lines,
            "key_lines_analysis": key_lines,
            "he_chong": hechong,
            "nayin": self.nayin,
            "prediction": {
                "direction": direction,
                "confidence": confidence,
                "reason": reason,
                "polymarket_suggestion": f"Polymarket BTC 5m {direction} Yes/No 參考"
            }
        }

# 測試
if __name__ == "__main__":
    predictor = YinyimingIChing("2026-06-05 15:30:00")
    print(predictor.predict_btc_5m())