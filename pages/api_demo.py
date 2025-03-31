import streamlit as st
import numpy as np
from typing import Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
import requests

# Initialize session state at the beginning
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chat_language' not in st.session_state:
    st.session_state.chat_language = "English"

app = FastAPI()

class ProbabilityRequest(BaseModel):
    initial_fortune: int
    target_fortune: int
    win_probability: float

class ChatRequest(BaseModel):
    message: str
    language: str = "English"
    game_state: dict = {
        "win_probability": 0.5,
        "initial_fortune": 50,
        "current_fortune": 50,
        "has_loan": False
    }

@app.post("/calculate_probability")
async def calculate_probability_endpoint(request: ProbabilityRequest):
    return calculate_ruin_probability(
        request.initial_fortune,
        request.target_fortune,
        request.win_probability
    )

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Chat API endpoint that provides strategy advice and explanations"""
    message = request.message.lower()
    lang = request.language
    
    # Strategy advice
    if "strategy" in message or "策略" in message:
        if request.game_state["win_probability"] < 0.5:
            return {
                "response": (
                    "Based on current win probability < 0.5, this is an unfavorable game. Consider:\n"
                    "1. Decreasing your bet size\n"
                    "2. Setting a strict loss limit\n"
                    "3. Avoiding the martingale strategy"
                ) if lang == "English" else (
                    "基于当前胜率小于0.5，这是一个不利的游戏。建议：\n"
                    "1. 降低赌注大小\n"
                    "2. 设置严格的损失限制\n"
                    "3. 避免使用马丁格尔策略"
                ),
                "suggested_actions": ["decrease_bet", "set_loss_limit"],
                "analysis": {
                    "risk_level": "high",
                    "win_probability": request.game_state["win_probability"]
                }
            }
        else:
            return {
                "response": (
                    "Current win probability > 0.5 suggests a favorable game. Consider:\n"
                    "1. Using Kelly criterion for optimal betting\n"
                    "2. Setting a win target\n"
                    "3. Maintaining consistent bet sizes"
                ) if lang == "English" else (
                    "当前胜率大于0.5，这是一个有利的游戏。建议：\n"
                    "1. 使用凯利准则优化下注\n"
                    "2. 设置合理的盈利目标\n"
                    "3. 保持稳定的赌注大小"
                ),
                "suggested_actions": ["use_kelly", "set_target"],
                "analysis": {
                    "risk_level": "moderate",
                    "win_probability": request.game_state["win_probability"]
                }
            }
    
    # Probability explanation
    elif "probability" in message or "概率" in message:
        return {
            "response": (
                f"Current game statistics:\n"
                f"- Win probability: {request.game_state['win_probability']:.2f}\n"
                f"- Expected value per bet: ${(2*request.game_state['win_probability']-1):.2f}"
            ) if lang == "English" else (
                f"当前游戏统计：\n"
                f"- 胜率：{request.game_state['win_probability']:.2f}\n"
                f"- 每次下注期望值：${(2*request.game_state['win_probability']-1):.2f}"
            ),
            "suggested_actions": ["view_math_analysis"],
            "analysis": {
                "risk_level": "info",
                "win_probability": request.game_state["win_probability"]
            }
        }
    
    # Default response
    return {
        "response": (
            "I can help you with:\n"
            "1. Game strategy analysis\n"
            "2. Probability calculations\n"
            "3. Risk assessment\n"
            "What would you like to know?"
        ) if lang == "English" else (
            "我可以帮您：\n"
            "1. 分析游戏策略\n"
            "2. 计算概率\n"
            "3. 评估风险\n"
            "请问您需要了解哪方面的信息？"
        ),
        "suggested_actions": ["view_strategy", "view_probability", "view_risk"],
        "analysis": {
            "risk_level": "info",
            "api_type": "general"
        }
    }

def calculate_ruin_probability(initial_fortune: int, target_fortune: int, win_probability: float) -> Dict:
    """Calculate ruin probability and related statistics"""
    q = 1 - win_probability  # failure probability
    if win_probability == 0.5:
        ruin_prob = 1 - (initial_fortune / target_fortune)
    else:
        ruin_prob = ((q/win_probability)**initial_fortune - 1) / ((q/win_probability)**target_fortune - 1)
    
    return {
        "ruin_probability": ruin_prob,
        "win_probability": 1 - ruin_prob,
        "expected_duration": initial_fortune * target_fortune,  # simplified expected duration
        "parameters": {
            "initial_fortune": initial_fortune,
            "target_fortune": target_fortune,
            "win_probability": win_probability
        }
    }

def analyze_betting_strategy(strategy_type: str, bet_size: float, stop_loss: float, 
                           win_probability: float, initial_fortune: float) -> Dict:
    """Analyze different betting strategies"""
    if strategy_type == "Martingale":
        risk_level = "High"
        max_loss = stop_loss
        max_bet = bet_size * (2 ** (stop_loss // bet_size))
    elif strategy_type == "Kelly":
        edge = 2 * win_probability - 1
        kelly_fraction = edge / 1.0 if edge > 0 else 0
        risk_level = "Medium"
        max_bet = kelly_fraction * initial_fortune
        max_loss = initial_fortune * (1 - kelly_fraction)
    else:  # Fixed
        risk_level = "Low"
        max_bet = bet_size
        max_loss = stop_loss

    return {
        "strategy": strategy_type,
        "risk_level": risk_level,
        "max_bet": max_bet,
        "max_loss": max_loss,
        "recommended_bet_size": min(bet_size, initial_fortune * 0.1),
        "parameters": {
            "strategy_type": strategy_type,
            "initial_bet_size": bet_size,
            "stop_loss": stop_loss,
            "win_probability": win_probability
        }
    }

def run_monte_carlo_simulation(num_simulations: int, initial_fortune: int, 
                             target_fortune: int, win_probability: float) -> Dict:
    """Run Monte Carlo simulation"""
    results = []
    durations = []
    final_fortunes = []
    
    for _ in range(num_simulations):
        fortune = initial_fortune
        steps = 0
        while fortune > 0 and fortune < target_fortune and steps < 1000:
            if np.random.random() < win_probability:
                fortune += 1
            else:
                fortune -= 1
            steps += 1
        results.append(fortune >= target_fortune)
        durations.append(steps)
        final_fortunes.append(fortune)
    
    win_rate = sum(results) / num_simulations
    avg_duration = sum(durations) / num_simulations
    
    return {
        "win_rate": win_rate,
        "average_duration": avg_duration,
        "max_duration": max(durations),
        "min_fortune": min(final_fortunes),
        "max_fortune": max(final_fortunes),
        "parameters": {
            "num_simulations": num_simulations,
            "initial_fortune": initial_fortune,
            "target_fortune": target_fortune,
            "win_probability": win_probability
        }
    }

def show_api_demo():
    st.title("Gambler's Ruin API Demo")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Probability Calculator", "Strategy Analyzer", "Monte Carlo Simulator"])
    
    with tab1:
        st.header("Probability Calculator API")
        col1, col2, col3 = st.columns(3)
        with col1:
            initial_fortune = st.number_input("Initial Fortune", min_value=1, value=50)
        with col2:
            target_fortune = st.number_input("Target Fortune", min_value=1, value=100)
        with col3:
            win_probability = st.slider("Win Probability", 0.0, 1.0, 0.5)
        
        if st.button("Calculate", key="calc_prob"):
            result = calculate_ruin_probability(initial_fortune, target_fortune, win_probability)
            st.json(result)
    
    with tab2:
        st.header("Strategy Analyzer API")
        col1, col2, col3 = st.columns(3)
        with col1:
            strategy_type = st.selectbox("Strategy Type", ["Martingale", "Kelly", "Fixed"])
        with col2:
            bet_size = st.number_input("Initial Bet Size", min_value=1, value=10)
        with col3:
            stop_loss = st.number_input("Stop Loss", min_value=0, value=50)
        
        if st.button("Analyze Strategy", key="analyze_strategy"):
            result = analyze_betting_strategy(strategy_type, bet_size, stop_loss, win_probability, initial_fortune)
            st.json(result)
    
    with tab3:
        st.header("Monte Carlo Simulator API")
        col1, col2 = st.columns(2)
        with col1:
            num_sims = st.number_input("Number of Simulations", min_value=100, value=1000)
        with col2:
            st.write("Using parameters from Probability Calculator")
        
        if st.button("Run Simulation", key="run_sim"):
            result = run_monte_carlo_simulation(num_sims, initial_fortune, target_fortune, win_probability)
            st.json(result)
    
    # API Documentation
    st.markdown("""
    ### API Documentation
    
    ```python
    # Example API Usage
    import requests
    
    # Calculate probability
    response = requests.post(
        "http://api.example.com/calculate_probability",
        json={
            "initial_fortune": 50,
            "target_fortune": 100,
            "win_probability": 0.5
        }
    )
    
    # Analyze strategy
    response = requests.post(
        "http://api.example.com/analyze_strategy",
        json={
            "strategy_type": "Martingale",
            "bet_size": 10,
            "stop_loss": 50,
            "win_probability": 0.5
        }
    )
    
    # Run simulation
    response = requests.post(
        "http://api.example.com/run_simulation",
        json={
            "num_simulations": 1000,
            "initial_fortune": 50,
            "target_fortune": 100,
            "win_probability": 0.5
        }
    )
    ```
    """)

    # Add chat interface in sidebar
    with st.sidebar:
        # Language selection
        selected_lang = st.radio(
            "Language",
            ["English", "中文"],
            horizontal=True,
            key="api_lang_select"
        )
        st.session_state.chat_language = selected_lang
        
        st.markdown("#### " + ("Chat Assistant" if selected_lang == "English" else "聊天助手"))
        
        # Chat input
        user_message = st.chat_input(
            "Ask about APIs..." if selected_lang == "English" else "询问API相关问题..."
        )
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if user_message:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            
            # Get current game state
            game_state = {
                "win_probability": 0.5,
                "initial_fortune": 50,
                "current_fortune": 50,
                "has_loan": False
            }
            
            # Get AI response
            response = get_chat_response(user_message, game_state)
            
            # Add AI response to history
            st.session_state.chat_history.append({"role": "assistant", "content": response["response"]})
            
            # Rerun to update display
            st.rerun()

def get_chat_response(user_message: str, game_state: Dict) -> Dict:
    """
    Rule-based chat response system
    """
    message = user_message.lower()
    current_lang = st.session_state.chat_language
    
    # API-related responses
    if "api" in message or "interface" in message:
        return {
            "response": (
                "We offer the following APIs:\n"
                "1. Basic Probability API\n"
                "2. Strategy Analysis API\n"
                "3. Simulation API\n"
                "Which API would you like to know more about?"
            ) if current_lang == "English" else (
                "我们提供以下API接口：\n"
                "1. 基础概率计算API\n"
                "2. 策略分析API\n"
                "3. 模拟器API\n"
                "您想了解哪个接口的详细信息？"
            ),
            "suggested_actions": ["view_api_docs", "try_api"],
            "analysis": {
                "risk_level": "info",
                "api_type": "overview"
            }
        }
    
    # Default response
    return {
        "response": (
            "I can help you with:\n"
            "1. API documentation\n"
            "2. Usage instructions\n"
            "3. Code examples\n"
            "What would you like to know?"
        ) if current_lang == "English" else (
            "您可以询问：\n"
            "1. API接口说明\n"
            "2. 使用方法\n"
            "3. 示例代码\n"
            "请问您需要了解哪方面的信息？"
        ),
        "suggested_actions": ["view_docs", "view_examples"],
        "analysis": {
            "risk_level": "info",
            "api_type": "general"
        }
    }

st.markdown("""
### API Usage Examples with API Key

