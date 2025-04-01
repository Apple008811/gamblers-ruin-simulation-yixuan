# Gambler's Ruin API

A FastAPI-based service for analyzing the Gambler's Ruin problem, providing probability calculations, strategy analysis, and Monte Carlo simulations.

## Features

- Calculate ruin probabilities and expected durations
- Analyze different betting strategies (Martingale, Kelly, Fixed)
- Run Monte Carlo simulations
- Interactive chat interface for strategy advice
- Bilingual support (English/Chinese)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gamblers-ruin-simulation
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

1. Start the API server:
```bash
uvicorn src.api_demo:app --reload
```

The API will be available at `http://localhost:8000`

2. Access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### 1. Calculate Probability
```python
POST /calculate_probability
{
    "initial_fortune": 50,
    "target_fortune": 100,
    "win_probability": 0.5
}
```

### 2. Chat Interface
```python
POST /chat
{
    "message": "What's the best strategy?",
    "language": "English",  # or "中文"
    "game_state": {
        "win_probability": 0.5,
        "initial_fortune": 50,
        "current_fortune": 50,
        "has_loan": False
    }
}
```

## Example Usage

```python
import requests

# Calculate probability
response = requests.post(
    "http://localhost:8000/calculate_probability",
    json={
        "initial_fortune": 50,
        "target_fortune": 100,
        "win_probability": 0.5
    }
)
print(response.json())

# Get strategy advice
response = requests.post(
    "http://localhost:8000/chat",
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
print(response.json())
```

## API Response Examples

### Probability Calculation Response
```json
{
    "ruin_probability": 0.5,
    "win_probability": 0.5,
    "expected_duration": 5000,
    "parameters": {
        "initial_fortune": 50,
        "target_fortune": 100,
        "win_probability": 0.5
    }
}
```

### Chat Response
```json
{
    "response": "Current win probability > 0.5 suggests a favorable game...",
    "suggested_actions": ["use_kelly", "set_target"],
    "analysis": {
        "risk_level": "moderate",
        "win_probability": 0.6
    }
}
```

## Development

The API is built using:
- FastAPI
- Pydantic
- NumPy

## License

[Your License Here] 