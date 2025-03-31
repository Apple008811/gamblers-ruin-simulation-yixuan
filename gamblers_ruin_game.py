import streamlit as st
import random
import time

class GamblersRuinGame:
    def __init__(self):
        self.initial_money = 100
        self.current_money = self.initial_money
        self.target_money = 200
        self.bet_size = 10
        self.win_probability = 0.5
        
    def play_round(self):
        if random.random() < self.win_probability:
            self.current_money += self.bet_size
            return True
        else:
            self.current_money -= self.bet_size
            return False

def run_game():
    st.title("赌徒破产游戏")
    
    # 游戏设置
    col1, col2 = st.columns(2)
    with col1:
        initial_money = st.number_input("初始资金", 10, 1000, 100)
        target_money = st.number_input("目标金额", initial_money + 10, 2000, 200)
    
    with col2:
        bet_size = st.number_input("每次赌注", 1, 50, 10)
        win_prob = st.slider("获胜概率", 0.0, 1.0, 0.5)
    
    # 游戏状态显示
    st.metric("当前资金", f"${game.current_money}")
    
    # 对话框
    with st.chat_message("assistant"):
        st.write("准备好开始了吗？每一轮我都会给你建议！")
    
    # 玩家操作按钮
    if st.button("开始新一轮"):
        result = game.play_round()
        show_round_result(result) 