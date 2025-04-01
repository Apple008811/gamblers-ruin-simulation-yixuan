import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Set page config
st.set_page_config(
    page_title="Interactive Demo (No Loan) - Gambler's Ruin",
    page_icon="🎮",
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

def show_interactive_demo_no_loan():
    show_navigation()
    
    st.title("🎮 Interactive Demo (without loan)")
    
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
    
    # Visualization
    fortunes = np.arange(1, target_fortune + 1)
    ruin_probs = []
    for n in fortunes:
        if win_prob != 0.5:
            ruin_probs.append((1 - (win_prob/(1-win_prob))**n)/(1 - (win_prob/(1-win_prob))**target_fortune))
        else:
            ruin_probs.append(n/target_fortune)
            
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(fortunes, ruin_probs, color=colors[0])
    ax.set_xlabel("Initial Fortune ($)")
    ax.set_ylabel("Probability of Ruin")
    ax.set_title("Ruin Probability vs Initial Fortune")
    ax.grid(True)
    st.pyplot(fig)

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
            
            # Plot sample paths
            fig_paths, ax_paths = plt.subplots(figsize=(4, 3))
            for i in range(min(10, len(paths))):
                ax_paths.plot(paths[i], alpha=0.5, color=colors[i % len(colors)])
            ax_paths.set_xlabel("Steps")
            ax_paths.set_ylabel("Fortune ($)")
            ax_paths.set_title("Sample Paths")
            ax_paths.grid(True)
            st.pyplot(fig_paths)

if __name__ == "__main__":
    show_interactive_demo_no_loan() 