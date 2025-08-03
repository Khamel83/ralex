import json, yaml, time
from litellm import completion
import os

# Ensure the script can find config.yaml
script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "config.yaml")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

api_key = config["openrouter_api_key"]
# Set the API key as an environment variable for litellm
os.environ["OPENROUTER_API_KEY"] = api_key

def run_prompt(model, prompt):
    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            api_base="https://openrouter.ai/api/v1"
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error with {model}: {e}")
        return None

def evaluate(prompt, response, evaluator):
    try:
        eval_prompt = f"Score the following answer from 1 to 10:\nQuestion: {prompt}\nAnswer: {response}"
        eval_response = completion(
            model=evaluator,
            messages=[{"role": "user", "content": eval_prompt}],
            api_base="https://openrouter.ai/api/v1"
        )
        return extract_score(eval_response["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"Eval failed: {e}")
        return 0

def extract_score(text):
    for token in text.split():
        try:
            val = float(token)
            if 0 <= val <= 10:
                return val
        except:
            continue
    return 0

def main():
    results = {m: [] for m in config["models"]}
    for prompt in config["prompts"]:
        for model in config["models"]:
            print(f"Running: {model} → {prompt[:30]}...")
            response = run_prompt(model, prompt)
            if response:
                score = evaluate(prompt, response, config["evaluator_model"])
                results[model].append(score)
            time.sleep(2)  # prevent rate limits

    avg_scores = {
        model: sum(scores) / len(scores) if scores else 0
        for model, scores in results.items()
    }

    output_path = os.path.join(script_dir, "weekly_top_models.json")
    with open(output_path, "w") as f:
        json.dump(
            {"top_models": [m for m, _ in top_models], "raw_scores": avg_scores},
            f, indent=2
        )

    print("\nTop 5 models this week:")
    for i, (model, score) in enumerate(top_models, 1):
        print(f"{i}. {model} → {score:.2f}")

if __name__ == "__main__":
    main()
