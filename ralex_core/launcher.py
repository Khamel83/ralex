#!/usr/bin/env python

import os
import sys
import re
import json
import difflib
import argparse
from collections import defaultdict
import asyncio

from ralex_core.openrouter_client import OpenRouterClient
from ralex_core.semantic_classifier import SemanticClassifier
from ralex_core.budget import BudgetManager
from ralex_core.code_executor import CodeExecutor
from ralex_core.agentos_integration import AgentOSEnhancer
from agent_os.session_manager import SessionManager


def parse_file_modifications(response_text):
    """Parses the LLM response to find file modification blocks."""
    pattern = r"```([a-zA-Z0-9_\./-]+)\n([\s\S]*?)\n```"
    matches = re.findall(pattern, response_text)
    modifications = {file_path: content for file_path, content in matches}
    return modifications


def parse_code_blocks(response_text):
    """Parses the LLM response to find executable code blocks."""
    pattern = r"```(python|bash|sh)\n([\s\S]*?)\n```"
    matches = re.findall(pattern, response_text)
    code_blocks = []
    for lang, code in matches:
        code_blocks.append({"language": lang, "code": code})
    return code_blocks


def load_config(file_path):
    """Loads a JSON configuration file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {file_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"Error: Invalid JSON in configuration file at {file_path}", file=sys.stderr
        )
        sys.exit(1)


def classify_intent(user_input):
    """Classifies user input into a predefined intent based on keywords."""
    user_input_lower = user_input.lower()
    if (
        "debug" in user_input_lower
        or "fix" in user_input_lower
        or "error" in user_input_lower
    ):
        return "debug"
    elif (
        "generate" in user_input_lower
        or "create" in user_input_lower
        or "build" in user_input_lower
    ):
        return "generate"
    elif (
        "edit" in user_input_lower
        or "modify" in user_input_lower
        or "change" in user_input_lower
    ):
        return "edit"
    elif (
        "review" in user_input_lower
        or "analyze" in user_input_lower
        or "suggest" in user_input_lower
    ):
        return "review"
    elif (
        "optimize" in user_input_lower
        or "performance" in user_input_lower
        or "faster" in user_input_lower
    ):
        return "optimize"
    elif (
        "format" in user_input_lower
        or "style" in user_input_lower
        or "lint" in user_input_lower
    ):
        return "format"
    elif (
        "explain" in user_input_lower
        or "document" in user_input_lower
        or "how to" in user_input_lower
    ):
        return "explain"
    else:
        return "default"


async def run_interactive_mode(
    settings, model_tiers, intent_routes, client, semantic_classifier, budget_optimizer
):
    """Runs the interactive CLI mode."""
    file_context = {}
    conversation_history = []
    code_executor = CodeExecutor()
    agentos = AgentOSEnhancer()
    session_manager = SessionManager(os.path.join(os.path.dirname(__file__), '..', 'session'))
    current_session = None # To store the active session

    # Track breakdown state for multi-step execution
    current_breakdown = None
    current_analysis = ""

    print("Welcome to Ralex with AgentOS Integration!")
    print("Type /add <file_path> to add a file to context, or /exit to quit.")
    print("AgentOS slash commands:", ", ".join(agentos.get_slash_commands().keys()))

    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ["/exit", "/quit"]:
                break

            # --- AgentOS Slash Commands ---
            if user_input.startswith("/"):
                parts = user_input.split(" ", 1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""

                if command == "/start":
                    start_parser = argparse.ArgumentParser(description="Start a new session", exit_on_error=False)
                    start_parser.add_argument("session_id", nargs='?', help="Optional session ID")
                    start_parser.add_argument("--template", help="Optional template name")
                    
                    try:
                        start_args = start_parser.parse_args(args.split())
                        session_id = start_args.session_id
                        template_name = start_args.template

                        current_session = session_manager.create_new_session(session_id=session_id, template_name=template_name)
                        print(f"New session started: {current_session['session_id']}")
                    except SystemExit: # argparse exits on error
                        print("Invalid /start command arguments.")
                    continue
                elif command in agentos.get_slash_commands():
                    result = agentos.handle_slash_command(command, args)
                    print(result)
                    continue
                else:
                    print(f"Unknown command: {command}")
                    print(
                        "Available commands:",
                        ", ".join(agentos.get_slash_commands().keys()),
                    )
                    continue

            # --- File Context Management (Task 2.3.1, 2.3.2, 2.3.3) ---
            if user_input.startswith("/add "):
                file_paths_str = user_input.split(" ", 1)[1].strip()
                for (
                    file_path_str
                ) in file_paths_str.split():  # Split by space to handle multiple files
                    try:
                        with open(file_path_str, "r", encoding="utf-8") as f:
                            file_context[file_path_str] = f.read()
                        print(f"Added '{file_path_str}' to context.")
                    except FileNotFoundError:
                        print(
                            f"Error: File not found at '{file_path_str}'",
                            file=sys.stderr,
                        )
                    except Exception as e:
                        print(f"Error reading file: {e}", file=sys.stderr)
                continue

            # --- AgentOS Smart Prompt Structuring ---
            if not file_context:
                print(
                    "Please add at least one file to the context with /add <file_path>",
                    file=sys.stderr,
                )
                continue

            # Use AgentOS to structure the prompt for cost optimization
            breakdown = agentos.structure_smart_prompt(user_input, file_context)

            print(f"\n🧠 AgentOS Analysis:")
            print(f"   Complexity: {breakdown.complexity}")
            print(f"   Estimated cost: ${breakdown.estimated_cost:.4f}")

            if breakdown.complexity == "low":
                # Simple task - go straight to cheap execution
                print("   Strategy: Direct execution (cheap model)")

                execution_prompt = agentos.create_execution_prompt(
                    breakdown.execution_tasks[0], file_context
                )

                messages = [{"role": "user", "content": execution_prompt}]
                if budget_optimizer.free_mode_enabled:
                    try:
                        selected_model_obj = await budget_optimizer.free_model_selector.select_model(task_complexity='simple', context_size=len(str(messages)))
                        selected_model = selected_model_obj['id']
                        tier = "free_base"
                        intent = "simple"
                    except NoAvailableFreeModelsError:
                        print("\n⚠️ No free models available for simple task. Falling back to paid models.")
                        selected_model = budget_optimizer.get_cheapest_model_in_tier("cheap")
                        tier = "cheap"
                        intent = "simple"
                else:
                    selected_model = budget_optimizer.get_cheapest_model_in_tier("cheap")
                    tier = "cheap"
                    intent = "simple"

            else:
                # Complex task - needs expensive analysis first
                print(
                    "   Strategy: Analysis first (smart model), then execution (cheap models)"
                )

                if current_breakdown is None:
                    # Step 1: Expensive analysis
                    print("   Phase: ANALYSIS (using smart model)")

                    messages = [{"role": "user", "content": breakdown.analysis_prompt}]
                    if budget_optimizer.free_mode_enabled:
                        try:
                            selected_model_obj = await budget_optimizer.free_model_selector.select_model(task_complexity='complex', context_size=len(str(messages)))
                            selected_model = selected_model_obj['id']
                            tier = "free_good"
                            intent = "analysis"
                        except NoAvailableFreeModelsError:
                            print("\n⚠️ No free models available for complex task. Falling back to paid models.")
                            selected_model = budget_optimizer.get_cheapest_model_in_tier(
                                "premium", model_tiers
                            )
                            tier = "premium"
                            intent = "analysis"
                    else:
                        selected_model = budget_optimizer.get_cheapest_model_in_tier(
                            "premium", model_tiers
                        )
                        tier = "premium"
                        intent = "analysis"

                else:
                    # Step 2+: Cheap execution of specific tasks
                    print(
                        f"   Phase: EXECUTION task {len(current_breakdown.execution_tasks) + 1}"
                    )

                    # This will be handled after we get the analysis response
                    pass

            # --- Intent Classification for fallback ---
            semantic_intent, confidence = semantic_classifier.classify(user_input)

            # Dynamic Tier Downgrade based on Confidence (Task 10.2.1 & 10.2.2)
            if confidence < 0.6:  # If semantic confidence is low
                # Try to find a cheaper tier that still matches the intent
                tier_hierarchy = [
                    "diamond",
                    "platinum",
                    "premium",
                    "gold",
                    "standard",
                    "silver",
                    "cheap",
                ]
                if budget_optimizer.free_mode_enabled:
                    tier_hierarchy.insert(0, "free_good")
                    tier_hierarchy.insert(0, "free_base")

                current_tier = intent_routes.get(semantic_intent, "default")
                current_tier_index = (
                    tier_hierarchy.index(current_tier)
                    if current_tier in tier_hierarchy
                    else -1
                )

                for i in range(current_tier_index + 1, len(tier_hierarchy)):
                    lower_tier = tier_hierarchy[i]
                    if lower_tier.startswith("free_") and budget_optimizer.free_mode_enabled:
                        try:
                            # For free tiers, try to select a model from the free_model_selector
                            selected_model_obj = await budget_optimizer.free_model_selector.select_model(
                                task_complexity='simple' if lower_tier == 'free_base' else 'complex',
                                context_size=len(str(messages))
                            )
                            selected_model = selected_model_obj['id']
                            tier = lower_tier
                            intent = semantic_intent
                            print(
                                f"\n💡 Downgrading to {lower_tier} tier ({selected_model}) due to low semantic confidence."
                            )
                            break
                        except NoAvailableFreeModelsError:
                            # If no free model available in this tier, continue to next
                            continue
                    else:
                        cheapest_in_lower_tier = (
                            budget_optimizer.get_cheapest_model_in_tier(
                                lower_tier, model_tiers
                            )
                        )
                        if cheapest_in_lower_tier:
                            # Check if the lower tier model is significantly cheaper and still reasonable
                            # For simplicity, we'll just pick the first cheaper one for now
                            intent = semantic_intent  # Keep the semantic intent
                            tier = lower_tier
                            selected_model = cheapest_in_lower_tier
                            print(
                                f"\n💡 Downgrading to {lower_tier} tier ({selected_model}) due to low semantic confidence."
                            )
                            break
                else:
                    # If no suitable lower tier found, stick with original semantic intent
                    intent = semantic_intent
                    tier = intent_routes.get(intent, "default")
                    if budget_optimizer.free_mode_enabled:
                        try:
                            selected_model_obj = await budget_optimizer.free_model_selector.select_model(
                                task_complexity='medium', # Default complexity for fallback
                                context_size=len(str(messages))
                            )
                            selected_model = selected_model_obj['id']
                            tier = "free_base" # Default to free_base if no other free tier found
                        except NoAvailableFreeModelsError:
                            selected_model = budget_optimizer.get_cheapest_model_in_tier(tier)
                    else:
                        selected_model = budget_optimizer.get_cheapest_model_in_tier(tier)
            else:
                # Use semantic if confident enough
                intent = semantic_intent
                tier = intent_routes.get(intent, "default")
                if budget_optimizer.free_mode_enabled:
                    try:
                        selected_model_obj = await budget_optimizer.free_model_selector.select_model(
                            task_complexity='medium', # Default complexity for confident semantic intent
                            context_size=len(str(messages))
                        )
                        selected_model = selected_model_obj['id']
                        tier = "free_base" # Default to free_base if free mode is on
                    except NoAvailableFreeModelsError:
                        selected_model = budget_optimizer.get_cheapest_model_in_tier(tier)
                else:
                    selected_model = budget_optimizer.get_cheapest_model_in_tier(tier)

            if not selected_model:
                print(
                    f"Error: No model found for tier '{tier}'. Please check your model_tiers.json and intent_routes.json.",
                    file=sys.stderr,
                )
                continue

            # --- Pre-execution Dry Run and Confirmation (Task 2.1.1 & 2.1.2) ---
            print(
                f"\nProposed Action: Intent '{intent}' using model '{selected_model}' (tier: {tier})"
            )

            # --- Budget Check (Task 5.2.3 & 5.2.4) ---
            budget_status = budget_optimizer.check_budget_status()
            if budget_status["status"] == "warning":
                print(
                    "\n⚠️  Budget Warning: You have spent ${:.2f} today out of your ${:.2f} daily limit ({:.2f}% used).".format(
                        budget_status["spent_today"],
                        budget_status["daily_limit"],
                        budget_status["percentage_used"],
                    )
                )
            elif budget_status["status"] == "exceeded":
                print(
                    "\n🚨 Budget Exceeded: You have spent ${:.2f} today out of your ${:.2f} daily limit ({:.2f}% used).".format(
                        budget_status["spent_today"],
                        budget_status["daily_limit"],
                        budget_status["percentage_used"],
                    )
                )
                confirm = input(
                    "You have exceeded your daily budget. Proceed anyway? [y/N] "
                ).lower()
                if confirm != "y":
                    print("Action cancelled due to budget.")
                    continue

            confirm = input("Proceed with this action? [Y/n] ").lower()
            if confirm == "n":
                print("Action cancelled.")
                continue

            print(
                f"\nAssistant (using {selected_model}, intent: {intent}, tier: {tier}):",
                end="",
                flush=True,
            )
            full_response = ""
            for chunk in await client.send_request(selected_model, messages):
                print(chunk, end="", flush=True)
                full_response += chunk
            print("\n")

            # --- AgentOS Breakdown Processing ---
            if breakdown.complexity != "low" and intent == "analysis":
                # We just completed the expensive analysis - extract tasks for cheap execution
                print("\n🔍 AgentOS Processing Analysis...")
                execution_tasks = agentos.parse_task_breakdown(full_response)

                if execution_tasks:
                    print(f"✅ Extracted {len(execution_tasks)} execution tasks:")
                    for i, task in enumerate(execution_tasks, 1):
                        print(f"   {i}. {task[:80]}...")

                    breakdown.execution_tasks = execution_tasks
                    current_breakdown = breakdown
                    current_analysis = full_response

                    print("\n💡 Next: Use cheap models to execute these tasks.")
                    print(
                        "   Type 'execute next' to run the first task, or continue with other requests."
                    )
                else:
                    print(
                        "⚠️  Could not extract clear tasks from analysis. Proceeding with normal execution."
                    )

            # Handle execution task requests
            if (
                user_input.lower() in ["execute next", "next", "continue"]
                and current_breakdown
                and current_breakdown.execution_tasks
            ):
                # Execute the next task with a cheap model
                next_task = current_breakdown.execution_tasks.pop(0)
                print(f"\n🚀 Executing task: {next_task}")

                execution_prompt = agentos.create_execution_prompt(
                    next_task, file_context, current_analysis
                )
                execution_messages = [{"role": "user", "content": execution_prompt}]

                # Override to use cheap model
                if budget_optimizer.free_mode_enabled:
                    try:
                        selected_model_obj = await budget_optimizer.free_model_selector.select_model(task_complexity='simple', context_size=len(str(execution_messages)))
                        selected_model = selected_model_obj['id']
                        tier = "free_base"
                        intent = "execution"
                    except NoAvailableFreeModelsError:
                        print("\n⚠️ No free models available for execution task. Falling back to paid models.")
                        selected_model = budget_optimizer.get_cheapest_model_in_tier("cheap")
                        tier = "cheap"
                        intent = "execution"
                else:
                    selected_model = budget_optimizer.get_cheapest_model_in_tier("cheap")
                    tier = "cheap"
                    intent = "execution"

                print(
                    f"Assistant (executing with {selected_model}):", end="", flush=True
                )
                execution_response = ""
                for chunk in await client.send_request(selected_model, execution_messages):
                    print(chunk, end="", flush=True)
                    execution_response += chunk
                print("\n")

                # Replace full_response for downstream processing
                full_response = execution_response

                if not current_breakdown.execution_tasks:
                    print("✅ All execution tasks completed!")
                    current_breakdown = None
                    current_analysis = ""
                else:
                    print(
                        f"📝 {len(current_breakdown.execution_tasks)} tasks remaining. Type 'next' to continue."
                    )

            # --- Code Execution (Task 6.1.3 & 6.1.4) ---
            code_blocks = parse_code_blocks(full_response)
            if code_blocks:
                print("The assistant proposed the following code to execute:")
                for i, block in enumerate(code_blocks):
                    print(
                        "\n--- Code Block {} ({}) ---".format(i + 1, block["language"])
                    )
                    print(block["code"])
                    print("---------------------------")

                confirm_exec = input("Execute this code? [y/N] ").lower()
                if confirm_exec in ["y", "yes"]:
                    for block in code_blocks:
                        if block["language"] == "python":
                            print(f"\nExecuting Python code...")
                            exec_result = code_executor.execute_python_code(
                                block["code"]
                            )
                            if exec_result["success"]:
                                print("Execution successful.")
                                if exec_result["stdout"]:
                                    print("Stdout:\n" + exec_result["stdout"])
                                if exec_result["stderr"]:
                                    print("Stderr:\n" + exec_result["stderr"])
                            else:
                                print("Execution failed.")
                                if exec_result["stdout"]:
                                    print("Stdout:\n" + exec_result["stdout"])
                                if exec_result["stderr"]:
                                    print("Stderr:\n" + exec_result["stderr"])
                        else:
                            print(
                                "Execution of {} code is not yet supported.".format(
                                    block["language"]
                                )
                            )

            # Update conversation history (Task 3.2.1)
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": full_response})

            # Record usage (Task 5.1.4)
            # For simplicity, estimating tokens based on response length. Real implementation would use tokenizers.
            estimated_tokens_sent = len(str(messages).split())  # Very rough estimate
            estimated_tokens_received = len(
                full_response.split()
            )  # Very rough estimate
            cost_per_token = 0.0  # Placeholder, will get from model_tiers later
            for t in model_tiers["tiers"][tier]:
                if t["name"] == selected_model:
                    cost_per_token = t["cost_per_token"]
                    break
            estimated_cost = (
                estimated_tokens_sent + estimated_tokens_received
            ) * cost_per_token
            budget_optimizer.record_usage(
                selected_model,
                estimated_tokens_sent,
                estimated_tokens_received,
                estimated_cost,
                task_type=intent,
            )

            # --- File Writing with Diff Preview (Task 2.2.1, 2.2.2, 2.5.1, 2.5.2, 2.5.3, 2.5.4) ---
            modifications = parse_file_modifications(full_response)
            if modifications:
                print("The assistant proposed the following changes:")
                for file_path, new_content in modifications.items():
                    original_content = ""
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="utf-8") as f:
                            original_content = f.read()

                    diff = difflib.unified_diff(
                        original_content.splitlines(keepends=True),
                        new_content.splitlines(keepends=True),
                        fromfile=file_path + " (original)",
                        tofile=file_path + " (proposed)",
                    )
                    print(f"\n--- Diff for {file_path} ---")
                    for line in diff:
                        if line.startswith("+"):
                            print(f"\033[92m{line}\033[0m", end="")  # Green
                        elif line.startswith("-"):
                            print(f"\033[91m{line}\033[0m", end="")  # Red
                        elif line.startswith("@"):
                            print(f"\033[94m{line}\033[0m", end="")  # Blue
                        else:
                            print(line, end="")
                    print("---------------------------")

                confirm = input("Apply these changes? [y/N] ").lower()
                if confirm in ["y", "yes"]:
                    for file_path, content in modifications.items():
                        try:
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(content)
                            print(f"Applied changes to {file_path}")
                        except Exception as e:
                            print(
                                f"Error writing to file {file_path}: {e}",
                                file=sys.stderr,
                            )
                    # Update the in-memory context as well
                    file_context.update(modifications)

        except KeyboardInterrupt:
            print("\nExiting Ralex...")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


async def main():
    """The main entry point for the Ralex agent."""
    parser = argparse.ArgumentParser(description="Ralex - Your AI Coding Assistant")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command (interactive mode)
    run_parser = subparsers.add_parser("run", help="Run Ralex in interactive mode")
    run_parser.add_argument(
        "--free-mode", action="store_true", help="Enable free mode (use free models)"
    )

    # Execute command (non-interactive mode)
    execute_parser = subparsers.add_parser(
        "execute", help="Execute a single task non-interactively"
    )
    execute_parser.add_argument(
        "--intent",
        required=True,
        help="The intent of the task (e.g., generate, edit, debug)",
    )
    execute_parser.add_argument(
        "--prompt", required=True, help="The user prompt/description for the task"
    )
    execute_parser.add_argument(
        "--files", nargs="*", help="Space-separated list of files to include in context"
    )
    execute_parser.add_argument(
        "--force-budget", action="store_true", help="Proceed even if budget is exceeded"
    )

    # Analytics command
    analytics_parser = subparsers.add_parser(
        "analytics", help="Display spending analytics"
    )

    # Version argument
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
        help="Show program's version number and exit",
    )

    args = parser.parse_args()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print(
            "Error: The OPENROUTER_API_KEY environment variable is not set.",
            file=sys.stderr,
        )
        print(
            "Please get a key from https://openrouter.ai/ and set the environment variable.",
            file=sys.stderr,
        )
        sys.exit(1)

    config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
    settings = load_config(os.path.join(config_dir, "settings.json"))
    model_tiers = load_config(os.path.join(config_dir, "model_tiers.json"))
    intent_routes = load_config(os.path.join(config_dir, "intent_routes.json"))

    client = OpenRouterClient(api_key, model_tiers, budget_optimizer.free_model_selector, args.free_mode)
    semantic_classifier = SemanticClassifier()
    budget_optimizer = BudgetManager(daily_limit=settings.get("daily_limit"), free_mode_enabled=args.free_mode)

    if args.command == "run":
        # Update free models if free mode is enabled
        if args.free_mode:
            await budget_optimizer.free_mode_manager.update_free_models()
        await run_interactive_mode(
            settings,
            model_tiers,
            intent_routes,
            client,
            semantic_classifier,
            budget_optimizer,
        )
    elif args.command == "execute":
        run_non_interactive_mode(
            args,
            settings,
            model_tiers,
            intent_routes,
            client,
            semantic_classifier,
            budget_optimizer,
        )
    elif args.command == "analytics":
        print("\n--- Ralex Spending Analytics ---")
        print("Daily Spending:")
        for date, amount in budget_optimizer.get_daily_total().items():
            print(f"  {date}: ${amount:.2f}")
        print("\nSpending by Model:")
        for model, amount in (
            budget_optimizer.get_usage_summary().get("model_breakdown", {}).items()
        ):
            print(f"  {model}: ${amount:.2f}")
        print("------------------------------")
    else:
        parser.print_help()

    print("\nGoodbye!")


if __name__ == "__main__":
    asyncio.run(main())
