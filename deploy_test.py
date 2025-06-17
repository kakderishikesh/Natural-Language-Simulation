#!/usr/bin/env python3
"""
Local deployment test script to verify configuration before deploying to Render.com
"""

import os
import sys
import subprocess
import time
import requests

def test_deployment_config():
    """Test if the deployment configuration is correct"""
    print("🧪 Testing Deployment Configuration")
    print("=" * 50)
    
    # Test 1: Check required files
    required_files = [
        "render.yaml",
        "runtime.txt", 
        "requirements.txt",
        "Backend/simulation_api.py"
    ]
    
    print("\n1️⃣ Checking required files...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            return False
    
    # Test 2: Check requirements.txt has necessary packages
    print("\n2️⃣ Checking requirements.txt...")
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read()
            required_packages = ["fastapi", "uvicorn", "simpy", "numpy"]
            for package in required_packages:
                if package.lower() in requirements.lower():
                    print(f"✅ {package}")
                else:
                    print(f"❌ {package} - MISSING!")
                    return False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False
    
    # Test 3: Test local startup with environment variables
    print("\n3️⃣ Testing local startup with deployment config...")
    
    # Set environment variables like Render would
    os.environ["PORT"] = "8000"
    os.environ["HOST"] = "0.0.0.0"
    
    try:
        # Start the server in background
        print("Starting server...")
        import subprocess
        env = os.environ.copy()
        env["PORT"] = "8000"
        env["HOST"] = "0.0.0.0"
        
        process = subprocess.Popen([
            sys.executable, "Backend/simulation_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(8)  # Give more time for startup
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health endpoint error: {e}")
            return False
        
        # Test simulation endpoint
        try:
            test_data = {"x": 7, "y": 3, "simulation_time": 50}
            response = requests.post("http://localhost:8000/simulate", json=test_data, timeout=10)
            if response.status_code == 200:
                print("✅ Simulation endpoint working")
            else:
                print(f"❌ Simulation endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Simulation endpoint error: {e}")
            return False
        
        # Stop the server
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"❌ Server startup error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All deployment tests passed!")
    print("\n📋 Next Steps:")
    print("1. Push your code to GitHub")
    print("2. Go to render.com and create a new web service")
    print("3. Connect your GitHub repository")
    print("4. Follow the DEPLOYMENT.md guide")
    
    return True

if __name__ == "__main__":
    success = test_deployment_config()
    if not success:
        print("\n❌ Deployment configuration issues found!")
        print("Please fix the issues above before deploying.")
        sys.exit(1)
    else:
        print("\n✅ Ready for deployment!")
        sys.exit(0) 