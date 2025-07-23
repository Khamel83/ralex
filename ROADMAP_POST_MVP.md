## Phase 8: Comprehensive Unit Testing

**Goal:** To ensure the correctness and stability of the `ralex` codebase through automated unit tests.

### Epic 8.1: Testing Framework Setup

- [ ] **Task 8.1.1:** Create a `tests/unit` directory for unit tests.
- [ ] **Task 8.1.2:** Create `tests/unit/test_semantic_classifier.py` and add basic unit tests for `SemanticClassifier` (e.g., test intent classification for known inputs).
- [ ] **Task 8.1.3:** Create `tests/unit/test_budget_optimizer.py` and add basic unit tests for `BudgetOptimizer` (e.g., test `record_usage`, `get_total_spent`, `check_budget_status`).
- [ ] **Task 8.1.4:** Create `tests/unit/test_code_executor.py` and add basic unit tests for `CodeExecutor` (e.g., test `execute_python_code` with simple valid/invalid code, timeout).
- [ ] **Task 8.1.5:** Create `tests/unit/test_launcher.py` and add basic unit tests for `launcher.py`'s core functions (e.g., `parse_file_modifications`, `parse_code_blocks`, `load_config`).
- [ ] **Task 8.1.6:** Configure `pytest` to discover and run these new unit tests.
- [ ] **Task 8.1.7:** Commit the changes with the message: `feat(testing): Setup unit testing framework and add initial tests`.

## Phase 9: Advanced Budget Optimization (Continued)

**Goal:** To implement intelligent downgrades and spending analytics.

### Epic 9.1: Intelligent Downgrades

- [ ] **Task 9.1.1:** Modify `ralex_core/budget_optimizer.py` to include logic for intelligent model downgrades when the budget is constrained. This will involve selecting a cheaper model from a lower tier if the preferred model exceeds the budget.
- [ ] **Task 9.1.2:** Update `ralex_core/launcher.py` to pass the budget status to the model selection logic.
- [ ] **Task 9.1.3:** Commit the changes with the message: `feat(budget): Implement intelligent model downgrades`.

### Epic 9.2: Spending Analytics

- [ ] **Task 9.2.1:** Modify `ralex_core/budget_optimizer.py` to include methods for generating spending analytics (e.g., `get_daily_spending`, `get_model_spending`).
- [ ] **Task 9.2.2:** Add a new CLI command (e.g., `ralex analytics`) to `ralex_core/launcher.py` that displays these spending analytics to the user.
- [ ] **Task 9.2.3:** Commit the changes with the message: `feat(budget): Add spending analytics CLI command`.