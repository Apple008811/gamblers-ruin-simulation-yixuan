"""
FastAPI application for Gambler's Ruin simulation and analysis.

This module provides endpoints for calculating ruin probabilities,
analyzing betting strategies, and running Monte Carlo simulations
for the Gambler's Ruin problem.
"""

import numpy as np
from typing import Dict, List, Optional, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Gambler's Ruin API",
    description="API for analyzing Gambler's Ruin problem and betting strategies",
    version="1.0.0"
)

class ProbabilityRequest(BaseModel):
    """Request model for probability calculation endpoint.
    
    Attributes:
        initial_fortune (int): Starting amount of money
        target_fortune (int): Target amount to reach
        win_probability (float): Probability of winning each bet
    """
    initial_fortune: int
    target_fortune: int
    win_probability: float

class ChatRequest(BaseModel):
    """Request model for chat endpoint.
    
    Attributes:
        message (str): User's message or query
        language (str): Preferred language for response (default: "English")
        game_state (dict): Current state of the game including probabilities and fortunes
    """
    message: str
    language: str = "English"
    game_state: dict = {
        "win_probability": 0.5,
        "initial_fortune": 50,
        "current_fortune": 50,
        "has_loan": False
    }

@app.post("/calculate_probability")
async def calculate_probability_endpoint(request: ProbabilityRequest) -> Dict[str, Union[float, Dict[str, Union[int, float]]]]:
    """Calculate ruin probability and related statistics.
    
    Args:
        request (ProbabilityRequest): Request containing initial fortune, target fortune, and win probability
        
    Returns:
        Dict containing:
            - ruin_probability (float): Probability of losing all money
            - win_probability (float): Probability of reaching target fortune
            - expected_duration (float): Expected number of bets until game ends
            - parameters (Dict): Input parameters used in calculation
    """
    return calculate_ruin_probability(
        request.initial_fortune,
        request.target_fortune,
        request.win_probability
    )

@app.post("/chat")
async def chat_endpoint(request: ChatRequest) -> Dict[str, Union[str, List[str], Dict[str, str]]]:
    """Provide strategy advice and explanations based on game state.
    
    Args:
        request (ChatRequest): Request containing message, language preference, and game state
        
    Returns:
        Dict containing:
            - response (str): Strategy advice or explanation
            - suggested_actions (List[str]): Recommended actions
            - analysis (Dict): Risk analysis and game statistics
    """
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

def calculate_ruin_probability(initial_fortune: int, target_fortune: int, win_probability: float) -> Dict[str, Union[float, Dict[str, Union[int, float]]]]:
    """Calculate ruin probability and related statistics for Gambler's Ruin problem.
    
    Args:
        initial_fortune (int): Starting amount of money
        target_fortune (int): Target amount to reach
        win_probability (float): Probability of winning each bet
        
    Returns:
        Dict containing:
            - ruin_probability (float): Probability of losing all money
            - win_probability (float): Probability of reaching target fortune
            - expected_duration (float): Expected number of bets until game ends
            - parameters (Dict): Input parameters used in calculation
    """
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
                           win_probability: float, initial_fortune: float) -> Dict[str, Union[str, float, Dict[str, Union[str, float]]]]:
    """Analyze different betting strategies for Gambler's Ruin problem.
    
    Args:
        strategy_type (str): Type of betting strategy ("Martingale", "Kelly", or "Fixed")
        bet_size (float): Initial bet size
        stop_loss (float): Maximum loss limit
        win_probability (float): Probability of winning each bet
        initial_fortune (float): Starting amount of money
        
    Returns:
        Dict containing:
            - strategy (str): Strategy type
            - risk_level (str): Risk assessment ("High", "Medium", "Low")
            - max_bet (float): Maximum bet size
            - max_loss (float): Maximum possible loss
            - recommended_bet_size (float): Recommended bet size
            - parameters (Dict): Input parameters used in analysis
    """
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
                             target_fortune: int, win_probability: float) -> Dict[str, Union[float, int, Dict[str, Union[int, float]]]]:
    """Run Monte Carlo simulation for Gambler's Ruin problem.
    
    Args:
        num_simulations (int): Number of simulations to run
        initial_fortune (int): Starting amount of money
        target_fortune (int): Target amount to reach
        win_probability (float): Probability of winning each bet
        
    Returns:
        Dict containing:
            - win_rate (float): Proportion of simulations reaching target fortune
            - average_duration (float): Average number of bets until game ends
            - max_duration (int): Maximum number of bets in any simulation
            - min_fortune (int): Minimum final fortune across all simulations
            - max_fortune (int): Maximum final fortune across all simulations
            - parameters (Dict): Input parameters used in simulation
    """
    results: List[bool] = []
    durations: List[int] = []
    final_fortunes: List[int] = []
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 