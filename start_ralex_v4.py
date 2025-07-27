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
    
    # Use absolute path to avoid path issues
    webui_dir = Path.cwd() / "archive" / "web-interfaces" / "ralex-webui" / "backend"
    if not webui_dir.exists():
        print(f"❌ OpenWebUI backend directory not found: {webui_dir}")
        return None
    
    # Set environment variables for OpenWebUI
    os.environ["PORT"] = "3000"
    os.environ["HOST"] = "0.0.0.0"
    os.environ["WEBUI_SECRET_KEY"] = "ralex-v4-secret-key"
    os.environ["ENV"] = "prod"
    
    # Install super minimal dependencies for Raspberry Pi (ARM compatibility)
    arm_minimal_requirements = Path.cwd() / "requirements-webui-minimal-arm.txt"
    ultraminimal_requirements = Path.cwd() / "requirements-webui-ultraminimal.txt"
    minimal_requirements = Path.cwd() / "requirements-webui-minimal.txt"
    requirements_file = webui_dir / "requirements.txt"
    
    # Use super minimal requirements for Raspberry Pi ARM compatibility
    if arm_minimal_requirements.exists():
        print("📦 Installing super minimal OpenWebUI dependencies for Raspberry Pi ARM...")
        requirements_to_use = arm_minimal_requirements
    elif ultraminimal_requirements.exists():
        print("📦 Installing ultra-minimal OpenWebUI dependencies for Raspberry Pi ARM...")
        requirements_to_use = ultraminimal_requirements
    elif minimal_requirements.exists():
        print("📦 Installing minimal OpenWebUI dependencies for Raspberry Pi...")
        requirements_to_use = minimal_requirements
    else:
        print("📦 Installing full OpenWebUI dependencies...")
        requirements_to_use = requirements_file
    
    if requirements_to_use.exists():
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_to_use)], 
                                  capture_output=True, text=True, timeout=300)  # 5 minute timeout
            if result.returncode != 0:
                print(f"⚠️  Warning: Some dependencies failed to install: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("⚠️  Warning: Dependency installation timed out, continuing with available packages...")
        except Exception as e:
            print(f"⚠️  Warning: Dependency installation failed: {e}")
    
    # Start OpenWebUI with better configuration for Raspberry Pi
    cmd = [
        sys.executable, "-m", "uvicorn", "open_webui.main:app", 
        "--host", "0.0.0.0", 
        "--port", "3000",
        "--workers", "1",
        "--timeout-keep-alive", "30",
        "--access-log"
    ]
    
    # Start with output visible to debug issues
    try:
        webui_process = subprocess.Popen(cmd, cwd=str(webui_dir), 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"❌ Failed to start OpenWebUI process: {e}")
        return None
    
    # Wait for OpenWebUI to start and become accessible
    max_retries = 15
    for i in range(max_retries):
        if webui_process.poll() is not None:
            print("❌ OpenWebUI process exited unexpectedly")
            return None
            
        try:
            response = requests.get("http://localhost:3000", timeout=2)
            if response.status_code in [200, 404]:  # 404 is ok, means server is responding
                print("✅ OpenWebUI started on port 3000")
                return webui_process
        except requests.exceptions.RequestException:
            pass
        
        print(f"⏳ Waiting for OpenWebUI to become accessible... ({i+1}/{max_retries})")
        time.sleep(2)
    
    print("❌ OpenWebUI failed to become accessible")
    return webui_process  # Return process anyway, might be slow to start

def main():
    """Main startup sequence"""
    print("🎯 Starting Ralex (v1.3.0) - Full Stack Integration")
    print("Components: AgentOS + LiteLLM + OpenRouter + OpenCode + OpenWebUI")
    print("Standards: .agent-os/standards/modern-development.yaml")
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
    
    # Get local IP for remote access
    try:
        import socket
        local_ip = subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
    except:
        local_ip = "localhost"
    
    print("\n🎉 Ralex V4 started successfully!")
    print("📊 RalexBridge API:")
    print(f"   • Local: http://localhost:8000")
    print(f"   • Network: http://{local_ip}:8000")
    print("🖥️  OpenWebUI:")
    print(f"   • Local: http://localhost:3000")
    print(f"   • Network: http://{local_ip}:3000")
    print(f"   • Tailscale: http://<tailscale-ip>:3000")
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