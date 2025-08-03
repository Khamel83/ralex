import asyncio
from datetime import datetime, timedelta

class NoAvailableFreeModelsError(Exception):
    """Custom exception for when no free models are available."""
    pass

class FreeModelSelector:
    def __init__(self, free_mode_manager):
        self.free_manager = free_mode_manager
        self.current_throttled = set()

    async def select_model(self, task_complexity: str, context_size: int):
        """Select best available free model for task"""

        # Determine tier based on complexity
        if task_complexity in ['simple', 'medium']:
            tier = 'base'  # Fast, efficient models
        else:
            tier = 'good'  # Best quality models

        # Try primary model first
        primary = self.free_manager.tiers[tier]['primary']
        if primary and primary['id'] not in self.current_throttled:
            if context_size <= primary.get('context_length', 0):
                return primary

        # Fall back to backups
        for backup in self.free_manager.tiers[tier]['backups']:
            if backup['id'] not in self.current_throttled:
                if context_size <= backup.get('context_length', 0):
                    return backup

        # Cross-tier fallback if needed
        other_tier = 'good' if tier == 'base' else 'base'
        cross_tier_models = []
        if self.free_manager.tiers[other_tier]['primary']:
            cross_tier_models.append(self.free_manager.tiers[other_tier]['primary'])
        cross_tier_models.extend(self.free_manager.tiers[other_tier]['backups'])

        for model in cross_tier_models:
            if model and model['id'] not in self.current_throttled:
                if context_size <= model.get('context_length', 0):
                    return model

        raise NoAvailableFreeModelsError("All free models throttled or unavailable")

    def mark_throttled(self, model_id: str, duration: int = 3600):
        """Mark model as throttled for specified duration"""
        self.current_throttled.add(model_id)
        # Schedule removal after duration
        asyncio.get_event_loop().call_later(
            duration,
            lambda: self.current_throttled.discard(model_id)
        )
