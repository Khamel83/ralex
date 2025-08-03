#!/usr/bin/env python3
"""
Advanced Complexity Analysis Engine for Agent-OS Intelligence
Implements machine learning-based complexity detection with execution history analysis.
"""

import json
import re
import math
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import time

class ComplexityFactor(Enum):
    LEXICAL = "lexical"           # Word patterns, technical terms
    SYNTACTIC = "syntactic"       # Code structure, commands
    SEMANTIC = "semantic"         # Meaning, context, relationships
    PROCEDURAL = "procedural"     # Steps, dependencies, workflow
    COGNITIVE = "cognitive"       # Mental model complexity
    TEMPORAL = "temporal"         # Time-based patterns, urgency

@dataclass
class ComplexityScore:
    factor: ComplexityFactor
    score: float  # 0.0-1.0
    confidence: float  # 0.0-1.0
    reasoning: str
    evidence: List[str]

@dataclass
class ComplexityAnalysis:
    overall_complexity: float  # 0.0-1.0 normalized
    complexity_level: str     # "low", "medium", "high"
    factor_scores: List[ComplexityScore]
    execution_prediction: Dict[str, float]
    resource_requirements: Dict[str, Any]
    risk_assessment: Dict[str, float]
    learning_insights: List[str]

@dataclass
class ExecutionHistory:
    prompt: str
    actual_complexity: float
    execution_time: float
    tokens_used: int
    success_rate: float
    error_patterns: List[str]
    timestamp: float

