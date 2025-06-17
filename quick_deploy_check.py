#!/usr/bin/env python3
"""
Quick deployment readiness check
"""

import os

def check_deployment_ready():
    print("🚀 Render.com Deployment Readiness Check")
    print("=" * 50)
    
    # Check required files
    required_files = {
        "render.yaml": "Render service configuration",
        "runtime.txt": "Python version specification", 
        "requirements.txt": "Python dependencies",
        "Backend/simulation_api.py": "Main API server",
        "DEPLOYMENT.md": "Deployment guide"
    }
    
    all_good = True
    
    print("\n📁 Required Files:")
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"✅ {file} - {description}")
        else:
            print(f"❌ {file} - MISSING! ({description})")
            all_good = False
    
    # Check requirements.txt content
    print("\n📦 Dependencies Check:")
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read()
            required_packages = ["fastapi", "uvicorn", "simpy", "numpy", "pydantic"]
            for package in required_packages:
                if package.lower() in requirements.lower():
                    print(f"✅ {package}")
                else:
                    print(f"❌ {package} - MISSING!")
                    all_good = False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        all_good = False
    
    # Check API file has CORS
    print("\n🌐 CORS Configuration:")
    try:
        with open("Backend/simulation_api.py", "r") as f:
            api_content = f.read()
            if "CORSMiddleware" in api_content:
                print("✅ CORS middleware configured")
            else:
                print("❌ CORS middleware missing")
                all_good = False
                
            if "os.environ.get" in api_content and "PORT" in api_content:
                print("✅ Environment variable handling configured")
            else:
                print("❌ Environment variable handling missing")
                all_good = False
    except Exception as e:
        print(f"❌ Error checking API file: {e}")
        all_good = False
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 ALL CHECKS PASSED! Ready for Render deployment!")
        print("\n📋 Next Steps:")
        print("1. Push your code to GitHub")
        print("2. Go to https://render.com")
        print("3. Create a new Web Service")
        print("4. Connect your GitHub repository")
        print("5. Use these settings:")
        print("   • Build Command: pip install -r requirements.txt")
        print("   • Start Command: python Backend/simulation_api.py")
        print("   • Environment: Python 3")
        print("\n📖 See DEPLOYMENT.md for detailed instructions")
        return True
    else:
        print("❌ Some checks failed! Please fix issues above.")
        return False

if __name__ == "__main__":
    success = check_deployment_ready()
    exit(0 if success else 1) 