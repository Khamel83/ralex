#!/usr/bin/env python3
"""
RalexBridge - Thin orchestrator connecting all 5 core components
AgentOS → LiteLLM → OpenRouter → OpenCode → Context Persistence
"""

import os
import sys
import json
import asyncio
import subprocess
from datetime import datetime
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

# Load environment variables from .env
load_env()

# Add ralex_core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ralex_core'))

from opencode_client import OpenCodeClient
from git_sync_manager import GitSyncManager

# Import intelligence router for cost optimization
try:
    from ralex_intelligent import RalexIntelligenceRouter
except ImportError:
    RalexIntelligenceRouter = None

class RalexBridge:
    def __init__(self):
        self.project_path = os.getcwd()
        self.opencode = OpenCodeClient(self.project_path)
        self.git_sync = GitSyncManager(self.project_path)
        self.context_dir = Path(self.project_path) / ".ralex"
        self.context_dir.mkdir(exist_ok=True)
        
        # Initialize intelligence router if available
        self.intelligence_router = None
        if RalexIntelligenceRouter:
            try:
                self.intelligence_router = RalexIntelligenceRouter()
            except Exception:
                pass  # Graceful fallback if intelligence router fails
        
    def apply_agentos_thinking(self, prompt: str) -> dict:
        """Apply AgentOS strategic thinking to structure the prompt"""
        # Use intelligence router if available
        if self.intelligence_router:
            try:
                routing_result = self.intelligence_router.route_query(prompt)
                thinking = {
                    "original_prompt": prompt,
                    "complexity": "simple" if routing_result["model_tier"] == "cheap" else "medium",
                    "requires_code": "create" in prompt.lower() or "write" in prompt.lower(),
                    "safety_check": "rm " not in prompt and "delete" not in prompt,
                    "model_tier": routing_result["model_tier"],
                    "route": routing_result["route"],
                    "enhanced_query": routing_result["query"]
                }
                return thinking
            except Exception:
                pass  # Fallback to simple classification
        
        # Fallback to simple classification
        thinking = {
            "original_prompt": prompt,
            "complexity": "medium",
            "requires_code": "create" in prompt.lower() or "write" in prompt.lower(),
            "safety_check": "rm " not in prompt and "delete" not in prompt
        }
        return thinking
    
    def load_intelligence_config(self) -> dict:
        """Load intelligence configuration for model tier mappings"""
        config_path = Path(".ralex/intelligence-config.yaml")
        if config_path.exists():
            try:
                import yaml
                with open(config_path) as f:
                    return yaml.safe_load(f)
            except Exception:
                pass
        return {"model_tiers": {"cheap": [], "medium": [], "premium": []}}
    
    def select_model_via_litellm(self, thinking: dict, tier: str = None) -> str:
        """Use LiteLLM to select appropriate model based on complexity and cost tier"""
        # Load intelligence config for model tier mappings
        intelligence_config = self.load_intelligence_config()
        
        if tier:
            # Use specified tier
            models = intelligence_config.get("model_tiers", {}).get(tier, [])
            if models:
                return models[0]  # Use first model in tier
        
        # Fallback to complexity-based selection
        if thinking["complexity"] == "high":
            return "openrouter/anthropic/claude-3.5-sonnet"
        elif thinking["requires_code"]:
            return "openrouter/anthropic/claude-3-haiku"
        else:
            return "openrouter/meta-llama/llama-3.1-8b-instruct"
    
    def call_openrouter_via_litellm(self, prompt: str, model: str) -> str:
        """Make API call to OpenRouter through LiteLLM"""
        try:
            # Import here to avoid startup dependencies
            import litellm
            
            # Set OpenRouter API key
            os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "")
            
            response = litellm.completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                api_base="https://openrouter.ai/api/v1"
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "No auth credentials found" in error_msg:
                return "OpenRouter API key required. Set OPENROUTER_API_KEY environment variable."
            elif "rate limit" in error_msg.lower():
                return "Rate limit exceeded. Please wait before making another request."
            elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                return "Network connection error. Check internet connectivity."
            else:
                return f"Error calling LiteLLM/OpenRouter: {error_msg}"
    
    def execute_via_opencode(self, ai_response: str, original_prompt: str) -> dict:
        """Execute AI response using OpenCode"""
        # For file creation requests, extract code from response
        if "create" in original_prompt.lower():
            # Extract filename and content from AI response
            lines = ai_response.split('\n')
            filename = None
            content_lines = []
            in_code_block = False
            code_type = None
            
            # Look for any file extension in the prompt or response
            import re
            file_extensions = ['.py', '.js', '.json', '.md', '.txt', '.html', '.css', '.yaml', '.yml', '.xml']
            
            for line in lines:
                # Detect code block start
                if line.startswith('```'):
                    if not in_code_block:
                        in_code_block = True
                        code_type = line[3:].strip() or 'text'
                        continue
                    else:
                        in_code_block = False
                        break
                elif in_code_block:
                    content_lines.append(line)
                elif not filename:
                    # Try to extract filename from text
                    for ext in file_extensions:
                        if ext in line:
                            words = line.split()
                            for word in words:
                                if ext in word:
                                    filename = word.strip('`"\'.:')
                                    break
                            if filename:
                                break
            
            if filename and content_lines:
                content = '\n'.join(content_lines)
                result = self.opencode.write_file(filename, content)
                return {"success": True, "output": f"Created {filename}", "details": result}
        
        # Fallback: just return the AI response
        return {"success": True, "output": ai_response}
    
    def save_context(self, session_data: dict):
        """Save session context to .ralex/ directory"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        session_file = self.context_dir / f"session_{timestamp}.md"
        
        content = f"""# Ralex Session {timestamp}

