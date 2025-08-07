#!/usr/bin/env python3
"""
Agent OS Context Analyzer - Reads and understands Agent OS project structure
This module analyzes the current project to understand its Agent OS context.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess
from datetime import datetime

class AgentOSContextAnalyzer:
    """Analyzes Agent OS project context"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
    
    def get_full_context(self) -> Dict[str, Any]:
        """Get complete project context"""
        context = {
            "project_root": str(self.project_root),
            "timestamp": datetime.now().isoformat(),
            "agent_os_structure": self._analyze_agent_os_structure(),
            "git_context": self._analyze_git_context(),
            "project_state": self._analyze_project_state(),
            "current_spec": self._find_current_spec(),
            "next_task": self._find_next_task(),
            "patterns": self._analyze_patterns(),
            "handover_docs": self._find_handover_docs(),
            "development_context": self._analyze_development_context()
        }
        return context
    
    def _analyze_agent_os_structure(self) -> Dict[str, Any]:
        """Analyze Agent OS directory structure"""
        structure = {
            "has_agent_os": False,
            "has_project_dir": False,
            "mission_file": None,
            "roadmap_file": None,
            "tech_stack_file": None,
            "specs_directory": None,
            "pattern_cache": None
        }
        
        # Check for .agent-os directory
        agent_os_dir = self.project_root / ".agent-os"
        if agent_os_dir.exists():
            structure["has_agent_os"] = True
            
            # Check for product documentation
            product_dir = agent_os_dir / "product"
            if product_dir.exists():
                mission_file = product_dir / "mission-lite.md"
                if mission_file.exists():
                    structure["mission_file"] = str(mission_file)
                    
                roadmap_file = product_dir / "roadmap.md"
                if roadmap_file.exists():
                    structure["roadmap_file"] = str(roadmap_file)
                    
                tech_stack_file = product_dir / "tech-stack.md"
                if tech_stack_file.exists():
                    structure["tech_stack_file"] = str(tech_stack_file)
            
            # Check for specs directory
            specs_dir = agent_os_dir / "specs"
            if specs_dir.exists():
                structure["specs_directory"] = str(specs_dir)
        
        # Check for .project directory (alternative structure)
        project_dir = self.project_root / ".project"
        if project_dir.exists():
            structure["has_project_dir"] = True
            
            patterns_dir = project_dir / "patterns"
            if patterns_dir.exists():
                structure["pattern_cache"] = str(patterns_dir)
        
        return structure
    
    def _analyze_git_context(self) -> Dict[str, Any]:
        """Analyze git context"""
        git_context = {
            "is_git_repo": False,
            "current_branch": None,
            "uncommitted_changes": 0,
            "recent_commits": [],
            "status": None
        }
        
        try:
            # Check if it's a git repo
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                git_context["is_git_repo"] = True
                
                # Get current branch
                branch_result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if branch_result.returncode == 0:
                    git_context["current_branch"] = branch_result.stdout.strip()
                
                # Get status
                status_result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if status_result.returncode == 0:
                    git_context["status"] = status_result.stdout
                    git_context["uncommitted_changes"] = len(status_result.stdout.strip().split('\n')) if status_result.stdout.strip() else 0
                
                # Get recent commits
                log_result = subprocess.run(
                    ["git", "log", "--oneline", "-5"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if log_result.returncode == 0:
                    git_context["recent_commits"] = log_result.stdout.strip().split('\n')
                    
        except Exception as e:
            git_context["error"] = str(e)
        
        return git_context
    
    def _analyze_project_state(self) -> Dict[str, Any]:
        """Analyze current project state"""
        state = {
            "package_files": [],
            "readme_exists": False,
            "documentation_dirs": [],
            "test_dirs": [],
            "estimated_size": "unknown"
        }
        
        # Look for package files
        package_files = [
            "package.json", "Gemfile", "requirements.txt", 
            "Cargo.toml", "go.mod", "composer.json"
        ]
        
        for package_file in package_files:
            if (self.project_root / package_file).exists():
                state["package_files"].append(package_file)
        
        # Check for README
        readme_files = ["README.md", "README.txt", "README.rst", "readme.md"]
        for readme in readme_files:
            if (self.project_root / readme).exists():
                state["readme_exists"] = True
                break
        
        # Look for documentation directories
        doc_dirs = ["docs", "doc", "documentation", "wiki"]
        for doc_dir in doc_dirs:
            if (self.project_root / doc_dir).exists():
                state["documentation_dirs"].append(doc_dir)
        
        # Look for test directories
        test_dirs = ["test", "tests", "spec", "specs", "__tests__"]
        for test_dir in test_dirs:
            if (self.project_root / test_dir).exists():
                state["test_dirs"].append(test_dir)
        
        # Estimate project size (rough)
        try:
            total_files = sum(1 for _ in self.project_root.rglob("*") if _.is_file())
            if total_files < 50:
                state["estimated_size"] = "small"
            elif total_files < 200:
                state["estimated_size"] = "medium"
            else:
                state["estimated_size"] = "large"
        except:
            state["estimated_size"] = "unknown"
        
        return state
    
    def _find_current_spec(self) -> Optional[Dict[str, Any]]:
        """Find the most recent/current spec"""
        specs_dir = self.project_root / ".agent-os" / "specs"
        
        if not specs_dir.exists():
            return None
        
        try:
            # Find most recent spec directory
            spec_dirs = [d for d in specs_dir.iterdir() if d.is_dir()]
            if not spec_dirs:
                return None
            
            # Sort by modification time (most recent first)
            spec_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            current_spec_dir = spec_dirs[0]
            
            spec_info = {
                "name": current_spec_dir.name,
                "path": str(current_spec_dir),
                "has_spec_md": (current_spec_dir / "spec.md").exists(),
                "has_tasks_md": (current_spec_dir / "tasks.md").exists(),
                "has_technical_spec": (current_spec_dir / "sub-specs" / "technical-spec.md").exists()
            }
            
            # Try to read tasks if available
            tasks_file = current_spec_dir / "tasks.md"
            if tasks_file.exists():
                try:
                    with open(tasks_file, 'r') as f:
                        tasks_content = f.read()
                        spec_info["tasks_content"] = tasks_content
                except:
                    pass
            
            return spec_info
            
        except Exception as e:
            return {"error": str(e)}
    
    def _find_next_task(self) -> Optional[str]:
        """Find the next uncompleted task"""
        current_spec = self._find_current_spec()
        
        if not current_spec or "tasks_content" not in current_spec:
            return "No active tasks found"
        
        tasks_content = current_spec["tasks_content"]
        lines = tasks_content.split('\n')
        
        # Look for unchecked tasks
        for line in lines:
            line = line.strip()
            if line.startswith('- [ ]'):
                # Extract task description
                task = line[5:].strip()  # Remove '- [ ] '
                return task
        
        return "All tasks appear to be completed"
    
    def _analyze_patterns(self) -> Dict[str, Any]:
        """Analyze available patterns"""
        patterns_info = {
            "has_pattern_cache": False,
            "pattern_files": [],
            "estimated_patterns": 0
        }
        
        # Check for Agent OS pattern cache
        agent_os_patterns = self.project_root / ".khamel83" / "pattern-cache"
        project_patterns = self.project_root / ".project" / "patterns"
        
        for patterns_dir in [agent_os_patterns, project_patterns]:
            if patterns_dir.exists():
                patterns_info["has_pattern_cache"] = True
                try:
                    pattern_files = list(patterns_dir.rglob("*.md"))
                    patterns_info["pattern_files"].extend([str(f) for f in pattern_files])
                    patterns_info["estimated_patterns"] += len(pattern_files)
                except:
                    pass
        
        return patterns_info
    
    def _find_handover_docs(self) -> Optional[Dict[str, Any]]:
        """Find handover documentation"""
        handover_info = {
            "found": False,
            "locations": []
        }
        
        # Common handover document patterns
        handover_patterns = [
            "handover*",
            "HANDOVER*", 
            "*handover*",
            "docs/handover*",
            ".agent-os/handover*",
            "transition*",
            "TRANSITION*"
        ]
        
        for pattern in handover_patterns:
            try:
                matches = list(self.project_root.glob(pattern))
                for match in matches:
                    if match.is_file():
                        handover_info["found"] = True
                        handover_info["locations"].append(str(match))
            except:
                continue
        
        return handover_info if handover_info["found"] else None
    
    def _analyze_development_context(self) -> Dict[str, Any]:
        """Analyze development environment context"""
        dev_context = {
            "likely_languages": [],
            "framework_indicators": [],
            "build_systems": [],
            "development_server_running": False
        }
        
        # Detect languages by file extensions
        language_indicators = {
            "javascript": [".js", ".jsx", ".ts", ".tsx"],
            "python": [".py"],
            "ruby": [".rb"],
            "java": [".java"],
            "go": [".go"],
            "rust": [".rs"],
            "php": [".php"],
            "c#": [".cs"],
            "c++": [".cpp", ".cc", ".cxx"]
        }
        
        try:
            all_files = list(self.project_root.rglob("*"))
            file_extensions = [f.suffix.lower() for f in all_files if f.is_file()]
            
            for language, extensions in language_indicators.items():
                if any(ext in file_extensions for ext in extensions):
                    dev_context["likely_languages"].append(language)
        except:
            pass
        
        # Detect frameworks and build systems
        framework_files = {
            "React": ["package.json"],  # Could check contents for react
            "Rails": ["Gemfile"],  # Could check contents for rails
            "Django": ["requirements.txt"],  # Could check contents for django
            "Next.js": ["next.config.js", "next.config.ts"],
            "Vue": ["vue.config.js"],
            "Angular": ["angular.json"]
        }
        
        build_files = {
            "npm": ["package.json"],
            "yarn": ["yarn.lock"],
            "bundler": ["Gemfile"],
            "pip": ["requirements.txt"],
            "cargo": ["Cargo.toml"],
            "maven": ["pom.xml"],
            "gradle": ["build.gradle"]
        }
        
        for framework, files in framework_files.items():
            if any((self.project_root / f).exists() for f in files):
                dev_context["framework_indicators"].append(framework)
        
        for build_system, files in build_files.items():
            if any((self.project_root / f).exists() for f in files):
                dev_context["build_systems"].append(build_system)
        
        # Check if development server might be running (basic check)
        try:
            import socket
            common_dev_ports = [3000, 3001, 4000, 5000, 8000, 8080, 9000]
            for port in common_dev_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('localhost', port))
                if result == 0:
                    dev_context["development_server_running"] = True
                    break
                sock.close()
        except:
            pass
        
        return dev_context

# Example usage
if __name__ == "__main__":
    analyzer = AgentOSContextAnalyzer()
    context = analyzer.get_full_context()
    print(json.dumps(context, indent=2))