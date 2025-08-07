# K83 Framework Technical Stack

> Last Updated: 2025-08-07
> Version: 1.0.0

## Core Framework

- **Language:** Python 3.8+
- **Architecture:** MCP Server + Agent OS Integration
- **Integration:** Claude Code native via slash commands
- **Package Manager:** pip (minimal dependencies)

## MCP Server Integration

### Essential MCP Servers (6 Core)
- **GitHub MCP** - Repository operations and automation
- **FileSystem MCP** - File and directory operations
- **Memory Bank MCP** - Persistent memory and context storage
- **Sequential Thinking MCP** - Structured reasoning and planning
- **Database MCP** - Database operations and schema management
- **Web Testing MCP** - Automated web application testing

### MCP Orchestration
- **MCP Manager** - Coordinates multiple MCP servers
- **Context Router** - Routes requests to appropriate MCP servers
- **State Synchronization** - Ensures consistency across MCP servers

## Agent OS Integration

### Core Agent OS Components
- **buildermethods/agent-os** - Base methodology and templates
- **Spec Templates** - Feature specification patterns
- **Implementation Patterns** - Code structure and quality standards
- **Testing Framework** - Agent OS testing methodology

### Auto-Sync System
- **Template Updates** - Automatic sync with latest Agent OS changes
- **Methodology Evolution** - Stays current with Agent OS improvements
- **Custom Extensions** - K83-specific Agent OS enhancements

## Context Management

### Persistent Storage
- **SQLite Database** - Local storage for session state and memory
- **File-based Context** - Markdown files for human-readable context
- **Git Integration** - Version control for context and project state

### Context Preservation
- **Session Serialization** - Complete conversation state capture
- **Model State Transfer** - Context maintained across model switches
- **Memory Persistence** - Long-term memory across multiple sessions

## Claude Code Integration

### Slash Command Interface
- **Command Parser** - Processes slash commands and arguments
- **MCP Router** - Routes commands to appropriate MCP servers
- **Response Formatter** - Formats responses for Claude Code display

### Native Integration
- **`.claude/mcp_config.json`** - Claude Code MCP server configuration
- **Auto-Discovery** - Automatic detection and registration of K83 MCP server
- **Seamless UX** - All functionality accessible without external commands

## Development Tools

### Code Quality
- **Python Black** - Code formatting
- **pylint** - Code analysis and linting
- **pytest** - Unit testing framework
- **mypy** - Static type checking

### CI/CD Integration
- **GitHub Actions** - Automated testing and deployment
- **Pre-commit Hooks** - Code quality enforcement
- **Semantic Versioning** - Automated version management

## External Dependencies

### AI/LLM Integration
- **OpenRouter** - Multi-model LLM access
- **Claude Code Router (CCR)** - Multi-model development environment
- **Model APIs** - Direct integration with various LLM providers

### Development Dependencies
- **Git** - Version control (required)
- **curl** - Installation script delivery
- **bash/zsh** - Shell script execution

## Deployment Architecture

### Installation Method
- **Single curl Command** - Complete setup in one step
- **Auto-Detection** - Detects project type and configures appropriately
- **Zero Configuration** - Works immediately after installation

### Update Mechanism
- **Auto-Update System** - Automatic updates to Agent OS and MCP servers
- **Version Management** - Maintains compatibility across updates
- **Rollback Capability** - Can revert to previous working versions

## Security Considerations

### API Key Management
- **Environment Variables** - Secure storage in `.env` files
- **Git Ignore** - Automatic exclusion of sensitive files
- **Key Rotation** - Support for API key updates

### Code Execution
- **Sandboxed Execution** - Safe code execution within controlled environment
- **Permission Model** - Granular permissions for different operations
- **Audit Trail** - Logging of all system operations

This technical stack enables K83 to provide a seamless, powerful, and secure AI development experience while maintaining the flexibility and extensibility needed for diverse development workflows.