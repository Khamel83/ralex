# K83 Agentic Workflow Template

> Template Version: 1.0.0
> Last Updated: 2025-08-07
> Usage: Autonomous Workflow Design

## Template Overview

This template guides the design and implementation of agentic workflows that combine Agent OS methodology with autonomous execution capabilities and MCP orchestration.

## Agentic Workflow Planning Template

### Workflow Assessment Matrix

```markdown
# Agentic Workflow Assessment: [WORKFLOW_NAME]

> Created: [CURRENT_DATE]
> Complexity Level: [Simple/Standard/Complex]
> Autonomy Level: [Fully Autonomous/Guided/Manual]

## Workflow Breakdown

### Input Requirements
- **User Intent:** [DESCRIBE_USER_GOAL]
- **Context Requirements:** [REQUIRED_CONTEXT_ELEMENTS]
- **Prerequisite Conditions:** [WHAT_MUST_BE_TRUE_BEFORE_STARTING]

### Autonomous Capability Assessment
- **Can `/yolo` Handle This?** [Yes/Partially/No]
- **Reasoning:** [WHY_THIS_AUTONOMY_LEVEL]
- **Manual Intervention Points:** [WHERE_HUMAN_INPUT_NEEDED]
- **Quality Gates:** [AUTOMATED_QUALITY_CHECKS]

### MCP Orchestration Requirements
- **Primary MCP Servers:** [LIST_PRIMARY_MCPS]
- **Coordination Pattern:** [DESCRIBE_HOW_MCPS_COORDINATE]
- **Error Recovery:** [HOW_TO_HANDLE_MCP_FAILURES]

## Phase-by-Phase Autonomous Execution Plan

### Phase 1: Analysis & Planning
**Autonomous Level:** [Fully/Partially/Manual]
**MCP Servers:** [Sequential Thinking, Memory Bank]

#### Automatic Steps:
1. [ ] Parse and analyze user request
2. [ ] Query Memory Bank for similar patterns
3. [ ] Generate execution plan with Sequential Thinking MCP
4. [ ] Validate plan feasibility

#### Quality Gates:
- [ ] Plan completeness check
- [ ] Resource availability validation
- [ ] Risk assessment completion

#### Manual Intervention Triggers:
- Complex architectural decisions needed
- Conflicting requirements detected
- Insufficient context for planning

### Phase 2: Implementation Planning
**Autonomous Level:** [Fully/Partially/Manual]
**MCP Servers:** [FileSystem, Database, Memory Bank]

#### Automatic Steps:
1. [ ] Generate code structure with FileSystem MCP
2. [ ] Plan database changes with Database MCP
3. [ ] Retrieve implementation patterns from Memory Bank
4. [ ] Create implementation roadmap

#### Quality Gates:
- [ ] Code structure validation
- [ ] Database schema compatibility check
- [ ] Pattern application verification

#### Manual Intervention Triggers:
- Breaking changes to existing systems
- Complex business logic requirements
- Integration with external systems

### Phase 3: Code Generation
**Autonomous Level:** [Fully/Partially/Manual]
**MCP Servers:** [FileSystem, GitHub, Memory Bank]

#### Automatic Steps:
1. [ ] Generate core implementation code
2. [ ] Apply established patterns and conventions
3. [ ] Create supporting files and configurations
4. [ ] Commit progress with GitHub MCP

#### Quality Gates:
- [ ] Code quality standards check
- [ ] Convention compliance validation
- [ ] Integration point verification

#### Manual Intervention Triggers:
- Security-sensitive code requirements
- Performance-critical implementations
- Complex algorithmic logic needed

### Phase 4: Testing & Validation
**Autonomous Level:** [Fully/Partially/Manual]
**MCP Servers:** [Web Testing, FileSystem, GitHub]

#### Automatic Steps:
1. [ ] Generate comprehensive test suite
2. [ ] Execute all tests and validate results
3. [ ] Fix basic implementation issues
4. [ ] Commit working implementation

#### Quality Gates:
- [ ] Test coverage threshold met
- [ ] All tests passing
- [ ] Performance benchmarks met

#### Manual Intervention Triggers:
- Test failures requiring design changes
- Performance issues needing optimization
- Complex debugging scenarios
```

## Autonomous Execution Patterns

