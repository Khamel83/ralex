#!/usr/bin/env python3
"""
Advanced Pattern Recognition System for Agent-OS Intelligence
Implements machine learning-based pattern recognition for improved task classification.
"""

import json
import re
import math
import hashlib
from typing import Dict, List, Optional, Tuple, Any, Set
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, Counter
import time

class PatternType(Enum):
    LEXICAL = "lexical"           # Word patterns and vocabulary
    STRUCTURAL = "structural"     # Syntax and command structures
    SEMANTIC = "semantic"         # Meaning and intent patterns
    BEHAVIORAL = "behavioral"     # Execution behavior patterns
    CONTEXTUAL = "contextual"     # Context-dependent patterns
    TEMPORAL = "temporal"         # Time-based patterns

@dataclass
class Pattern:
    pattern_id: str
    pattern_type: PatternType
    pattern_data: Dict[str, Any]
    confidence: float
    frequency: int
    success_rate: float
    associated_tasks: List[str]
    creation_time: float
    last_used: float

@dataclass
class PatternMatch:
    pattern: Pattern
    match_strength: float
    relevance_score: float
    evidence: List[str]
    recommendations: List[str]

@dataclass
class ClassificationPrediction:
    predicted_task_type: str
    confidence: float
    pattern_matches: List[PatternMatch]
    reasoning: str
    alternative_predictions: List[Tuple[str, float]]

