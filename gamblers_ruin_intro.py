import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def show_introduction():
    st.title("赌徒破产问题 (Gambler's Ruin)")
    
    # 理论介绍
    st.header("什么是赌徒破产问题？")
    st.write("""
    赌徒破产问题是一个经典的概率论问题，描述了一个赌徒与赌场对赌的情况...
    """)
    
    # 数学公式（使用LaTeX）
    st.header("数学模型")
    st.latex(r"""
    P(破产) = \begin{cases} 
    \frac{1-(\frac{q}{p})^n}{1-(\frac{q}{p})^N} & \text{if } p \neq q \\
    \frac{n}{N} & \text{if } p = q
    \end{cases}
    """)
    
    # 交互式演示
    st.header("概率可视化")
    p = st.slider("获胜概率 p", 0.0, 1.0, 0.5)
    initial_money = st.slider("初始资金", 1, 100, 50)
    
    # 显示模拟结果图表
    plot_probability_distribution(p, initial_money) 