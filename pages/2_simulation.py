import streamlit as st
import plotly.graph_objects as go
import numpy as np

def run_simulation():
    st.title("Gambler's Ruin Simulation")
    
    # Simulation parameters
    st.sidebar.header("Simulation Parameters")
    num_simulations = st.sidebar.slider("Number of Simulations", 1, 1000, 100)
    win_prob = st.sidebar.slider("Win Probability", 0.0, 1.0, 0.5)
    initial_money = st.sidebar.slider("Initial Money", 10, 1000, 100)
    target_money = st.sidebar.slider("Target Money", initial_money + 10, 2000, 200)
    
    # Run simulation
    results = simulate_multiple_games(num_simulations, win_prob, initial_money, target_money)
    
    # Display results
    show_simulation_results(results)

def simulate_multiple_games(num_sims, p, initial, target):
    results = []
    for _ in range(num_sims):
        money = initial
        steps = 0
        while money > 0 and money < target:
            steps += 1
            if np.random.random() < p:
                money += 1
            else:
                money -= 1
        results.append({
            'final_money': money,
            'steps': steps,
            'result': 'win' if money >= target else 'ruin'
        })
    return results

def show_simulation_results(results):
    # Calculate statistics
    wins = sum(1 for r in results if r['result'] == 'win')
    win_rate = wins / len(results)
    
    # Display summary statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Win Rate", f"{win_rate:.2%}")
    with col2:
        st.metric("Average Steps", f"{sum(r['steps'] for r in results)/len(results):.1f}")
    with col3:
        st.metric("Total Simulations", len(results))
    
    # Create histogram of results
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=[r['steps'] for r in results],
        name='Steps Distribution'
    ))
    fig.update_layout(
        title='Distribution of Steps until Game End',
        xaxis_title='Number of Steps',
        yaxis_title='Frequency'
    )
    st.plotly_chart(fig)

# 交互式模拟
# 概率分布图表
# 历史数据分析 