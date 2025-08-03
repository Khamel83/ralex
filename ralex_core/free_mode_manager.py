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
        self.config_file = os.path.join(os.path.dirname(__file__), '..", "config", 'free_mode.yaml')
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
        Ranks models based on a combination of factors.
        This is a placeholder and should be refined with actual performance metrics.
        For now, it prioritizes context length and then model ID alphabetically.
        """
        # Sort by context length (descending), then by ID (ascending)
        return sorted(models, key=lambda x: (x.get('context_length', 0), x.get('id')), reverse=True)

    def select_base_tier(self, ranked_models):
        """
        Selects models for the 'base' tier.
        Prioritizes speed, context window, and efficiency.
        """
        candidates = []
        for m in ranked_models:
            # Placeholder criteria: minimum context, and common chat/instruct models
            if m.get('context_length', 0) >= 8192 and \
               ('instruct' in m.get('id', '').lower() or 'chat' in m.get('id', '').lower()):
                candidates.append(m)
        
        return {
            'primary': candidates[0] if candidates else None,
            'backups': candidates[1:4]  # Top 3 backups
        }

    def select_good_tier(self, ranked_models):
        """
        Selects models for the 'good' tier.
        Prioritizes quality, context window, and broader capabilities.
        """
        candidates = []
        for m in ranked_models:
            # Placeholder criteria: reasonable context, and not basic models like gemma
            if m.get('context_length', 0) >= 4096 and \
               not m.get('id', '').startswith('google/gemma'):
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
