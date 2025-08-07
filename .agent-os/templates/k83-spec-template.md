# K83 Specification Template

> Template Version: 1.0.0
> Last Updated: 2025-08-07
> Usage: Agent OS + K83 MCP + Agentic Workflows

## Template Overview

This template extends the standard Agent OS specification template with K83-specific elements for MCP integration and agentic workflow support.

## File Structure Template

```
.agent-os/specs/YYYY-MM-DD-feature-name/
├── spec.md                 # Main specification (use template below)
├── spec-lite.md           # Summary version
├── tasks.md               # Implementation tasks with MCP integration
└── sub-specs/
    ├── technical-spec.md  # Technical details with MCP orchestration
    ├── database-schema.md # Database changes (Database MCP integration)
    ├── api-spec.md        # API design (Web Testing MCP integration)
    └── tests.md           # Testing strategy (Web Testing MCP integration)
```

## Main Specification Template (spec.md)

```markdown
# Spec Requirements Document

> Spec: [SPEC_NAME]
> Created: [CURRENT_DATE]
> Status: Planning
> K83 Integration Level: [Basic/Standard/Advanced]
> Primary MCP Servers: [LIST_PRIMARY_MCPS]

## Overview

[FEATURE_DESCRIPTION]

**K83 Integration Summary:**
This feature leverages [LIST_MCP_SERVERS] for [DESCRIBE_MCP_BENEFITS] and supports [AGENTIC_CAPABILITIES].

## User Stories

### Standard User Stories
[STANDARD_AGENT_OS_USER_STORIES]

### Agentic Workflow Stories
- **As a developer using `/yolo`**, I want [AUTONOMOUS_CAPABILITY] so that [AUTONOMOUS_BENEFIT]
- **As a developer using `/orchestrate`**, I want [ORCHESTRATED_CAPABILITY] so that [ORCHESTRATED_BENEFIT]
- **As a developer switching models**, I want [CONTEXT_CONTINUITY] so that [CONTINUITY_BENEFIT]

## Spec Scope

### Feature Scope
[STANDARD_FEATURE_SCOPE]

### MCP Integration Scope
- **FileSystem MCP:** [FILESYSTEM_OPERATIONS]
- **GitHub MCP:** [GIT_OPERATIONS]  
- **Database MCP:** [DATABASE_OPERATIONS]
- **Memory Bank MCP:** [MEMORY_OPERATIONS]
- **Sequential Thinking MCP:** [REASONING_OPERATIONS]
- **Web Testing MCP:** [TESTING_OPERATIONS]

### Agentic Workflow Scope
- **Autonomous Development Support:** [YOLO_CAPABILITIES]
- **Orchestrated Development Support:** [ORCHESTRATE_CAPABILITIES]
- **Context Preservation Requirements:** [CONTEXT_NEEDS]

## Out of Scope

### Feature Out of Scope
[STANDARD_OUT_OF_SCOPE]

### K83 Integration Out of Scope
- **MCP Limitations:** [WHAT_MCPS_CANNOT_DO]
- **Agentic Limitations:** [WHAT_AUTONOMOUS_WORKFLOWS_CANNOT_HANDLE]
- **Context Limitations:** [WHAT_CONTEXT_CANNOT_PRESERVE]

## Expected Deliverable

### Standard Deliverables
[STANDARD_AGENT_OS_DELIVERABLES]

### K83 Enhanced Deliverables
- **MCP-Coordinated Implementation:** [MCP_DELIVERABLES]
- **Agentic Workflow Support:** [AGENTIC_DELIVERABLES]
- **Context Preservation Infrastructure:** [CONTEXT_DELIVERABLES]

## K83 Integration Details

### MCP Server Coordination Matrix

| Task Category | Primary MCP | Secondary MCPs | Coordination Pattern |
|---------------|-------------|----------------|---------------------|
| [TASK_TYPE_1] | [PRIMARY_MCP_1] | [SECONDARY_MCPS_1] | [COORDINATION_1] |
| [TASK_TYPE_2] | [PRIMARY_MCP_2] | [SECONDARY_MCPS_2] | [COORDINATION_2] |

### Agentic Workflow Readiness Assessment

#### `/yolo` Autonomous Development
- **Readiness Level:** [Ready/Partial/Not Ready]
- **Autonomous Tasks:** [LIST_AUTONOMOUS_TASKS]
- **Manual Intervention Points:** [LIST_MANUAL_POINTS]
- **Quality Gates:** [LIST_QUALITY_CHECKS]

#### `/orchestrate` Coordinated Development  
- **Orchestration Complexity:** [Simple/Standard/Complex]
- **Coordination Requirements:** [LIST_COORDINATION_NEEDS]
- **Human Oversight Requirements:** [LIST_OVERSIGHT_NEEDS]
- **Integration Challenges:** [LIST_INTEGRATION_CHALLENGES]

### Context Preservation Requirements

#### Session State Requirements
- **Persistent State Elements:** [LIST_STATE_ELEMENTS]
- **Cross-Session Continuity:** [DESCRIBE_CONTINUITY_NEEDS]
- **Model Switch Support:** [DESCRIBE_MODEL_SWITCH_NEEDS]

#### Memory Bank Integration
- **Knowledge Storage:** [WHAT_TO_STORE_IN_MEMORY_BANK]
- **Pattern Recognition:** [WHAT_PATTERNS_TO_RECOGNIZE]
- **Decision History:** [WHAT_DECISIONS_TO_TRACK]

## Spec Documentation

- Tasks: @.agent-os/specs/[FOLDER]/tasks.md
- Technical Specification: @.agent-os/specs/[FOLDER]/sub-specs/technical-spec.md
- Database Schema: @.agent-os/specs/[FOLDER]/sub-specs/database-schema.md
- API Specification: @.agent-os/specs/[FOLDER]/sub-specs/api-spec.md
- Testing Strategy: @.agent-os/specs/[FOLDER]/sub-specs/tests.md

## Implementation Success Criteria

### Standard Agent OS Success Criteria
[STANDARD_SUCCESS_CRITERIA]

### K83 Integration Success Criteria
- **MCP Orchestration:** [MCP_SUCCESS_CRITERIA]
- **Agentic Workflow Support:** [AGENTIC_SUCCESS_CRITERIA]  
- **Context Preservation:** [CONTEXT_SUCCESS_CRITERIA]
- **Performance Standards:** [PERFORMANCE_STANDARDS]
```

