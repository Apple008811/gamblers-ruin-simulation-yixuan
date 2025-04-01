import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Set page config
st.set_page_config(
    page_title="Interactive Demo (With Loan) - Gambler's Ruin",
    page_icon="💰",
    layout="wide"
)

# Custom color scheme
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
custom_cmap = LinearSegmentedColormap.from_list('custom', colors)

def show_navigation():
    st.sidebar.title("Navigation")
    pages = {
        "Home": "1_Home",
        "Introduction": "2_Introduction",
        "Mathematical Analysis": "3_Mathematical_Analysis",
        "Interactive Demo (No Loan)": "4_Interactive_Demo_No_Loan",
        "Interactive Demo (With Loan)": "5_Interactive_Demo_With_Loan",
        "API Demo": "6_API_Demo"
    }
    
    for page_name, page_file in pages.items():
        if st.sidebar.button(page_name):
            st.switch_page(f"{page_file}.py")

def show_interactive_demo_with_loan():
    show_navigation()
    
    st.title("💰 Interactive Demo (with loan)")
    
    col1, col2 = st.columns(2)
    with col1:
        initial_fortune = st.number_input("Initial Fortune ($)", 1, 1000, 100, key="with_loan_initial")
        target_fortune = st.number_input("Target Fortune ($)", initial_fortune + 1, 2000, 200, key="with_loan_target")
        credit_limit = st.number_input("Credit Limit ($)", 0, 1000, 100, key="credit_limit")
    
    with col2:
        win_prob = st.slider("Win Probability", 0.0, 1.0, 0.5, 0.01, key="with_loan_prob")
        max_bet = st.number_input("Maximum Bet ($)", 1, 100, 10, key="max_bet")
        
    # Calculate ruin probability
    if win_prob != 0.5:
        ruin_prob = (1 - (win_prob/(1-win_prob))**(initial_fortune + credit_limit))/(1 - (win_prob/(1-win_prob))**(target_fortune + credit_limit))
    else:
        ruin_prob = (initial_fortune + credit_limit)/(target_fortune + credit_limit)
        
    st.write(f"Probability of Ruin: {ruin_prob:.2%}")
    
    # Risk Analysis
    expected_value = win_prob * max_bet - (1 - win_prob) * max_bet
    st.write(f"Expected Value per Bet: ${expected_value:.2f}")
    
    if expected_value > 0:
        st.success("Strategy is profitable in the long run!")
    elif expected_value < 0:
        st.warning("Strategy is not profitable in the long run.")
    else:
        st.info("Strategy is break-even in the long run.")
    
    # Visualization
    credit_limits = np.arange(0, credit_limit + 1)
    ruin_probs = []
    for limit in credit_limits:
        if win_prob != 0.5:
            ruin_probs.append((1 - (win_prob/(1-win_prob))**(initial_fortune + limit))/(1 - (win_prob/(1-win_prob))**(target_fortune + limit)))
        else:
            ruin_probs.append((initial_fortune + limit)/(target_fortune + limit))
            
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(credit_limits, ruin_probs, color=colors[0])
    ax.set_xlabel("Credit Limit ($)")
    ax.set_ylabel("Probability of Ruin")
    ax.set_title("Ruin Probability vs Credit Limit")
    ax.grid(True)
    st.pyplot(fig)

if __name__ == "__main__":
    show_interactive_demo_with_loan() 