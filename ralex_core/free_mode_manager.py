import asyncio
import json
import os
import httpx
import yaml
from datetime import datetime, timedelta

class FreeModeManager:
    def __init__(self):
        self.tiers = {
            'base': {'primary': None, 'backups': []},
            'good': {'primary': None, 'backups': []}
        }
        self.last_update = None
        self.cache_file = os.path.join(os.path.dirname(__file__), 'free_mode_cache.json')
        self.config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'free_mode.yaml')
        self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
                if config and 'update_interval' in config:
                    self.update_interval = timedelta(seconds=config['update_interval'])
                else:
                    self.update_interval = timedelta(weeks=1) # Default to 1 week
        else:
            self.update_interval = timedelta(weeks=1) # Default to 1 week

    async def update_free_models(self):
        """Weekly update of free model tiers"""
        if self.last_update and (datetime.now() - self.last_update) < self.update_interval:
            print("Free models already updated recently. Skipping.")
            return

        print("Updating free model tiers from OpenRouter...")
        models = await self.fetch_openrouter_models()
        free_models = self.filter_free_models(models)

        print(f"Found {len(free_models)} free models")

        # Rank by performance and context window (placeholder for actual ranking logic)
        ranked = self.rank_models_by_capability(free_models)

        # Assign to tiers
        self.tiers['base'] = self.select_base_tier(ranked)  # Fast + efficient
        self.tiers['good'] = self.select_good_tier(ranked)  # Best quality

        self.last_update = datetime.now()
        self.cache_model_config()
        print("Free mode updated successfully")

    async def fetch_openrouter_models(self):
        """Fetches all models from OpenRouter API."""
        url = "https://openrouter.ai/api/v1/models"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json().get('data', [])

    def filter_free_models(self, models):
        """Filters out models that are truly free (price is 0)."""
        free_models = []
        for model in models:
            pricing = model.get('pricing', {})
            try:
                prompt_cost = float(pricing.get('prompt', 1.0))
                completion_cost = float(pricing.get('completion', 1.0))
                if prompt_cost == 0.0 and completion_cost == 0.0:
                    free_models.append(model)
            except ValueError:
                # Handle cases where pricing might not be a valid number
                continue
        return free_models

    def rank_models_by_capability(self, models):
        """
        Ranks models based on a combination of factors, prioritizing available and relevant metrics:
        1. Explicit coding/instruction capabilities (keywords in ID)
        2. Context length
        3. Model ID alphabetically (as a tie-breaker)
        """
        def get_ranking_key(model):
            model_id = model.get('id', '').lower()
            context_length = model.get('context_length', 0)

            # Prioritize models with 'coder', 'instruct', 'chat' in their ID
            # Assign higher scores for these keywords
            capability_score = 0
            if 'coder' in model_id:
                capability_score += 3
            if 'instruct' in model_id:
                capability_score += 2
            if 'chat' in model_id:
                capability_score += 1

            # Combine scores for a comprehensive ranking
            # Higher context_length and capability_score are better
            return (capability_score, context_length, model_id)

        # Sort in reverse order for scores (higher is better), and ascending for ID
        return sorted(models, key=get_ranking_key, reverse=True)

    def select_base_tier(self, ranked_models):
        """
        Selects models for the 'base' tier.
        Prioritizes models that are fast, efficient, and highly capable for common coding tasks.
        Aims for models like Qwen3 Coder, Gemini 2.0 Flash.
        """
        candidates = []
        for m in ranked_models:
            model_id = m.get('id', '').lower()
            context_length = m.get('context_length', 0)

            # Criteria for base tier:
            # - Minimum context length of 8192
            # - Explicitly coding or instruction-following models preferred
            if context_length >= 8192 and \
               ('coder' in model_id or 'instruct' in model_id or 'chat' in model_id):
                candidates.append(m)
        
        return {
            'primary': candidates[0] if candidates else None,
            'backups': candidates[1:4]  # Top 3 backups
        }

    def select_good_tier(self, ranked_models):
        """
        Selects models for the 'good' tier.
        Prioritizes models with the highest quality, larger context windows, and advanced reasoning capabilities.
        Aims for models like Gemini 2.5 Pro.
        """
        candidates = []
        for m in ranked_models:
            model_id = m.get('id', '').lower()
            context_length = m.get('context_length', 0)

            # Criteria for good tier:
            # - Minimum context length of 32768 (or higher for complex tasks)
            # - Avoid very small or basic models (e.g., Llama 3B, Gemma)
            if context_length >= 32768 and \
               not ('llama-3.2-3b' in model_id or 'gemma' in model_id):
                candidates.append(m)

        return {
            'primary': candidates[0] if candidates else None,
            'backups': candidates[1:4]  # Top 3 backups
        }

    def cache_model_config(self):
        """Caches the current free model configuration to a JSON file."""
        config_to_cache = {
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'tiers': {
                tier_name: {
                    'primary': {
                        'id': tier_data['primary']['id'],
                        'context_length': tier_data['primary'].get('context_length', 0)
                    } if tier_data['primary'] else None,
                    'backups': [
                        {'id': b['id'], 'context_length': b.get('context_length', 0)}
                        for b in tier_data['backups']
                    ]
                }
                for tier_name, tier_data in self.tiers.items()
            }
        }
        with open(self.cache_file, 'w') as f:
            json.dump(config_to_cache, f, indent=4)

    def load_cached_config(self):
        """Loads the cached free model configuration from a JSON file."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                config = json.load(f)
                self.last_update = datetime.fromisoformat(config['last_update']) if config['last_update'] else None
                for tier_name, tier_data in config['tiers'].items():
                    self.tiers[tier_name]['primary'] = tier_data['primary']
                    self.tiers[tier_name]['backups'] = tier_data['backups']
                print("Loaded cached free mode configuration.")
                return True
        return False

if __name__ == "__main__":
    # Example usage for testing
    async def main():
        manager = FreeModeManager()
        # Try to load from cache first
        if not manager.load_cached_config():
            await manager.update_free_models()
        
        print("\n--- Current Free Model Tiers ---")
        for tier_name, tier_data in manager.tiers.items():
            primary_model = tier_data['primary']['id'] if tier_data['primary'] else "N/A"
            backup_models = ", ".join([b['id'] for b in tier_data['backups']]) if tier_data['backups'] else "N/A"
            print(f"Tier: {tier_name.capitalize()}")
            print(f"  Primary: {primary_model}")
            print(f"  Backups: {backup_models}")
        
        print(f"Last updated: {manager.last_update}")

    asyncio.run(main())
