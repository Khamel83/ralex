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

# Add ralex_core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ralex_core'))

from opencode_client import OpenCodeClient
from git_sync_manager import GitSyncManager

class RalexBridge:
    def __init__(self):
        self.project_path = os.getcwd()
        self.opencode = OpenCodeClient(self.project_path)
        self.git_sync = GitSyncManager(self.project_path)
        self.context_dir = Path(self.project_path) / ".ralex"
        self.context_dir.mkdir(exist_ok=True)
        
    def apply_agentos_thinking(self, prompt: str) -> dict:
        """Apply AgentOS strategic thinking to structure the prompt"""
        # Load AgentOS standards
        standards_path = Path("agent_os/standards")
        thinking = {
            "original_prompt": prompt,
            "complexity": "medium",  # Simple classification for now
            "requires_code": "create" in prompt.lower() or "write" in prompt.lower(),
            "safety_check": "rm " not in prompt and "delete" not in prompt
        }
        return thinking
    
    def select_model_via_litellm(self, thinking: dict) -> str:
        """Use LiteLLM to select appropriate model based on complexity"""
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
            return f"Error calling LiteLLM/OpenRouter: {str(e)}"
    
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
            
            # Step 2: LiteLLM model selection
            model = self.select_model_via_litellm(thinking)
            
            # Step 3: OpenRouter API call via LiteLLM
            ai_response = self.call_openrouter_via_litellm(prompt, model)
            
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

# FastAPI wrapper for OpenWebUI integration
if __name__ == "__main__":
    # Simple CLI test
    import asyncio
    
    if len(sys.argv) < 2:
        print("Usage: python ralex_bridge.py 'your prompt here'")
        sys.exit(1)
    
    bridge = RalexBridge()
    result = asyncio.run(bridge.process_request(sys.argv[1]))
    print(json.dumps(result, indent=2))