import pandas as pd
import streamlit as st
from datetime import datetime

class GameDatabase:
    def __init__(self):
        # 初始化数据存储
        if 'game_records' not in st.session_state:
            st.session_state.game_records = pd.DataFrame(
                columns=['player', 'timestamp', 'bet_amount', 'result', 'balance']
            )
    
    def save_game_record(self, player, bet_amount, result, balance):
        new_record = pd.DataFrame({
            'player': [player],
            'timestamp': [datetime.now()],
            'bet_amount': [bet_amount],
            'result': [result],
            'balance': [balance]
        })
        st.session_state.game_records = pd.concat([
            st.session_state.game_records, new_record
        ]) 