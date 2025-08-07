# Slash Commands API Reference

The K83 Framework provides a comprehensive set of slash commands for agentic development workflows. All commands are available directly in Claude Code without any external setup.

## Table of Contents

- [Agentic Workflows](#agentic-workflows)
- [Development Commands](#development-commands)
- [Context & Memory Management](#context--memory-management)
- [Utility Commands](#utility-commands)
- [Advanced Commands](#advanced-commands)
- [Command Syntax](#command-syntax)
- [Error Handling](#error-handling)
- [Configuration](#configuration)

## Agentic Workflows

### `/yolo` - Autonomous Development

**Syntax**: `/yolo "description of feature or task"`

**Description**: Initiates fully autonomous development mode. K83 will automatically create specifications, implement code, run tests, fix issues, and commit the working solution to git.

**Parameters**:
- `description` (required): Natural language description of what you want to build

**Examples**:
```bash
# Build a complete authentication system
/yolo "implement JWT authentication with login/logout endpoints and middleware"

# Create a REST API with database integration
/yolo "build user management API with PostgreSQL and CRUD operations"

# Add a specific feature to existing code
/yolo "add password reset functionality with email verification"

# Fix and enhance existing functionality
/yolo "fix the user registration bug and add input validation"
```

**Workflow**:
1. **Analysis**: Analyzes the request and current project context
2. **Planning**: Creates detailed AgentOS specification
3. **Implementation**: Generates code following best practices
4. **Testing**: Writes and runs comprehensive tests
5. **Iteration**: Fixes any issues found during testing
6. **Completion**: Commits working solution to git

**Output**:
- Complete working implementation
- Comprehensive test suite
- Git commit with descriptive message
- Documentation updates (if applicable)

### `/orchestrate` - Guided AgentOS Workflow

**Syntax**: `/orchestrate "complex project description"`

**Description**: Applies the full AgentOS methodology with human oversight at each phase. Provides more control than `/yolo` while maintaining systematic approach.

**Parameters**:
- `description` (required): Detailed description of the complex task or project

**Examples**:
```bash
# Build a complete web application
/orchestrate "create React dashboard with authentication, user management, and analytics"

# Design and implement a microservice
/orchestrate "build order processing microservice with event sourcing and CQRS"

# Refactor existing system
/orchestrate "refactor monolithic application into microservices architecture"
```

**Phases**:
1. **Planning Phase** (15-30 minutes)
   - Requirements analysis
   - Architecture design
   - Technology decisions
   - Implementation roadmap

2. **Implementation Phase** (varies by complexity)
   - Systematic code generation
   - Test-driven development
   - Continuous integration
   - Quality assurance

3. **Review Phase** (10-20 minutes)
   - Code review and optimization
   - Integration testing
   - Documentation validation
   - Final quality check

**Interaction Points**:
- Approval required between phases
- Ability to modify approach based on feedback
- Real-time progress monitoring

## Development Commands

### `/spec` - Create Specification

**Syntax**: `/spec "requirements description"`

**Description**: Creates a detailed AgentOS specification document for the given requirements.

**Parameters**:
- `requirements` (required): Description of what needs to be specified

**Examples**:
```bash
/spec "user profile management with avatar uploads and permissions"
/spec "real-time chat system with WebSocket connections"
/spec "payment processing integration with Stripe"
```

**Output**:
- Detailed specification document in `.agent-os/specs/`
- Technical requirements and constraints
- Implementation approach
- Acceptance criteria
- Testing requirements

### `/implement` - Code Implementation

**Syntax**: `/implement [specification_path]`

**Description**: Generates code based on the current or specified AgentOS specification.

**Parameters**:
- `specification_path` (optional): Path to specific specification file

**Examples**:
```bash
# Implement current active specification
/implement

# Implement specific specification
/implement ".agent-os/specs/2025-01-29-user-auth/spec.md"
```

**Features**:
- Context-aware implementation
- Best practice application
- Project convention adherence
- Automatic dependency management

### `/test-and-fix` - Automated Testing

**Syntax**: `/test-and-fix [test_scope]`

**Description**: Runs comprehensive tests and automatically fixes any issues found.

**Parameters**:
- `test_scope` (optional): Specific scope to test (unit, integration, e2e, all)

**Examples**:
```bash
# Run all tests and fix issues
/test-and-fix

# Run only unit tests
/test-and-fix unit

# Run integration tests
/test-and-fix integration
```

**Process**:
1. Identifies appropriate test framework
2. Runs existing tests or generates new ones
3. Analyzes test failures
4. Implements fixes
5. Re-runs tests until all pass
6. Commits fixes if successful

## Context & Memory Management

### `/save-session` - Save Context

**Syntax**: `/save-session "description"`

**Description**: Saves the current conversation context and creates a git commit with the current state.

**Parameters**:
- `description` (required): Description of the current milestone or session

**Examples**:
```bash
/save-session "completed user authentication module"
/save-session "milestone: database schema and migrations ready"
/save-session "finished API endpoints for user management"
```

**Actions**:
- Exports current conversation to `claude_context.md`
- Creates git commit with all changes
- Tags commit with session description
- Updates project state tracking

### `/switch-model` - Change AI Model

**Syntax**: `/switch-model "model_name"`

**Description**: Switches to a different AI model while preserving full conversation context.

**Parameters**:
- `model_name` (required): Name of the target model

**Supported Models**:
- `gpt-4-turbo`
- `gpt-4`
- `claude-3-opus`
- `claude-3-sonnet`
- `gemini-pro`
- `qwen-coder`
- `deepseek-chat`

**Examples**:
```bash
# Switch to GPT-4 Turbo for complex reasoning
/switch-model "gpt-4-turbo"

# Switch to specialized coding model
/switch-model "qwen-coder"

# Switch to Claude Opus for creative tasks
/switch-model "claude-3-opus"
```

### `/memory-save` - Store Information

**Syntax**: `/memory-save "information"`

**Description**: Stores important information in persistent memory for later retrieval.

**Parameters**:
- `information` (required): Information to store

**Examples**:
```bash
/memory-save "project uses React 18 with TypeScript and Tailwind CSS"
/memory-save "authentication system uses bcrypt with 12 salt rounds"
/memory-save "database connection uses connection pooling with max 20 connections"
```

### `/memory-recall` - Retrieve Information

**Syntax**: `/memory-recall "query"`

**Description**: Retrieves relevant information from persistent memory based on the query.

**Parameters**:
- `query` (required): Search query for information retrieval

**Examples**:
```bash
/memory-recall "authentication implementation"
/memory-recall "database configuration"
/memory-recall "React components structure"
```

## Utility Commands

### `/agent-os-update` - Update AgentOS

**Syntax**: `/agent-os-update [component]`

**Description**: Syncs with the latest AgentOS methodology updates and templates.

**Parameters**:
- `component` (optional): Specific component to update (templates, instructions, patterns)

**Examples**:
```bash
# Update everything
/agent-os-update

# Update only templates
/agent-os-update templates

# Update instructions
/agent-os-update instructions
```

### `/git-smart` - Intelligent Git Operations

**Syntax**: `/git-smart <operation> [options]`

**Description**: Performs intelligent git operations with context awareness.

**Operations**:
- `commit`: Create contextual commit message
- `branch`: Create and switch to feature branch
- `merge`: Merge with conflict resolution
- `status`: Enhanced status with insights

**Examples**:
```bash
# Smart commit with generated message
/git-smart commit

# Create feature branch
/git-smart branch "user-authentication"

# Enhanced status
/git-smart status
```

### `/web-test` - Web Application Testing

**Syntax**: `/web-test <url> [test_type]`

**Description**: Performs automated testing of web applications.

**Parameters**:
- `url` (required): URL to test
- `test_type` (optional): Type of testing (functionality, accessibility, performance, all)

**Examples**:
```bash
# Complete web application testing
/web-test "http://localhost:3000"

# Accessibility testing only
/web-test "http://localhost:3000" accessibility

# Performance testing
/web-test "http://localhost:3000" performance
```

## Advanced Commands

### `/pattern-apply` - Apply Design Patterns

**Syntax**: `/pattern-apply "pattern_name" [context]`

**Description**: Applies established design patterns to current code or specifications.

**Parameters**:
- `pattern_name` (required): Name of the design pattern
- `context` (optional): Specific context or component to apply pattern to

**Examples**:
```bash
/pattern-apply "repository-pattern" "user data access"
/pattern-apply "factory-pattern" "payment processing"
/pattern-apply "observer-pattern" "event handling"
```

### `/analyze-complexity` - Complexity Analysis

**Syntax**: `/analyze-complexity [scope]`

**Description**: Analyzes code complexity and provides recommendations for improvements.

**Parameters**:
- `scope` (optional): Specific files or directories to analyze

**Examples**:
```bash
# Analyze entire project
/analyze-complexity

# Analyze specific directory
/analyze-complexity "src/components"

# Analyze specific file
/analyze-complexity "src/auth/login.ts"
```

### `/security-audit` - Security Analysis

**Syntax**: `/security-audit [scope]`

**Description**: Performs security analysis and identifies potential vulnerabilities.

**Parameters**:
- `scope` (optional): Specific scope for security audit

**Examples**:
```bash
# Full security audit
/security-audit

# Audit authentication components
/security-audit "auth"

# Audit API endpoints
/security-audit "api"
```

## Command Syntax

### General Syntax Rules

1. **Command Format**: All commands start with `/` followed by the command name
2. **Parameters**: Parameters can be required or optional
3. **Quoting**: Use quotes around multi-word parameters
4. **Flags**: Optional flags use `--flag` or `-f` format

### Parameter Types

- **String**: Text parameters (quoted if multiple words)
- **Path**: File or directory paths (relative or absolute)
- **URL**: Web URLs (http:// or https://)
- **Enum**: Predefined values from a list
- **Boolean**: true/false values

### Examples of Proper Syntax

```bash
# Correct
/yolo "build user authentication system"
/spec "user profile management"
/memory-save "important configuration details"

# Incorrect
/yolo build user authentication system  # Missing quotes
/spec                                   # Missing required parameter
/memory-save                           # Missing required parameter
```

## Error Handling

### Common Errors

#### Syntax Errors
```bash
# Error: Missing required parameter
/yolo
# Solution: Provide description
/yolo "build authentication system"

# Error: Invalid command
/invalid-command
# Solution: Use valid command name
/yolo "build authentication system"
```

#### Context Errors
```bash
# Error: No active specification
/implement
# Solution: Create specification first
/spec "user management system"
/implement
```

#### Permission Errors
```bash
# Error: Git permission denied
/git-smart commit
# Solution: Configure git credentials
git config user.name "Your Name"
git config user.email "your@email.com"
```

### Error Recovery

When commands fail, K83 provides:
1. **Clear Error Messages**: Descriptive error messages with context
2. **Suggested Solutions**: Actionable steps to resolve the issue
3. **Automatic Retry**: Some commands automatically retry with corrections
4. **Rollback Support**: Ability to undo changes when possible

## Configuration

### Global Configuration

Configuration is stored in `.k83/config.yaml`:

```yaml
# Default model preferences
models:
  default: "claude-3-sonnet"
  coding: "qwen-coder"
  analysis: "gpt-4-turbo"

# Memory settings
memory:
  max_entries: 1000
  retention_days: 30

# Git settings
git:
  auto_commit: true
  commit_prefix: "feat(k83):"
  
# Testing preferences
testing:
  framework: "pytest"
  coverage_threshold: 80
```

### Project-Specific Configuration

Project settings in `.k83/project.yaml`:

```yaml
# Project type affects command behavior
project_type: "web_application"

# Language-specific settings
language: "python"
framework: "fastapi"

# Custom patterns and templates
patterns:
  - "custom-auth-pattern"
  - "api-response-pattern"

# Deployment settings
deployment:
  platform: "docker"
  environment: "development"
```

### Environment Variables

Key environment variables:

```bash
# API Keys
export OPENROUTER_API_KEY="your_api_key"
export GITHUB_TOKEN="your_github_token"

# K83 Configuration
export K83_LOG_LEVEL="INFO"
export K83_AUTO_UPDATE="true"
export K83_DEFAULT_MODEL="claude-3-sonnet"
```

## Best Practices

### Command Usage

1. **Be Specific**: Provide clear, detailed descriptions
2. **Use Context**: Build on previous commands and context
3. **Save Progress**: Use `/save-session` at logical milestones
4. **Test Regularly**: Use `/test-and-fix` during development

### Memory Management

1. **Save Important Info**: Use `/memory-save` for key decisions and configurations
2. **Regular Cleanup**: Periodically review and clean up stored memories
3. **Descriptive Storage**: Store information with clear, searchable descriptions

### Model Selection

1. **Task-Appropriate Models**: Choose models based on task requirements
2. **Context Preservation**: Use `/switch-model` to maintain conversation context
3. **Performance Consideration**: Balance capability with response time

---

## Troubleshooting

For common issues and solutions, see the [Troubleshooting Guide](../troubleshooting.md).

For additional help:
- [GitHub Discussions](https://github.com/your-repo/k83/discussions)
- [Issue Tracker](https://github.com/your-repo/k83/issues)
- [Community Discord](https://discord.gg/k83-framework)

---

*K83 Slash Commands API - Powering Agentic Development Workflows*