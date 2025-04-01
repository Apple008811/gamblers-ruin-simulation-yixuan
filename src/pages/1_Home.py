import streamlit as st

# Set page config
st.set_page_config(
    page_title="Gambler's Ruin Problem",
    page_icon="🎲",
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

def show_home():
    show_navigation()
    
    st.title("🎲 Welcome to Gambler's Ruin Problem")
    
    st.write("""
    This interactive application explores the classic Gambler's Ruin problem through 
    various lenses: mathematical analysis, interactive simulations, and real-world applications.
    """)
    
    st.header("Navigation")
    st.write("""
    Use the sidebar to navigate through different aspects of the problem:
    
    1. **Introduction**: Basic concepts and problem formulation
    2. **Mathematical Analysis**: Formulas and transition matrix analysis
    3. **Interactive Demo (No Loan)**: Simulate gambling scenarios without credit
    4. **Interactive Demo (With Loan)**: Explore scenarios with credit limits
    5. **API Demo**: Interact with the Gambler's Ruin API
    """)
    
    st.header("Getting Started")
    st.write("""
    We recommend starting with the Introduction page to understand the basic concepts,
    then moving through the mathematical analysis before exploring the interactive demos.
    The API demo is available for developers who want to integrate these calculations
    into their own applications.
    """)

if __name__ == "__main__":
    show_home() 