class PatternRecognitionEngine:
    """
    Agent-OS Intelligence: Advanced pattern recognition with machine learning.
    
    Features:
    - Multi-type pattern extraction and learning
    - Real-time pattern matching and classification
    - Behavioral pattern analysis from execution history
    - Context-aware pattern recognition
    - Temporal pattern detection and adaptation
    - Pattern evolution and refinement
    """
    
    def __init__(self, patterns_file: Optional[str] = None):
        self.patterns_file = patterns_file or Path(__file__).parent / "patterns-database.json"
        self.patterns: Dict[str, Pattern] = self._load_patterns()
        self.pattern_index = self._build_pattern_index()
        self.learning_parameters = self._initialize_learning_parameters()
        
    def _load_patterns(self) -> Dict[str, Pattern]:
        """Load learned patterns from persistent storage."""
        if not self.patterns_file.exists():
            return self._initialize_base_patterns()
        
        try:
            with open(self.patterns_file) as f:
                data = json.load(f)
                patterns = {}
                for pattern_id, pattern_data in data.get("patterns", {}).items():
                    patterns[pattern_id] = Pattern(
                        pattern_id=pattern_id,
                        pattern_type=PatternType(pattern_data["pattern_type"]),
                        pattern_data=pattern_data["pattern_data"],
                        confidence=pattern_data["confidence"],
                        frequency=pattern_data["frequency"],
                        success_rate=pattern_data["success_rate"],
                        associated_tasks=pattern_data["associated_tasks"],
                        creation_time=pattern_data["creation_time"],
                        last_used=pattern_data["last_used"]
                    )
                return patterns
        except:
            return self._initialize_base_patterns()
    
    def _save_patterns(self):
        """Save patterns to persistent storage."""
        self.patterns_file.parent.mkdir(exist_ok=True)
        with open(self.patterns_file, 'w') as f:
            patterns_data = {}
            for pattern_id, pattern in self.patterns.items():
                patterns_data[pattern_id] = asdict(pattern)
            
            json.dump({
                "patterns": patterns_data,
                "learning_parameters": self.learning_parameters,
                "last_updated": time.time()
            }, f, indent=2)
    
    def _initialize_base_patterns(self) -> Dict[str, Pattern]:
        """Initialize base patterns for bootstrapping the system."""
        base_patterns = {}
        current_time = time.time()
        
        # File operation patterns
        file_patterns = {
            "create_file": {
                "keywords": ["create", "write", "make", "generate"],
                "file_indicators": [r"\w+\.\w+", "file", "document"],
                "task_types": ["simple"]
            },
            "modify_file": {
                "keywords": ["edit", "modify", "update", "change", "fix"],
                "file_indicators": ["file", "code", "function"],
                "task_types": ["simple", "complex"]
            },
            "analyze_code": {
                "keywords": ["analyze", "review", "explain", "understand"],
                "code_indicators": ["code", "function", "class", "method"],
                "task_types": ["analysis"]
            }
        }
        
        for pattern_name, pattern_info in file_patterns.items():
            pattern_id = self._generate_pattern_id(pattern_name)
            base_patterns[pattern_id] = Pattern(
                pattern_id=pattern_id,
                pattern_type=PatternType.LEXICAL,
                pattern_data=pattern_info,
                confidence=0.7,
                frequency=1,
                success_rate=0.8,
                associated_tasks=pattern_info["task_types"],
                creation_time=current_time,
                last_used=current_time
            )
        
        # Mobile patterns
        mobile_patterns = {
            "mobile_api": {
                "keywords": ["mobile", "api", "endpoint", "opencat", "ios"],
                "indicators": ["mobile", "app", "client"],
                "task_types": ["mobile"]
            },
            "integration": {
                "keywords": ["integrate", "connect", "sync", "interface"],
                "indicators": ["api", "system", "service"],
                "task_types": ["complex", "mobile"]
            }
        }
        
        for pattern_name, pattern_info in mobile_patterns.items():
            pattern_id = self._generate_pattern_id(pattern_name)
            base_patterns[pattern_id] = Pattern(
                pattern_id=pattern_id,
                pattern_type=PatternType.SEMANTIC,
                pattern_data=pattern_info,
                confidence=0.8,
                frequency=1,
                success_rate=0.9,
                associated_tasks=pattern_info["task_types"],
                creation_time=current_time,
                last_used=current_time
            )
        
        # Complexity patterns
        complexity_patterns = {
            "architecture": {
                "keywords": ["architecture", "design", "refactor", "restructure"],
                "complexity_indicators": ["entire", "comprehensive", "complete"],
                "task_types": ["complex"]
            },
            "optimization": {
                "keywords": ["optimize", "performance", "improve", "enhance"],
                "scope_indicators": ["system", "codebase", "application"],
                "task_types": ["complex"]
            }
        }
        
        for pattern_name, pattern_info in complexity_patterns.items():
            pattern_id = self._generate_pattern_id(pattern_name)
            base_patterns[pattern_id] = Pattern(
                pattern_id=pattern_id,
                pattern_type=PatternType.STRUCTURAL,
                pattern_data=pattern_info,
                confidence=0.9,
                frequency=1,
                success_rate=0.7,
                associated_tasks=pattern_info["task_types"],
                creation_time=current_time,
                last_used=current_time
            )
        
        return base_patterns
    
    def _build_pattern_index(self) -> Dict[str, List[str]]:
        """Build inverted index for fast pattern lookup."""
        index = defaultdict(list)
        
        for pattern_id, pattern in self.patterns.items():
            # Index by keywords
            keywords = pattern.pattern_data.get("keywords", [])
            for keyword in keywords:
                index[keyword.lower()].append(pattern_id)
            
            # Index by indicators
            indicators = pattern.pattern_data.get("indicators", [])
            for indicator in indicators:
                index[indicator.lower()].append(pattern_id)
            
            # Index by task types
            for task_type in pattern.associated_tasks:
                index[f"task_type:{task_type}"].append(pattern_id)
        
        return dict(index)
    
    def _initialize_learning_parameters(self) -> Dict[str, float]:
        """Initialize learning parameters for pattern evolution."""
        return {
            "learning_rate": 0.01,
            "confidence_threshold": 0.6,
            "frequency_decay": 0.95,
            "pattern_creation_threshold": 0.8,
            "pattern_deletion_threshold": 0.1,
            "temporal_decay_factor": 0.1,
            "similarity_threshold": 0.7
        }
    
    def recognize_patterns(self, prompt: str, context: Optional[Dict] = None) -> ClassificationPrediction:
        """
        Recognize patterns in prompt and predict task classification.
        
        Args:
            prompt: User input to analyze
            context: Additional context information
            
        Returns:
            ClassificationPrediction with pattern-based recommendations
        """
        context = context or {}
        
        # Extract potential patterns from prompt
        candidate_patterns = self._extract_candidate_patterns(prompt, context)
        
        # Match against known patterns
        pattern_matches = []
        for pattern_id in candidate_patterns:
            if pattern_id in self.patterns:
                pattern = self.patterns[pattern_id]
                match = self._evaluate_pattern_match(pattern, prompt, context)
                if match:
                    pattern_matches.append(match)
        
        # Score and rank pattern matches
        ranked_matches = sorted(pattern_matches, 
                              key=lambda x: x.match_strength * x.relevance_score, 
                              reverse=True)
        
        # Generate classification prediction
        prediction = self._generate_classification_prediction(ranked_matches, prompt, context)
        
        # Update pattern usage statistics
        self._update_pattern_usage(ranked_matches)
        
        return prediction
    
    def _extract_candidate_patterns(self, prompt: str, context: Dict) -> List[str]:
        """Extract candidate patterns from prompt using index."""
        candidates = set()
        prompt_words = prompt.lower().split()
        
        # Direct keyword matching
        for word in prompt_words:
            if word in self.pattern_index:
                candidates.update(self.pattern_index[word])
        
        # N-gram matching
        for i in range(len(prompt_words) - 1):
            bigram = f"{prompt_words[i]} {prompt_words[i+1]}"
            if bigram in self.pattern_index:
                candidates.update(self.pattern_index[bigram])
        
        # Context-based candidates
        if context.get("interface") == "mobile":
            candidates.update(self.pattern_index.get("task_type:mobile", []))
        
        if context.get("file_count", 0) > 5:
            candidates.update(self.pattern_index.get("task_type:batch", []))
        
        return list(candidates)
    
    def _evaluate_pattern_match(self, pattern: Pattern, prompt: str, context: Dict) -> Optional[PatternMatch]:
        """Evaluate how well a pattern matches the given prompt."""
        match_strength = 0.0
        evidence = []
        recommendations = []
        
        pattern_data = pattern.pattern_data
        prompt_lower = prompt.lower()
        
        # Keyword matching
        keywords = pattern_data.get("keywords", [])
        keyword_matches = sum(1 for keyword in keywords if keyword in prompt_lower)
        if keywords:
            keyword_score = keyword_matches / len(keywords)
            match_strength += keyword_score * 0.4
            if keyword_matches > 0:
                evidence.append(f"Keyword matches: {keyword_matches}/{len(keywords)}")
        
        # Indicator matching
        indicators = pattern_data.get("indicators", [])
        indicator_matches = sum(1 for indicator in indicators if indicator in prompt_lower)
        if indicators:
            indicator_score = indicator_matches / len(indicators)
            match_strength += indicator_score * 0.3
            if indicator_matches > 0:
                evidence.append(f"Indicator matches: {indicator_matches}/{len(indicators)}")
        
        # File pattern matching
        file_indicators = pattern_data.get("file_indicators", [])
        file_matches = 0
        for file_pattern in file_indicators:
            if re.search(file_pattern, prompt):
                file_matches += 1
        if file_indicators:
            file_score = file_matches / len(file_indicators)
            match_strength += file_score * 0.2
            if file_matches > 0:
                evidence.append(f"File pattern matches: {file_matches}")
        
        # Context matching
        context_score = self._evaluate_context_match(pattern, context)
        match_strength += context_score * 0.1
        
        # Apply pattern confidence and success rate
        relevance_score = pattern.confidence * pattern.success_rate
        
        # Apply temporal decay (recent patterns are more relevant)
        time_decay = self._calculate_temporal_decay(pattern.last_used)
        relevance_score *= time_decay
        
        # Generate recommendations
        if match_strength > 0.6:
            if pattern.pattern_type == PatternType.STRUCTURAL:
                recommendations.append("Consider breaking into smaller subtasks")
            elif pattern.pattern_type == PatternType.SEMANTIC and "mobile" in pattern.associated_tasks:
                recommendations.append("Ensure mobile workflow compatibility")
        
        if match_strength > self.learning_parameters["confidence_threshold"]:
            return PatternMatch(
                pattern=pattern,
                match_strength=match_strength,
                relevance_score=relevance_score,
                evidence=evidence,
                recommendations=recommendations
            )
        
        return None
    
    def _evaluate_context_match(self, pattern: Pattern, context: Dict) -> float:
        """Evaluate context-specific pattern matching."""
        score = 0.0
        
        # File count context
        file_count = context.get("file_count", 0)
        if "batch" in pattern.associated_tasks and file_count > 3:
            score += 0.3
        elif "simple" in pattern.associated_tasks and file_count <= 2:
            score += 0.2
        
        # Interface context
        interface = context.get("interface", "")
        if "mobile" in pattern.associated_tasks and interface == "mobile":
            score += 0.4
        
        # Complexity context
        if "complexity_indicators" in pattern.pattern_data:
            # This would need actual complexity analysis
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_temporal_decay(self, last_used: float) -> float:
        """Calculate temporal decay factor for pattern relevance."""
        current_time = time.time()
        days_since_use = (current_time - last_used) / (24 * 3600)
        
        # Exponential decay with 30-day half-life
        decay_factor = math.exp(-days_since_use * self.learning_parameters["temporal_decay_factor"])
        return max(0.1, decay_factor)  # Minimum 10% relevance
    
    def _generate_classification_prediction(self, pattern_matches: List[PatternMatch], 
                                          prompt: str, context: Dict) -> ClassificationPrediction:
        """Generate task classification prediction from pattern matches."""
        if not pattern_matches:
            return ClassificationPrediction(
                predicted_task_type="simple",
                confidence=0.3,
                pattern_matches=[],
                reasoning="No significant patterns detected - defaulting to simple task",
                alternative_predictions=[("analysis", 0.2), ("mobile", 0.1)]
            )
        
        # Vote-based classification
        task_votes = defaultdict(float)
        total_weight = 0.0
        
        for match in pattern_matches:
            weight = match.match_strength * match.relevance_score
            for task_type in match.pattern.associated_tasks:
                task_votes[task_type] += weight
            total_weight += weight
        
        # Normalize votes
        if total_weight > 0:
            normalized_votes = {task: vote/total_weight for task, vote in task_votes.items()}
        else:
            normalized_votes = {"simple": 1.0}
        
        # Get primary prediction
        predicted_task = max(normalized_votes.items(), key=lambda x: x[1])
        predicted_task_type = predicted_task[0]
        confidence = predicted_task[1]
        
        # Get alternative predictions
        alternative_predictions = sorted(
            [(task, score) for task, score in normalized_votes.items() if task != predicted_task_type],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        # Generate reasoning
        reasoning = self._generate_reasoning(pattern_matches, predicted_task_type, confidence)
        
        return ClassificationPrediction(
            predicted_task_type=predicted_task_type,
            confidence=confidence,
            pattern_matches=pattern_matches[:5],  # Top 5 matches
            reasoning=reasoning,
            alternative_predictions=alternative_predictions
        )
    
    def _generate_reasoning(self, pattern_matches: List[PatternMatch], 
                          predicted_task: str, confidence: float) -> str:
        """Generate human-readable reasoning for the prediction."""
        if not pattern_matches:
            return "No strong patterns detected"
        
        top_pattern = pattern_matches[0]
        reasoning = f"Primary pattern: {top_pattern.pattern.pattern_type.value} "
        reasoning += f"(strength: {top_pattern.match_strength:.2f})"
        
        if len(pattern_matches) > 1:
            reasoning += f" + {len(pattern_matches)-1} supporting patterns"
        
        if confidence > 0.8:
            reasoning += " - High confidence prediction"
        elif confidence > 0.6:
            reasoning += " - Moderate confidence prediction"
        else:
            reasoning += " - Low confidence prediction"
        
        return reasoning
    
    def _update_pattern_usage(self, pattern_matches: List[PatternMatch]):
        """Update pattern usage statistics."""
        current_time = time.time()
        
        for match in pattern_matches:
            pattern = match.pattern
            pattern.frequency += 1
            pattern.last_used = current_time
            
            # Apply frequency decay to other patterns
            for other_pattern in self.patterns.values():
                if other_pattern.pattern_id != pattern.pattern_id:
                    other_pattern.frequency *= self.learning_parameters["frequency_decay"]
    
    def learn_from_execution(self, prompt: str, predicted_task: str, actual_task: str,
                           success: bool, execution_time: float, context: Optional[Dict] = None):
        """Learn from execution results to improve pattern recognition."""
        context = context or {}
        
        # Extract new patterns if prediction was wrong or low confidence
        if predicted_task != actual_task or not success:
            self._extract_new_patterns(prompt, actual_task, context)
        
        # Update pattern success rates
        pattern_matches = self.recognize_patterns(prompt, context).pattern_matches
        for match in pattern_matches:
            pattern = match.pattern
            
            if actual_task in pattern.associated_tasks:
                # Correct prediction - boost success rate
                pattern.success_rate = min(0.95, pattern.success_rate * 1.02)
                pattern.confidence = min(0.95, pattern.confidence * 1.01)
            else:
                # Incorrect prediction - reduce success rate
                pattern.success_rate *= 0.98
                pattern.confidence *= 0.99
        
        # Evolve patterns based on performance
        self._evolve_patterns()
        
        # Save updated patterns
        self._save_patterns()
    
    def _extract_new_patterns(self, prompt: str, task_type: str, context: Dict):
        """Extract new patterns from successful executions."""
        # Simple pattern extraction - could be much more sophisticated
        words = prompt.lower().split()
        
        # Look for recurring word combinations
        if len(words) >= 3:
            for i in range(len(words) - 2):
                trigram = " ".join(words[i:i+3])
                
                # Check if this trigram appears in successful task types
                pattern_id = self._generate_pattern_id(trigram)
                
                if pattern_id not in self.patterns:
                    # Create new pattern
                    new_pattern = Pattern(
                        pattern_id=pattern_id,
                        pattern_type=PatternType.LEXICAL,
                        pattern_data={
                            "keywords": words[i:i+3],
                            "trigram": trigram
                        },
                        confidence=0.5,
                        frequency=1,
                        success_rate=0.8,
                        associated_tasks=[task_type],
                        creation_time=time.time(),
                        last_used=time.time()
                    )
                    
                    self.patterns[pattern_id] = new_pattern
                    self._rebuild_pattern_index()
    
    def _evolve_patterns(self):
        """Evolve patterns by removing low-performing ones and consolidating similar ones."""
        # Remove low-performing patterns
        patterns_to_remove = []
        for pattern_id, pattern in self.patterns.items():
            if (pattern.success_rate < self.learning_parameters["pattern_deletion_threshold"] and
                pattern.frequency < 5):
                patterns_to_remove.append(pattern_id)
        
        for pattern_id in patterns_to_remove:
            del self.patterns[pattern_id]
        
        # Consolidate similar patterns (simplified implementation)
        # In a full implementation, this would use more sophisticated similarity measures
        if patterns_to_remove:
            self._rebuild_pattern_index()
    
    def _rebuild_pattern_index(self):
        """Rebuild the pattern index after pattern changes."""
        self.pattern_index = self._build_pattern_index()
    
    def _generate_pattern_id(self, pattern_name: str) -> str:
        """Generate unique pattern ID."""
        return hashlib.md5(pattern_name.encode()).hexdigest()[:16]
    
    def get_pattern_analytics(self) -> Dict:
        """Get pattern recognition performance analytics."""
        if not self.patterns:
            return {"message": "No patterns available"}
        
        total_patterns = len(self.patterns)
        
        # Pattern type distribution
        type_distribution = defaultdict(int)
        success_rates = []
        frequencies = []
        
        for pattern in self.patterns.values():
            type_distribution[pattern.pattern_type.value] += 1
            success_rates.append(pattern.success_rate)
            frequencies.append(pattern.frequency)
        
        avg_success_rate = sum(success_rates) / len(success_rates)
        avg_frequency = sum(frequencies) / len(frequencies)
        
        # Task type coverage
        task_coverage = defaultdict(int)
        for pattern in self.patterns.values():
            for task_type in pattern.associated_tasks:
                task_coverage[task_type] += 1
        
        # High-performing patterns
        high_performers = [
            pattern for pattern in self.patterns.values()
            if pattern.success_rate > 0.8 and pattern.frequency > 5
        ]
        
        return {
            "total_patterns": total_patterns,
            "pattern_type_distribution": dict(type_distribution),
            "avg_success_rate": avg_success_rate,
            "avg_frequency": avg_frequency,
            "task_type_coverage": dict(task_coverage),
            "high_performing_patterns": len(high_performers),
            "learning_parameters": self.learning_parameters
        }
    
    def optimize_patterns(self) -> Dict:
        """Optimize pattern database for better performance."""
        optimization_results = {
            "patterns_before": len(self.patterns),
            "actions_taken": []
        }
        
        # Remove redundant patterns
        redundant_patterns = self._find_redundant_patterns()
        for pattern_id in redundant_patterns:
            del self.patterns[pattern_id]
            optimization_results["actions_taken"].append(f"Removed redundant pattern: {pattern_id}")
        
        # Boost high-performing patterns
        for pattern in self.patterns.values():
            if pattern.success_rate > 0.9 and pattern.frequency > 10:
                pattern.confidence = min(0.95, pattern.confidence * 1.05)
                optimization_results["actions_taken"].append(f"Boosted high performer: {pattern.pattern_id}")
        
        # Rebuild index
        self._rebuild_pattern_index()
        
        optimization_results["patterns_after"] = len(self.patterns)
        optimization_results["patterns_removed"] = len(redundant_patterns)
        
        # Save optimized patterns
        self._save_patterns()
        
        return optimization_results
    
    def _find_redundant_patterns(self) -> List[str]:
        """Find and identify redundant patterns for removal."""
        redundant = []
        
        patterns_list = list(self.patterns.values())
        for i, pattern1 in enumerate(patterns_list):
            for j, pattern2 in enumerate(patterns_list[i+1:], i+1):
                if self._patterns_similar(pattern1, pattern2):
                    # Keep the one with higher success rate
                    if pattern1.success_rate < pattern2.success_rate:
                        redundant.append(pattern1.pattern_id)
                    else:
                        redundant.append(pattern2.pattern_id)
        
        return list(set(redundant))  # Remove duplicates
    
    def _patterns_similar(self, pattern1: Pattern, pattern2: Pattern) -> bool:
        """Check if two patterns are similar enough to be considered redundant."""
        # Simplified similarity check
        if pattern1.pattern_type != pattern2.pattern_type:
            return False
        
        # Check keyword overlap
        keywords1 = set(pattern1.pattern_data.get("keywords", []))
        keywords2 = set(pattern2.pattern_data.get("keywords", []))
        
        if keywords1 and keywords2:
            overlap = len(keywords1.intersection(keywords2))
            union = len(keywords1.union(keywords2))
            similarity = overlap / union if union > 0 else 0
            
            return similarity > self.learning_parameters["similarity_threshold"]
        
        return False

def quick_recognize_patterns(prompt: str, context: Optional[Dict] = None) -> ClassificationPrediction:
    """Quick pattern recognition function for CLI integration."""
    engine = PatternRecognitionEngine()
    return engine.recognize_patterns(prompt, context)

if __name__ == "__main__":
    # Test pattern recognition engine
    engine = PatternRecognitionEngine()
    
    test_prompts = [
        "create a simple hello.py file",
        "refactor the entire codebase architecture using design patterns",
        "fix the mobile API endpoint for OpenCat integration",
        "analyze the performance of our distributed system",
        "optimize the database queries for better performance"
    ]
    
    print("=== Pattern Recognition Engine Testing ===")
    
    for prompt in test_prompts:
        print(f"\n--- Analyzing: {prompt} ---")
        
        prediction = engine.recognize_patterns(prompt)
        
        print(f"Predicted Task Type: {prediction.predicted_task_type}")
        print(f"Confidence: {prediction.confidence:.3f}")
        print(f"Reasoning: {prediction.reasoning}")
        
        if prediction.pattern_matches:
            print("Pattern Matches:")
            for match in prediction.pattern_matches[:3]:  # Top 3
                print(f"  {match.pattern.pattern_type.value}: {match.match_strength:.3f}")
                if match.evidence:
                    print(f"    Evidence: {', '.join(match.evidence)}")
        
        if prediction.alternative_predictions:
            print("Alternatives:")
            for alt_task, alt_conf in prediction.alternative_predictions[:2]:
                print(f"  {alt_task}: {alt_conf:.3f}")
    
    print(f"\n--- Pattern Analytics ---")
    analytics = engine.get_pattern_analytics()
    for key, value in analytics.items():
        print(f"{key}: {value}")
    
    print(f"\n--- Pattern Optimization ---")
    optimization = engine.optimize_patterns()
    print(f"Optimization results: {optimization}")