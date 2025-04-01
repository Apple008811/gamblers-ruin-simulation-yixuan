import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
from matplotlib.colors import LinearSegmentedColormap

# Set page config
st.set_page_config(
    page_title="Gambler's Ruin Problem",
    page_icon="🎲",
    layout="wide"
)

# Custom color scheme
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
custom_cmap = LinearSegmentedColormap.from_list('custom', colors)

def matrix_power(matrix, power):
    """Calculate the power of a matrix using numpy."""
    if power == 1:
        return matrix
    result = matrix.copy()
    for _ in range(power - 1):
        result = np.dot(result, matrix)
    return result

def show_introduction():
    st.title("🎲 Gambler's Ruin Problem")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Introduction",
        "Mathematical Analysis",
        "Interactive Demo (without loan)",
        "Interactive Demo (with loan)",
        "API Demo"
    ])
    
    with tab1:
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

    with tab2:
        st.header("Mathematical Analysis")
        st.write("""
        The probability of ruin (R) for a gambler with initial fortune n, 
        target fortune N, and win probability p can be calculated using the formula:
        """)
        
        st.latex(r'''
        R = \begin{cases} 
        \frac{1-(\frac{p}{q})^n}{1-(\frac{p}{q})^N} & \text{if } p \neq q \\
        \frac{n}{N} & \text{if } p = q
        \end{cases}
        ''')
        
        st.write("""
        Where:
        - p is the probability of winning each bet
        - q = 1-p is the probability of losing each bet
        - n is the initial fortune
        - N is the target fortune
        """)

        st.subheader("Transition Matrix Analysis")
        st.write("""
        We can also analyze this problem using a transition matrix. For example, 
        with a maximum fortune of 3, the transition matrix P would be:
        """)
        
        st.latex(r'''
        P = \begin{bmatrix} 
        1 & 0 & 0 & 0 \\
        q & 0 & p & 0 \\
        0 & q & 0 & p \\
        0 & 0 & 0 & 1
        \end{bmatrix}
        ''')

        st.write("""
        This matrix shows:
        - States 0 (ruin) and 3 (target) are absorbing states
        - Other states can transition to adjacent states with probabilities p and q
        """)

        # Interactive matrix analysis
        st.subheader("Interactive Matrix Analysis")
        col1, col2 = st.columns(2)
        with col1:
            states = st.number_input("Number of States", 3, 10, 4, key="matrix_states")
            win_prob_matrix = st.slider("Win Probability", 0.0, 1.0, 0.5, 0.01, key="matrix_prob")
        with col2:
            power = st.number_input("Matrix Power", 1, 100, 1, key="matrix_power")

        # Create transition matrix
        P = np.zeros((states, states))
        P[0,0] = P[-1,-1] = 1  # Absorbing states
        for i in range(1, states-1):
            P[i,i-1] = 1 - win_prob_matrix  # Probability of losing
            P[i,i+1] = win_prob_matrix      # Probability of winning

        # Display initial matrix
        st.write("Initial Transition Matrix:")
        st.write(P)

        # Calculate and display powered matrix
        if power > 1:
            P_n = matrix_power(P, power)
            st.write(f"Transition Matrix after {power} steps:")
            st.write(P_n)

        # Replace matplotlib heatmap with Plotly heatmap
        fig_matrix = go.Figure(data=go.Heatmap(
            z=P,
            colorscale='RdBu',
            zmid=0,
            text=np.round(P, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False,
            showscale=True,
            colorbar=dict(title='Probability')
        ))
        fig_matrix.update_layout(
            title="Transition Matrix Heatmap",
            xaxis_title="To State",
            yaxis_title="From State",
            height=400,
            width=600
        )
        st.plotly_chart(fig_matrix, use_container_width=True)

    with tab3:
        st.header("Interactive Demo (without loan)")
        
        col1, col2 = st.columns(2)
        with col1:
            initial_fortune = st.number_input("Initial Fortune ($)", 1, 1000, 100, key="no_loan_initial")
            target_fortune = st.number_input("Target Fortune ($)", initial_fortune + 1, 2000, 200, key="no_loan_target")
        
        with col2:
            win_prob = st.slider("Win Probability", 0.0, 1.0, 0.5, 0.01, key="no_loan_prob")
            
        if win_prob != 0.5:
            ruin_prob = (1 - (win_prob/(1-win_prob))**initial_fortune)/(1 - (win_prob/(1-win_prob))**target_fortune)
        else:
            ruin_prob = initial_fortune/target_fortune
            
        st.write(f"Probability of Ruin: {ruin_prob:.2%}")
        
        # Calculate fortunes and ruin probabilities for the plot
        fortunes = np.arange(1, target_fortune + 1)
        ruin_probs = []
        for n in fortunes:
            if win_prob != 0.5:
                ruin_probs.append((1 - (win_prob/(1-win_prob))**n)/(1 - (win_prob/(1-win_prob))**target_fortune))
            else:
                ruin_probs.append(n/target_fortune)
        
        # Replace matplotlib line plot with Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fortunes,
            y=ruin_probs,
            mode='lines',
            name='Ruin Probability',
            line=dict(color=colors[0])
        ))
        fig.update_layout(
            title="Ruin Probability vs Initial Fortune",
            xaxis_title="Initial Fortune ($)",
            yaxis_title="Probability of Ruin",
            height=400,
            width=600,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

        # Add simulation feature
        if st.button("Run Simulation", key="sim_button"):
            num_simulations = 1000
            wins = 0
            paths = []
            
            with st.spinner("Running simulation..."):
                for _ in range(num_simulations):
                    fortune = initial_fortune
                    path = [fortune]
                    while fortune > 0 and fortune < target_fortune:
                        if np.random.random() < win_prob:
                            fortune += 1
                        else:
                            fortune -= 1
                        path.append(fortune)
                    paths.append(path)
                    if fortune >= target_fortune:
                        wins += 1
                
                win_rate = wins / num_simulations
                st.success(f"Simulation completed! Win Rate: {win_rate:.2%}")
                
                # Replace matplotlib sample paths plot with Plotly
                fig_paths = go.Figure()
                for i in range(min(10, len(paths))):
                    fig_paths.add_trace(go.Scatter(
                        y=paths[i],
                        mode='lines',
                        name=f'Path {i+1}',
                        line=dict(color=colors[i % len(colors)], width=1)
                    ))
                fig_paths.update_layout(
                    title="Sample Paths",
                    xaxis_title="Steps",
                    yaxis_title="Fortune ($)",
                    height=400,
                    width=600,
                    showlegend=True
                )
                st.plotly_chart(fig_paths, use_container_width=True)

    with tab4:
        st.header("Interactive Demo (with loan)")
        
        col1, col2 = st.columns(2)
        with col1:
            initial_fortune_loan = st.number_input("Initial Fortune ($)", 1, 1000, 100, key="loan_initial")
            target_fortune_loan = st.number_input("Target Fortune ($)", initial_fortune_loan + 1, 2000, 200, key="loan_target")
            credit_limit = st.number_input("Credit Limit ($)", 0, 1000, 50)
        
        with col2:
            win_prob_loan = st.slider("Win Probability", 0.0, 1.0, 0.5, 0.01, key="loan_prob")
            max_bet = st.number_input("Maximum Bet ($)", 1, 100, 10)
            
        total_capital = initial_fortune_loan + credit_limit
        if win_prob_loan != 0.5:
            ruin_prob_loan = (1 - (win_prob_loan/(1-win_prob_loan))**total_capital)/(1 - (win_prob_loan/(1-win_prob_loan))**target_fortune_loan)
        else:
            ruin_prob_loan = total_capital/target_fortune_loan
            
        st.write(f"Probability of Ruin: {ruin_prob_loan:.2%}")
        st.write(f"Maximum Possible Loss: ${total_capital}")

        # Additional analysis for loan scenario
        st.subheader("Risk Analysis")
        expected_value = (2 * win_prob_loan - 1) * max_bet
        st.write(f"Expected Value per Bet: ${expected_value:.2f}")
        
        if expected_value > 0:
            st.write("Strategy: Favorable - Consider larger bets within risk tolerance")
        elif expected_value < 0:
            st.write("Strategy: Unfavorable - Consider reducing bet size or avoiding play")
        else:
            st.write("Strategy: Neutral - Game is fair, but house edge may apply")

        # Replace matplotlib loan scenario plot with Plotly
        fig_loan = go.Figure()
        fig_loan.add_trace(go.Scatter(
            x=credit_limits,
            y=ruin_probs_loan,
            mode='lines',
            name='Ruin Probability',
            line=dict(color=colors[0])
        ))
        fig_loan.update_layout(
            title="Ruin Probability vs Credit Limit",
            xaxis_title="Credit Limit ($)",
            yaxis_title="Probability of Ruin",
            height=400,
            width=600,
            showlegend=True
        )
        st.plotly_chart(fig_loan, use_container_width=True)

    with tab5:
        st.header("API Demo")
        
        st.subheader("Calculate Ruin Probability")
        col1, col2 = st.columns(2)
        with col1:
            api_initial = st.number_input("Initial Fortune ($)", 1, 1000, 100, key="api_initial")
            api_target = st.number_input("Target Fortune ($)", api_initial + 1, 2000, 200, key="api_target")
        with col2:
            api_prob = st.slider("Win Probability", 0.0, 1.0, 0.5, 0.01, key="api_prob")
            
        if st.button("Calculate", key="calc_button"):
            with st.spinner("Calculating..."):
                try:
                    response = requests.post(
                        "http://localhost:8000/calculate_probability",
                        json={
                            "initial_fortune": api_initial,
                            "target_fortune": api_target,
                            "win_probability": api_prob
                        },
                        timeout=5  # Add timeout
                    )
                    response.raise_for_status()  # Raise exception for bad status codes
                    result = response.json()
                    
                    # Create a nice display for results
                    st.success("Calculation completed successfully!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Ruin Probability", f"{result['ruin_probability']:.2%}")
                    with col2:
                        st.metric("Expected Duration", f"{result['expected_duration']:.1f} bets")
                        
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the server. Please check if the API is running.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {str(e)}")
        
        st.subheader("Analyze Strategy")
        col1, col2 = st.columns(2)
        with col1:
            strategy_initial = st.number_input("Initial Fortune ($)", 1, 1000, 100, key="strategy_initial")
            strategy_target = st.number_input("Target Fortune ($)", strategy_initial + 1, 2000, 200, key="strategy_target")
        with col2:
            strategy_prob = st.slider("Win Probability", 0.0, 1.0, 0.5, 0.01, key="strategy_prob")
            bet_multiplier = st.number_input("Bet Multiplier", 0.1, 2.0, 1.0, 0.1)
            
        if st.button("Analyze", key="analyze_button"):
            with st.spinner("Analyzing strategy..."):
                try:
                    response = requests.post(
                        "http://localhost:8000/analyze_strategy",
                        json={
                            "initial_fortune": strategy_initial,
                            "target_fortune": strategy_target,
                            "win_probability": strategy_prob,
                            "bet_multiplier": bet_multiplier
                        },
                        timeout=5
                    )
                    response.raise_for_status()
                    result = response.json()
                    
                    # Create a nice display for results
                    st.success("Analysis completed successfully!")
                    
                    # Display results in a more organized way
                    st.markdown("### Strategy Analysis Results")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Risk Level", result['risk_level'])
                    with col2:
                        st.metric("Expected Return", f"${result['expected_return']:.2f}")
                    with col3:
                        st.info(result['recommendation'])
                        
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the server. Please check if the API is running.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    show_introduction() 