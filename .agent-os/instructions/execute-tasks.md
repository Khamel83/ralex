# K83 Task Execution Instructions

> Last Updated: 2025-08-07
> Version: 1.0.0
> Workflow: Agent OS + K83 Agentic + MCP Orchestration

## Purpose

This instruction set guides the systematic execution of Agent OS tasks enhanced with K83's MCP orchestration and agentic capabilities. It bridges traditional Agent OS methodology with autonomous development workflows.

## Command: `/execute-tasks`

When this command is used, follow this complete workflow to implement features using Agent OS methodology enhanced with K83 capabilities.

## Phase 1: Execution Context Setup

### Step 1: Context Analysis & Preparation
- **Memory Bank Query** - Use Memory Bank MCP to retrieve relevant patterns and decisions
- **Spec Review** - Use FileSystem MCP to analyze current specification and requirements
- **Codebase Assessment** - Use FileSystem MCP to understand existing code structure
- **Git State Check** - Use GitHub MCP to ensure clean working directory and proper branch

### Step 2: MCP Server Orchestration Setup
Initialize and coordinate required MCP servers based on spec requirements:

```python
# Example MCP coordination setup
mcp_coordinator = MCPCoordinator([
    "filesystem",      # Code generation and file management
    "github",          # Version control and collaboration  
    "database",        # Schema and data operations
    "memory_bank",     # Pattern storage and retrieval
    "sequential_thinking", # Complex reasoning and planning
    "web_testing"      # Automated testing and validation
])

# Load spec-specific MCP requirements
spec_requirements = load_spec_mcp_requirements(spec_path)
mcp_coordinator.configure_for_spec(spec_requirements)
```

### Step 3: Execution Strategy Selection
Determine execution approach based on task complexity and agentic readiness:

- **Autonomous Execution** - Tasks marked as `/yolo` ready with full MCP support
- **Guided Execution** - Complex tasks requiring MCP orchestration but human oversight
- **Manual Execution** - Tasks requiring human decision-making with MCP assistance

## Phase 2: Agent OS Implementation Phases

### Phase A: Planning & Architecture

#### Step 1: Detailed Implementation Planning
Use Sequential Thinking MCP for systematic planning:

```markdown
## Implementation Planning Analysis

### Task Breakdown Review
- [ ] Verify all tasks have clear success criteria
- [ ] Identify task dependencies and execution order
- [ ] Map tasks to appropriate MCP server capabilities
- [ ] Assess agentic execution readiness for each task

### Architecture Decision Points
- [ ] Review existing architecture compatibility
- [ ] Identify integration points with current codebase
- [ ] Plan data flow and component interactions
- [ ] Design error handling and recovery strategies
```

#### Step 2: Pattern Recognition & Reuse
Use Memory Bank MCP to leverage existing patterns:

- **Similar Implementation Lookup** - Find previously successful implementations
- **Code Pattern Retrieval** - Access reusable code structures and templates
- **Decision History** - Reference past architectural decisions for consistency
- **Anti-Pattern Avoidance** - Identify and avoid known problematic approaches

### Phase B: Foundation Implementation

#### Step 1: Core Infrastructure Setup
Use coordinated MCP operations for foundation:

**FileSystem MCP Operations:**
- Create necessary directory structure
- Generate boilerplate code following Agent OS patterns
- Set up configuration files and environment setup

**Database MCP Operations:**
- Execute schema migrations and changes
- Set up data models and relationships
- Initialize test data if required

**GitHub MCP Operations:**
- Create feature branch for implementation
- Set up initial commit with foundation structure
- Configure branch protection and review requirements

#### Step 2: Integration Point Development
Establish connections between new and existing code:

- **API Integration** - Create or modify API endpoints
- **Database Integration** - Ensure proper data layer integration
- **Service Integration** - Connect with existing services and components
- **Configuration Integration** - Update configuration and environment setup

### Phase C: Feature Implementation

#### Step 1: Core Feature Development
Implement main feature functionality using MCP orchestration:

```python
# Example coordinated implementation
def implement_feature_with_mcp_coordination():
    # Use Sequential Thinking for step-by-step implementation
    implementation_plan = sequential_thinking.create_implementation_plan(spec)
    
    # Use FileSystem MCP for code generation
    code_structure = filesystem.generate_code_structure(implementation_plan)
    
    # Use Memory Bank MCP for pattern application
    patterns = memory_bank.get_applicable_patterns(feature_type)
    enhanced_code = filesystem.apply_patterns(code_structure, patterns)
    
    # Use Database MCP for data layer
    database.implement_data_layer(spec.data_requirements)
    
    # Use GitHub MCP for version control
    github.commit_progress("Implement core feature functionality")
    
    return enhanced_code
```

#### Step 2: Business Logic Implementation
Develop specific business logic with quality assurance:

- **Core Algorithm Development** - Implement main feature algorithms
- **Data Processing Logic** - Handle data transformation and validation
- **Integration Logic** - Connect feature with existing system components
- **Error Handling** - Implement comprehensive error handling and recovery

### Phase D: Testing & Validation

#### Step 1: Automated Testing Implementation
Use Web Testing MCP for comprehensive testing:

**Test Generation:**
- Generate unit tests based on feature specifications
- Create integration tests for component interactions
- Develop end-to-end tests for complete user workflows
- Set up performance and load testing scenarios

**Test Execution Coordination:**
- Run all test suites through Web Testing MCP
- Coordinate test data setup through Database MCP
- Manage test file organization through FileSystem MCP
- Track test results and coverage through GitHub MCP