### Simple Autonomous Pattern (`/yolo`)
```python
# Template: Simple Autonomous Workflow
class SimpleAutonomousWorkflow:
    def __init__(self, request, mcp_coordinator):
        self.request = request
        self.mcp = mcp_coordinator
        self.state = WorkflowState()
        
    async def execute(self):
        """
        Execute simple autonomous workflow with error handling.
        """
        try:
            # Phase 1: Plan
            plan = await self.autonomous_planning()
            self.state.update(plan=plan)
            
            # Phase 2: Implement
            implementation = await self.autonomous_implementation(plan)
            self.state.update(implementation=implementation)
            
            # Phase 3: Validate
            validation = await self.autonomous_validation(implementation)
            self.state.update(validation=validation)
            
            # Phase 4: Finalize
            result = await self.autonomous_finalization(validation)
            
            return AutonomousResult(
                success=True,
                result=result,
                state=self.state
            )
            
        except RequiresHumanIntervention as e:
            return self.escalate_to_human(e, self.state)
        except Exception as e:
            return self.handle_autonomous_error(e, self.state)
    
    async def autonomous_planning(self):
        # Use Sequential Thinking MCP for analysis
        analysis = await self.mcp.sequential_thinking.analyze(self.request)
        
        # Query Memory Bank for patterns
        patterns = await self.mcp.memory_bank.find_patterns(analysis)
        
        # Generate execution plan
        plan = await self.mcp.sequential_thinking.create_plan(analysis, patterns)
        
        # Validate plan feasibility
        if not self.validate_plan_feasibility(plan):
            raise RequiresHumanIntervention("Complex planning needed")
            
        return plan
    
    async def autonomous_implementation(self, plan):
        # Generate code with FileSystem MCP
        code = await self.mcp.filesystem.generate_code(plan)
        
        # Handle database changes if needed
        if plan.requires_database_changes:
            await self.mcp.database.apply_changes(plan.database_changes)
        
        # Commit progress
        await self.mcp.github.commit_progress("Autonomous implementation")
        
        return code
    
    async def autonomous_validation(self, implementation):
        # Generate and run tests
        tests = await self.mcp.web_testing.generate_tests(implementation)
        test_results = await self.mcp.web_testing.run_tests(tests)
        
        # Auto-fix simple issues
        if test_results.has_simple_failures:
            fixed_implementation = await self.auto_fix_issues(
                implementation, test_results.failures
            )
            return await self.autonomous_validation(fixed_implementation)
        
        # Escalate complex issues
        if test_results.has_complex_failures:
            raise RequiresHumanIntervention("Complex test failures")
        
        return test_results
```

### Complex Orchestrated Pattern (`/orchestrate`)
```python
# Template: Complex Orchestrated Workflow
class ComplexOrchestratedWorkflow:
    def __init__(self, request, mcp_coordinator):
        self.request = request
        self.mcp = mcp_coordinator
        self.state = OrchestrationState()
        self.human_interaction = HumanInteractionHandler()
        
    async def execute(self):
        """
        Execute complex workflow with human collaboration.
        """
        # Break down complex request
        breakdown = await self.decompose_complex_request()
        
        # Execute phases with human oversight
        for phase in breakdown.phases:
            phase_result = await self.execute_orchestrated_phase(phase)
            
            # Human review at key checkpoints
            if phase.requires_human_review:
                review_result = await self.human_interaction.review_phase(
                    phase, phase_result
                )
                if not review_result.approved:
                    phase_result = await self.revise_phase(phase, review_result)
            
            self.state.complete_phase(phase, phase_result)
        
        # Final integration and delivery
        final_result = await self.integrate_and_deliver()
        
        return OrchestrationResult(
            success=True,
            result=final_result,
            phases_completed=len(breakdown.phases),
            human_interactions=self.state.human_interactions
        )
    
    async def execute_orchestrated_phase(self, phase):
        """Execute individual phase with appropriate autonomy level."""
        if phase.autonomy_level == 'full':
            return await self.execute_autonomous_phase(phase)
        elif phase.autonomy_level == 'guided':
            return await self.execute_guided_phase(phase)
        else:
            return await self.execute_manual_phase(phase)
```

## Error Recovery & Learning Templates

### Autonomous Error Recovery
```python
# Template: Autonomous Error Recovery
class AutonomousErrorRecovery:
    def __init__(self, memory_bank_mcp):
        self.memory_bank = memory_bank_mcp
        self.recovery_strategies = self.load_recovery_strategies()
    
    async def handle_autonomous_error(self, error, context):
        """
        Comprehensive autonomous error recovery.
        """
        # Classify error type
        error_type = self.classify_error(error)
        
        # Check for learned recovery patterns
        learned_recovery = await self.memory_bank.find_recovery_pattern(
            error_type, context
        )
        
        if learned_recovery:
            # Apply learned recovery strategy
            recovery_result = await self.apply_recovery_strategy(
                learned_recovery, error, context
            )
            
            if recovery_result.success:
                # Store successful recovery for future use
                await self.memory_bank.store_success_pattern(
                    error_type, recovery_result.strategy, context
                )
                return recovery_result
        
        # Try standard recovery strategies
        for strategy in self.recovery_strategies[error_type]:
            try:
                recovery_result = await self.attempt_recovery(
                    strategy, error, context
                )
                
                if recovery_result.success:
                    # Learn new successful recovery
                    await self.memory_bank.store_recovery_pattern(
                        error_type, strategy, context, recovery_result
                    )
                    return recovery_result
                    
            except Exception as recovery_error:
                # Log recovery attempt failure
                self.log_recovery_failure(strategy, recovery_error)
        
        # Escalate to human if all recovery attempts fail
        return self.escalate_to_human(error, context, self.tried_strategies)
```

