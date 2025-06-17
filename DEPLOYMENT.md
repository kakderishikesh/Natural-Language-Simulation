# 🚀 Deployment Guide: Render.com

This guide walks you through deploying the Natural Language Simulation API to Render.com for cloud hosting.

## 📋 Prerequisites

- GitHub account with your repository
- Render.com account (free tier available)
- Your code pushed to a GitHub repository

## 🔧 Step 1: Prepare Repository

Ensure these files are in your repository root:
- ✅ `render.yaml` - Render service configuration
- ✅ `runtime.txt` - Python version specification  
- ✅ `requirements.txt` - Python dependencies
- ✅ `Backend/simulation_api.py` - Your API with CORS enabled

## 🌐 Step 2: Deploy to Render

### Option A: Using Render Dashboard (Recommended)

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

### Option B: Using render.yaml (Automatic)

1. Push the `render.yaml` file to your repository
2. Go to Render dashboard → **"New +"** → **"Blueprint"**
3. Connect your repository and deploy

## 🎯 Step 3: Get Your API URL

After deployment, Render will provide you with a URL like:
```
https://natural-language-simulation-api-[random].onrender.com
```

**Save this URL** - you'll need it for OpenAI Assistant configuration.

## 🧪 Step 4: Test Your Deployed API

### Health Check:
```bash
curl https://your-app-name.onrender.com/health
```

### Test Simulation:
```bash
curl -X POST "https://your-app-name.onrender.com/simulate" \
  -H "Content-Type: application/json" \
  -d '{"x": 7, "y": 3, "simulation_time": 100}'
```

## 🤖 Step 5: Update OpenAI Assistant Configuration

Update your OpenAI Assistant function to use the new cloud URL:

### Function Schema (Updated):
```json
{
  "name": "run_simulation",
  "description": "Run a discrete event simulation with specified parameters for a queueing system with two workstations.",
  "parameters": {
    "type": "object",
    "properties": {
      "x": {
        "type": "integer",
        "minimum": 1,
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
        "description": "Duration of simulation in minutes (after 20-minute warm-up period)."
      }
    },
    "required": ["x", "y", "simulation_time"],
    "additionalProperties": false
  }
}
```

### API Endpoint Configuration:
- **Base URL**: `https://your-app-name.onrender.com`
- **Endpoint**: `POST /simulate`
- **Headers**: `Content-Type: application/json`

## 📊 Step 6: Update Environment Variables

Update your `.env` file:
```env
ASSISTANT_ID=asst_w0IWjdDaqYwYxCFrriBNXjc5
OPENAI_API_KEY=sk-proj-...
API_BASE_URL=https://your-app-name.onrender.com
```

## ⚡ Performance Notes

### Free Tier Limitations:
- **Cold starts**: ~30 seconds delay after inactivity
- **Sleep after 15 minutes** of no requests
- **750 hours/month** free compute time

### Paid Tier Benefits:
- **No cold starts**
- **Always-on service**
- **Better performance**
- **Custom domains**

## 🔍 Monitoring & Debugging

### View Logs:
1. Go to your Render dashboard
2. Click on your service
3. Go to **"Logs"** tab to see real-time logs

### Health Monitoring:
- Render automatically monitors `/health` endpoint
- Service will restart if health checks fail

## 🚨 Common Issues & Solutions

### Issue: Build Fails
**Solution**: Check `requirements.txt` has all dependencies
```bash
# Test locally first
pip install -r requirements.txt
python Backend/simulation_api.py
```

### Issue: Import Errors
**Solution**: Ensure path handling in `simulation_api.py` is correct
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
```

### Issue: CORS Errors
**Solution**: CORS middleware is already added, but you can restrict origins:
```python
allow_origins=["https://chat.openai.com", "https://api.openai.com"]
```

### Issue: OpenAI Can't Reach API
**Solution**: 
- Verify API is deployed and accessible
- Check OpenAI Assistant function configuration
- Test with curl first

## 🔄 Updates & Redeployment

### Automatic Redeployment:
- Push changes to your GitHub repository
- Render automatically rebuilds and deploys

### Manual Redeployment:
1. Go to Render dashboard
2. Click your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

## 🎉 Success Checklist

- ✅ API deployed to Render.com
- ✅ Health check endpoint working
- ✅ Simulation endpoint responding
- ✅ OpenAI Assistant function updated with new URL
- ✅ Natural language queries working end-to-end

## 📚 Next Steps

1. **Test thoroughly** with various simulation parameters
2. **Monitor usage** via Render dashboard
3. **Consider upgrading** to paid plan for production use
4. **Set up custom domain** (paid plans only)
5. **Add monitoring** and alerting for production environments

Your simulation API is now globally accessible! 🌍 