# Complete Deployment Guide

This comprehensive guide walks you through deploying the entire Natural Language Simulation system - both backend API and frontend web interface - to make it accessible to anyone on the internet.

## 🏗️ System Architecture

```
Frontend (Streamlit) → OpenAI Assistant → Backend API (FastAPI) → SimPy Simulation
```

## 📋 Prerequisites

- GitHub account with your repository
- Render.com account (free tier available)
- OpenAI API key with credits
- Your OpenAI Assistant ID (create one at platform.openai.com)

## Part 1: Backend Deployment (Render.com)

### Step 1: Prepare Backend Repository

Ensure these files are in your repository root:
- `render.yaml` - Render service configuration
- `runtime.txt` - Python version specification  
- `requirements.txt` - Python dependencies
- `Backend/simulation_api.py` - Your API with CORS enabled

### Step 2: Deploy Backend to Render

#### Option A: Using Render Dashboard (Recommended)

1. **Go to [render.com](https://render.com)** and sign in
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - **Name**: `natural-language-simulation-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python Backend/simulation_api.py`
   - **Plan**: `Free` (or choose paid for better performance)

5. **Add Environment Variables:**
   - `PORT`: `8000` (Render will override this automatically)
   - `HOST`: `0.0.0.0`

6. **Click "Create Web Service"**

#### Option B: Using render.yaml (Automatic)

1. Push the `render.yaml` file to your repository
2. Go to Render dashboard → **"New +"** → **"Blueprint"**
3. Connect your repository and deploy

### Step 3: Get Your Backend API URL

After deployment, Render will provide you with a URL like:
```
https://natural-language-simulation-api-[random].onrender.com
```

**Save this URL** - you'll need it for OpenAI Assistant and frontend configuration.

### Step 4: Test Your Deployed Backend

#### Health Check:
```bash
curl https://your-backend-url.onrender.com/health
```

#### Test Simulation:
```bash
curl -X POST "https://your-backend-url.onrender.com/simulate" \
  -H "Content-Type: application/json" \
  -d '{"x": 7, "y": 3, "simulation_time": 100}'
```

Expected response:
```json
{
  "parameters": {"x": 7, "y": 3, "simulation_time": 100},
  "results": {
    "average_time_in_system": 16.31,
    "average_queue_time": 11.38,
    "total_entities_processed": 50,
    "throughput_per_hour": 10.0
  },
  "summary": "Simulation completed..."
}
```

## Part 2: OpenAI Assistant Configuration

### Step 1: Configure Function in Assistant

1. Go to [platform.openai.com/assistants](https://platform.openai.com/assistants)
2. Find your assistant or create a new one
3. Click **"Edit"** → **"Functions"** → **"Add Function"**

### Step 2: Add Function Definition

**Function Name**: `run_simulation`

**Description**: 
```
Run a discrete event simulation with specified parameters for a queueing system with two workstations. WS2 is dynamically activated/deactivated based on queue thresholds.
```

**Parameters Schema**:
```json
{
  "type": "object",
  "properties": {
    "x": {
      "type": "integer",
      "minimum": 2,
      "description": "Queue length threshold to activate WS2. Must be greater than y."
    },
    "y": {
      "type": "integer",
      "minimum": 1,
      "description": "Queue length threshold to deactivate WS2. Must be less than x."
    },
    "simulation_time": {
      "type": "integer",
      "minimum": 10,
      "description": "Duration of simulation in minutes."
    }
  },
  "required": ["x", "y", "simulation_time"]
}
```

### Step 3: Update System Instructions

```
You are a Natural Language Simulation Assistant specialized in discrete event simulation analysis.

Your role is to:
1. Help users understand and run queueing system simulations
2. Extract simulation parameters (x, y, simulation_time) from natural language queries
3. Call the run_simulation function when users request simulations
4. Interpret results and provide insights about system performance

Simulation Parameters:
- x: Queue threshold to activate WS2 (must be > y, minimum 2)
- y: Queue threshold to deactivate WS2 (must be < x, minimum 1)  
- simulation_time: Duration in minutes (minimum 10)

When users ask for simulation runs, call the run_simulation function with the extracted parameters. Then provide clear analysis of the results including performance insights and recommendations.
```

## Part 3: Frontend Deployment

### Option 1: Streamlit Cloud (Recommended - Free & Easy)

#### Step 1: Prepare Frontend Repository
1. Fork this repository to your GitHub account
2. Ensure the `frontend/` folder contains all necessary files

#### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your forked repository
5. Set the following:
   - **Branch**: `main`
   - **Main file path**: `frontend/app.py`
   - **App URL**: Choose a custom URL (optional)

#### Step 3: Configure Secrets
1. In the Streamlit Cloud dashboard, go to your app settings
2. Click on "Secrets"
3. Add the following secrets:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key-here"
   ASSISTANT_ID = "your-assistant-id-here"
   ```
4. Save the secrets

#### Step 4: Deploy Frontend
1. Click "Deploy"
2. Wait for the deployment to complete
3. Your app will be available at `https://your-app-name.streamlit.app`

### Option 2: Local Development

#### Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pip install -r requirements.txt

# Create local secrets file
cp .streamlit/secrets.toml .streamlit/secrets_local.toml

# Edit the local secrets file with your API key
# OPENAI_API_KEY = "your-actual-api-key"
# ASSISTANT_ID = "your-assistant-id"
```

#### Run Locally
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Option 3: Heroku Deployment

#### Step 1: Prepare Files
Create `frontend/Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

#### Step 2: Deploy
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-frontend-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY="your-api-key"
heroku config:set ASSISTANT_ID="your-assistant-id"

# Deploy
git subtree push --prefix frontend heroku main
```

### Option 4: Docker Deployment

#### Create Dockerfile in frontend/
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

#### Build and Run
```bash
# Build image
docker build -t simulation-frontend .

# Run container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="your-api-key" \
  -e ASSISTANT_ID="your-assistant-id" \
  simulation-frontend
```

## Part 4: Complete System Testing

### Step 1: Verify Backend
```bash
curl -X GET "https://your-backend-url.onrender.com/health"
curl -X POST "https://your-backend-url.onrender.com/simulate" \
  -H "Content-Type: application/json" \
  -d '{"x": 7, "y": 3, "simulation_time": 300}'
```

### Step 2: Test OpenAI Assistant
1. Go to OpenAI Playground
2. Test with: "What if x is 7 and y is 3 and simulation runs for 300 minutes?"
3. Verify it calls the function (not hallucinating)

### Step 3: Test Frontend
1. Open your deployed Streamlit app
2. Ask: "Run a simulation with x=5, y=2, for 1000 minutes"
3. Verify you see:
   - "🔄 Running simulation..." message
   - Real API call logs in terminal (if running locally)
   - Structured results with metrics

## Environment Variables Summary

### Backend (Render.com):
- `PORT`: `8000`
- `HOST`: `0.0.0.0`

### Frontend (Streamlit Cloud):
- `OPENAI_API_KEY`: Your OpenAI API key
- `ASSISTANT_ID`: Your OpenAI Assistant ID

### Local Development:
```env
ASSISTANT_ID=your-assistant-id
OPENAI_API_KEY=your-openai-api-key
API_BASE_URL=https://your-backend-url.onrender.com
```

## Troubleshooting

### Backend Issues

1. **Build Fails**: Check `requirements.txt` has all dependencies
2. **Import Errors**: Ensure path handling in `simulation_api.py` is correct
3. **CORS Errors**: CORS middleware is already configured
4. **Health Check Fails**: Verify `/health` endpoint is accessible

### Frontend Issues

1. **App won't start**: Check that all dependencies are installed
2. **API key errors**: Verify your OpenAI API key is correct and has credits
3. **Assistant not responding**: Check that the Assistant ID is correct
4. **Function not calling**: Ensure function is properly configured in OpenAI Assistant

### Common Solutions

```bash
# Test backend directly
curl -v https://your-backend-url.onrender.com/health

# Check frontend logs
streamlit run app.py --logger.level=debug

# Verify OpenAI Assistant function
# Go to platform.openai.com/assistants and check function configuration
```

## Performance Considerations

### Backend (Render Free Tier):
- **Cold starts**: ~30 seconds delay after inactivity
- **Sleep after 15 minutes** of no requests
- **750 hours/month** free compute time

### Frontend (Streamlit Cloud):
- **Free tier**: 1GB RAM, shared CPU
- **Automatic scaling**: Handles multiple users
- **Custom domains**: Available on paid plans

## Production Recommendations

1. **Upgrade to paid plans** for better performance
2. **Add monitoring** and alerting
3. **Implement caching** for simulation results
4. **Add authentication** if needed
5. **Set up custom domains**
6. **Enable HTTPS** (automatic on cloud platforms)

## Success Checklist

- ✅ Backend API deployed to Render.com
- ✅ Backend health check working
- ✅ Backend simulation endpoint responding
- ✅ OpenAI Assistant function configured
- ✅ OpenAI Assistant calling real API (not hallucinating)
- ✅ Frontend deployed to Streamlit Cloud
- ✅ Frontend connecting to OpenAI Assistant
- ✅ Frontend showing real simulation results
- ✅ End-to-end natural language queries working

## URLs to Save

After deployment, you'll have:
- **Backend API**: `https://your-backend-name.onrender.com`
- **Frontend App**: `https://your-frontend-name.streamlit.app`
- **API Documentation**: `https://your-backend-name.onrender.com/docs`

## Next Steps

1. **Share your frontend URL** with users
2. **Monitor usage** via platform dashboards
3. **Collect feedback** and iterate
4. **Scale up** as needed for production use
5. **Add new features** based on user needs

Your complete Natural Language Simulation system is now live and accessible to anyone on the internet! 🚀 