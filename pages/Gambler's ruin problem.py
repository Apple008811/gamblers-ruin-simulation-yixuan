import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List
import json

def show_introduction():
    st.title("Gambler's Ruin Problem")
    
    # 创建四个标签页
    tab1, tab2, tab3, tab4 = st.tabs([
        "Introduction",
        "Mathematical Analysis",
        "Interactive Demo (without loan)",
        "Interactive Demo (with loan)"
    ])
    
    # Tab 1: Introduction
    with tab1:
        st.header("What is Gambler's Ruin?")
        st.write("""
        The Gambler's Ruin problem is a classic probability theory problem that models 
        a gambler who starts with an initial fortune and plays a fair game against a casino 
        with infinite resources.
        
        **Key Concepts:**
        1. A gambler starts with initial fortune n
        2. The casino has infinite resources (fortune N → ∞)
        3. Each game has probability p of winning and q = (1-p) of losing
        4. The gambler's goal is to reach a target fortune
        """)
        
        # Add historical context
        st.subheader("Historical Background")
        st.write("""
        The problem was first studied by Blaise Pascal and Pierre de Fermat in the 17th century.
        It represents one of the earliest problems in probability theory and has applications in:
        - Economics and Finance
        - Statistical Physics
        - Population Genetics
        - Risk Management
        """)
    
    # Tab 2: Mathematical Analysis
    with tab2:
        st.header("Mathematical Model")
        
        # Basic probability explanation
        st.subheader("Basic Probability")
        st.write("""
        In each game:
        - Probability of winning: p
        - Probability of losing: q = 1-p
        - Amount won/lost per game: ±1 unit
        """)
        
        # Formula explanation
        st.subheader("Probability of Ruin")
        st.latex(r"""
        P(\text{ruin}) = \begin{cases} 
        \frac{1-(\frac{q}{p})^n}{1-(\frac{q}{p})^N} & \text{if } p \neq q \\
        \frac{n}{N} & \text{if } p = q
        \end{cases}
        """)
        
        st.write("""
        Where:
        - n: initial fortune
        - N: casino's fortune (typically N → ∞)
        - p: probability of winning each game
        - q: probability of losing each game
        """)
        
        # Special cases
        st.subheader("Special Cases")
        st.write("""
        1. Fair Game (p = q = 0.5):
           - Ruin is certain as N → ∞
           - Probability of ruin = n/N
        
        2. Unfavorable Game (p < 0.5):
           - Ruin is certain as N → ∞
        
        3. Favorable Game (p > 0.5):
           - Probability of ruin < 1
           - Still possible to lose everything
        """)
        
        # In Tab 2: Mathematical Analysis
        st.markdown("#### Advanced Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Expected Duration Analysis**")
            st.latex(r"""
            E[T|i] = \begin{cases}
            \frac{i(n-i)}{p-q} & \text{if } p \neq q \\
            i(n-i) & \text{if } p = q
            \end{cases}
            """)
        
        with col2:
            st.markdown("**Variance Analysis**")
            st.latex(r"""
            Var[T|i] = \begin{cases}
            \frac{i(n-i)((n+i)-2i)}{(p-q)^2} & \text{if } p \neq q \\
            i(n-i)(n+i-2) & \text{if } p = q
            \end{cases}
            """)
    
    # Tab 3: Interactive Demo (without loan)
    with tab3:
        st.markdown("##### Interactive Probability Visualization")  
        
        # Parameters in two columns
        col1, col2 = st.columns(2)
        with col1:
            p = st.slider("Win Probability (p)", 0.0, 1.0, 0.5, 0.01)
            initial_fortune = st.slider("Starting amount (i)", 1, 100, 50)
        
        with col2:
            target_fortune = st.slider("Goal amount (n)", 60, 200, 112)
            bet_size = st.slider("Bet Size (j)", 1, 100, 1)
        
        # Current settings in horizontal layout with smaller text
        st.markdown("""
        <div style='display: flex; justify-content: space-between; font-size: 0.9em;'>
            <div>Win Probability: {:.2f}</div>
            <div>Starting amount: ${}</div>
            <div>Goal amount: ${}</div>
            <div>Bet Size: ${}</div>
            <div>Total payout: ${}</div>
        </div>
        """.format(p, initial_fortune, target_fortune, bet_size, target_fortune - initial_fortune), unsafe_allow_html=True)
        
        # Game status message before the plot
        if p < 0.5:
            st.error("Unfavorable game - ruin is mathematically certain in the long run.")
        elif p > 0.5:
            st.success("Favorable game - but ruin is still possible!")
        else:
            st.info("Fair game - in the long run, total loss is likely.")
        
        # Visualization with reduced size
        fig, ax = plt.subplots(figsize=(8, 3))  # Reduced height
        x = np.linspace(1, initial_fortune * 2, 100)
        y = calculate_ruin_probability(p, x, target_fortune)
        
        ax.plot(x, y, 'b-', label='Probability of Ruin')
        ax.axvline(x=initial_fortune, color='r', linestyle='--', label='Current Position')
        ax.fill_between(x, y, alpha=0.2)
        
        ax.set_xlabel('Initial Fortune ($)', fontsize=10)
        ax.set_ylabel('Probability of Ruin', fontsize=10)
        ax.set_title('Ruin Probability vs Initial Fortune', fontsize=10, pad=5)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
        
        plt.tight_layout()
        
        # Display plot with less padding
        st.pyplot(fig, use_container_width=True)
        
        # Add spacing between plot and matrix
        st.markdown("---")
        
        # Add number of states slider
        num_states = st.slider("Number of States", 4, 10, 4)
        
        # Define transition matrix P with dynamic size
        P = np.zeros((num_states, num_states))
        
        # Set absorbing states (first and last states)
        P[0, 0] = 1.0
        P[-1, -1] = 1.0
        
        # Set transition probabilities for intermediate states
        for i in range(1, num_states-1):
            P[i, i-1] = p
            P[i, i+1] = 1-p
        
        # Display matrices in two columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Current State (P)**")
            st.write(pd.DataFrame(
                P,
                columns=[f'State {i}' for i in range(num_states)],
                index=[f'State {i}' for i in range(num_states)]
            ).style.format("{:.3f}"))

        with col2:
            power = st.slider("Matrix Power", 1, 50, 10)
            P_power = np.linalg.matrix_power(P, power)
            st.markdown(f"**P^{power}**")
            st.write(pd.DataFrame(
                P_power,
                columns=[f'State {i}' for i in range(num_states)],
                index=[f'State {i}' for i in range(num_states)]
            ).style.format("{:.3f}"))

    # Tab 4: Interactive Demo (with loan)
    with tab4:
        st.markdown("##### Interactive Probability Visualization (with loan)")
        
        # Parameters in three columns for better organization
        col1, col2, col3 = st.columns(3)
        with col1:
            p = st.slider("Win Probability (p)", 0.0, 1.0, 0.5, 0.01, key="p_loan")
            initial_fortune = st.slider("Starting amount (i)", 1, 100, 50, key="i_loan")
        
        with col2:
            target_fortune = st.slider("Goal amount (n)", 60, 200, 112, key="n_loan")
            credit_limit = st.slider("Credit limit (k)", 0, 100, 20, key="k_loan")
        
        with col3:
            max_bet = st.slider("Maximum bet (m)", 1, 100, 10, key="m_loan")
            bet_multiplier = st.slider("Losing streak multiplier", 1.0, 5.0, 2.0, 0.1, key="multiplier")

        # Current settings in horizontal layout
        st.markdown("""
        <div style='display: flex; justify-content: space-between; font-size: 0.9em;'>
            <div>Win Probability: {:.2f}</div>
            <div>Starting amount: ${}</div>
            <div>Goal amount: ${}</div>
            <div>Credit limit: ${}</div>
            <div>Max bet: ${}</div>
            <div>Bet multiplier: {:.1f}x</div>
        </div>
        """.format(p, initial_fortune, target_fortune, credit_limit, max_bet, bet_multiplier), 
        unsafe_allow_html=True)

        # Add strategy explanation
        st.markdown("""
        **Betting Strategy:**
        - Start with base bet of $1
        - On each loss, multiply bet by {:.1f} (up to max bet of ${})
        - Can borrow up to ${} when fortune reaches 0
        """.format(bet_multiplier, max_bet, credit_limit))
        
        # Game status message with loan consideration
        if p < 0.5:
            st.error("""⚠️ High Risk Strategy:
            - Unfavorable odds (p < 0.5)
            - Increasing bets during losing streaks
            - Potential to accumulate significant debt""")
        elif p > 0.5:
            st.success("""✓ Potentially Profitable:
            - Favorable odds (p > 0.5)
            - Credit line provides safety net
            - But beware of maximum loss = initial fortune + credit limit""")
        else:
            st.info("""ℹ️ Fair Game with Increased Risk:
            - Even odds (p = 0.5)
            - Martingale strategy is risky
            - Credit line increases potential losses""")
        
        # Enhanced visualization with loan impact
        fig, ax = plt.subplots(figsize=(8, 3))
        x = np.linspace(1, initial_fortune * 2, 100)
        y_no_loan = calculate_ruin_probability(p, x, target_fortune)
        y_with_loan = calculate_ruin_probability_with_loan(p, x, target_fortune, credit_limit, max_bet)
        
        ax.plot(x, y_no_loan, 'b--', label='Without Loan', alpha=0.5)
        ax.plot(x, y_with_loan, 'r-', label='With Loan')
        ax.axvline(x=initial_fortune, color='g', linestyle='--', label='Current Position')
        ax.fill_between(x, y_with_loan, alpha=0.2, color='red')
        
        ax.set_xlabel('Initial Fortune ($)', fontsize=10)
        ax.set_ylabel('Probability of Ruin', fontsize=10)
        ax.set_title('Ruin Probability Comparison (with vs without loan)', fontsize=10, pad=5)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

        # After the existing visualization in Tab 4
        st.markdown("---")
        st.markdown("#### Monte Carlo Simulation")
        
        col1, col2 = st.columns(2)
        with col1:
            num_simulations = st.slider("Number of simulations", 100, 1000, 500, key="num_sims_loan")
        with col2:
            if st.button("Run Simulations"):
                results = run_simulations(
                    num_simulations, initial_fortune, target_fortune,
                    p, credit_limit, max_bet, bet_multiplier
                )
                
                # Display results
                cols = st.columns(4)
                cols[0].metric("Win Rate", f"{results['win_rate']:.1%}")
                cols[1].metric("Avg. Duration", f"{results['avg_duration']:.1f}")
                cols[2].metric("Max Loss", f"${results['max_loss']:.0f}")
                cols[3].metric("Expected Value", 
                             f"${(2*p-1)*bet_size:.2f}/bet")
                
                # Plot simulation paths
                fig = go.Figure()
                for path in results['paths'][:10]:  # Plot first 10 paths
                    fig.add_trace(go.Scatter(
                        y=path,
                        mode='lines',
                        opacity=0.3
                    ))
                fig.add_hline(y=target_fortune, line_dash="dash", 
                             annotation_text="Target")
                fig.add_hline(y=-credit_limit, line_dash="dash", 
                             annotation_text="Credit Limit")
                fig.update_layout(
                    title="Sample Paths",
                    xaxis_title="Steps",
                    yaxis_title="Fortune ($)",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

def calculate_ruin_probability(p, n, N):
    q = 1 - p
    if p == 0.5:
        return n/N
    else:
        return (1 - (q/p)**n)/(1 - (q/p)**N)

def calculate_ruin_probability_with_loan(p, n, N, k, m):
    """
    Calculate ruin probability with credit line and maximum bet
    p: win probability
    n: initial fortune
    N: target fortune
    k: credit limit
    m: maximum bet allowed
    """
    q = 1 - p
    if p == 0.5:
        return np.maximum(0, (n + k)/(N + k))
    else:
        return np.maximum(0, (1 - (q/p)**n)/(1 - (q/p)**(N+k)))

def run_simulations(num_sims, initial, target, p, credit_limit, max_bet, multiplier):
    results = {
        'wins': 0,
        'durations': [],
        'max_losses': [],
        'paths': []
    }
    
    for _ in range(num_sims):
        fortune = initial
        steps = 0
        current_bet = 1
        losing_streak = 0
        min_fortune = fortune
        path = [fortune]
        
        while fortune > -credit_limit and fortune < target:
            steps += 1
            # Adjust bet size based on losing streak
            current_bet = min(max_bet, 1 * (multiplier ** losing_streak))
            
            if np.random.random() < p:
                fortune += current_bet
                losing_streak = 0
            else:
                fortune -= current_bet
                losing_streak += 1
            
            min_fortune = min(min_fortune, fortune)
            path.append(fortune)
        
        results['paths'].append(path)
        results['durations'].append(steps)
        results['max_losses'].append(abs(min(0, min_fortune)))
        if fortune >= target:
            results['wins'] += 1
    
    results['win_rate'] = results['wins'] / num_sims
    results['avg_duration'] = np.mean(results['durations'])
    results['max_loss'] = max(results['max_losses'])
    
    return results

# Remove the chat interface code from Tab 3
# Instead, create a function to handle chat messages globally

def handle_chat_message(message: str) -> None:
    """
    Handle incoming chat messages from the floating chat box
    """
    if message:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": message})
        
        # Get current game state from any page
        game_state = {
            "win_probability": 0.5,  # Default value
            "initial_fortune": 50,   # Default value
            "current_fortune": 50,   # Default value
            "has_loan": False
        }
        
        # Get AI response
        response = get_chat_response(message, game_state)
        
        # Add AI response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response["response"]})
        
        # Update chat display
        update_chat_display()

def update_chat_display() -> None:
    """
    Update the floating chat box display
    """
    chat_body = ""
    for msg in st.session_state.chat_history[-5:]:  # Show last 5 messages
        role_class = "user-msg" if msg["role"] == "user" else "assistant-msg"
        chat_body += f"<div class='{role_class}'>{msg['content']}</div>"
    
    st.markdown(f"""
    <script>
        document.getElementById('chat-body').innerHTML = `{chat_body}`;
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_introduction() 