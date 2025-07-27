#!/usr/bin/env python3
"""
Ralex V4 Startup Script - Orchestrates all components
1. Start RalexBridge API server
2. Configure OpenWebUI to use RalexBridge
3. Start OpenWebUI
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

# Load .env file if it exists
def load_env():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load environment variables
load_env()

def start_ralex_bridge():
    """Start the RalexBridge API server"""
    print("🚀 Starting RalexBridge API server...")
    
    # Start FastAPI server in background
    cmd = [sys.executable, "ralex_api.py"]
    bridge_process = subprocess.Popen(cmd, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
    
    # Wait for server to start
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ RalexBridge API server started successfully")
                return bridge_process
        except:
            pass
        
        print(f"⏳ Waiting for RalexBridge API server... ({i+1}/{max_retries})")
        time.sleep(2)
    
    print("❌ Failed to start RalexBridge API server")
    return None

def configure_openwebui():
    """Configure OpenWebUI to use RalexBridge"""
    print("🔧 Configuring OpenWebUI to use RalexBridge...")
    
    # Set environment variables for OpenWebUI
    os.environ["OPENAI_API_BASE_URL"] = "http://localhost:8000/v1"
    os.environ["OPENAI_API_KEY"] = "dummy-key-for-ralex-bridge"
    os.environ["MODEL_FILTER_ENABLED"] = "False"
    
    print("✅ OpenWebUI configured to use RalexBridge")

def start_openwebui():
    """Start OpenWebUI"""
    print("🌐 Starting OpenWebUI...")
    
    webui_dir = Path("archive/web-interfaces/ralex-webui")
    if not webui_dir.exists():
        print("❌ OpenWebUI directory not found")
        return None
    
    # Set environment variables for OpenWebUI
    os.environ["PORT"] = "3000"
    os.environ["HOST"] = "0.0.0.0"
    
    # Change to OpenWebUI directory
    os.chdir(webui_dir)
    
    # Start OpenWebUI with custom port
    cmd = ["python", "-m", "uvicorn", "open_webui.main:app", "--host", "0.0.0.0", "--port", "3000"]
    webui_process = subprocess.Popen(cmd)
    
    print("✅ OpenWebUI started on port 3000")
    return webui_process

def main():
    """Main startup sequence"""
    print("🎯 Starting Ralex V4 - Full Stack Integration")
    print("Components: AgentOS + LiteLLM + OpenRouter + OpenCode + OpenWebUI")
    print("=" * 60)
    
    # Check required environment variables
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ OPENROUTER_API_KEY environment variable not set!")
        print("Please set it with: export OPENROUTER_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Start components in order
    bridge_process = start_ralex_bridge()
    if not bridge_process:
        sys.exit(1)
    
    configure_openwebui()
    webui_process = start_openwebui()
    
    print("\n🎉 Ralex V4 started successfully!")
    print("📊 RalexBridge API: http://localhost:8000")
    print("🖥️  OpenWebUI: http://localhost:3000")
    print("📁 Context saved to: .ralex/")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep processes running
        bridge_process.wait()
        webui_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping Ralex V4...")
        bridge_process.terminate()
        webui_process.terminate()
        print("✅ All services stopped")

if __name__ == "__main__":
    main()