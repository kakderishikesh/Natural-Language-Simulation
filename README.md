# Natural Language Simulation (DES)

An experimental project that integrates **Natural Language Processing** with **Discrete Event Simulation** using SimPy. This system allows you to query simulation models using natural language and get human-readable results.

## 🌟 Features

- **🔗 API-Hosted Simulation**: FastAPI web service that wraps the SimPy simulation model
- **🤖 AI Agent**: Natural language query processing and parameter extraction
- **📊 Automatic Analysis**: Converts simulation results into human-readable insights
- **🎯 Interactive Interface**: Command-line interface for real-time queries
- **📖 Auto-Documentation**: OpenAPI/Swagger documentation for the API

## 🏗️ System Architecture

```
Natural Language Query → AI Agent → Parameter Extraction → API Call → Simulation → Results → Natural Language Response
```

The system consists of:

1. **Backend Package** (`Backend/`): Core backend components
   - **Simulation Core** (`Backend/simulation.py`): Original SimPy-based queueing system simulation
   - **API Server** (`Backend/simulation_api.py`): FastAPI wrapper that hosts the simulation
   - **AI Agent** (`Backend/ai_agent.py`): Natural language processing and API interaction
   - **API Tests** (`Backend/test_api.py`): Comprehensive API testing suite
2. **Demo Interface** (`demo.py`): Complete demonstration of the system

## 🚀 Quick Start

### Installation

1. Clone the repository and navigate to the project directory
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the System

#### Option 1: OpenAI Assistant Integration (Primary Use Case)
1. **Start the Backend API:**
   ```bash
   python Backend/simulation_api.py
   ```
2. **Configure your OpenAI Assistant** with the function schema (see Backend/README.md)
3. **Chat with your assistant** using natural language queries!

#### Option 2: Complete Demo (Standalone Testing)
```bash
python demo.py
```
This starts the API server and provides an interactive menu with options to:
- Run the AI agent interactively
- Test with pre-written demo queries
- Test the API directly

#### Option 2: Manual Setup

1. **Start the API Server:**
   ```bash
   python Backend/simulation_api.py
   ```
   The API will be available at `http://localhost:8000`
   
2. **Run the AI Agent:**
   ```bash
   python Backend/ai_agent.py
   ```

#### Option 3: API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation

## 🗣️ Natural Language Queries

The AI agent understands various query formats:

### Example Queries:
- "What if x is 5 and y is 3 and the simulation run is 1000 minutes?"
- "How would the stats look if x=8, y=2, and simulation time is 500 minutes?"
- "Run simulation with activation threshold 10, deactivation threshold 4, for 2000 minutes"
- "What happens when x equals 6 and y equals 2 and we run for 1500 mins?"

### Parameters:
- **x**: Queue length threshold to activate WS2 (workstation 2)
- **y**: Queue length threshold to deactivate WS2 
- **simulation_time**: Duration of simulation in minutes (after 20-minute warm-up)

## 📊 Example Response

```
Based on your query: "What if x is 5 and y is 3 and the simulation run is 1000 minutes?"

I extracted the following parameters:
- x (WS2 activation threshold): 5
- y (WS2 deactivation threshold): 3  
- Simulation duration: 1000 minutes

Simulation completed with x=5, y=3 over 1000 minutes.

Performance Summary:
- Average time entities spent in the system: 12.45 minutes
- Average queue waiting time: 6.78 minutes  
- System processed 189 entities
- Throughput: 11.34 entities per hour
- Time in system ranged from 6.23 to 28.91 minutes

Key Performance Indicators:
• **System Efficiency**: Entities spent an average of 12.45 minutes in the system
• **Queue Performance**: Average waiting time was 6.78 minutes
• **Throughput**: The system processed 11.34 entities per hour
• **Volume**: 189 entities were processed during the simulation

The adaptive workstation strategy (activating WS2 at 5 entities, deactivating below 3) helped manage the workload efficiently.
```

## 🔧 API Endpoints

### `POST /simulate`
Run a simulation with specified parameters

**Request:**
```json
{
  "x": 5,
  "y": 3,
  "simulation_time": 1000
}
```

**Response:**
```json
{
  "parameters": {"x": 5, "y": 3, "simulation_time": 1000},
  "results": {
    "average_time_in_system": 12.45,
    "min_time_in_system": 6.23,
    "max_time_in_system": 28.91,
    "average_queue_time": 6.78,
    "total_entities_processed": 189,
    "throughput_per_hour": 11.34
  },
  "summary": "Detailed human-readable summary..."
}
```

### `GET /health`
Check if the simulation service is running

### `GET /`
Get API information and version

## 🎯 Use Cases

This system is perfect for:

- **Simulation Analysis**: Quick "what-if" scenario testing
- **Educational Purposes**: Teaching discrete event simulation concepts
- **Research**: Experimenting with NLP + simulation integration
- **Prototyping**: Testing different simulation parameters efficiently
- **Business Analysis**: Non-technical stakeholders can query simulations

## 🤖 OpenAI Assistant Integration

This system is designed to work with OpenAI Assistants for natural language querying.

### **Assistant Configuration:**
- **Assistant Name**: Simulation Helper
- **Assistant ID**: `asst_w0IWjdDaqYwYxCFrriBNXjc5`
- **Model**: GPT-4o
- **API Integration**: Calls local simulation API at `http://localhost:8000`

### **Setup Instructions:**

1. **Configure Function in OpenAI Assistant:**
   - Add a new function called `run_simulation`
   - Use the schema provided in `Backend/README.md`
   - Function should make HTTP POST requests to your local API

2. **Update System Instructions:**
   ```
   You are a Natural Language Simulation Assistant specialized in discrete event simulation analysis. 
   
   Your role is to:
   1. Help users understand and run queueing system simulations
   2. Extract simulation parameters (x, y, simulation_time) from natural language queries
   3. Call the simulation API and interpret results in a user-friendly way
   4. Provide insights about system performance, throughput, and queue behavior
   
   When users ask simulation questions, extract the parameters and use the run_simulation function.
   ```

3. **Start Your Backend:**
   ```bash
   python Backend/simulation_api.py
   ```

4. **Test with Natural Language:**
   - "What if x is 7 and y is 3 and simulation runs for 1000 minutes?"
   - "How would the system perform with activation threshold 10, deactivation threshold 4, over 500 minutes?"

### **Environment Variables:**
Create a `.env` file with:
```
ASSISTANT_ID=asst_w0IWjdDaqYwYxCFrriBNXjc5
OPENAI_API_KEY=sk-proj-...
```

## 🔮 Future Enhancements

- Advanced OpenAI integration with GPT-4 Vision for visualization
- Support for more complex simulation parameters
- Real-time streaming of simulation results
- Web-based user interface
- Simulation result visualization and charts
- Parameter optimization using ML
- Support for multiple simulation models
- Integration with OpenAI Code Interpreter for data analysis

## 📋 Dependencies

- **SimPy**: Discrete event simulation framework
- **FastAPI**: Modern web framework for APIs
- **Uvicorn**: ASGI server for FastAPI
- **Requests**: HTTP library for API calls
- **NumPy**: Numerical computations
- **Pydantic**: Data validation and parsing

## 🤝 Contributing

This is an experimental project. Feel free to:
- Add new natural language patterns
- Improve the parameter extraction logic
- Add support for more simulation models
- Enhance the response formatting
- Add visualization capabilities

## 📄 License

[Add your license here]
