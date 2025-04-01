import streamlit as st

# Set page config
st.set_page_config(
    page_title="Gambler's Ruin Problem",
    page_icon="🎲",
    layout="wide"
)

def show_introduction():
    st.title("🎲 Gambler's Ruin Problem")
    
    st.header("What is Gambler's Ruin?")
    st.write("""
    The Gambler's Ruin problem is a classic probability theory problem that studies 
    a gambler who starts with an initial fortune and plays a fair game against 
    an opponent (usually a casino) with infinite resources. The gambler's goal is 
    to reach a certain target fortune, but they risk going bankrupt in the process.

    Key concepts:
    1. Initial fortune (n): The amount of money the gambler starts with
    2. Target fortune (N): The amount the gambler aims to reach
    3. Win probability (p): The probability of winning each bet
    4. Loss probability (q = 1-p): The probability of losing each bet
    """)

if __name__ == "__main__":
    show_introduction() 