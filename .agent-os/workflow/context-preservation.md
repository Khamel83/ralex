# K83 Context Preservation Workflows

> Last Updated: 2025-08-07
> Version: 1.0.0

## Overview

K83 context preservation enables seamless continuity across sessions, model switches, and development environments. Context includes conversation history, project state, Agent OS specifications, memory bank contents, and execution progress.

## Context Types & Storage

### Conversation Context
**Content:** Full dialogue history between user and AI
**Storage:** 
- SQLite database for structured queries and relationships
- Markdown files for human readability and version control
- Git history for collaboration and branching

### Project State Context  
**Content:** Current Agent OS specs, active tasks, implementation progress
**Storage:**
- Agent OS `.agent-os/` directory structure
- Memory Bank MCP for persistent project knowledge
- Git commits for state versioning

### Execution Context
**Content:** Agentic workflow progress, current phase, intermediate results
**Storage:**
- SQLite for structured execution state
- Temporary files for intermediate artifacts
- Memory Bank MCP for key decisions and learnings

### MCP Server Context
**Content:** State of all 6 MCP servers, active connections, cached data
**Storage:**
- Individual MCP server state files
- Coordinated state synchronization
- Health monitoring and connection status

## Context Preservation Commands

### `/save-session "milestone note"`
**Purpose:** Capture complete current state with descriptive milestone

**Workflow:**
1. **Context Capture**
   - Serialize current conversation history
   - Save Agent OS spec and task progress
   - Capture MCP server states
   - Record current execution phase

2. **State Storage**
   - Update SQLite database with structured state
   - Generate human-readable markdown summary
   - Store memory bank updates
   - Create git commit with milestone note

3. **Validation**
   - Verify all context components saved successfully
   - Test context reconstruction capability
   - Update context integrity checksums

### `/switch-model [model-name]`
**Purpose:** Change AI model while preserving complete context

**Workflow:**
1. **Pre-Switch Context Capture**
   - Save current conversation state
   - Capture any incomplete workflows
   - Store model-specific preferences and patterns

2. **Context Transfer Preparation**
   - Generate model-appropriate context summary
   - Prepare context for new model's capabilities
   - Identify any model-specific adaptations needed

3. **Model Switch Execution**
   - Initialize new model session
   - Load complete context history
   - Restore Agent OS state and specifications
   - Resume any interrupted workflows

4. **Post-Switch Validation**
   - Verify context reconstruction accuracy
   - Test workflow continuity
   - Update model usage patterns in memory

### `/resume-session [session-id]`
**Purpose:** Restore complete context from previous session

**Workflow:**
1. **Session Identification**
   - Locate session by ID or use most recent
   - Verify session integrity and completeness
   - Check for any context corruption

2. **Context Reconstruction**
   - Restore conversation history and state
   - Reload Agent OS specifications and progress
   - Reconnect MCP servers and restore their state
   - Resume any interrupted agentic workflows

3. **State Validation**
   - Verify all context components loaded correctly
   - Test MCP server connectivity and functionality
   - Validate Agent OS spec consistency

## Model Switching Patterns

### Capability-Based Context Adaptation
Different models receive context optimized for their capabilities:

**Code-Focused Models:**
- Emphasize technical specifications and implementation details
- Include code patterns and architectural decisions
- Provide detailed error handling and testing context

**Planning-Focused Models:**
- Emphasize high-level specifications and user stories
- Include project roadmap and feature prioritization
- Provide strategic decision context and trade-offs

**General-Purpose Models:**
- Balanced context including both strategic and tactical elements
- Full conversation history for natural continuation
- Complete Agent OS methodology context

### Context Compression & Expansion
```
Full Context → Analyze Model Capabilities → Compress/Expand Context → Transfer → Validate
```

**Compression Strategies:**
- Summarize less critical conversation threads
- Focus on active Agent OS specs and tasks
- Preserve key decisions and architectural choices

**Expansion Strategies:**
- Restore full context for capable models
- Include detailed technical implementation history
- Provide comprehensive project background

## Session Continuity Patterns

### Cross-Environment Context Transfer
Moving between Claude Code, Cursor, CCR, and other environments:

1. **Export Phase**
   - Extract context from source environment
   - Convert to universal format
   - Validate export completeness

2. **Transfer Phase**  
   - Move context via git, file system, or direct transfer
   - Apply environment-specific formatting
   - Prepare for target environment import

3. **Import Phase**
   - Load context into target environment
   - Reconstruct conversation flow
   - Restore MCP server connections

### Workflow Resumption
Continuing interrupted agentic workflows across sessions:

**Workflow State Preservation:**
- Current phase in Agent OS methodology
- Completed tasks and remaining work
- Intermediate artifacts and generated code
- Error states and recovery strategies

**Resumption Process:**
- Identify workflow interruption point
- Validate intermediate state integrity
- Resume execution from checkpoint
- Apply any context updates since interruption

## Memory Bank Integration

### Long-Term Context Storage
**Project Memory:**
- Key architectural decisions and rationale
- Successful patterns and anti-patterns learned
- User preferences and coding style
- Team standards and conventions

**Cross-Project Memory:**
- Reusable Agent OS spec templates
- Common implementation patterns
- Lessons learned from previous projects
- Best practices evolved over time

### Context-Aware Memory Retrieval
```
Current Context → Memory Query → Relevant Memories → Context Enhancement → Improved Development
```

**Memory Query Patterns:**
- Find similar previous implementations
- Retrieve relevant architectural decisions
- Identify applicable code patterns
- Access related troubleshooting knowledge

## Git Integration for Context

### Context Versioning
- **Automatic Commits** - Context saved with each milestone
- **Branch Awareness** - Context preserved across git branches
- **Merge Handling** - Context conflict resolution
- **History Navigation** - Access context from any commit

### Collaborative Context
- **Shared Context** - Team access to project context and decisions
- **Context Merging** - Combine context from multiple team members
- **Permission Models** - Control access to sensitive context elements

## Context Integrity & Validation

### Integrity Checks
- **Checksum Validation** - Detect context corruption
- **Consistency Verification** - Ensure context components align
- **Completeness Testing** - Verify all context elements present
- **Recovery Procedures** - Handle context corruption gracefully

### Performance Optimization
- **Context Indexing** - Fast context search and retrieval
- **Compression** - Efficient storage of large context histories
- **Caching** - Quick access to frequently used context elements
- **Cleanup** - Remove obsolete or redundant context data

## Error Handling & Recovery

### Context Loss Prevention
- **Multiple Backups** - Redundant context storage
- **Incremental Saves** - Frequent context updates
- **Recovery Points** - Known good context states
- **Emergency Procedures** - Context recovery from partial data

### Graceful Degradation
- **Partial Context Recovery** - Work with incomplete context
- **Context Reconstruction** - Rebuild missing context from available data
- **User Confirmation** - Verify reconstructed context accuracy
- **Progressive Enhancement** - Build context confidence over time

The K83 context preservation system ensures that development workflows maintain perfect continuity regardless of tool switches, model changes, or session interruptions, creating a truly seamless AI development experience.