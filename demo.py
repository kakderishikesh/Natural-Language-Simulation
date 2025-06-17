#!/usr/bin/env python3
"""
Demo script for the Natural Language Simulation System

This script demonstrates how to:
1. Start the simulation API server
2. Test the AI agent with natural language queries
"""

import subprocess
import time
import requests
import signal
import sys
from multiprocessing import Process
from Backend.ai_agent import NaturalLanguageSimulationAgent

def start_api_server():
    """Start the FastAPI server"""
    import uvicorn
    from Backend.simulation_api import app
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def wait_for_api(max_attempts=10):
    """Wait for the API server to be ready"""
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ API server is ready!")
                return True
        except requests.exceptions.RequestException:
            if attempt < max_attempts - 1:
                print(f"⏳ Waiting for API server... (attempt {attempt + 1}/{max_attempts})")
                time.sleep(2)
    
    print("❌ API server failed to start")
    return False

def run_demo_queries():
    """Run some demo queries to show the system in action"""
    agent = NaturalLanguageSimulationAgent()
    
    demo_queries = [
        "What if x is 5 and y is 3 and the simulation run is 1000 minutes?",
        "How would the stats look if x=8, y=2, and simulation time is 500 minutes?",
        "Run simulation with activation threshold 10, deactivation threshold 4, for 2000 minutes",
        "What happens when x equals 6 and y equals 2 and we run for 1500 mins?"
    ]
    
    print("\n🎯 Running Demo Queries")
    print("=" * 60)
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n📝 Demo Query #{i}: {query}")
        print("-" * 40)
        
        try:
            response = agent.process_query(query)
            print("🤖 AI Agent Response:")
            print(response)
        except Exception as e:
            print(f"❌ Error processing query: {str(e)}")
        
        print("\n" + "=" * 60)
        
        if i < len(demo_queries):
            input("Press Enter to continue to next demo query...")

def main():
    print("🚀 Natural Language Simulation System Demo")
    print("=" * 50)
    
    # Start API server in background
    print("🔄 Starting API server...")
    server_process = Process(target=start_api_server)
    server_process.start()
    
    try:
        # Wait for server to be ready
        if not wait_for_api():
            return
        
        print("\n🌐 API Server is running at: http://localhost:8000")
        print("📖 API Documentation available at: http://localhost:8000/docs")
        
        while True:
            print("\n🎮 Choose an option:")
            print("1. Run interactive AI agent")
            print("2. Run demo queries")
            print("3. Test API directly")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                print("\n🤖 Starting Interactive AI Agent...")
                print("Type your natural language queries below:")
                from Backend.ai_agent import main as agent_main
                agent_main()
                
            elif choice == "2":
                run_demo_queries()
                
            elif choice == "3":
                print("\n🔧 Testing API directly...")
                test_api_directly()
                
            elif choice == "4":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user")
    
    finally:
        print("🔄 Shutting down API server...")
        server_process.terminate()
        server_process.join()
        print("✅ Demo completed!")

def test_api_directly():
    """Test the API directly with HTTP requests"""
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get("http://localhost:8000/health")
        print(f"Health check: {response.json()}")
        
        # Test simulation endpoint
        print("\nTesting simulation endpoint...")
        test_data = {"x": 5, "y": 3, "simulation_time": 100}
        response = requests.post("http://localhost:8000/simulate", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Simulation completed successfully!")
            print(f"Parameters: {result['parameters']}")
            print(f"Results: {result['results']}")
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")

if __name__ == "__main__":
    main() 