## Original Prompt
{session_data['original_prompt']}

## AgentOS Thinking
- Complexity: {session_data['thinking']['complexity']}
- Requires Code: {session_data['thinking']['requires_code']}
- Safety Check: {session_data['thinking']['safety_check']}

## Model Selected
{session_data['model']}

## AI Response
{session_data['ai_response']}

## Execution Result
{session_data['execution_result']}
"""
        
        with open(session_file, 'w') as f:
            f.write(content)
        
        # Auto-commit to git
        try:
            self.git_sync.commit_changes(f"Add session {timestamp}")
        except:
            pass  # Ignore git errors for now
    
    async def process_request(self, prompt: str) -> dict:
        """Main orchestration pipeline"""
        try:
            # Step 1: AgentOS strategic thinking
            thinking = self.apply_agentos_thinking(prompt)
            
            if not thinking["safety_check"]:
                return {"error": "Unsafe command detected by AgentOS"}
            
            # Step 2: LiteLLM model selection with cost tier
            tier = thinking.get("model_tier", None)
            model = self.select_model_via_litellm(thinking, tier)
            
            # Step 3: OpenRouter API call via LiteLLM with enhanced query
            query_to_use = thinking.get("enhanced_query", prompt)
            ai_response = self.call_openrouter_via_litellm(query_to_use, model)
            
            # Step 4: OpenCode execution
            execution_result = self.execute_via_opencode(ai_response, prompt)
            
            # Step 5: Context persistence
            session_data = {
                "original_prompt": prompt,
                "thinking": thinking,
                "model": model,
                "ai_response": ai_response,
                "execution_result": execution_result
            }
            self.save_context(session_data)
            
            return {
                "success": True,
                "model_used": model,
                "response": ai_response,
                "execution": execution_result,
                "context_saved": True
            }
            
        except Exception as e:
            return {"error": f"Bridge error: {str(e)}"}

# CLI interface with health check
if __name__ == "__main__":
    import asyncio
    
    # Health check command
    if len(sys.argv) == 2 and sys.argv[1] in ['--health', '--check', '--status']:
        print("🔍 Ralex V4 Health Check")
        print("========================")
        
        # Check API key
        api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key:
            print("✅ OpenRouter API key configured")
        else:
            print("❌ OpenRouter API key not set")
            print("   Run: export OPENROUTER_API_KEY='your-key-here'")
            
        # Check dependencies
        try:
            import litellm
            print("✅ LiteLLM available")
        except ImportError:
            print("❌ LiteLLM missing - run: pip install litellm")
            
        # Check write permissions
        try:
            with open('.ralex_test', 'w') as f:
                f.write('test')
            os.remove('.ralex_test')
            print("✅ File write permissions OK")
        except:
            print("❌ Cannot write files in current directory")
            
        # Check git
        try:
            import subprocess
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            print("✅ Git available")
        except:
            print("⚠️  Git not available (optional)")
            
        print("\n🎯 Try: python ralex_bridge.py 'create a test.py file'")
        sys.exit(0)
    
    # Help command
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ['--help', '-h']):
        print("🎯 Ralex V4 - Voice-Controlled AI Coding Assistant")
        print("================================================")
        print("")
        print("Usage:")
        print("  python ralex_bridge.py 'your command here'")
        print("")
        print("Examples:")
        print("  python ralex_bridge.py 'create a calculator.py with add/subtract functions'")
        print("  python ralex_bridge.py 'create a config.json with database settings'")
        print("  python ralex_bridge.py 'create an index.html with a contact form'")
        print("")
        print("Options:")
        print("  --health    Check system health and configuration")
        print("  --help      Show this help message")
        print("")
        print("Setup:")
        print("  1. Set API key: export OPENROUTER_API_KEY='your-key'")
        print("  2. Get free key: https://openrouter.ai")
        print("")
        print("Documentation:")
        print("  README: cat README_V4.md")
        print("  Setup:  cat QUICKSTART.md")
        print("  Status: cat PRODUCTION_READINESS.md")
        sys.exit(0)
    
    if len(sys.argv) < 2:
        print("❌ Error: No command provided")
        print("Usage: python ralex_bridge.py 'your prompt here'")
        print("Help:  python ralex_bridge.py --help")
        sys.exit(1)
    
    # Check API key before processing
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ Error: OpenRouter API key not set")
        print("Solution: export OPENROUTER_API_KEY='your-key-here'")
        print("Get free key: https://openrouter.ai")
        sys.exit(1)
    
    try:
        bridge = RalexBridge()
        result = asyncio.run(bridge.process_request(sys.argv[1]))
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            if "API" in result["error"]:
                print("💡 Check your OpenRouter API key and internet connection")
            sys.exit(1)
        else:
            print(json.dumps(result, indent=2))
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        print("💡 Run: python ralex_bridge.py --health")
        sys.exit(1)