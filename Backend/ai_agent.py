import re
import requests
import json
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class SimulationQuery:
    x: int
    y: int
    simulation_time: int
    confidence: float

class NaturalLanguageSimulationAgent:
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        
    def extract_parameters(self, query: str) -> Optional[SimulationQuery]:
        """
        Extract simulation parameters from natural language query
        """
        query = query.lower().strip()
        
        # Initialize parameters
        x, y, simulation_time = None, None, None
        confidence = 0.0
        
        # Patterns for extracting x parameter
        x_patterns = [
            r'x\s*(?:is|=|equals?)\s*(\d+)',
            r'x\s*(\d+)',
            r'threshold\s*(?:is|=|equals?)\s*(\d+)',
            r'activate\s*(?:at|when)\s*(\d+)',
            r'upper\s*(?:threshold|limit)\s*(?:is|=|equals?)\s*(\d+)'
        ]
        
        # Patterns for extracting y parameter
        y_patterns = [
            r'y\s*(?:is|=|equals?)\s*(\d+)',
            r'y\s*(\d+)',
            r'deactivate\s*(?:at|when|below)\s*(\d+)',
            r'lower\s*(?:threshold|limit)\s*(?:is|=|equals?)\s*(\d+)'
        ]
        
        # Patterns for extracting simulation time
        time_patterns = [
            r'simulation\s*(?:time|run|duration)\s*(?:is|=|equals?|of)\s*(\d+)\s*(?:min|minute|minutes)',
            r'run\s*(?:for|is|of)\s*(\d+)\s*(?:min|minute|minutes)',
            r'(\d+)\s*(?:min|minute|minutes)\s*(?:simulation|run)',
            r'time\s*(?:is|=|equals?)\s*(\d+)\s*(?:min|minute|minutes)',
            r'duration\s*(?:is|=|equals?)\s*(\d+)\s*(?:min|minute|minutes)'
        ]
        
        # Extract x
        for pattern in x_patterns:
            match = re.search(pattern, query)
            if match:
                x = int(match.group(1))
                confidence += 0.3
                break
        
        # Extract y
        for pattern in y_patterns:
            match = re.search(pattern, query)
            if match:
                y = int(match.group(1))
                confidence += 0.3
                break
        
        # Extract simulation time
        for pattern in time_patterns:
            match = re.search(pattern, query)
            if match:
                simulation_time = int(match.group(1))
                confidence += 0.4
                break
        
        # If we couldn't extract all parameters, try alternative extraction
        if not all([x, y, simulation_time]):
            # Look for any numbers in the query and try to infer their meaning
            numbers = re.findall(r'\b(\d+)\b', query)
            if len(numbers) >= 3:
                # Assume order: x, y, simulation_time
                x = x or int(numbers[0])
                y = y or int(numbers[1])
                simulation_time = simulation_time or int(numbers[2])
                confidence = max(confidence, 0.6)
        
        if all([x, y, simulation_time]):
            return SimulationQuery(x=x, y=y, simulation_time=simulation_time, confidence=confidence)
        
        return None
    
    def validate_parameters(self, params: SimulationQuery) -> Tuple[bool, str]:
        """
        Validate extracted parameters
        """
        if params.x <= 0 or params.y <= 0 or params.simulation_time <= 0:
            return False, "All parameters must be positive integers"
        
        if params.x <= params.y:
            return False, "x (activation threshold) should be greater than y (deactivation threshold)"
        
        if params.simulation_time < 10:
            return False, "Simulation time should be at least 10 minutes for meaningful results"
            
        return True, "Parameters are valid"
    
    def run_simulation(self, params: SimulationQuery) -> Dict:
        """
        Send request to simulation API
        """
        try:
            response = requests.post(
                f"{self.api_base_url}/simulate",
                json={
                    "x": params.x,
                    "y": params.y,
                    "simulation_time": params.simulation_time
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API returned status {response.status_code}: {response.text}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to connect to simulation API: {str(e)}"}
    
    def format_response(self, query: str, params: SimulationQuery, simulation_result: Dict) -> str:
        """
        Format the simulation results into a natural language response
        """
        if "error" in simulation_result:
            return f"I encountered an error while running the simulation: {simulation_result['error']}"
        
        summary = simulation_result.get("summary", "")
        results = simulation_result.get("results", {})
        
        response = f"""
Based on your query: "{query}"

I extracted the following parameters:
- x (WS2 activation threshold): {params.x}
- y (WS2 deactivation threshold): {params.y}  
- Simulation duration: {params.simulation_time} minutes

{summary}

Key Performance Indicators:
• **System Efficiency**: Entities spent an average of {results.get('average_time_in_system', 'N/A')} minutes in the system
• **Queue Performance**: Average waiting time was {results.get('average_queue_time', 'N/A')} minutes
• **Throughput**: The system processed {results.get('throughput_per_hour', 'N/A')} entities per hour
• **Volume**: {results.get('total_entities_processed', 'N/A')} entities were processed during the simulation

The adaptive workstation strategy (activating WS2 at {params.x} entities, deactivating below {params.y}) helped manage the workload efficiently.
        """.strip()
        
        return response
    
    def process_query(self, query: str) -> str:
        """
        Main method to process a natural language query end-to-end
        """
        # Extract parameters
        params = self.extract_parameters(query)
        
        if not params:
            return """
I couldn't extract the simulation parameters from your query. Please make sure to specify:
- x (activation threshold for WS2)
- y (deactivation threshold for WS2)  
- simulation time in minutes

Example: "What if x is 5 and y is 7 and the simulation run is 1000 minutes?"
            """.strip()
        
        if params.confidence < 0.5:
            return f"""
I extracted these parameters but I'm not very confident:
- x: {params.x}
- y: {params.y}
- simulation time: {params.simulation_time} minutes

Please confirm if these are correct, or rephrase your query more clearly.
            """.strip()
        
        # Validate parameters
        valid, message = self.validate_parameters(params)
        if not valid:
            return f"Parameter validation failed: {message}"
        
        # Run simulation
        result = self.run_simulation(params)
        
        # Format and return response
        return self.format_response(query, params, result)

def main():
    """
    Interactive command-line interface for the AI agent
    """
    agent = NaturalLanguageSimulationAgent()
    
    print("🤖 Natural Language Simulation AI Agent")
    print("=" * 50)
    print("Ask me questions about simulation scenarios!")
    print("Example: 'What if x is 5 and y is 3 and simulation runs for 1000 minutes?'")
    print("Type 'quit' to exit.\n")
    
    while True:
        try:
            query = input("🔍 Your query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
                
            if not query:
                continue
                
            print("\n🔄 Processing your query...\n")
            response = agent.process_query(query)
            print("🤖 " + response)
            print("\n" + "=" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 