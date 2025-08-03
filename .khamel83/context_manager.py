#!/usr/bin/env python3
"""
Agent-OS Context Manager
Optimizes context for cost efficiency through smart compaction and enrichment.
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

class ContextStrategy(Enum):
    COMPRESS = "compress"
    SUMMARIZE = "summarize"
    TRUNCATE = "truncate"
    ENRICH = "enrich"
    PRESERVE = "preserve"

@dataclass
class ContextMetrics:
    token_count: int
    char_count: int
    line_count: int
    relevance_score: float
    compaction_ratio: float
    estimated_cost: float

@dataclass
class ContextOptimization:
    original_size: int
    optimized_size: int
    strategy_used: ContextStrategy
    tokens_saved: int
    cost_savings: float
    relevance_preserved: float

class AgentOSContextManager:
    """
    Core context optimization for Agent-OS cost efficiency.
    
    Key Principles:
    1. Monitor context size for cost optimization
    2. Compact when approaching limits or for simple tasks
    3. Enrich when context is sparse and task is complex
    4. Preserve critical context (mobile workflows, recent changes)
    5. Learn patterns for optimal context per task type
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or Path(__file__).parent / "context-config.json"
        self.config = self._load_config()
        self.context_history = []
        self.optimization_stats = []
        
    def _load_config(self) -> Dict:
        """Load context optimization configuration."""
        default_config = {
            "token_limits": {
                "simple": 1000,      # Simple tasks need minimal context
                "complex": 8000,     # Complex tasks can use more context
                "mobile": 2000,      # Mobile tasks need moderate context
                "batch": 4000,       # Batch tasks need structured context
                "analysis": 6000     # Analysis needs comprehensive context
            },
            "cost_per_token": {
                "input": 0.000001,   # $1/1M tokens input
                "output": 0.000002   # $2/1M tokens output
            },
            "compaction_strategies": {
                "aggressive": 0.3,   # Compress to 30% of original
                "moderate": 0.6,     # Compress to 60% of original
                "conservative": 0.8  # Compress to 80% of original
            },
            "preservation_patterns": [
                r"mobile|opencat|ios",
                r"api|endpoint|integration",
                r"error|bug|fix",
                r"TODO|FIXME|NOTE"
            ]
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    loaded = json.load(f)
                    return {**default_config, **loaded}
            except:
                pass
                
        return default_config
    
    def analyze_context(self, context: str, metadata: Optional[Dict] = None) -> ContextMetrics:
        """Analyze context to determine optimization needs."""
        metadata = metadata or {}
        
        # Basic measurements
        char_count = len(context)
        line_count = len(context.split('\n'))
        
        # Estimate token count (rough approximation: ~4 chars per token)
        token_count = max(1, char_count // 4)
        
        # Calculate relevance score based on content patterns
        relevance_score = self._calculate_relevance(context, metadata)
        
        # Estimate cost
        estimated_cost = token_count * self.config["cost_per_token"]["input"]
        
        # Determine if compaction is beneficial
        task_type = metadata.get("task_type", "simple")
        token_limit = self.config["token_limits"].get(task_type, 1000)
        compaction_ratio = min(1.0, token_limit / token_count) if token_count > 0 else 1.0
        
        return ContextMetrics(
            token_count=token_count,
            char_count=char_count,
            line_count=line_count,
            relevance_score=relevance_score,
            compaction_ratio=compaction_ratio,
            estimated_cost=estimated_cost
        )
    
    def optimize_context(self, context: str, task_type: str = "simple", 
                        metadata: Optional[Dict] = None) -> Tuple[str, ContextOptimization]:
        """
        Main optimization function implementing Agent-OS cost efficiency.
        
        Returns:
            Tuple of (optimized_context, optimization_metrics)
        """
        metadata = metadata or {}
        original_metrics = self.analyze_context(context, {**metadata, "task_type": task_type})
        
        # Determine optimization strategy
        strategy = self._select_strategy(original_metrics, task_type, metadata)
        
        # Apply optimization
        if strategy == ContextStrategy.COMPRESS:
            optimized_context = self._compress_context(context, metadata)
        elif strategy == ContextStrategy.SUMMARIZE:
            optimized_context = self._summarize_context(context, metadata)
        elif strategy == ContextStrategy.TRUNCATE:
            optimized_context = self._truncate_context(context, metadata)
        elif strategy == ContextStrategy.ENRICH:
            optimized_context = self._enrich_context(context, metadata)
        else:  # PRESERVE
            optimized_context = context
            
        # Calculate optimization results
        optimized_metrics = self.analyze_context(optimized_context, {**metadata, "task_type": task_type})
        
        optimization = ContextOptimization(
            original_size=original_metrics.token_count,
            optimized_size=optimized_metrics.token_count,
            strategy_used=strategy,
            tokens_saved=original_metrics.token_count - optimized_metrics.token_count,
            cost_savings=original_metrics.estimated_cost - optimized_metrics.estimated_cost,
            relevance_preserved=optimized_metrics.relevance_score / max(original_metrics.relevance_score, 0.1)
        )
        
        # Track optimization for learning
        self.optimization_stats.append(optimization)
        
        return optimized_context, optimization
    
    def _calculate_relevance(self, context: str, metadata: Dict) -> float:
        """Calculate relevance score for context preservation."""
        relevance = 0.5  # Base relevance
        
        # Boost relevance for preservation patterns
        for pattern in self.config["preservation_patterns"]:
            if re.search(pattern, context, re.IGNORECASE):
                relevance += 0.2
        
        # Task-specific relevance
        task_type = metadata.get("task_type", "simple")
        if task_type == "mobile" and re.search(r"mobile|opencat|ios|api", context, re.IGNORECASE):
            relevance += 0.3
        elif task_type == "complex" and re.search(r"architecture|design|pattern", context, re.IGNORECASE):
            relevance += 0.3
        elif task_type == "analysis" and re.search(r"explain|analyze|documentation", context, re.IGNORECASE):
            relevance += 0.3
            
        # Recent context is more relevant
        if metadata.get("recency", 0) > 0.8:
            relevance += 0.2
            
        return min(1.0, relevance)
    
    def _select_strategy(self, metrics: ContextMetrics, task_type: str, metadata: Dict) -> ContextStrategy:
        """Select optimal context strategy based on Agent-OS principles."""
        token_limit = self.config["token_limits"][task_type]
        
        # If context is within limits and relevant, preserve it
        if metrics.token_count <= token_limit and metrics.relevance_score > 0.7:
            return ContextStrategy.PRESERVE
        
        # If context is much larger than limit, aggressive optimization needed
        if metrics.token_count > token_limit * 2:
            if task_type in ["simple", "mobile"]:
                return ContextStrategy.TRUNCATE  # Fast and cheap
            else:
                return ContextStrategy.COMPRESS  # More sophisticated
        
        # If context is moderately oversized, summarize
        if metrics.token_count > token_limit:
            return ContextStrategy.SUMMARIZE
        
        # If context is too small for complex tasks, enrich
        if task_type in ["complex", "analysis"] and metrics.token_count < token_limit * 0.3:
            return ContextStrategy.ENRICH
            
        return ContextStrategy.PRESERVE
    
    def _compress_context(self, context: str, metadata: Dict) -> str:
        """Compress context while preserving essential information."""
        lines = context.split('\n')
        
        # Preserve critical lines (errors, TODOs, recent changes)
        critical_lines = []
        regular_lines = []
        
        for line in lines:
            is_critical = any(
                re.search(pattern, line, re.IGNORECASE) 
                for pattern in self.config["preservation_patterns"]
            )
            
            if is_critical or len(line.strip()) < 10:  # Keep short lines
                critical_lines.append(line)
            else:
                regular_lines.append(line)
        
        # Compress regular lines by removing redundancy
        compressed_regular = []
        seen_concepts = set()
        
        for line in regular_lines:
            # Extract key concepts (words > 4 chars)
            concepts = set(word.lower() for word in re.findall(r'\b\w{4,}\b', line))
            
            # Keep line if it introduces new concepts
            new_concepts = concepts - seen_concepts
            if new_concepts or len(compressed_regular) < 5:  # Always keep some context
                compressed_regular.append(line)
                seen_concepts.update(concepts)
        
        # Combine critical and compressed content
        result_lines = critical_lines + compressed_regular[:20]  # Limit total lines
        return '\n'.join(result_lines)
    
    def _summarize_context(self, context: str, metadata: Dict) -> str:
        """Create intelligent summary of context."""
        # Simple rule-based summarization for now
        # In production, this could use a small summarization model
        
        lines = context.split('\n')
        summary_lines = []
        
        # Extract file names, function names, key operations
        summary_lines.append("=== CONTEXT SUMMARY ===")
        
        file_mentions = re.findall(r'\b\w+\.\w{2,4}\b', context)
        if file_mentions:
            summary_lines.append(f"Files: {', '.join(set(file_mentions[:5]))}")
        
        function_mentions = re.findall(r'def\s+(\w+)|function\s+(\w+)|class\s+(\w+)', context)
        if function_mentions:
            functions = [f for group in function_mentions for f in group if f]
            summary_lines.append(f"Functions/Classes: {', '.join(set(functions[:5]))}")
        
        # Key operations and errors
        key_lines = [line.strip() for line in lines 
                    if any(keyword in line.lower() 
                          for keyword in ['error', 'todo', 'fixme', 'import', 'def ', 'class '])]
        
        summary_lines.extend(key_lines[:10])
        summary_lines.append("=== END SUMMARY ===")
        
        return '\n'.join(summary_lines)
    
    def _truncate_context(self, context: str, metadata: Dict) -> str:
        """Aggressively truncate context for simple tasks."""
        lines = context.split('\n')
        
        # Keep only the most recent and relevant lines
        preserved_lines = []
        
        for line in lines[-50:]:  # Last 50 lines
            # Always preserve critical patterns
            if any(re.search(pattern, line, re.IGNORECASE) 
                  for pattern in self.config["preservation_patterns"]):
                preserved_lines.append(line)
            # Keep lines with actual content
            elif len(line.strip()) > 10:
                preserved_lines.append(line)
                
        return '\n'.join(preserved_lines[-20:])  # Max 20 lines
    
    def _enrich_context(self, context: str, metadata: Dict) -> str:
        """Add relevant context when beneficial for complex tasks."""
        # For now, add helpful context markers
        enriched = f"""=== ENRICHED CONTEXT ===
Task Type: {metadata.get('task_type', 'unknown')}
Project: Ralex (OpenCode.ai Intelligent Wrapper)
Architecture: Agent-OS Cost Optimization Framework

Original Context:
{context}

=== ADDITIONAL CONTEXT ===
- Ralex transforms to OpenCode.ai wrapper with Agent-OS optimization
- Mobile workflow (OpenCat iOS) must be preserved
- Cost optimization through intelligent task routing
- LiteLLM handles model selection, Ralex handles execution strategy
"""
        return enriched
    
    def get_optimization_stats(self) -> Dict:
        """Get statistics on context optimization performance."""
        if not self.optimization_stats:
            return {"message": "No optimizations performed yet"}
        
        total_tokens_saved = sum(opt.tokens_saved for opt in self.optimization_stats)
        total_cost_savings = sum(opt.cost_savings for opt in self.optimization_stats)
        avg_relevance_preserved = sum(opt.relevance_preserved for opt in self.optimization_stats) / len(self.optimization_stats)
        
        strategy_counts = {}
        for opt in self.optimization_stats:
            strategy = opt.strategy_used.value
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        return {
            "total_optimizations": len(self.optimization_stats),
            "total_tokens_saved": total_tokens_saved,
            "total_cost_savings": total_cost_savings,
            "avg_relevance_preserved": avg_relevance_preserved,
            "strategy_usage": strategy_counts,
            "estimated_savings_percent": (total_tokens_saved / max(sum(opt.original_size for opt in self.optimization_stats), 1)) * 100
        }

def optimize_for_task(context: str, task_type: str, metadata: Optional[Dict] = None) -> Tuple[str, Dict]:
    """Quick context optimization function for integration."""
    manager = AgentOSContextManager()
    optimized_context, optimization = manager.optimize_context(context, task_type, metadata)
    
    return optimized_context, {
        "original_tokens": optimization.original_size,
        "optimized_tokens": optimization.optimized_size,
        "strategy": optimization.strategy_used.value,
        "tokens_saved": optimization.tokens_saved,
        "cost_savings": optimization.cost_savings,
        "relevance_preserved": optimization.relevance_preserved
    }

if __name__ == "__main__":
    # Test context optimization
    test_context = """
    # Example context with various elements
    import os
    import sys
    from pathlib import Path
    
    # TODO: Fix the mobile API integration
    def process_opencat_request(data):
        # Handle OpenCat iOS integration
        return {"status": "success"}
    
    class RalexAPI:
        def __init__(self):
            self.mobile_endpoints = []
            
        def handle_request(self, request):
            # FIXME: Error handling needed here
            if request.type == "mobile":
                return self.mobile_workflow(request)
            else:
                return self.standard_workflow(request)
    
    # This is a long file with lots of content that might need compression
    # when we're dealing with simple tasks that don't need all this context
    # Adding more content to trigger optimization strategies
    
    def another_function():
        pass
        
    def yet_another_function():
        pass
        
    # More code content here
    for i in range(100):
        print(f"Processing item {i}")
        
    # Even more content to make this large
    """ * 10  # Repeat to make it much longer
    
    manager = AgentOSContextManager()
    
    for task_type in ["simple", "complex", "mobile", "analysis"]:
        print(f"\n=== Testing {task_type.upper()} task optimization ===")
        optimized, stats = manager.optimize_context(test_context, task_type)
        print(f"Original: {stats.original_size} tokens")
        print(f"Optimized: {stats.optimized_size} tokens")
        print(f"Strategy: {stats.strategy_used.value}")
        print(f"Tokens saved: {stats.tokens_saved}")
        print(f"Cost savings: ${stats.cost_savings:.6f}")
        print(f"Relevance preserved: {stats.relevance_preserved:.2f}")