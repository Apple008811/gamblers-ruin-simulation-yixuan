import streamlit as st
import requests
import json

# Set page config
st.set_page_config(
    page_title="API Demo - Gambler's Ruin",
    page_icon="🔌",
    layout="wide"
)

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

def show_api_demo():
    show_navigation()
    
    st.title("🔌 API Demo")
    
    st.write("""
    This page demonstrates how to use the Gambler's Ruin API to calculate probabilities and analyze strategies.
    The API provides endpoints for calculating ruin probabilities and analyzing betting strategies.
    """)
    
    # API Configuration
    st.subheader("API Configuration")
    api_url = st.text_input("API URL", "http://localhost:8000")
    
    # Calculate Ruin Probability
    st.subheader("Calculate Ruin Probability")
    col1, col2 = st.columns(2)
    
    with col1:
        initial_fortune = st.number_input("Initial Fortune ($)", 1, 1000, 100, key="api_initial")
        target_fortune = st.number_input("Target Fortune ($)", initial_fortune + 1, 2000, 200, key="api_target")
    
    with col2:
        win_prob = st.slider("Win Probability", 0.0, 1.0, 0.5, 0.01, key="api_prob")
        bet_multiplier = st.number_input("Bet Multiplier", 1.0, 10.0, 1.0, 0.1, key="bet_multiplier")
    
    if st.button("Calculate"):
        try:
            response = requests.post(
                f"{api_url}/calculate",
                json={
                    "initial_fortune": initial_fortune,
                    "target_fortune": target_fortune,
                    "win_probability": win_prob,
                    "bet_multiplier": bet_multiplier
                },
                timeout=5
            )
            response.raise_for_status()
            result = response.json()
            st.success(f"Probability of Ruin: {result['ruin_probability']:.2%}")
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Please check if the server is running.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {str(e)}")
    
    # Analyze Strategy
    st.subheader("Analyze Strategy")
    col1, col2 = st.columns(2)
    
    with col1:
        strategy_initial = st.number_input("Initial Fortune ($)", 1, 1000, 100, key="strategy_initial")
        strategy_target = st.number_input("Target Fortune ($)", strategy_initial + 1, 2000, 200, key="strategy_target")
    
    with col2:
        strategy_prob = st.slider("Win Probability", 0.0, 1.0, 0.5, 0.01, key="strategy_prob")
        strategy_multiplier = st.number_input("Bet Multiplier", 1.0, 10.0, 1.0, 0.1, key="strategy_multiplier")
    
    if st.button("Analyze"):
        try:
            response = requests.post(
                f"{api_url}/analyze",
                json={
                    "initial_fortune": strategy_initial,
                    "target_fortune": strategy_target,
                    "win_probability": strategy_prob,
                    "bet_multiplier": strategy_multiplier
                },
                timeout=5
            )
            response.raise_for_status()
            result = response.json()
            
            st.success("Strategy Analysis Results:")
            st.write(f"Probability of Ruin: {result['ruin_probability']:.2%}")
            st.write(f"Expected Value per Bet: ${result['expected_value']:.2f}")
            st.write(f"Risk Level: {result['risk_level']}")
            st.write(f"Recommended Action: {result['recommendation']}")
            
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Please check if the server is running.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    show_api_demo() 