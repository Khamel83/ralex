#!/usr/bin/env python3
"""
Pattern Manager - Manages pattern library and learning for Agent OS integration
This module handles pattern recognition, storage, and reuse.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import re

@dataclass
class Pattern:
    """Represents a reusable pattern"""
    name: str
    description: str
    task_type: str
    complexity: str
    components: List[str]
    success_rate: float
    usage_count: int
    last_used: str
    template: Dict[str, Any]
    tags: List[str]
    created_date: str
    updated_date: str

class PatternManager:
    """Manages patterns for Agent OS integration"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.patterns_cache = {}
        self._load_patterns()
    
    def find_matching_patterns(self, task_description: str, threshold: float = 0.6) -> List[Dict[str, Any]]:
        """Find patterns that match the given task description"""
        
        matches = []
        task_lower = task_description.lower()
        task_words = set(re.findall(r'\w+', task_lower))
        
        for pattern_id, pattern in self.patterns_cache.items():
            # Calculate similarity score
            confidence = self._calculate_pattern_confidence(task_description, pattern)
            
            if confidence >= threshold:
                matches.append({
                    "name": pattern.name,
                    "description": pattern.description,
                    "confidence": confidence,
                    "success_rate": pattern.success_rate,
                    "usage_count": pattern.usage_count,
                    "task_type": pattern.task_type,
                    "complexity": pattern.complexity,
                    "template": pattern.template,
                    "pattern_id": pattern_id
                })
        
        # Sort by confidence and success rate
        matches.sort(key=lambda x: (x["confidence"], x["success_rate"]), reverse=True)
        return matches
    
    def save_successful_pattern(self, 
                              task_description: str,
                              methodology_used: str,
                              phases: List[Dict[str, Any]],
                              success_metrics: Dict[str, Any],
                              context: Dict[str, Any] = None) -> str:
        """Save a successful task execution as a reusable pattern"""
        
        # Generate pattern from successful execution
        pattern = self._create_pattern_from_execution(
            task_description, methodology_used, phases, success_metrics, context
        )
        
        # Generate unique pattern ID
        pattern_id = self._generate_pattern_id(pattern)
        
        # Check if similar pattern already exists
        existing_pattern_id = self._find_similar_existing_pattern(pattern)
        
        if existing_pattern_id:
            # Update existing pattern
            self._update_existing_pattern(existing_pattern_id, pattern, success_metrics)
            return existing_pattern_id
        else:
            # Save as new pattern
            self.patterns_cache[pattern_id] = pattern
            self._save_pattern_to_file(pattern_id, pattern)
            return pattern_id
    
    def get_pattern_usage_stats(self) -> Dict[str, Any]:
        """Get statistics about pattern usage"""
        
        if not self.patterns_cache:
            return {"total_patterns": 0, "most_used": None, "success_rates": {}}
        
        total_patterns = len(self.patterns_cache)
        total_usage = sum(p.usage_count for p in self.patterns_cache.values())
        
        # Find most used pattern
        most_used = max(self.patterns_cache.values(), key=lambda p: p.usage_count)
        
        # Calculate success rates by category
        success_rates = {}
        task_types = set(p.task_type for p in self.patterns_cache.values())
        
        for task_type in task_types:
            patterns_of_type = [p for p in self.patterns_cache.values() if p.task_type == task_type]
            if patterns_of_type:
                avg_success_rate = sum(p.success_rate for p in patterns_of_type) / len(patterns_of_type)
                success_rates[task_type] = {
                    "average_success_rate": avg_success_rate,
                    "pattern_count": len(patterns_of_type),
                    "total_usage": sum(p.usage_count for p in patterns_of_type)
                }
        
        return {
            "total_patterns": total_patterns,
            "total_usage": total_usage,
            "most_used": {
                "name": most_used.name,
                "usage_count": most_used.usage_count,
                "success_rate": most_used.success_rate
            },
            "success_rates": success_rates
        }
    
    def suggest_pattern_improvements(self, pattern_id: str, recent_results: List[Dict[str, Any]]) -> List[str]:
        """Suggest improvements to a pattern based on recent usage"""
        
        if pattern_id not in self.patterns_cache:
            return ["Pattern not found"]
        
        pattern = self.patterns_cache[pattern_id]
        suggestions = []
        
        # Analyze recent success rates
        if recent_results:
            recent_success_rate = sum(1 for r in recent_results if r.get("success", False)) / len(recent_results)
            
            if recent_success_rate < pattern.success_rate * 0.8:  # Significant drop
                suggestions.append("Pattern success rate has declined - consider reviewing and updating")
            
            # Check for common failure points
            failures = [r for r in recent_results if not r.get("success", True)]
            if failures:
                failure_reasons = [f.get("failure_reason", "unknown") for f in failures]
                common_failures = max(set(failure_reasons), key=failure_reasons.count)
                suggestions.append(f"Common failure: {common_failures} - consider adding mitigation")
        
        # Check pattern age
        try:
            created_date = datetime.fromisoformat(pattern.created_date)
            days_old = (datetime.now() - created_date).days
            
            if days_old > 90:  # Pattern is older than 3 months
                suggestions.append("Pattern is over 3 months old - consider reviewing for relevance")
        except:
            pass
        
        # Usage-based suggestions
        if pattern.usage_count > 20 and pattern.success_rate > 0.9:
            suggestions.append("High-performing pattern - consider promoting to global template")
        elif pattern.usage_count < 3:
            suggestions.append("Low usage pattern - consider if it's too specific or needs better tagging")
        
        return suggestions if suggestions else ["Pattern appears to be performing well"]
    
    def _load_patterns(self):
        """Load patterns from various sources"""
        
        # Load from project pattern cache
        project_patterns_dir = self.project_root / ".project" / "patterns"
        if project_patterns_dir.exists():
            self._load_patterns_from_directory(project_patterns_dir)
        
        # Load from Agent OS pattern cache
        agent_os_patterns_dir = self.project_root / ".khamel83" / "pattern-cache"
        if agent_os_patterns_dir.exists():
            self._load_patterns_from_directory(agent_os_patterns_dir)
        
        # Load from global patterns (if available)
        global_patterns_dir = Path.home() / ".agent-os" / "global-patterns"
        if global_patterns_dir.exists():
            self._load_patterns_from_directory(global_patterns_dir)
    
    def _load_patterns_from_directory(self, patterns_dir: Path):
        """Load patterns from a specific directory"""
        
        try:
            pattern_files = list(patterns_dir.glob("*.json"))
            
            for pattern_file in pattern_files:
                try:
                    with open(pattern_file, 'r') as f:
                        pattern_data = json.load(f)
                        
                        # Convert to Pattern object
                        pattern = Pattern(**pattern_data)
                        pattern_id = pattern_file.stem
                        self.patterns_cache[pattern_id] = pattern
                        
                except Exception as e:
                    print(f"Error loading pattern {pattern_file}: {e}")
                    
        except Exception as e:
            print(f"Error loading patterns from {patterns_dir}: {e}")
    
    def _calculate_pattern_confidence(self, task_description: str, pattern: Pattern) -> float:
        """Calculate confidence that a pattern matches the task"""
        
        task_lower = task_description.lower()
        task_words = set(re.findall(r'\w+', task_lower))
        
        confidence = 0.0
        
        # Check task type match
        if pattern.task_type.lower() in task_lower:
            confidence += 0.3
        
        # Check component matches
        component_matches = 0
        for component in pattern.components:
            if component.lower() in task_lower:
                component_matches += 1
        
        if pattern.components:
            confidence += 0.3 * (component_matches / len(pattern.components))
        
        # Check tag matches
        tag_matches = 0
        for tag in pattern.tags:
            if tag.lower() in task_lower:
                tag_matches += 1
        
        if pattern.tags:
            confidence += 0.2 * (tag_matches / len(pattern.tags))
        
        # Check description similarity
        description_words = set(re.findall(r'\w+', pattern.description.lower()))
        word_overlap = len(task_words.intersection(description_words))
        total_words = len(task_words.union(description_words))
        
        if total_words > 0:
            confidence += 0.2 * (word_overlap / total_words)
        
        return min(confidence, 1.0)  # Cap at 1.0
    
    def _create_pattern_from_execution(self,
                                     task_description: str,
                                     methodology_used: str,
                                     phases: List[Dict[str, Any]],
                                     success_metrics: Dict[str, Any],
                                     context: Dict[str, Any] = None) -> Pattern:
        """Create a pattern from a successful task execution"""
        
        # Extract pattern name from task description
        pattern_name = self._generate_pattern_name(task_description)
        
        # Determine task type
        task_type = self._infer_task_type(task_description, phases)
        
        # Extract components
        components = self._extract_components(phases)
        
        # Generate tags
        tags = self._generate_tags(task_description, phases, context)
        
        # Determine complexity
        complexity = self._infer_complexity(phases, success_metrics)
        
        # Create template from phases
        template = {
            "methodology": methodology_used,
            "phases": phases,
            "success_factors": success_metrics.get("success_factors", []),
            "common_pitfalls": success_metrics.get("pitfalls", []),
            "estimated_time": success_metrics.get("actual_time", "unknown")
        }
        
        now = datetime.now().isoformat()
        
        return Pattern(
            name=pattern_name,
            description=task_description,
            task_type=task_type,
            complexity=complexity,
            components=components,
            success_rate=1.0,  # Start with 100% since this was successful
            usage_count=1,
            last_used=now,
            template=template,
            tags=tags,
            created_date=now,
            updated_date=now
        )
    
    def _generate_pattern_id(self, pattern: Pattern) -> str:
        """Generate a unique ID for a pattern"""
        
        # Create hash from pattern name and key components
        content = f"{pattern.name}_{pattern.task_type}_{'_'.join(sorted(pattern.components))}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _find_similar_existing_pattern(self, new_pattern: Pattern) -> Optional[str]:
        """Find if a similar pattern already exists"""
        
        for pattern_id, existing_pattern in self.patterns_cache.items():
            # Check for high similarity
            similarity = self._calculate_pattern_similarity(new_pattern, existing_pattern)
            
            if similarity > 0.8:  # Very similar
                return pattern_id
        
        return None
    
    def _calculate_pattern_similarity(self, pattern1: Pattern, pattern2: Pattern) -> float:
        """Calculate similarity between two patterns"""
        
        similarity = 0.0
        
        # Task type match
        if pattern1.task_type == pattern2.task_type:
            similarity += 0.3
        
        # Component overlap
        components1 = set(pattern1.components)
        components2 = set(pattern2.components)
        
        if components1 or components2:
            overlap = len(components1.intersection(components2))
            total = len(components1.union(components2))
            similarity += 0.4 * (overlap / total if total > 0 else 0)
        
        # Name/description similarity (simple word overlap)
        words1 = set(re.findall(r'\w+', pattern1.name.lower()))
        words2 = set(re.findall(r'\w+', pattern2.name.lower()))
        
        if words1 or words2:
            word_overlap = len(words1.intersection(words2))
            total_words = len(words1.union(words2))
            similarity += 0.3 * (word_overlap / total_words if total_words > 0 else 0)
        
        return similarity
    
    def _update_existing_pattern(self, pattern_id: str, new_pattern: Pattern, success_metrics: Dict[str, Any]):
        """Update an existing pattern with new information"""
        
        existing_pattern = self.patterns_cache[pattern_id]
        
        # Update usage count
        existing_pattern.usage_count += 1
        
        # Update success rate (weighted average)
        total_attempts = existing_pattern.usage_count
        existing_successes = existing_pattern.success_rate * (total_attempts - 1)
        new_success = 1.0  # This execution was successful
        existing_pattern.success_rate = (existing_successes + new_success) / total_attempts
        
        # Update last used
        existing_pattern.last_used = datetime.now().isoformat()
        existing_pattern.updated_date = datetime.now().isoformat()
        
        # Merge any new tags or components
        existing_pattern.tags = list(set(existing_pattern.tags + new_pattern.tags))
        existing_pattern.components = list(set(existing_pattern.components + new_pattern.components))
        
        # Save updated pattern
        self._save_pattern_to_file(pattern_id, existing_pattern)
    
    def _save_pattern_to_file(self, pattern_id: str, pattern: Pattern):
        """Save pattern to file"""
        
        # Choose save location (prefer project patterns)
        patterns_dir = self.project_root / ".project" / "patterns"
        
        if not patterns_dir.exists():
            patterns_dir.mkdir(parents=True, exist_ok=True)
        
        pattern_file = patterns_dir / f"{pattern_id}.json"
        
        try:
            with open(pattern_file, 'w') as f:
                json.dump(asdict(pattern), f, indent=2)
        except Exception as e:
            print(f"Error saving pattern {pattern_id}: {e}")
    
    def _generate_pattern_name(self, task_description: str) -> str:
        """Generate a pattern name from task description"""
        
        # Extract key words and create a readable name
        words = re.findall(r'\w+', task_description.lower())
        
        # Filter out common words
        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        key_words = [w for w in words if w not in stop_words][:4]  # Take first 4 key words
        
        return "_".join(key_words)
    
    def _infer_task_type(self, task_description: str, phases: List[Dict[str, Any]]) -> str:
        """Infer task type from description and phases"""
        
        task_lower = task_description.lower()
        
        # Check for common task type indicators
        if any(word in task_lower for word in ["api", "endpoint", "route"]):
            return "api_development"
        elif any(word in task_lower for word in ["database", "schema", "model"]):
            return "database_work"
        elif any(word in task_lower for word in ["auth", "login", "user"]):
            return "authentication"
        elif any(word in task_lower for word in ["ui", "component", "frontend"]):
            return "frontend_development"
        elif any(word in task_lower for word in ["test", "testing"]):
            return "testing"
        else:
            return "general_development"
    
    def _extract_components(self, phases: List[Dict[str, Any]]) -> List[str]:
        """Extract components from phase information"""
        
        components = []
        
        for phase in phases:
            # Look for micro-tasks or activities
            micro_tasks = phase.get("micro_tasks", [])
            activities = phase.get("activities", [])
            
            for task in micro_tasks + activities:
                # Extract component names (simplified)
                words = re.findall(r'\w+', task.lower())
                # Look for nouns that might be components
                potential_components = [w for w in words if len(w) > 3 and w not in ['implement', 'create', 'build', 'test']]
                components.extend(potential_components[:2])  # Take first 2
        
        # Remove duplicates and return
        return list(set(components))
    
    def _generate_tags(self, task_description: str, phases: List[Dict[str, Any]], context: Dict[str, Any] = None) -> List[str]:
        """Generate tags for the pattern"""
        
        tags = []
        task_lower = task_description.lower()
        
        # Add technology tags based on context
        if context:
            languages = context.get("development_context", {}).get("likely_languages", [])
            tags.extend(languages)
            
            frameworks = context.get("development_context", {}).get("framework_indicators", [])
            tags.extend([f.lower() for f in frameworks])
        
        # Add methodology tags
        methodology_used = phases[0].get("methodology", "unknown") if phases else "unknown"
        tags.append(methodology_used)
        
        # Add complexity tags
        if len(phases) > 2:
            tags.append("complex")
        elif len(phases) == 1:
            tags.append("simple")
        else:
            tags.append("medium")
        
        # Add functional tags
        if "crud" in task_lower:
            tags.append("crud")
        if "security" in task_lower or "auth" in task_lower:
            tags.append("security")
        if "performance" in task_lower:
            tags.append("performance")
        
        return list(set(tags))  # Remove duplicates
    
    def _infer_complexity(self, phases: List[Dict[str, Any]], success_metrics: Dict[str, Any]) -> str:
        """Infer complexity from phases and metrics"""
        
        if len(phases) >= 3:
            return "complex"
        elif len(phases) == 2:
            return "medium"
        else:
            return "simple"

# Example usage
if __name__ == "__main__":
    manager = PatternManager()
    
    # Example pattern matching
    matches = manager.find_matching_patterns("implement user authentication")
    print(f"Found {len(matches)} matching patterns")
    
    for match in matches:
        print(f"- {match['name']} (confidence: {match['confidence']:.2f})")
    
    # Example usage stats
    stats = manager.get_pattern_usage_stats()
    print(f"\nPattern library stats: {stats['total_patterns']} patterns")