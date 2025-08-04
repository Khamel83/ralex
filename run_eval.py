import json, yaml, time, os, asyncio, aiohttp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

api_key = os.getenv("OPENROUTER_API_KEY")
api_base = "https://openrouter.ai/api/v1"

async def run_prompt(model, prompt):
    """Run prompt using direct OpenRouter API call"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{api_base}/chat/completions", headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    error_text = await response.text()
                    print(f"Error with {model}: HTTP {response.status} - {error_text}")
                    return None
    except Exception as e:
        print(f"Error with {model}: {e}")
        return None

async def evaluate(prompt, response, evaluator):
    """Evaluate response using direct OpenRouter API call"""
    eval_prompt = f"Score the following answer from 1 to 10:\nQuestion: {prompt}\nAnswer: {response}"
    try:
        eval_response = await run_prompt(evaluator, eval_prompt)
        if eval_response:
            return extract_score(eval_response)
        return 0
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

async def main():
    results = {m: [] for m in config["models"]}
    for prompt in config["prompts"]:
        for model in config["models"]:
            print(f"Running: {model} → {prompt[:30]}...")
            response = await run_prompt(model, prompt)
            if response:
                score = await evaluate(prompt, response, config["evaluator_model"])
                results[model].append(score)
            await asyncio.sleep(2)  # Rate limiting

    avg_scores = {
        model: round(sum(scores) / len(scores), 2) if scores else 0
        for model, scores in results.items()
    }

    top_models = sorted(avg_scores.items(), key=lambda x: -x[1])[:5]
    with open("weekly_top_models.json", "w") as f:
        json.dump(
            {"top_models": [m for m, _ in top_models], "raw_scores": avg_scores},
            f, indent=2
        )

    print("\nTop 5 models this week:")
    for i, (model, score) in enumerate(top_models, 1):
        print(f"{i}. {model} → {score:.2f}")

if __name__ == "__main__":
    asyncio.run(main())