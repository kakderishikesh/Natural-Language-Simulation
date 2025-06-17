import streamlit as st
import openai
import json
import os
from typing import Dict, Any
import time

# Configure the page
st.set_page_config(
    page_title="Natural Language Simulation Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'assistant_id' not in st.session_state:
    st.session_state.assistant_id = None
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None

def initialize_openai():
    """Initialize OpenAI client with API key"""
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    assistant_id = st.secrets.get("ASSISTANT_ID") or os.getenv("ASSISTANT_ID")
    
    if not api_key:
        st.error("OpenAI API key not found. Please configure it in Streamlit secrets or environment variables.")
        st.stop()
    
    if not assistant_id:
        st.error("Assistant ID not found. Please configure it in Streamlit secrets or environment variables.")
        st.stop()
    
    client = openai.OpenAI(api_key=api_key)
    st.session_state.assistant_id = assistant_id
    
    return client

def create_thread(client):
    """Create a new conversation thread"""
    try:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        return thread.id
    except Exception as e:
        st.error(f"Error creating thread: {str(e)}")
        return None

def call_simulation_api(x, y, simulation_time):
    """Call the actual simulation API"""
    try:
        import requests
        
        # Log the request
        print(f"🔄 Making API call to simulation backend...")
        print(f"📤 Request: POST https://natural-language-simulation-api.onrender.com/simulate")
        print(f"📤 Payload: {{'x': {x}, 'y': {y}, 'simulation_time': {simulation_time}}}")
        
        response = requests.post(
            "https://natural-language-simulation-api.onrender.com/simulate",
            json={"x": x, "y": y, "simulation_time": simulation_time},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Log the response
        print(f"📥 Response: {response.status_code}")
        print(f"📥 Response body: {response.text[:200]}...")  # First 200 chars
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        print(f"❌ API call failed: {str(e)}")
        return {"error": f"Failed to call simulation API: {str(e)}"}

def send_message(client, thread_id, message):
    """Send message to the assistant and get response with function calling support"""
    try:
        # Add message to thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
        
        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=st.session_state.assistant_id
        )
        
        # Wait for completion and handle function calls
        with st.spinner("Processing your request..."):
            while run.status in ['queued', 'in_progress', 'cancelling']:
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                
                # Handle function calls
                if run.status == 'requires_action':
                    tool_outputs = []
                    
                    for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                        if tool_call.function.name == "run_simulation":
                            # Parse function arguments
                            import json
                            args = json.loads(tool_call.function.arguments)
                            
                            # Show what we're doing
                            st.info(f"🔄 Running simulation with x={args['x']}, y={args['y']}, simulation_time={args['simulation_time']}")
                            
                            # Call the actual API
                            result = call_simulation_api(args['x'], args['y'], args['simulation_time'])
                            
                            # Prepare tool output
                            tool_outputs.append({
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(result)
                            })
                    
                    # Submit tool outputs
                    if tool_outputs:
                        run = client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread_id,
                            run_id=run.id,
                            tool_outputs=tool_outputs
                        )
        
        if run.status == 'completed':
            # Get messages
            messages = client.beta.threads.messages.list(
                thread_id=thread_id
            )
            
            # Get the latest assistant message
            for message in messages.data:
                if message.role == "assistant":
                    return message.content[0].text.value
                    
        elif run.status == 'failed':
            st.error(f"Assistant run failed: {run.last_error}")
            return None
            
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")
        return None

def display_simulation_results(response_text):
    """Parse and display simulation results in a structured way"""
    try:
        # Try to extract structured data if present
        if "average_time_in_system" in response_text:
            st.subheader("Simulation Results")
            
            # Create columns for metrics
            col1, col2, col3 = st.columns(3)
            
            # Extract metrics using simple string parsing
            lines = response_text.split('\n')
            metrics = {}
            
            for line in lines:
                if "Average time entities spent in the system:" in line:
                    metrics['avg_time'] = line.split(':')[1].strip()
                elif "Average queue waiting time:" in line:
                    metrics['avg_queue'] = line.split(':')[1].strip()
                elif "Throughput:" in line and "entities per hour" in line:
                    metrics['throughput'] = line.split(':')[1].strip()
                elif "Total entities processed:" in line:
                    metrics['total_entities'] = line.split(':')[1].strip()
            
            # Display metrics in columns
            with col1:
                if 'avg_time' in metrics:
                    st.metric("Average Time in System", metrics['avg_time'])
                if 'total_entities' in metrics:
                    st.metric("Entities Processed", metrics['total_entities'])
            
            with col2:
                if 'avg_queue' in metrics:
                    st.metric("Average Queue Time", metrics['avg_queue'])
            
            with col3:
                if 'throughput' in metrics:
                    st.metric("Throughput", metrics['throughput'])
        
        # Always show the full response
        st.subheader("Analysis")
        st.write(response_text)
        
    except Exception as e:
        # If parsing fails, just show the response
        st.write(response_text)

def main():
    # Header
    st.title("Natural Language Simulation Assistant")
    st.markdown("**Ask questions about discrete event simulation scenarios in natural language!**")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This assistant helps you run discrete event simulations by understanding natural language queries.
        
        **Example queries:**
        - "What if x is 7 and y is 3 and simulation runs for 1000 minutes?"
        - "How would the system perform with activation threshold 10, deactivation threshold 4, over 500 minutes?"
        - "Run a simulation with x=5, y=2, for 2000 minutes"
        
        **Parameters:**
        - **x**: Queue threshold to activate WS2 (must be > y)
        - **y**: Queue threshold to deactivate WS2 (must be < x)
        - **simulation_time**: Duration in minutes (minimum 10)
        """)
        
        st.header("System Status")
        
        # Check API status
        try:
            import requests
            response = requests.get("https://natural-language-simulation-api.onrender.com/health", timeout=5)
            if response.status_code == 200:
                st.success("Simulation API: Online")
            else:
                st.error("Simulation API: Offline")
        except:
            st.warning("Simulation API: Checking...")
        
        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.session_state.thread_id = None
            st.rerun()
    
    # Initialize OpenAI
    client = initialize_openai()
    
    # Create thread if needed
    if not st.session_state.thread_id:
        thread_id = create_thread(client)
        if not thread_id:
            st.stop()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                display_simulation_results(message["content"])
            else:
                st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about simulation scenarios..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get assistant response
        response = send_message(client, st.session_state.thread_id, prompt)
        
        if response:
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display assistant response
            with st.chat_message("assistant"):
                display_simulation_results(response)
        else:
            st.error("Failed to get response from assistant")

    # Example prompts
    st.subheader("Try these example queries:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Example 1: Basic Simulation"):
            example_prompt = "What if x is 7 and y is 3 and simulation runs for 1000 minutes?"
            st.session_state.messages.append({"role": "user", "content": example_prompt})
            
            response = send_message(client, st.session_state.thread_id, example_prompt)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    with col2:
        if st.button("Example 2: Performance Analysis"):
            example_prompt = "How would the system perform with activation threshold 10, deactivation threshold 4, over 500 minutes?"
            st.session_state.messages.append({"role": "user", "content": example_prompt})
            
            response = send_message(client, st.session_state.thread_id, example_prompt)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()

if __name__ == "__main__":
    main() 