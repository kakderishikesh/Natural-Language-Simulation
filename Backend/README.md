# Backend - Natural Language Simulation System

This is the backend package for the Natural Language Simulation system, containing all core simulation and API components.

## Backend Components

### Core Files:
- **`simulation.py`** - SimPy-based discrete event simulation engine
- **`simulation_api.py`** - FastAPI web server that hosts the simulation
- **`ai_agent.py`** - Local natural language processing agent (standalone)
- **`test_api.py`** - Comprehensive API testing suite

## Running the Backend

### Start the API Server:
```bash
# From project root
python Backend/simulation_api.py

# The API will be available at:
# http://localhost:8000
```

### API Endpoints:
- **Health Check**: `GET /health`
- **API Info**: `GET /`
- **Run Simulation**: `POST /simulate`
- **Documentation**: `GET /docs` (Interactive Swagger UI)

## OpenAI Assistant Integration

### Assistant Configuration:
- **Assistant Name**: Simulation Helper
- **Assistant ID**: `asst_w0IWjdDaqYwYxCFrriBNXjc5`
- **Model**: GPT-4o
- **API Base URL**: `https://natural-language-simulation-api.onrender.com`

### Function Definition for OpenAI Assistant:

```json
{
  "name": "run_simulation",
  "description": "Run a discrete event simulation with specified parameters for a queueing system with two workstations (WS1 and WS2). WS2 is dynamically activated/deactivated based on queue thresholds.",
  "parameters": {
    "type": "object",
    "properties": {
      "x": {
        "type": "integer",
        "minimum": 1,
        "description": "Queue length threshold to activate WS2 (workstation 2). Must be greater than y."
      },
      "y": {
        "type": "integer",
        "minimum": 1,
        "description": "Queue length threshold to deactivate WS2. Must be less than x."
      },
      "simulation_time": {
        "type": "integer",
        "minimum": 10,
        "description": "Duration of simulation in minutes (after 20-minute warm-up period)."
      }
    },
    "required": ["x", "y", "simulation_time"]
  }
}
```

### System Instructions for Assistant:
```
You are a Natural Language Simulation Assistant specialized in discrete event simulation analysis. 

Your role is to:
1. Help users understand and run queueing system simulations
2. Extract simulation parameters (x, y, simulation_time) from natural language queries
3. Call the simulation API and interpret results in a user-friendly way
4. Provide insights about system performance, throughput, and queue behavior

Simulation Parameters:
- x: Queue threshold to activate WS2 (must be > y)
- y: Queue threshold to deactivate WS2 (must be < x)  
- simulation_time: Duration in minutes (minimum 10)

When users ask simulation questions, extract the parameters and use the run_simulation function. Then provide clear, human-readable analysis of the results including performance insights and recommendations.

Example queries you should handle:
- "What if x is 7 and y is 3 and simulation runs for 1000 minutes?"
- "How would the system perform with activation threshold 10, deactivation threshold 4, over 500 minutes?"
- "Run a simulation with x=5, y=2, for 2000 minutes"
```

## API Request/Response Format

### Request Format:
```json
{
  "x": 7,
  "y": 3,
  "simulation_time": 1000
}
```

### Response Format:
```json
{
  "parameters": {"x": 7, "y": 3, "simulation_time": 1000},
  "results": {
    "average_time_in_system": 28.73,
    "min_time_in_system": 0.41,
    "max_time_in_system": 115.07,
    "average_queue_time": 22.82,
    "total_entities_processed": 190,
    "throughput_per_hour": 11.4
  },
  "summary": "Human-readable analysis of simulation results..."
}
```

## Testing the Backend

### Run All Tests:
```bash
python Backend/test_api.py
```

### Manual API Testing:
```bash
# Health check
curl -X GET "http://localhost:8000/health"

# Run simulation
curl -X POST "http://localhost:8000/simulate" \
  -H "Content-Type: application/json" \
  -d '{"x": 7, "y": 3, "simulation_time": 1000}'
```

## Technical Details

### Simulation Model:
- **Arrival Process**: Exponential distribution (mean = 5 minutes)
- **Service Times**: 
  - WS1: Exponential (mean = 6 minutes)
  - WS2: Exponential (mean = 8 minutes)
- **Warm-up Period**: 20 minutes
- **Adaptive Control**: WS2 activation based on queue thresholds

### API Framework:
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation and serialization
- **SimPy**: Discrete event simulation engine

### Error Handling:
- Parameter validation (x > y, positive values)
- Timeout protection (30-second limit)
- Meaningful error messages
- HTTP status code compliance

## Performance Metrics

The simulation tracks and returns:
- **Average time in system**: Total time entities spend in the system
- **Queue waiting time**: Time entities wait in queues
- **Throughput**: Entities processed per hour
- **System utilization**: Min/max processing times
- **Entity volume**: Total entities processed

## Environment Setup

Required environment variables (in `.env`):
```
ASSISTANT_ID=asst_w0IWjdDaqYwYxCFrriBNXjc5
OPENAI_API_KEY=sk-proj-...
```

## Known Issues

- Backend must be started before OpenAI Assistant can call it
- Local hosting requires port 8000 to be available
- Long simulations (>5000 minutes) may timeout

## Future Enhancements

- Dockerization for easy deployment
- Database integration for result storage
- Real-time simulation streaming
- Advanced visualization capabilities
- Multi-model simulation support 