class AdvancedComplexityAnalyzer:
    """
    Agent-OS Intelligence Layer: Advanced complexity analysis with learning capabilities.
    
    Features:
    - Multi-factor complexity analysis (lexical, syntactic, semantic, procedural, cognitive, temporal)
    - Machine learning from execution history
    - Predictive complexity scoring
    - Resource requirement estimation
    - Risk assessment integration
    - Pattern recognition for similar tasks
    """
    
    def __init__(self, history_file: Optional[str] = None):
        self.history_file = history_file or Path(__file__).parent / "complexity-history.json"
        self.execution_history: List[ExecutionHistory] = self._load_history()
        self.pattern_cache = {}
        self.learning_weights = self._initialize_learning_weights()
        
    def _load_history(self) -> List[ExecutionHistory]:
        """Load execution history for learning."""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file) as f:
                data = json.load(f)
                return [
                    ExecutionHistory(**item) for item in data.get("execution_history", [])
                ]
        except:
            return []
    
    def _save_history(self):
        """Save execution history for persistence."""
        self.history_file.parent.mkdir(exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump({
                "execution_history": [asdict(h) for h in self.execution_history],
                "learning_weights": self.learning_weights,
                "last_updated": time.time()
            }, f, indent=2)
    
    def _initialize_learning_weights(self) -> Dict[str, float]:
        """Initialize learning weights for different complexity factors."""
        return {
            "lexical_weight": 0.15,
            "syntactic_weight": 0.25,
            "semantic_weight": 0.20,
            "procedural_weight": 0.20,
            "cognitive_weight": 0.15,
            "temporal_weight": 0.05,
            "history_influence": 0.3,
            "pattern_matching": 0.4
        }
    
    def analyze_complexity(self, prompt: str, context: Optional[Dict] = None) -> ComplexityAnalysis:
        """
        Perform comprehensive complexity analysis using Agent-OS intelligence.
        
        Args:
            prompt: User input to analyze
            context: Additional context (files, session data, etc.)
            
        Returns:
            ComplexityAnalysis with detailed multi-factor assessment
        """
        context = context or {}
        
        # Multi-factor analysis
        factor_scores = []
        
        # 1. Lexical Complexity Analysis
        lexical_score = self._analyze_lexical_complexity(prompt, context)
        factor_scores.append(lexical_score)
        
        # 2. Syntactic Complexity Analysis
        syntactic_score = self._analyze_syntactic_complexity(prompt, context)
        factor_scores.append(syntactic_score)
        
        # 3. Semantic Complexity Analysis
        semantic_score = self._analyze_semantic_complexity(prompt, context)
        factor_scores.append(semantic_score)
        
        # 4. Procedural Complexity Analysis
        procedural_score = self._analyze_procedural_complexity(prompt, context)
        factor_scores.append(procedural_score)
        
        # 5. Cognitive Complexity Analysis
        cognitive_score = self._analyze_cognitive_complexity(prompt, context)
        factor_scores.append(cognitive_score)
        
        # 6. Temporal Complexity Analysis
        temporal_score = self._analyze_temporal_complexity(prompt, context)
        factor_scores.append(temporal_score)
        
        # Calculate overall complexity using learned weights
        overall_complexity = self._calculate_weighted_complexity(factor_scores)
        
        # Apply historical learning
        historical_adjustment = self._apply_historical_learning(prompt, overall_complexity)
        overall_complexity = overall_complexity * 0.7 + historical_adjustment * 0.3
        
        # Determine complexity level
        complexity_level = self._determine_complexity_level(overall_complexity)
        
        # Generate predictions and assessments
        execution_prediction = self._predict_execution_requirements(overall_complexity, factor_scores)
        resource_requirements = self._estimate_resource_requirements(overall_complexity, context)
        risk_assessment = self._assess_risks(factor_scores, context)
        learning_insights = self._generate_learning_insights(factor_scores, overall_complexity)
        
        return ComplexityAnalysis(
            overall_complexity=overall_complexity,
            complexity_level=complexity_level,
            factor_scores=factor_scores,
            execution_prediction=execution_prediction,
            resource_requirements=resource_requirements,
            risk_assessment=risk_assessment,
            learning_insights=learning_insights
        )
    
    def _analyze_lexical_complexity(self, prompt: str, context: Dict) -> ComplexityScore:
        """Analyze lexical complexity - vocabulary, technical terms, specificity."""
        evidence = []
        score = 0.0
        
        # Word count influence
        word_count = len(prompt.split())
        if word_count > 50:
            score += 0.3
            evidence.append(f"Long prompt: {word_count} words")
        elif word_count > 20:
            score += 0.15
        
        # Technical terminology density
        technical_terms = [
            'algorithm', 'architecture', 'refactor', 'optimize', 'implement', 
            'integrate', 'deploy', 'configure', 'migrate', 'transform',
            'framework', 'pattern', 'paradigm', 'methodology', 'infrastructure'
        ]
        
        tech_matches = sum(1 for term in technical_terms if term in prompt.lower())
        tech_density = tech_matches / max(word_count, 1)
        
        if tech_density > 0.1:
            score += 0.4
            evidence.append(f"High technical density: {tech_matches} terms")
        elif tech_density > 0.05:
            score += 0.2
            evidence.append(f"Moderate technical terms: {tech_matches}")
        
        # Domain-specific jargon
        domain_patterns = {
            'mobile': ['ios', 'android', 'opencat', 'mobile', 'app'],
            'ai_ml': ['model', 'training', 'inference', 'llm', 'neural'],
            'backend': ['api', 'endpoint', 'database', 'server', 'microservice'],
            'frontend': ['ui', 'ux', 'component', 'react', 'vue'],
            'devops': ['docker', 'kubernetes', 'ci/cd', 'deployment', 'pipeline']
        }
        
        domain_matches = 0
        for domain, terms in domain_patterns.items():
            matches = sum(1 for term in terms if term in prompt.lower())
            if matches >= 2:
                domain_matches += 1
                evidence.append(f"Domain expertise required: {domain}")
        
        if domain_matches >= 2:
            score += 0.3
        elif domain_matches >= 1:
            score += 0.15
        
        # Abstract vs concrete language
        abstract_indicators = ['enhance', 'improve', 'optimize', 'streamline', 'leverage']
        concrete_indicators = ['create', 'delete', 'copy', 'move', 'install']
        
        abstract_count = sum(1 for term in abstract_indicators if term in prompt.lower())
        concrete_count = sum(1 for term in concrete_indicators if term in prompt.lower())
        
        if abstract_count > concrete_count and abstract_count >= 2:
            score += 0.2
            evidence.append("Abstract/conceptual language detected")
        
        reasoning = f"Lexical analysis: {len(evidence)} complexity indicators found"
        
        return ComplexityScore(
            factor=ComplexityFactor.LEXICAL,
            score=min(score, 1.0),
            confidence=0.8,
            reasoning=reasoning,
            evidence=evidence
        )
    
    def _analyze_syntactic_complexity(self, prompt: str, context: Dict) -> ComplexityScore:
        """Analyze syntactic complexity - structure, commands, code patterns."""
        evidence = []
        score = 0.0
        
        # Command complexity
        command_patterns = [
            r'\bfor\s+\w+\s+in\b',  # loops
            r'\bif\s+.*\bthen\b',   # conditionals
            r'\bwhile\s+.*\bdo\b',  # while loops
            r'\|\s*\w+',            # pipes
            r'&&|\|\|',             # logical operators
            r'\$\(\w+\)',           # command substitution
        ]
        
        for pattern in command_patterns:
            if re.search(pattern, prompt):
                score += 0.15
                evidence.append(f"Complex syntax pattern: {pattern}")
        
        # Multi-step instructions
        step_indicators = ['then', 'next', 'after', 'subsequently', 'finally', 'and then']
        step_count = sum(1 for indicator in step_indicators if indicator in prompt.lower())
        
        if step_count >= 3:
            score += 0.3
            evidence.append(f"Multi-step process: {step_count} steps")
        elif step_count >= 2:
            score += 0.2
        
        # Code structure complexity
        code_indicators = [
            r'class\s+\w+', r'def\s+\w+', r'function\s+\w+',  # definitions
            r'import\s+\w+', r'from\s+\w+', r'include\s+',    # imports
            r'\{.*\}', r'\[.*\]',                             # data structures
        ]
        
        code_matches = sum(1 for pattern in code_indicators if re.search(pattern, prompt))
        if code_matches >= 3:
            score += 0.25
            evidence.append(f"Complex code structure: {code_matches} patterns")
        
        # Nested operations
        nesting_patterns = ['within', 'inside', 'nested', 'embedded', 'contained in']
        nesting_count = sum(1 for pattern in nesting_patterns if pattern in prompt.lower())
        
        if nesting_count >= 2:
            score += 0.2
            evidence.append("Nested operations detected")
        
        reasoning = f"Syntactic analysis: {len(evidence)} structural complexity indicators"
        
        return ComplexityScore(
            factor=ComplexityFactor.SYNTACTIC,
            score=min(score, 1.0),
            confidence=0.85,
            reasoning=reasoning,
            evidence=evidence
        )
    
    def _analyze_semantic_complexity(self, prompt: str, context: Dict) -> ComplexityScore:
        """Analyze semantic complexity - meaning, relationships, context requirements."""
        evidence = []
        score = 0.0
        
        # Relationship complexity
        relationship_words = [
            'integrate', 'connect', 'synchronize', 'coordinate', 'align',
            'interface', 'compatibility', 'interoperability', 'bridge'
        ]
        
        relationship_count = sum(1 for word in relationship_words if word in prompt.lower())
        if relationship_count >= 2:
            score += 0.3
            evidence.append(f"Complex relationships: {relationship_count} indicators")
        
        # Contextual dependencies
        context_indicators = [
            'considering', 'taking into account', 'based on', 'depending on',
            'in the context of', 'given that', 'assuming', 'provided that'
        ]
        
        context_deps = sum(1 for indicator in context_indicators if indicator in prompt.lower())
        if context_deps >= 2:
            score += 0.25
            evidence.append("High contextual dependencies")
        
        # Ambiguity and uncertainty
        uncertainty_words = [
            'might', 'could', 'should', 'possibly', 'potentially', 'likely',
            'approximately', 'roughly', 'somewhat', 'unclear', 'uncertain'
        ]
        
        uncertainty_count = sum(1 for word in uncertainty_words if word in prompt.lower())
        if uncertainty_count >= 3:
            score += 0.2
            evidence.append("High uncertainty/ambiguity")
        
        # Multi-domain knowledge required
        file_count = context.get('file_count', 0)
        if file_count > 10:
            score += 0.3
            evidence.append(f"Multi-file context: {file_count} files")
        elif file_count > 5:
            score += 0.15
        
        # Cross-system implications
        system_terms = ['api', 'database', 'frontend', 'backend', 'mobile', 'web', 'cloud']
        system_mentions = sum(1 for term in system_terms if term in prompt.lower())
        
        if system_mentions >= 3:
            score += 0.25
            evidence.append("Cross-system complexity")
        
        reasoning = f"Semantic analysis: {len(evidence)} meaning complexity indicators"
        
        return ComplexityScore(
            factor=ComplexityFactor.SEMANTIC,
            score=min(score, 1.0),
            confidence=0.75,
            reasoning=reasoning,
            evidence=evidence
        )
    
    def _analyze_procedural_complexity(self, prompt: str, context: Dict) -> ComplexityScore:
        """Analyze procedural complexity - workflow, dependencies, orchestration."""
        evidence = []
        score = 0.0
        
        # Sequential complexity
        sequence_words = ['first', 'second', 'third', 'finally', 'before', 'after', 'during']
        sequence_count = sum(1 for word in sequence_words if word in prompt.lower())
        
        if sequence_count >= 4:
            score += 0.3
            evidence.append(f"Complex sequence: {sequence_count} steps")
        elif sequence_count >= 2:
            score += 0.15
        
        # Dependency management
        dependency_words = [
            'depends on', 'requires', 'prerequisite', 'blocking', 'waiting for',
            'conditional', 'if and only if', 'must be done before'
        ]
        
        dependency_count = sum(1 for phrase in dependency_words if phrase in prompt.lower())
        if dependency_count >= 2:
            score += 0.25
            evidence.append("Complex dependencies")
        
        # Parallel execution
        parallel_indicators = ['simultaneously', 'concurrently', 'in parallel', 'at the same time']
        parallel_count = sum(1 for indicator in parallel_indicators if indicator in prompt.lower())
        
        if parallel_count >= 1:
            score += 0.2
            evidence.append("Parallel execution complexity")
        
        # Error handling and rollback
        error_handling = ['rollback', 'undo', 'revert', 'error handling', 'try-catch', 'exception']
        error_count = sum(1 for term in error_handling if term in prompt.lower())
        
        if error_count >= 2:
            score += 0.2
            evidence.append("Error handling complexity")
        
        # Resource coordination
        resource_words = ['allocate', 'manage', 'coordinate', 'schedule', 'queue', 'throttle']
        resource_count = sum(1 for word in resource_words if word in prompt.lower())
        
        if resource_count >= 2:
            score += 0.15
            evidence.append("Resource management complexity")
        
        reasoning = f"Procedural analysis: {len(evidence)} workflow complexity indicators"
        
        return ComplexityScore(
            factor=ComplexityFactor.PROCEDURAL,
            score=min(score, 1.0),
            confidence=0.8,
            reasoning=reasoning,
            evidence=evidence
        )
    
    def _analyze_cognitive_complexity(self, prompt: str, context: Dict) -> ComplexityScore:
        """Analyze cognitive complexity - mental model requirements, reasoning depth."""
        evidence = []
        score = 0.0
        
        # Abstract reasoning
        reasoning_words = [
            'analyze', 'evaluate', 'synthesize', 'compare', 'contrast',
            'infer', 'deduce', 'conclude', 'hypothesize', 'theorize'
        ]
        
        reasoning_count = sum(1 for word in reasoning_words if word in prompt.lower())
        if reasoning_count >= 3:
            score += 0.3
            evidence.append(f"High reasoning demand: {reasoning_count} indicators")
        elif reasoning_count >= 1:
            score += 0.15
        
        # Creative/innovative aspects
        creative_words = [
            'design', 'architect', 'innovate', 'creative', 'novel', 'unique',
            'brainstorm', 'ideate', 'conceptualize', 'envision'
        ]
        
        creative_count = sum(1 for word in creative_words if word in prompt.lower())
        if creative_count >= 2:
            score += 0.25
            evidence.append("Creative/innovative thinking required")
        
        # Problem-solving depth
        problem_indicators = [
            'solve', 'debug', 'troubleshoot', 'diagnose', 'investigate',
            'root cause', 'systematic', 'methodical'
        ]
        
        problem_count = sum(1 for indicator in problem_indicators if indicator in prompt.lower())
        if problem_count >= 2:
            score += 0.2
            evidence.append("Deep problem-solving required")
        
        # Mental model complexity (multiple perspectives)
        perspective_words = [
            'perspective', 'viewpoint', 'angle', 'approach', 'methodology',
            'paradigm', 'framework', 'model', 'theory'
        ]
        
        perspective_count = sum(1 for word in perspective_words if word in prompt.lower())
        if perspective_count >= 2:
            score += 0.2
            evidence.append("Multiple mental models required")
        
        # Knowledge synthesis
        synthesis_words = ['combine', 'merge', 'integrate', 'unify', 'consolidate', 'synthesize']
        synthesis_count = sum(1 for word in synthesis_words if word in prompt.lower())
        
        if synthesis_count >= 2:
            score += 0.15
            evidence.append("Knowledge synthesis required")
        
        reasoning = f"Cognitive analysis: {len(evidence)} mental complexity indicators"
        
        return ComplexityScore(
            factor=ComplexityFactor.COGNITIVE,
            score=min(score, 1.0),
            confidence=0.7,
            reasoning=reasoning,
            evidence=evidence
        )
    
    def _analyze_temporal_complexity(self, prompt: str, context: Dict) -> ComplexityScore:
        """Analyze temporal complexity - time constraints, urgency, scheduling."""
        evidence = []
        score = 0.0
        
        # Urgency indicators
        urgency_words = [
            'urgent', 'asap', 'immediately', 'quickly', 'fast', 'rush',
            'deadline', 'time-critical', 'emergency', 'priority'
        ]
        
        urgency_count = sum(1 for word in urgency_words if word in prompt.lower())
        if urgency_count >= 2:
            score += 0.3
            evidence.append("High urgency/time pressure")
        elif urgency_count >= 1:
            score += 0.15
        
        # Timing coordination
        timing_words = [
            'schedule', 'coordinate', 'synchronize', 'timing', 'sequence',
            'delay', 'timing', 'when', 'schedule'
        ]
        
        timing_count = sum(1 for word in timing_words if word in prompt.lower())
        if timing_count >= 2:
            score += 0.2
            evidence.append("Timing coordination required")
        
        # Historical/temporal context
        temporal_references = [
            'previous', 'earlier', 'before', 'after', 'history', 'legacy',
            'migration', 'upgrade', 'version', 'backwards compatible'
        ]
        
        temporal_count = sum(1 for ref in temporal_references if ref in prompt.lower())
        if temporal_count >= 3:
            score += 0.15
            evidence.append("Temporal/historical complexity")
        
        reasoning = f"Temporal analysis: {len(evidence)} time complexity indicators"
        
        return ComplexityScore(
            factor=ComplexityFactor.TEMPORAL,
            score=min(score, 1.0),
            confidence=0.6,
            reasoning=reasoning,
            evidence=evidence
        )
    
    def _calculate_weighted_complexity(self, factor_scores: List[ComplexityScore]) -> float:
        """Calculate overall complexity using learned weights."""
        weighted_sum = 0.0
        total_weight = 0.0
        
        weight_map = {
            ComplexityFactor.LEXICAL: self.learning_weights["lexical_weight"],
            ComplexityFactor.SYNTACTIC: self.learning_weights["syntactic_weight"],
            ComplexityFactor.SEMANTIC: self.learning_weights["semantic_weight"],
            ComplexityFactor.PROCEDURAL: self.learning_weights["procedural_weight"],
            ComplexityFactor.COGNITIVE: self.learning_weights["cognitive_weight"],
            ComplexityFactor.TEMPORAL: self.learning_weights["temporal_weight"]
        }
        
        for score in factor_scores:
            weight = weight_map.get(score.factor, 0.1)
            weighted_sum += score.score * weight * score.confidence
            total_weight += weight * score.confidence
        
        return weighted_sum / max(total_weight, 0.1)
    
    def _apply_historical_learning(self, prompt: str, base_complexity: float) -> float:
        """Apply learning from execution history to adjust complexity."""
        if not self.execution_history:
            return base_complexity
        
        # Find similar prompts in history
        similar_executions = []
        for history in self.execution_history:
            similarity = self._calculate_prompt_similarity(prompt, history.prompt)
            if similarity > 0.6:  # 60% similarity threshold
                similar_executions.append((history, similarity))
        
        if not similar_executions:
            return base_complexity
        
        # Weight historical complexity by similarity and recency
        total_weight = 0.0
        weighted_complexity = 0.0
        
        current_time = time.time()
        for history, similarity in similar_executions:
            # Recent history is more relevant
            recency_weight = math.exp(-(current_time - history.timestamp) / (30 * 24 * 3600))  # 30-day decay
            weight = similarity * recency_weight
            
            weighted_complexity += history.actual_complexity * weight
            total_weight += weight
        
        if total_weight > 0:
            historical_complexity = weighted_complexity / total_weight
            return historical_complexity
        
        return base_complexity
    
    def _calculate_prompt_similarity(self, prompt1: str, prompt2: str) -> float:
        """Calculate semantic similarity between prompts."""
        # Simple word-based similarity (could be enhanced with embeddings)
        words1 = set(prompt1.lower().split())
        words2 = set(prompt2.lower().split())
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / max(union, 1) if union > 0 else 0.0
    
    def _determine_complexity_level(self, overall_complexity: float) -> str:
        """Determine complexity level from normalized score."""
        if overall_complexity >= 0.7:
            return "high"
        elif overall_complexity >= 0.4:
            return "medium"
        else:
            return "low"
    
    def _predict_execution_requirements(self, complexity: float, factor_scores: List[ComplexityScore]) -> Dict[str, float]:
        """Predict execution requirements based on complexity analysis."""
        base_time = 5.0  # seconds
        base_tokens = 200
        base_cost = 0.001  # USD
        
        # Complexity multipliers
        time_multiplier = 1 + (complexity * 3)  # 1x to 4x
        token_multiplier = 1 + (complexity * 2)  # 1x to 3x
        cost_multiplier = 1 + (complexity * 1.5)  # 1x to 2.5x
        
        # Factor-specific adjustments
        for score in factor_scores:
            if score.factor == ComplexityFactor.PROCEDURAL and score.score > 0.5:
                time_multiplier *= 1.5  # Procedural complexity takes longer
            elif score.factor == ComplexityFactor.COGNITIVE and score.score > 0.5:
                token_multiplier *= 1.3  # Cognitive tasks need more tokens
        
        return {
            "estimated_time": base_time * time_multiplier,
            "estimated_tokens": int(base_tokens * token_multiplier),
            "estimated_cost": base_cost * cost_multiplier,
            "confidence": 0.7
        }
    
    def _estimate_resource_requirements(self, complexity: float, context: Dict) -> Dict[str, Any]:
        """Estimate resource requirements for execution."""
        return {
            "model_tier": "premium" if complexity > 0.7 else "standard" if complexity > 0.4 else "budget",
            "execution_mode": "interactive" if complexity > 0.8 else "yolo",
            "safety_level": "high" if complexity > 0.6 else "medium",
            "timeout": int(300 * (1 + complexity)),  # 5-10 minutes
            "retry_limit": 3 if complexity > 0.5 else 1,
            "context_preservation": "full" if complexity > 0.6 else "optimized"
        }
    
    def _assess_risks(self, factor_scores: List[ComplexityScore], context: Dict) -> Dict[str, float]:
        """Assess execution risks based on complexity factors."""
        risks = {
            "execution_failure": 0.1,
            "resource_overrun": 0.1,
            "unintended_consequences": 0.1,
            "data_loss": 0.05,
            "performance_degradation": 0.1
        }
        
        # Increase risks based on complexity factors
        for score in factor_scores:
            if score.factor == ComplexityFactor.PROCEDURAL and score.score > 0.6:
                risks["execution_failure"] += 0.2
            elif score.factor == ComplexityFactor.SYNTACTIC and score.score > 0.7:
                risks["unintended_consequences"] += 0.15
            elif score.factor == ComplexityFactor.SEMANTIC and score.score > 0.6:
                risks["resource_overrun"] += 0.1
        
        return risks
    
    def _generate_learning_insights(self, factor_scores: List[ComplexityScore], 
                                  overall_complexity: float) -> List[str]:
        """Generate insights for continuous learning."""
        insights = []
        
        # Identify dominant complexity factors
        top_factors = sorted(factor_scores, key=lambda x: x.score, reverse=True)[:2]
        
        if top_factors:
            insights.append(f"Primary complexity drivers: {top_factors[0].factor.value}")
            
        if overall_complexity > 0.8:
            insights.append("Consider breaking into smaller subtasks")
        elif overall_complexity < 0.2:
            insights.append("Simple task - opportunity for automation")
        
        # Pattern recommendations
        if any(score.factor == ComplexityFactor.PROCEDURAL and score.score > 0.6 
               for score in factor_scores):
            insights.append("Complex workflow detected - consider step-by-step execution")
        
        return insights
    
    def record_execution(self, prompt: str, complexity: float, execution_time: float,
                        tokens_used: int, success: bool, errors: List[str] = None):
        """Record execution results for learning."""
        execution = ExecutionHistory(
            prompt=prompt,
            actual_complexity=complexity,
            execution_time=execution_time,
            tokens_used=tokens_used,
            success_rate=1.0 if success else 0.0,
            error_patterns=errors or [],
            timestamp=time.time()
        )
        
        self.execution_history.append(execution)
        
        # Keep only recent history (last 1000 entries)
        if len(self.execution_history) > 1000:
            self.execution_history = self.execution_history[-1000:]
        
        # Update learning weights based on performance
        self._update_learning_weights(execution)
        
        # Save updated history
        self._save_history()
    
    def _update_learning_weights(self, execution: ExecutionHistory):
        """Update learning weights based on execution performance."""
        # This is a simple implementation - could be much more sophisticated
        if execution.success_rate < 0.5:  # Poor performance
            # Slightly reduce confidence in current weights
            for weight_key in self.learning_weights:
                if "weight" in weight_key:
                    self.learning_weights[weight_key] *= 0.99
        elif execution.success_rate > 0.9:  # Excellent performance
            # Slightly increase confidence in current weights
            for weight_key in self.learning_weights:
                if "weight" in weight_key:
                    self.learning_weights[weight_key] *= 1.01
    
    def get_learning_stats(self) -> Dict:
        """Get learning and performance statistics."""
        if not self.execution_history:
            return {"message": "No execution history available"}
        
        total_executions = len(self.execution_history)
        successful_executions = sum(1 for h in self.execution_history if h.success_rate > 0.5)
        
        avg_complexity = sum(h.actual_complexity for h in self.execution_history) / total_executions
        avg_execution_time = sum(h.execution_time for h in self.execution_history) / total_executions
        
        return {
            "total_executions": total_executions,
            "success_rate": successful_executions / total_executions,
            "avg_complexity": avg_complexity,
            "avg_execution_time": avg_execution_time,
            "learning_weights": self.learning_weights,
            "pattern_cache_size": len(self.pattern_cache)
        }

def quick_analyze_complexity(prompt: str, context: Optional[Dict] = None) -> ComplexityAnalysis:
    """Quick complexity analysis function for CLI integration."""
    analyzer = AdvancedComplexityAnalyzer()
    return analyzer.analyze_complexity(prompt, context)

if __name__ == "__main__":
    # Test advanced complexity analyzer
    analyzer = AdvancedComplexityAnalyzer()
    
    test_prompts = [
        "create a simple hello.py file",
        "refactor the entire codebase architecture using advanced design patterns and comprehensive optimization",
        "integrate the mobile API with OpenCat while maintaining backwards compatibility and implementing proper error handling",
        "analyze and explain the complex relationships between microservices in our distributed system"
    ]
    
    print("=== Advanced Complexity Analyzer Testing ===")
    
    for prompt in test_prompts:
        print(f"\n--- Analyzing: {prompt[:50]}... ---")
        
        analysis = analyzer.analyze_complexity(prompt)
        
        print(f"Overall Complexity: {analysis.overall_complexity:.3f} ({analysis.complexity_level})")
        print(f"Factor Scores:")
        for factor_score in analysis.factor_scores:
            print(f"  {factor_score.factor.value}: {factor_score.score:.3f} - {factor_score.reasoning}")
        
        print(f"Execution Prediction:")
        for key, value in analysis.execution_prediction.items():
            print(f"  {key}: {value}")
        
        print(f"Learning Insights: {', '.join(analysis.learning_insights)}")
    
    print(f"\n--- Learning Stats ---")
    stats = analyzer.get_learning_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")