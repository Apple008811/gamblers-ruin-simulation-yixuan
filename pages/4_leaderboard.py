import streamlit as st
import pandas as pd

def show_leaderboard():
    st.title("排行榜")
    
    # 获取所有玩家的统计数据
    leaderboard_data = pd.DataFrame({
        "玩家": ["Player1", "Player2", "Player3"],
        "总收益": [1000, 800, 600],
        "胜率": [0.6, 0.55, 0.52],
        "游戏场次": [100, 80, 70]
    })
    
    # 显示排行榜
    st.dataframe(leaderboard_data) 