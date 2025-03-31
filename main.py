import streamlit as st
from gamblers_ruin_intro import show_introduction
from gamblers_ruin_game import run_game

def main():
    st.set_page_config(page_title="Gambler's Ruin", layout="wide")
    
    # 创建标签页
    tab1, tab2 = st.tabs(["理论介绍", "游戏模拟"])
    
    with tab1:
        show_introduction()
    
    with tab2:
        run_game()

if __name__ == "__main__":
    main() 