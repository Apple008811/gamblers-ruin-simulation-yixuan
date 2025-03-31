from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional
import numpy as np

# 创建 FastAPI 应用
app = FastAPI(
    title="Gambler's Ruin API",
    description="API for calculating probabilities and analyzing betting strategies",
    version="1.0.0"
)

# API key configuration
API_KEY = "your-secret-key"  # In production, this should be in environment variables

# Data Models
class ProbabilityRequest(BaseModel):
    initial_fortune: float
    target_fortune: float
    win_probability: float

class StrategyRequest(BaseModel):
    initial_fortune: float
    target_fortune: float
    win_probability: float
    bet_multiplier: float

# API key verification
async def verify_api_key(api_key: str = Header(None)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# Add calculation functions
def calculate_ruin_probability(initial_fortune: int, target_fortune: int, win_probability: float) -> dict:
    """Calculate ruin probability and related statistics"""
    q = 1 - win_probability  # failure probability
    if win_probability == 0.5:
        ruin_prob = 1 - (initial_fortune / target_fortune)
    else:
        ruin_prob = ((q/win_probability)**initial_fortune - 1) / ((q/win_probability)**target_fortune - 1)
    
    return {
        "ruin_probability": ruin_prob,
        "win_probability": 1 - ruin_prob,
        "expected_duration": initial_fortune * target_fortune,
        "parameters": {
            "initial_fortune": initial_fortune,
            "target_fortune": target_fortune,
            "win_probability": win_probability
        }
    }

def analyze_betting_strategy(strategy_type: str, bet_size: float, stop_loss: float, 
                           win_probability: float, initial_fortune: float) -> dict:
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

# API endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to Gambler's Ruin API"}

@app.post("/calculate_probability")
async def calculate_probability(request: ProbabilityRequest):
    if request.win_probability <= 0 or request.win_probability >= 1:
        raise HTTPException(status_code=400, detail="Win probability must be between 0 and 1")
    
    if request.win_probability != 0.5:
        ruin_prob = (1 - (request.win_probability/(1-request.win_probability))**request.initial_fortune) / \
                   (1 - (request.win_probability/(1-request.win_probability))**request.target_fortune)
    else:
        ruin_prob = request.initial_fortune/request.target_fortune
    
    expected_duration = request.initial_fortune * request.target_fortune
    
    return {
        "ruin_probability": float(ruin_prob),
        "expected_duration": float(expected_duration)
    }

@app.post("/analyze_strategy")
async def analyze_strategy(request: StrategyRequest):
    if request.bet_multiplier <= 0:
        raise HTTPException(status_code=400, detail="Bet multiplier must be positive")
    
    expected_return = request.initial_fortune * (2 * request.win_probability - 1) * request.bet_multiplier
    
    if expected_return < 0:
        risk_level = "High"
        recommendation = "This strategy is likely to result in losses"
    elif expected_return == 0:
        risk_level = "Medium"
        recommendation = "This strategy is expected to break even"
    else:
        risk_level = "Low"
        recommendation = "This strategy may be profitable"
    
    return {
        "risk_level": risk_level,
        "expected_return": float(expected_return),
        "recommendation": recommendation
    } 