### Learning & Pattern Evolution
```python
# Template: Autonomous Learning System
class AutonomousLearningSystem:
    def __init__(self, memory_bank_mcp):
        self.memory_bank = memory_bank_mcp
        
    async def learn_from_execution(self, workflow, execution_result):
        """
        Learn from autonomous execution outcomes.
        """
        # Extract patterns from successful execution
        if execution_result.success:
            success_patterns = self.extract_success_patterns(
                workflow, execution_result
            )
            await self.memory_bank.store_patterns(success_patterns)
        
        # Learn from errors and recovery
        if execution_result.errors:
            error_patterns = self.extract_error_patterns(
                workflow, execution_result.errors
            )
            await self.memory_bank.store_error_patterns(error_patterns)
        
        # Update workflow optimization suggestions
        optimizations = self.identify_optimizations(workflow, execution_result)
        await self.memory_bank.store_optimizations(optimizations)
    
    async def evolve_autonomous_capabilities(self):
        """
        Evolve autonomous capabilities based on accumulated learning.
        """
        # Analyze success patterns
        success_analysis = await self.memory_bank.analyze_success_patterns()
        
        # Identify new autonomous opportunities
        new_opportunities = self.identify_autonomy_opportunities(success_analysis)
        
        # Update autonomous workflow definitions
        for opportunity in new_opportunities:
            await self.update_workflow_definition(opportunity)
        
        # Generate improved error recovery strategies
        improved_strategies = self.generate_improved_strategies(success_analysis)
        self.update_recovery_strategies(improved_strategies)
```

## Context Preservation Templates

### Workflow State Management
```python
# Template: Agentic Workflow State Management
class AgenticWorkflowState:
    def __init__(self, workflow_id):
        self.workflow_id = workflow_id
        self.phases = []
        self.current_phase = None
        self.context = {}
        self.checkpoints = []
        
    def create_checkpoint(self, description):
        """Create resumable checkpoint in workflow."""
        checkpoint = WorkflowCheckpoint(
            phase=self.current_phase,
            context=deepcopy(self.context),
            timestamp=datetime.now(),
            description=description
        )
        self.checkpoints.append(checkpoint)
        return checkpoint
    
    def serialize_for_model_switch(self):
        """Prepare state for model switching."""
        return {
            'workflow_id': self.workflow_id,
            'current_phase': self.current_phase,
            'completed_phases': [p for p in self.phases if p.completed],
            'context_summary': self.generate_context_summary(),
            'next_steps': self.generate_next_steps(),
            'resumption_instructions': self.generate_resumption_instructions()
        }
    
    def restore_from_serialized(self, serialized_state):
        """Restore state after model switch."""
        self.workflow_id = serialized_state['workflow_id']
        self.current_phase = serialized_state['current_phase']
        self.restore_phases(serialized_state['completed_phases'])
        self.restore_context(serialized_state['context_summary'])
```

### Model Switch Continuity
```python
# Template: Model Switch Continuity
class ModelSwitchContinuity:
    def __init__(self, memory_bank_mcp):
        self.memory_bank = memory_bank_mcp
    
    async def prepare_for_model_switch(self, workflow_state):
        """Prepare workflow for model switching."""
        # Create comprehensive context summary
        context_summary = self.create_model_agnostic_summary(workflow_state)
        
        # Store detailed state in Memory Bank
        await self.memory_bank.store_workflow_state(
            workflow_state.workflow_id, workflow_state
        )
        
        # Generate resumption instructions
        resumption_guide = self.generate_resumption_guide(workflow_state)
        
        return ModelSwitchPackage(
            context_summary=context_summary,
            resumption_guide=resumption_guide,
            state_id=workflow_state.workflow_id
        )
    
    async def resume_after_model_switch(self, switch_package):
        """Resume workflow after model switch."""
        # Restore detailed state from Memory Bank
        workflow_state = await self.memory_bank.restore_workflow_state(
            switch_package.state_id
        )
        
        # Validate state consistency
        if not self.validate_state_consistency(workflow_state):
            return self.request_state_clarification(switch_package)
        
        # Resume workflow execution
        return self.resume_workflow_execution(workflow_state)
```

## Usage Guidelines

### When to Use This Template
- Designing new autonomous workflows for K83
- Converting manual processes to agentic workflows
- Planning complex orchestrated development workflows
- Implementing error recovery and learning systems

### Template Customization
- Replace [PLACEHOLDER] values with specific workflow details
- Adjust autonomy levels based on workflow complexity
- Customize MCP server coordination for specific needs
- Add project-specific quality gates and validation

### Best Practices
- Always plan for error recovery and human escalation
- Design workflows to learn and improve from experience
- Ensure context preservation for session continuity
- Balance autonomy with quality and safety requirements

This template enables the creation of robust, intelligent agentic workflows that combine the best of Agent OS methodology with autonomous execution capabilities while maintaining safety, quality, and continuity.