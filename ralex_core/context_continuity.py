import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ContextContinuitySystem:
    def __init__(self):
        pass

    def merge_context(self, existing_context: Dict, new_context: Dict) -> Dict:
        """Merges new context into existing context, handling conflicts intelligently."""
        merged_context = existing_context.copy()
        for key, new_value in new_context.items():
            if key in merged_context:
                # Simple conflict resolution: new context overrides old
                # More complex logic could involve merging lists, dicts, etc.
                logger.info(f"Conflict detected for key '{key}'. Overwriting with new value.")
                merged_context[key] = new_value
            else:
                merged_context[key] = new_value
        logger.info("Context merged successfully.")
        return merged_context

    def compress_context(self, context: Dict, max_size: int = 1024) -> Dict:
        """Compresses context to fit within a maximum size, prioritizing relevance."""
        # This is a placeholder for actual compression logic.
        # Real compression would involve summarization, entity extraction, or vector embeddings.
        compressed_context = {}
        current_size = 0

        # Prioritize certain keys (e.g., 'active_files', 'recent_commands')
        priority_keys = ["active_files", "recent_commands", "current_project"]
        for key in priority_keys:
            if key in context:
                item_size = len(str(context[key])) # Rough size estimate
                if current_size + item_size <= max_size:
                    compressed_context[key] = context[key]
                    current_size += item_size
                else:
                    logger.warning(f"Could not add priority key '{key}' due to size limit.")

        # Add other keys until max_size is reached
        for key, value in context.items():
            if key not in compressed_context:
                item_size = len(str(value)) # Rough size estimate
                if current_size + item_size <= max_size:
                    compressed_context[key] = value
                    current_size += item_size
                else:
                    logger.warning(f"Context compression: Skipping key '{key}' due to size limit.")
                    break # Stop if max_size is reached
        
        logger.info(f"Context compressed to approximately {current_size} characters (max {max_size}).")
        return compressed_context

    def score_context_relevance(self, context: Dict, current_task: str) -> Dict:
        """Scores the relevance of context elements to the current task."""
        # This is a conceptual placeholder. Real relevance scoring would use NLP techniques.
        scored_context = {}
        for key, value in context.items():
            relevance_score = 0
            if current_task.lower() in str(value).lower():
                relevance_score = 1.0 # Highly relevant
            elif any(word in str(value).lower() for word in current_task.lower().split()):
                relevance_score = 0.5 # Partially relevant
            else:
                relevance_score = 0.1 # Low relevance
            scored_context[key] = {"value": value, "relevance_score": relevance_score}
        logger.info("Context relevance scored.")
        return scored_context

# Example Usage (for testing/demonstration)
if __name__ == "__main__":
    system = ContextContinuitySystem()

    # Test 1: Merge context
    existing = {"user": "Alice", "project": "Ralex", "files": ["a.py"]}
    new = {"project": "Ralex-Mobile", "files": ["b.py"], "device": "iPhone"}
    merged = system.merge_context(existing, new)
    print(f"\n--- Merged Context ---")
    print(merged)

    # Test 2: Compress context
    large_context = {
        "user": "Bob",
        "project": "LargeProject",
        "active_files": [f"file_{i}.py" for i in range(50)],
        "recent_commands": [f"command_{i}" for i in range(20)],
        "notes": """This is a very long note about the project history and various considerations that need to be kept in mind. It contains a lot of details that might not be immediately relevant but are important for full context. We need to ensure that this part of the context is handled gracefully during compression, either by summarizing it or by truncating it if necessary to meet the size constraints. The goal is to retain as much useful information as possible while staying within the limits."""
    }
    compressed = system.compress_context(large_context, max_size=200)
    print(f"\n--- Compressed Context (max 200) ---")
    print(compressed)

    # Test 3: Score context relevance
    task = "fix bug in file_10.py"
    scored = system.score_context_relevance(large_context, task)
    print(f"\n--- Scored Context Relevance for '{task}' ---")
    for key, data in scored.items():
        print(f"  {key}: {data['relevance_score']:.2f} - {data['value'][:50]}...")