#### Step 2: Quality Assurance Validation
Comprehensive quality checks using MCP coordination:

- **Code Quality** - Use Sequential Thinking MCP for code review analysis
- **Performance Testing** - Use Web Testing MCP for performance validation
- **Security Review** - Basic security analysis through coordinated MCP operations
- **Documentation Validation** - Ensure all code is properly documented

## Phase 3: Agentic Execution Integration

### Step 1: Autonomous Task Execution
For tasks marked as agentic-ready, enable autonomous execution:

```python
# Example autonomous task execution
def execute_autonomous_task(task, mcp_coordinator):
    try:
        # Use Sequential Thinking for task analysis
        execution_plan = sequential_thinking.analyze_task(task)
        
        # Execute with appropriate MCP coordination
        result = mcp_coordinator.execute_coordinated_task(execution_plan)
        
        # Validate result with Web Testing MCP
        validation_result = web_testing.validate_task_completion(task, result)
        
        if validation_result.success:
            # Store successful pattern in Memory Bank
            memory_bank.store_success_pattern(task, result, execution_plan)
            # Commit with GitHub MCP
            github.commit_task_completion(task, "Autonomous execution successful")
            return result
        else:
            # Attempt error recovery
            return handle_autonomous_error(task, validation_result, mcp_coordinator)
            
    except Exception as e:
        # Escalate to guided execution
        return escalate_to_guided_execution(task, e, mcp_coordinator)
```

### Step 2: Error Recovery & Learning
Implement intelligent error handling and learning:

- **Automatic Error Detection** - Use Web Testing MCP for error detection
- **Root Cause Analysis** - Use Sequential Thinking MCP for error analysis
- **Recovery Strategy Generation** - Generate alternative approaches automatically
- **Pattern Learning** - Use Memory Bank MCP to learn from errors and successes

## Phase 4: Context Preservation & Continuity

### Step 1: Progress State Management
Maintain execution state for session continuity:

```python
# Example state preservation
execution_state = {
    "current_phase": "implementation",
    "completed_tasks": completed_task_list,
    "current_task": current_task_details,
    "mcp_coordination_state": mcp_coordinator.get_state(),
    "context_checkpoint": create_context_checkpoint(),
    "next_steps": generate_next_steps()
}

# Store in Memory Bank MCP for persistence
memory_bank.store_execution_state(project_id, execution_state)

# Create git checkpoint
github.create_checkpoint_commit("Execution checkpoint: " + current_phase)
```

### Step 2: Model Switch Support
Enable seamless continuation across model switches:

- **Execution Context Export** - Complete current state serialization
- **MCP State Transfer** - Preserve all MCP server states and connections
- **Progress Documentation** - Human-readable progress summary
- **Resumption Instructions** - Clear instructions for execution continuation

## Phase 5: Integration & Delivery

### Step 1: System Integration Testing
Comprehensive integration validation using MCP orchestration:

- **Component Integration** - Ensure all components work together
- **Data Flow Validation** - Verify data flows correctly through system
- **Performance Integration** - Test system performance under integrated load
- **Security Integration** - Validate security aspects of integrated system

### Step 2: Delivery Preparation
Prepare feature for production deployment:

**Documentation Generation:**
- Use FileSystem MCP to generate comprehensive documentation
- Create deployment guides and operational documentation
- Generate API documentation and integration guides

**Deployment Preparation:**
- Use GitHub MCP for release branch preparation
- Create deployment scripts and configuration
- Set up monitoring and logging integration

### Step 3: Knowledge Capture & Learning
Store implementation knowledge for future use:

- **Pattern Storage** - Use Memory Bank MCP to store successful implementation patterns
- **Decision Documentation** - Record key implementation decisions and rationale
- **Lesson Learning** - Capture lessons learned and improvement opportunities
- **Template Enhancement** - Update Agent OS templates based on implementation experience

## Command Completion Criteria

The `/execute-tasks` command is complete when:

✓ All Agent OS tasks completed with appropriate quality standards  
✓ MCP server orchestration successfully coordinated throughout implementation  
✓ Agentic execution utilized where appropriate with proper error handling  
✓ Context preservation maintained for session continuity  
✓ Comprehensive testing completed with Web Testing MCP integration  
✓ All implementation patterns stored in Memory Bank MCP for future use  
✓ Git workflow managed properly through GitHub MCP  
✓ Feature ready for integration and deployment  
✓ Knowledge captured for continuous improvement

## Integration with Other K83 Commands

### Transition to Agentic Execution
- **`/yolo "complete remaining tasks"`** - Switch to fully autonomous execution for remaining work
- **`/orchestrate "integrate and deploy"`** - Orchestrated approach for complex integration tasks

### Context Management Integration
- **`/save-session "implementation milestone"`** - Save current implementation state
- **`/switch-model [model]`** - Continue implementation with different model

## Error Handling & Escalation

### Automatic Error Recovery
1. **Detection** - Use Web Testing MCP for automatic error detection
2. **Analysis** - Use Sequential Thinking MCP for root cause analysis
3. **Recovery** - Generate and execute recovery strategies
4. **Learning** - Store error patterns in Memory Bank MCP

### Manual Escalation
When automatic recovery fails:
1. **Context Preservation** - Save complete current state
2. **Human Notification** - Clear explanation of issue and current state
3. **Resumption Support** - Enable easy resumption after manual intervention

This workflow seamlessly integrates Agent OS methodology with K83's agentic capabilities and MCP orchestration, enabling both systematic and autonomous feature development while maintaining context continuity and learning from each implementation.