import streamlit as st
import random
from datetime import datetime
import pandas as pd

class GamblersRuinGame:
    def __init__(self):
        # Initialize game state
        if 'player_name' not in st.session_state:
            st.session_state.player_name = None
        if 'balance' not in st.session_state:
            st.session_state.balance = 1000
        if 'game_history' not in st.session_state:
            st.session_state.game_history = []
    
    def run(self):
        if not st.session_state.player_name:
            self.show_login()
        else:
            self.show_game()
    
    def show_login(self):
        st.title("Welcome to Gambler's Ruin Game")
        with st.form("login_form"):
            player_name = st.text_input("Enter your name")
            submitted = st.form_submit_button("Start Playing")
            if submitted and player_name:
                st.session_state.player_name = player_name
                st.experimental_rerun()
    
    def show_game(self):
        st.title(f"Welcome, {st.session_state.player_name}!")
        
        # Game controls
        col1, col2 = st.columns(2)
        with col1:
            bet_amount = st.number_input("Bet Amount", 1, 100, 10)
            if st.button("Place Bet"):
                self.place_bet(bet_amount)
        
        with col2:
            st.metric("Current Balance", f"${st.session_state.balance}")
        
        # Game history
        self.show_history()
    
    def place_bet(self, amount):
        if amount > st.session_state.balance:
            st.error("Insufficient funds!")
            return
        
        # Process bet
        win = random.random() < 0.5
        if win:
            st.session_state.balance += amount
            result = "Won"
        else:
            st.session_state.balance -= amount
            result = "Lost"
        
        # Record history
        st.session_state.game_history.append({
            'timestamp': datetime.now(),
            'bet_amount': amount,
            'result': result,
            'balance': st.session_state.balance
        })
        
        # Show result
        if win:
            st.success(f"You won ${amount}!")
        else:
            st.error(f"You lost ${amount}")
    
    def show_history(self):
        if st.session_state.game_history:
            st.subheader("Game History")
            history_df = pd.DataFrame(st.session_state.game_history)
            st.dataframe(history_df) 