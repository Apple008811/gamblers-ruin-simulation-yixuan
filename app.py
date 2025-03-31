import streamlit as st

# 必须是第一个 Streamlit 命令
st.set_page_config(
    page_title="Gambler's Ruin",
    page_icon="🎲",
    layout="wide"
)

st.sidebar.success("Select a page above.")

st.title("Welcome to Gambler's Ruin Problem Analysis")
st.write("""
This application provides tools for analyzing the Gambler's Ruin problem through:
- Mathematical analysis
- Interactive demonstrations
- API integration
""")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chat_language' not in st.session_state:
    st.session_state.chat_language = "中文"

def main():
    # 创建两列布局
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.image("https://images.unsplash.com/photo-1518893883800-45cd0954574b?auto=format&fit=crop&w=1000&q=80", 
                width=100)
    
    with col2:
        st.title("Gambler's Ruin: Interactive Learning Platform")
    
    st.write("""
    ## Welcome to the Gambler's Ruin Simulation Platform
    
    This interactive platform helps you understand the famous Gambler's Ruin problem 
    through theory, simulation, and hands-on gaming experience.
    
    ### Available Sections:
    
    1. **📚 Introduction**
       - Learn the theoretical foundations
       - Understand the mathematical model
       - Explore interactive visualizations
    
    2. **🔬 Simulation**
       - Run Monte Carlo simulations
       - Analyze different strategies
       - Visualize outcomes
    
    3. **🎮 Game**
       - Play the actual game
       - Test different betting strategies
       - Track your performance
    
    Choose a section from the sidebar to begin your exploration!
    """)

if __name__ == "__main__":
    main() 