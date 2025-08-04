import json, yaml, os
from litellm import completion

# Ensure the script can find config.yaml
script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "config.yaml")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

api_key = config["openrouter_api_key"]
os.environ["OPENROUTER_API_KEY"] = api_key

def test_single_model_call():
    model_to_test = config["models"][0] # Take the first model from config.yaml
    prompt = "Hello, how are you?"

    print(f"\n--- Testing single model call: {model_to_test} ---")
    try:
        response = completion(
            model=model_to_test,
            messages=[{"role": "user", "content": prompt}],
            api_base="https://openrouter.ai/api/v1"
        )
        print("Response received successfully!")
        print(f"Model: {response.model}")
        print(f"Content: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Error during test call: {e}")

if __name__ == "__main__":
    test_single_model_call()
