## Phase 8: Comprehensive Unit Testing

**Goal:** To ensure the correctness and stability of the `ralex` codebase through automated unit tests.

### Epic 8.1: Testing Framework Setup

- [x] **Task 8.1.1:** Create a `tests/unit` directory for unit tests.
- [x] **Task 8.1.2:** Create `tests/unit/test_semantic_classifier.py` and add basic unit tests for `SemanticClassifier` (e.g., test intent classification for known inputs).
- [x] **Task 8.1.3:** Create `tests/unit/test_budget_optimizer.py` and add basic unit tests for `BudgetOptimizer` (e.g., test `record_usage`, `get_total_spent`, `check_budget_status`).
- [x] **Task 8.1.4:** Create `tests/unit/test_code_executor.py` and add basic unit tests for `CodeExecutor` (e.g., test `execute_python_code` with simple valid/invalid code, timeout).
- [x] **Task 8.1.5:** Create `tests/unit/test_launcher.py` and add basic unit tests for `launcher.py`'s core functions (e.g., `parse_file_modifications`, `parse_code_blocks`, `load_config`).
- [x] **Task 8.1.6:** Configure `pytest` to discover and run these new unit tests.
- [x] **Task 8.1.7:** Commit the changes with the message: `feat(testing): Setup unit testing framework and add initial tests`.

## Phase 9: Advanced Budget Optimization (Continued)

**Goal:** To implement intelligent downgrades and spending analytics.

### Epic 9.1: Intelligent Downgrades

- [x] **Task 9.1.1:** Modify `ralex_core/budget_optimizer.py` to include logic for intelligent model downgrades when the budget is constrained. This will involve selecting a cheaper model from a lower tier if the preferred model exceeds the budget.
- [x] **Task 9.1.2:** Update `ralex_core/launcher.py` to pass the budget status to the model selection logic.
- [x] **Task 9.1.3:** Commit the changes with the message: `feat(budget): Implement intelligent model downgrades`.

### Epic 9.2: Spending Analytics

- [x] **Task 9.2.1:** Modify `ralex_core/budget_optimizer.py` to include methods for generating spending analytics (e.g., `get_daily_spending`, `get_model_spending`).
- [x] **Task 9.2.2:** Add a new CLI command (e.g., `ralex analytics`) to `ralex_core/launcher.py` that displays these spending analytics to the user.
- [x] **Task 9.2.3:** Commit the changes with the message: `feat(budget): Add spending analytics CLI command`.

## Future Considerations

This section outlines potential future enhancements and areas for further development.

### Model Selection & Cost Optimization

- **Dynamic Tiering Refinement:** Currently, tiers are fixed. Future work could involve dynamically adjusting tier definitions based on real-world model performance and cost changes.
- **Predictive Cost Analysis:** Implement more accurate token estimation and predictive cost analysis before making LLM calls.
- **Model Performance Tracking:** Track success rates and quality of responses per model to inform dynamic model selection.

### External Tool Integration

- **Pluggable Executors:** Expand the `ralex_core/executors` directory with more specialized executors for various tools and IDEs (e.g., Continue.dev, Cursor, custom shell scripts).
- **`gemini-mcp-tool` Integration:** Investigate integrating `https://github.com/jamubc/gemini-mcp-tool` as a specialized executor for Gemini models, potentially enabling more advanced interactions or leveraging specific Gemini capabilities.

### Agentic Capabilities

- **Multi-Step Reasoning & Planning:** Implement a more sophisticated agentic loop that allows Ralex to break down complex tasks into smaller sub-tasks, plan execution, and self-correct.
- **Self-Correction & Reflection:** Enable Ralex to analyze its own outputs and execution results, identify errors, and attempt to correct them autonomously.
- **Goal-Oriented Execution:** Allow users to define high-level goals, and Ralex will work towards achieving them through iterative steps.

### Testing & Quality Assurance

- **Integration Tests:** Develop end-to-end integration tests that simulate real-world workflows across different executors and models.
- **Performance Benchmarking:** Establish a robust benchmarking suite to measure Ralex's performance (speed, cost, accuracy) over time.
- **Code Quality & Linting:** Integrate automated code quality checks (e.g., `flake8`, `mypy`) into the development workflow.

### CLI & User Experience

- **Custom Commands:** Allow users to define custom commands and aliases for common tasks.
- **Configuration via CLI:** Enable modification of `settings.json` and other config files directly through CLI commands.
- **Improved Output Formatting:** Enhance the readability and interactivity of CLI output (e.g., richer diff displays, progress indicators).
