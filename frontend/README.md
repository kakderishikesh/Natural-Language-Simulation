# Natural Language Simulation Assistant - Frontend

A Streamlit web interface that allows users to interact with the Natural Language Simulation Assistant through natural language queries.

## Features

- Interactive chat interface for natural language simulation queries
- Real-time simulation results display with structured metrics
- System status monitoring
- Example queries to get started
- Responsive design with sidebar information

## Setup

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure secrets:
   - Copy `.streamlit/secrets.toml` to your local `.streamlit/secrets.toml`
   - Add your OpenAI API key and Assistant ID

3. Run the application:
```bash
streamlit run app.py
```

### Environment Variables

The app requires these environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `ASSISTANT_ID`: Your OpenAI Assistant ID

## Deployment

### Streamlit Cloud (Recommended)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from the `frontend/` folder
5. Add secrets in the Streamlit Cloud dashboard:
   - `OPENAI_API_KEY`
   - `ASSISTANT_ID`

### Local Network Deployment

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## Usage

1. Enter natural language queries about simulation scenarios
2. View structured results with key performance metrics
3. Use example queries to get started
4. Clear conversation history as needed

### Example Queries

- "What if x is 7 and y is 3 and simulation runs for 1000 minutes?"
- "How would the system perform with activation threshold 10, deactivation threshold 4, over 500 minutes?"
- "Run a simulation with x=5, y=2, for 2000 minutes"

## API Integration

The frontend connects to:
- **Simulation API**: https://natural-language-simulation-api.onrender.com
- **OpenAI Assistant**: Via OpenAI API with function calling

## Security

- API keys are stored securely in Streamlit secrets
- No sensitive data is logged or stored client-side
- HTTPS encryption for all API communications 