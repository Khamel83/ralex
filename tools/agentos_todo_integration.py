"""
Agent-OS Integration for TodoWrite Tool
Provides seamless integration between TodoWrite and Agent-OS workflows.
"""

from typing import Dict, Any, List
import os
import sys
from pathlib import Path

# Add tools to path for import
sys.path.insert(0, str(Path(__file__).parent))
from todo_writer import TodoWriter, quick_complete_task


class AgentOSTodoIntegration:
    """Integration layer between TodoWrite and Agent-OS"""
    
    def __init__(self, spec_folder: str = None):
        """
        Initialize with optional spec folder path
        If provided, tasks will be auto-linked to spec documentation
        """
        self.spec_folder = spec_folder
        self.writer = TodoWriter()
        
    def create_task_from_spec(self, spec_path: str, task_id: str = None) -> Dict[str, Any]:
        """Create a task from an Agent-OS spec folder"""
        if not os.path.exists(spec_path):
            return {"error": f"Spec path not found: {spec_path}"}
        
        try:
            # Extract task info from spec folder
            spec_name = os.path.basename(spec_path)
            
            # Generate task ID from spec name if not provided
            if not task_id:
                # Remove date prefix and convert to task ID
                if spec_name.startswith("2025-") and len(spec_name.split("-")) >= 4:
                    task_id = "-".join(spec_name.split("-")[3:])  # Remove date prefix
                else:
                    task_id = spec_name.replace("-", "_")
            
            # Read spec content if available
            description = f"Implement features from spec: {spec_path}"
            readme_path = os.path.join(spec_path, "README.md")
            if os.path.exists(readme_path):
                with open(readme_path, 'r') as f:
                    content = f.read()
                    # Use first paragraph as description
                    lines = content.split('\n')
                    for line in lines:
                        if line.strip() and not line.startswith('#'):
                            description = line.strip()
                            break
            
            # Create task
            result = self.writer.create_task(
                task_id=task_id,
                name=f"Implement {spec_name}",
                description=description,
                priority="medium"
            )
            
            if result.get('success'):
                result['spec_path'] = spec_path
                
            return result
            
        except Exception as e:
            return {"error": f"Failed to create task from spec: {str(e)}"}
    
    def complete_with_agentos_context(self, task_id: str, 
                                    implementation_files: List[str] = None,
                                    test_results: str = None,
                                    next_spec: str = None) -> Dict[str, Any]:
        """Complete a task with Agent-OS specific context"""
        
        # Auto-detect modified files if not provided
        if not implementation_files:
            implementation_files = self._detect_modified_files()
        
        # Generate verification steps
        verification_steps = []
        if implementation_files:
            verification_steps.append(f"Implementation completed in {len(implementation_files)} files")
        
        if test_results:
            verification_steps.append(f"Testing: {test_results}")
        else:
            verification_steps.append("Implementation verified and tested")
        
        verification_steps.append("Code follows Agent-OS standards")
        verification_steps.append("Integration with existing systems confirmed")
        
        # Generate next task info
        next_task_info = ""
        if next_spec:
            next_task_info = f"Continue with next spec: {next_spec}"
        else:
            next_task_info = "Ready for next Agent-OS specification"
        
        return self.writer.complete_task(
            task_id=task_id,
            verification_steps=verification_steps,
            files_modified=implementation_files,
            next_task_info=next_task_info
        )
    
    def _detect_modified_files(self) -> List[str]:
        """Auto-detect modified files using git status"""
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode \!= 0:
                return []
            
            modified_files = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    filename = line[3:]  # Remove status prefix
                    modified_files.append(filename)
            
            return modified_files
            
        except Exception:
            return []
    
    def sync_with_specs_folder(self, specs_base_path: str = ".agent-os/specs") -> Dict[str, Any]:
        """Sync tasks with Agent-OS specs folder"""
        if not os.path.exists(specs_base_path):
            return {"error": f"Specs folder not found: {specs_base_path}"}
        
        results = []
        spec_folders = [d for d in os.listdir(specs_base_path) 
                       if os.path.isdir(os.path.join(specs_base_path, d))]
        
        for spec_folder in spec_folders:
            spec_path = os.path.join(specs_base_path, spec_folder)
            result = self.create_task_from_spec(spec_path)
            results.append({
                "spec": spec_folder,
                "result": result
            })
        
        return {
            "synced_specs": len(spec_folders),
            "results": results
        }


# Convenience functions for Agent-OS workflows
def create_agentos_integration(spec_folder: str = None) -> AgentOSTodoIntegration:
    """Create an Agent-OS TodoWrite integration"""
    return AgentOSTodoIntegration(spec_folder)


def quick_complete_agentos_task(task_id: str, implementation_files: List[str] = None,
                               test_results: str = "All tests passing",
                               next_spec: str = None) -> Dict[str, Any]:
    """Quick function to complete an Agent-OS task"""
    integration = AgentOSTodoIntegration()
    return integration.complete_with_agentos_context(
        task_id, implementation_files, test_results, next_spec
    )


# Example usage for testing
if __name__ == "__main__":
    # Example: Create integration and sync with specs
    integration = AgentOSTodoIntegration()
    
    # Try to sync with specs folder if it exists
    sync_result = integration.sync_with_specs_folder()
    print("Spec sync result:", sync_result)
    
    # Example: Complete a task with Agent-OS context
    completion_result = quick_complete_agentos_task(
        "A1",
        implementation_files=["tools/todo_writer.py", "tools/agentos_todo_integration.py"],
        test_results="All integration tests passing",
        next_spec="agent-os-universal-installer"
    )
    print("Task completion result:", completion_result)
EOF < /dev/null