import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ralex_core.free_mode_manager import FreeModeManager
from ralex_core.free_model_selector import FreeModelSelector, NoAvailableFreeModelsError

async def test_model_selection():
    manager = FreeModeManager()
    # Ensure models are updated or loaded from cache
    if not manager.load_cached_config():
        await manager.update_free_models()

    selector = FreeModelSelector(manager)

    print("\n--- Testing Model Selection ---")

    # Test 1: Simple task, base tier
    try:
        model = await selector.select_model(task_complexity='simple', context_size=1000)
        print(f"Simple task (base tier): Selected {model['id']}")
        assert model is not None
    except NoAvailableFreeModelsError as e:
        print(f"Simple task (base tier): {e}")

    # Test 2: Complex task, good tier
    try:
        model = await selector.select_model(task_complexity='complex', context_size=5000)
        print(f"Complex task (good tier): Selected {model['id']}")
        assert model is not None
    except NoAvailableFreeModelsError as e:
        print(f"Complex task (good tier): {e}")

    # Test 3: Mark primary base model as throttled and re-select
    if manager.tiers['base']['primary']:
        primary_base_id = manager.tiers['base']['primary']['id']
        selector.mark_throttled(primary_base_id, duration=1) # Throttle for 1 second
        print(f"Marked {primary_base_id} as throttled.")
        await asyncio.sleep(0.1) # Give event loop a chance to process
        try:
            model = await selector.select_model(task_complexity='simple', context_size=1000)
            print(f"Simple task (base tier, after throttling primary): Selected {model['id']}")
            assert model['id'] != primary_base_id
        except NoAvailableFreeModelsError as e:
            print(f"Simple task (base tier, after throttling primary): {e}")

    # Test 4: Attempt to select with very large context (should fail if no model fits)
    try:
        model = await selector.select_model(task_complexity='complex', context_size=999999)
        print(f"Very large context: Selected {model['id']}")
    except NoAvailableFreeModelsError as e:
        print(f"Very large context: {e}")
        assert "unavailable" in str(e)

    print("\n--- Model Selection Tests Complete ---")

if __name__ == "__main__":
    asyncio.run(test_model_selection())
