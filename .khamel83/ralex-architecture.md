# Ralex Architecture: OpenCode.ai Intelligent Wrapper

## System Design
```
User → Ralex CLI → Agent-OS Analysis → LiteLLM Routing → OpenCode.ai Execution
                     ↓
                Universal Logger → Budget Tracking
```

## Core Components
- **CLI Interface**: Unified command entry point
- **Task Classifier**: Simple/complex/mobile task analysis
- **OpenCode.ai Wrapper**: YOLO execution with error handling
- **LiteLLM Router**: Model selection and routing
- **Universal Logger**: All operations tracked with unique IDs
- **Budget Manager**: Hourly and daily budget enforcement

## Integration Points
- **Existing Ralex API**: Preserve all endpoints
- **Mobile Workflow**: OpenCat iOS compatibility
- **Agent-OS Framework**: Cost optimization and patterns
- **Session Management**: Context persistence

## Key Features
- YOLO mode via OpenCode.ai
- Budget-optimized model routing
- Mobile integration preserved
- Universal operation logging
- Pattern caching and reuse