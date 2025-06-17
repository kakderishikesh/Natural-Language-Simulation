from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulation import run_simulation
import numpy as np
from typing import Dict, Any

app = FastAPI(title="Natural Language Simulation API", version="1.0.0")

# Add CORS middleware for OpenAI Assistant integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    x: int
    y: int
    simulation_time: int

class SimulationResponse(BaseModel):
    parameters: Dict[str, int]
    results: Dict[str, Any]
    summary: str

@app.get("/")
def read_root():
    return {"message": "Natural Language Simulation API", "version": "1.0.0"}

@app.post("/simulate", response_model=SimulationResponse)
def run_simulation_endpoint(request: SimulationRequest):
    """
    Run a discrete event simulation with specified parameters
    
    - **x**: Queue length threshold to activate WS2
    - **y**: Queue length threshold to deactivate WS2  
    - **simulation_time**: Duration of simulation in minutes (after 20-min warm-up)
    """
    # Validate parameters first
    if request.x <= 0 or request.y <= 0 or request.simulation_time <= 0:
        raise HTTPException(status_code=400, detail="All parameters must be positive integers")
    
    if request.x <= request.y:
        raise HTTPException(status_code=400, detail="x should be greater than y for meaningful control")
    
    try:
        
        # Run simulation
        stats = run_simulation(request.x, request.y, request.simulation_time)
        
        # Calculate results
        if len(stats.time_in_system) == 0:
            raise HTTPException(status_code=400, detail="No entities processed. Try increasing simulation time.")
        
        avg_time_in_system = np.mean(stats.time_in_system)
        min_time_in_system = np.min(stats.time_in_system)
        max_time_in_system = np.max(stats.time_in_system)
        avg_queue_time = np.mean(stats.queue_times)
        total_entities = len(stats.time_in_system)
        
        results = {
            "average_time_in_system": round(avg_time_in_system, 2),
            "min_time_in_system": round(min_time_in_system, 2),
            "max_time_in_system": round(max_time_in_system, 2),
            "average_queue_time": round(avg_queue_time, 2),
            "total_entities_processed": total_entities,
            "throughput_per_hour": round(total_entities / (request.simulation_time / 60), 2)
        }
        
        # Create summary
        summary = f"""
        Simulation completed with x={request.x}, y={request.y} over {request.simulation_time} minutes.
        
        Performance Summary:
        - Average time entities spent in the system: {results['average_time_in_system']:.2f} minutes
        - Average queue waiting time: {results['average_queue_time']:.2f} minutes  
        - System processed {results['total_entities_processed']} entities
        - Throughput: {results['throughput_per_hour']:.2f} entities per hour
        - Time in system ranged from {results['min_time_in_system']:.2f} to {results['max_time_in_system']:.2f} minutes
        
        The system automatically activated WS2 when WS1 queue reached {request.x} entities 
        and deactivated it when the queue dropped below {request.y} entities.
        """.strip()
        
        return SimulationResponse(
            parameters={"x": request.x, "y": request.y, "simulation_time": request.simulation_time},
            results=results,
            summary=summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "simulation_ready": True}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port) 