## Summary Template (spec-lite.md)

```markdown
# [FEATURE_NAME] - K83 Enhanced Summary

[ELEVATOR_PITCH_WITH_AGENTIC_BENEFITS]

## Key Points
- **Core Feature:** [CORE_FUNCTIONALITY]
- **MCP Integration:** [KEY_MCP_BENEFITS] 
- **Agentic Support:** [AUTONOMOUS_CAPABILITIES]
- **Context Continuity:** [CONTEXT_BENEFITS]

## K83 Readiness
- **`/yolo` Ready:** [YES/PARTIAL/NO] - [BRIEF_EXPLANATION]
- **`/orchestrate` Ready:** [YES/PARTIAL/NO] - [BRIEF_EXPLANATION]
- **Context Preserving:** [YES/PARTIAL/NO] - [BRIEF_EXPLANATION]
```

## Usage Guidelines

### When to Use This Template
- All new features in K83-enabled projects
- Converting existing features to K83-compatible specifications
- Features that will leverage MCP orchestration or agentic workflows

### Template Customization
- Replace all [PLACEHOLDER] values with specific content
- Remove sections not applicable to your specific feature
- Add project-specific sections as needed
- Ensure Agent OS compatibility is maintained

### MCP Integration Planning
- Identify which of the 6 core MCP servers are relevant
- Plan coordination patterns for multi-MCP operations
- Consider error handling and fallback scenarios
- Design for performance and resource efficiency

### Agentic Workflow Preparation
- Assess which tasks can be automated with `/yolo`
- Plan orchestration requirements for `/orchestrate`
- Design quality gates and validation checkpoints
- Consider error recovery and human intervention points

## Template Evolution

This template evolves with:
- **Agent OS Updates** - Sync with buildermethods/agent-os template changes
- **K83 Enhancements** - Add new MCP servers and agentic capabilities
- **Usage Learning** - Improve based on real-world usage patterns
- **Community Feedback** - Incorporate improvements from K83 community

## Related Templates

- **Standard Agent OS Templates** - Use when K83 features not needed
- **MCP Integration Template** - For MCP-specific integration planning
- **Agentic Workflow Template** - For autonomous workflow design
- **Context Preservation Template** - For session continuity planning

This template ensures that all specifications are ready for both traditional Agent OS workflows and enhanced K83 agentic capabilities while maintaining full compatibility with the Agent OS ecosystem.