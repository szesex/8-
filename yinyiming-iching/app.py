"""
Streamlit Demo for yinyiming-iching
隱姓埋名易經卦爻 Polymarket BTC 5m 預測
"""

import streamlit as st
from src.yinyiming_iching.iching import YinyimingIChing

st.set_page_config(page_title="隱姓埋名易經卦爻 BTC 5m", layout="wide")
st.title("🔮 隱姓埋名易經卦爻 Polymarket BTC 5m 預測")
st.markdown("參考 kinqimen + 盲派分輕重 + 納音 + 合沖心法")

with st.sidebar:
    st.header("輸入時間")
    date = st.date_input("日期", value=None)
    time = st.time_input("時間 (HKT)", value=None)
    if st.button("起卦預測"):
        if date and time:
            dt_str = f"{date} {time}"
            predictor = YinyimingIChing(dt_str)
            result = predictor.predict_btc_5m()
            st.session_state.result = result

if "result" in st.session_state:
    res = st.session_state.result
    st.subheader("卦象與分析")
    st.json(res)

    pred = res["prediction"]
    if "UP" in pred["direction"]:
        st.success(f"**預測方向：{pred['direction']}** (信心 {pred['confidence']}%)")
    elif "DOWN" in pred["direction"]:
        st.error(f"**預測方向：{pred['direction']}** (信心 {pred['confidence']}%)")
    else:
        st.warning(f"**預測方向：{pred['direction']}** (信心 {pred['confidence']}%)")

    st.info(pred["reason"])
    st.caption(pred["polymarket_suggestion"])

st.markdown("---")
st.caption("隱姓埋名 | 實戰驗證為主 | 風險自負 | 繼續自學繼續驗證")