```python
import requests

# Set your API key
headers = {
    "api_key": "your-secret-key"
}

# Calculate probability
response = requests.post(
    "http://localhost:8000/calculate_probability",
    headers=headers,
    json={
        "initial_fortune": 50,
        "target_fortune": 100,
        "win_probability": 0.5
    }
)

# Analyze strategy
response = requests.post(
    "http://localhost:8000/analyze_strategy",
    headers=headers,
    json={
        "strategy_type": "Martingale",
        "bet_size": 10,
        "stop_loss": 50,
        "win_probability": 0.5,
        "initial_fortune": 100
    }
)

# Chat API
response = requests.post(
    "http://localhost:8000/chat",
    headers=headers,
    json={
        "message": "What's the best strategy?",
        "language": "English",
        "game_state": {
            "win_probability": 0.6,
            "initial_fortune": 50,
            "current_fortune": 45,
            "has_loan": False
        }
    }
)
```

### Testing the API
1. Start the API server:
```bash
uvicorn api:app --reload
```

2. Make sure to include the API key in all requests
3. The API key should be passed in the headers as shown above
""")

# 展示如何使用 API
st.markdown("""
### Example API Usage:
```python
import requests

headers = {"api_key": "your-secret-key"}
response = requests.post(
    "http://localhost:8000/chat",
    headers=headers,
    json={"message": "Hello"}
)
```
""")

# 提供测试界面
message = st.text_input("Test the chat API:")
if st.button("Send"):
    response = requests.post(
        "http://localhost:8000/chat",
        headers={"api_key": "your-secret-key"},
        json={"message": message}
    )
    st.json(response.json())

if __name__ == "__main__":
    show_api_demo() 