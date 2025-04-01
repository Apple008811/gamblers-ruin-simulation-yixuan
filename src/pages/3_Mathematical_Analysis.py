import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Set page config
st.set_page_config(
    page_title="Mathematical Analysis - Gambler's Ruin",
    page_icon="📊",
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

def matrix_power(matrix, power):
    """Calculate the power of a matrix using numpy."""
    if power == 1:
        return matrix
    result = matrix.copy()
    for _ in range(power - 1):
        result = np.dot(result, matrix)
    return result

def show_mathematical_analysis():
    show_navigation()
    
    st.title("📊 Mathematical Analysis")
    
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

    # Add matrix visualization
    fig_matrix, ax_matrix = plt.subplots(figsize=(4, 3))
    im = ax_matrix.imshow(P, cmap=custom_cmap)
    plt.colorbar(im)
    ax_matrix.set_title("Transition Matrix Heatmap")
    ax_matrix.set_xlabel("To State")
    ax_matrix.set_ylabel("From State")
    st.pyplot(fig_matrix)

if __name__ == "__main__":
    show_mathematical_analysis() 