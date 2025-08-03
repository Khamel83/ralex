# Refactoring Plan

This document outlines the files and classes to be renamed as part of the codebase refactoring initiative.

## Files to Rename

*   `ralex_core/v4_orchestrator.py` -> `ralex_core/orchestrator.py`
*   `tests/unit/test_v4_orchestrator.py` -> `tests/unit/test_orchestrator.py`
*   `start_ralex_v4.py` -> `start_ralex.py`
*   `ralex_core/v4_api.py` -> `ralex_core/api.py`
*   `ralex_core/litellm_v4_router.py` -> `ralex_core/litellm_router.py`
*   `ralex_core/agentos_v4_integration.py` -> `ralex_core/agentos_integration.py`
*   `docs/V4_ARCHITECTURE.md` -> `docs/ARCHITECTURE.md`
*   `V4_COMPLETION_STATUS.md` -> `COMPLETION_STATUS.md`
*   `README_V4.md` -> `README_V2.md` (to avoid conflict with existing README.md)
*   `RALEX_V4_SPECIFICATION.md` -> `RALEX_SPECIFICATION.md`
*   `RALEX_V4_SETUP.md` -> `RALEX_SETUP.md`
*   `RALEX_V4_ROADMAP.md` -> `RALEX_ROADMAP.md`

## Classes to Rename

*   `RalexV4Orchestrator` -> `RalexOrchestrator`
*   `TestRalexV4Orchestrator` -> `TestRalexOrchestrator`
*   `AgentOSV4Enhancer` -> `AgentOSEnhancer`
*   `LiteLLMV4Router` -> `LiteLLMRouter`
