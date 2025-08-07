# K83 Framework - Universal AgentOS + Agentic Coding

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Documentation Status](https://img.shields.io/badge/docs-complete-brightgreen.svg)](./docs/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![AgentOS Compatible](https://img.shields.io/badge/AgentOS-compatible-purple.svg)](https://buildermethods.com/agent-os)

**K83** is a revolutionary framework that brings AgentOS methodology + agentic workflows + context preservation directly into Claude Code via slash commands. No external tools required - everything works seamlessly within Claude Code itself.

**One command installs everything. Slash commands do everything else.**

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture Overview](#architecture-overview)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [Security](#security)
- [Support](#support)

## Features

### 🎯 Agentic Workflows
- **Autonomous Coding**: `/yolo` mode for autonomous coding until completion
- **Intelligent Orchestration**: `/orchestrate` applies full AgentOS methodology
- **Context-Aware Execution**: Maintains state across complex multi-step operations

### 📋 AgentOS Integration
- **Full Methodology Support**: Complete buildermethods/agent-os implementation
- **Spec-Driven Development**: Automatic specification creation and management
- **Three-Phase Execution**: Planning → Implementation → Review cycles

### 🧠 Persistent Memory & Context
- **Cross-Session Persistence**: Context preserved across sessions and model switches
- **Multi-Tool Compatibility**: Seamless transitions between Claude Code, Cursor, and CCR
- **Smart State Management**: Automatic detection and export of conversation history

### 🔧 25 Essential MCP Servers
- **GitHub Integration**: Direct repository operations and PR management
- **FileSystem Operations**: Advanced file and directory manipulation
- **Memory Bank**: Persistent knowledge storage and retrieval
- **Sequential Thinking**: Step-by-step reasoning and planning
- **Database Operations**: SQL operations and schema management
- **Web Testing**: Automated web application testing
- **And 19 more specialized servers**

### ⚡ Zero Configuration
- **One-Command Install**: Single curl command installs everything
- **Auto-Configuration**: Detects project type and applies appropriate settings
- **Auto-Updates**: Stays synced with latest AgentOS changes

## Quick Start

### Install K83 (30 seconds)

**Install in any Git project:**
```bash
curl -sSL https://raw.githubusercontent.com/your-repo/k83/main/install-k83.sh | bash
```

### Start Using Immediately

**In Claude Code:**
```bash
# Autonomous feature development
/yolo "build user authentication system with JWT and middleware"

# Complex project orchestration
/orchestrate "create REST API with PostgreSQL and admin dashboard"

# Step-by-step development
/spec "user profile management with avatar uploads"
/implement
/test-and-fix

# Context and memory management
/save-session "milestone completed"
/memory-save "authentication system uses bcrypt with 12 rounds"
```

**That's it. Everything else is automatic.**

## Architecture Overview

K83 integrates multiple systems into a cohesive development environment:

```
┌─────────────────────────────────────────────────────────────┐
│                    K83 Framework                            │
├─────────────────────────────────────────────────────────────┤
│  Claude Code Interface (Slash Commands)                    │
├─────────────────────────────────────────────────────────────┤
│                 AgentOS Foundation                          │
│  • Methodology Engine    • Spec Management                 │
│  • Pattern Recognition  • Task Breakdown                   │
├─────────────────────────────────────────────────────────────┤
│               25 MCP Servers (Specialized Agents)          │
│  GitHub | FileSystem | Memory | Database | Web | ...       │
├─────────────────────────────────────────────────────────────┤
│              Context & State Management                     │
│  • Cross-session persistence  • Multi-tool compatibility   │
│  • Intelligent state sync     • Model switching            │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

- **AgentOS Foundation**: buildermethods/agent-os methodology and templates
- **Claude Code MCP Server**: Slash command interface and orchestration
- **Sub-Agent System**: Specialized agents for spec, code, test, review tasks
- **25 Essential MCP Servers**: GitHub, FileSystem, Memory, Sequential Thinking, Database, Web, and more
- **Context Manager**: Persistent memory and session state across model switches
- **Auto-Sync System**: Stays updated with latest AgentOS changes

## Installation

### Prerequisites

Before installing K83, ensure you have:

1. **Python 3.8+**: Core K83 scripts are written in Python
2. **Git**: For automated version control and repository operations
3. **Node.js 18+**: Required for some MCP servers
4. **Claude Code**: The primary interface for K83 workflows

### Automatic Installation

The installer automatically handles all setup:

```bash
# Install in any Git project
curl -sSL https://raw.githubusercontent.com/your-repo/k83/main/install-k83.sh | bash
```

### What Gets Installed

The installer automatically:
- ✅ Creates `.k83/` directory with all components
- ✅ Downloads and configures 25 MCP servers
- ✅ Syncs latest AgentOS instructions and templates
- ✅ Configures Claude Code integration (`.claude/mcp_config.json`)
- ✅ Sets up persistent memory and context management
- ✅ Detects project type and applies appropriate configurations
- ✅ Creates comprehensive documentation and examples

### Manual Installation

For advanced users or custom installations:

```bash
# Clone the repository
git clone https://github.com/your-repo/k83.git
cd k83

# Run the setup script
./scripts/setup.sh

# Configure your project
./scripts/configure-project.sh /path/to/your/project
```

### Verification

Verify your installation:

```bash
# Check K83 status
python3 ralex-integration-package/agent_os_bridge.py --version

# Test slash commands in Claude Code
/yolo "create a simple hello world function"
```

## Usage

### Available Slash Commands

#### 🎯 Agentic Workflows

**`/yolo "build feature X"`**
- Autonomous coding until completion
- Applies full AgentOS methodology automatically
- Handles spec creation, implementation, testing, and fixes
- Example: `/yolo "implement JWT authentication with login/logout endpoints and middleware"`

**`/orchestrate "complex task"`**
- Full AgentOS methodology workflow with human oversight
- Three-phase execution: Planning → Implementation → Review
- Example: `/orchestrate "build REST API with PostgreSQL, authentication, and admin dashboard"`

#### 📋 Development Commands

**`/spec "requirements"`**
- Create detailed AgentOS specification
- Generates comprehensive technical requirements
- Example: `/spec "user profile management with avatar uploads and permissions"`

**`/implement`**
- Generate code from current specification
- Uses context-aware implementation patterns
- Automatically applies best practices and project conventions

**`/test-and-fix`**
- Run comprehensive test suite
- Auto-fix issues found during testing
- Iterates until all tests pass

#### 🧠 Context & Memory

**`/save-session "note"`**
- Save current context and create git commit
- Preserves conversation state for later retrieval
- Example: `/save-session "completed user authentication module"`

**`/switch-model gpt-4`**
- Change AI models while preserving context
- Seamlessly continue work with different model capabilities
- Example: `/switch-model "gpt-4-turbo"`

**`/memory-save "information"`**
- Store important information in persistent memory
- Retrievable across sessions and projects
- Example: `/memory-save "project uses React 18 with TypeScript and Tailwind"`

**`/memory-recall "query"`**
- Retrieve information from persistent memory
- Smart search across all stored knowledge
- Example: `/memory-recall "authentication implementation details"`

#### 🔧 Utilities

**`/agent-os-update`**
- Sync with latest AgentOS methodology updates
- Downloads new templates and best practices
- Maintains compatibility with AgentOS ecosystem

**`/git-smart commit`**
- Intelligent git operations with context awareness
- Generates meaningful commit messages
- Example: `/git-smart commit "add user authentication system"`

**`/web-test url`**
- Automated web application testing
- Comprehensive functionality and accessibility testing
- Example: `/web-test "http://localhost:3000"`

### Example Workflows

#### Autonomous Feature Development

```bash
# Single command builds complete feature
/yolo "implement JWT authentication with login/logout endpoints and middleware"

# K83 automatically:
# 1. Creates AgentOS specification
# 2. Implements code with proper structure
# 3. Writes comprehensive tests
# 4. Fixes any issues found
# 5. Commits working solution to git
```

#### Complex Project Orchestration

```bash
# Full AgentOS methodology applied
/orchestrate "build REST API with PostgreSQL, authentication, and admin dashboard"

# Uses AgentOS phases:
# - Planning & Architecture (15-30 minutes)
# - Implementation & Testing (varies by complexity)
# - Review & Integration (10-20 minutes)
```

#### Iterative Development with Context Preservation

```bash
# Step by step with full state management
/spec "user profile management with avatar uploads"
/implement
/test-and-fix
/memory-save "user profiles completed with file uploads using multer"
/save-session "milestone: user management system completed"

# Switch to different model while preserving context
/switch-model "gpt-4-turbo"
/yolo "add OAuth integration to existing auth system"
```

#### Cross-Tool Development

```bash
# Work in Claude Code
/yolo "build user authentication"
/save-session "auth system completed"

# Switch to terminal
k83-save    # Exports context and commits to git
k83-resume  # Launches CCR with next model and full context

# Continue in CCR with different model
/flash      # Save progress and sync back to git
exit

# Return to Claude Code with updated context
/agent-os-update  # Sync latest changes
```

## API Reference

For detailed API documentation, see:
- [Slash Commands API](./docs/api/slash-commands.md)
- [Python API Reference](./docs/api/python-api.md)
- [MCP Servers API](./docs/api/mcp-servers.md)

## Examples

Explore real-world usage scenarios:
- [Getting Started Examples](./examples/getting-started/)
- [Web Development](./examples/web-development/)
- [API Development](./examples/api-development/)
- [Database Operations](./examples/database/)
- [Testing Workflows](./examples/testing/)

## Contributing

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and setup for development
git clone https://github.com/your-repo/k83.git
cd k83
./scripts/dev-setup.sh

# Run tests
./scripts/test.sh

# Submit changes
./scripts/pre-commit.sh
```

## Security

Security is a top priority for K83. Please see our [Security Policy](./SECURITY.md) for:
- Reporting vulnerabilities
- Security best practices
- Authentication and authorization
- Data protection guidelines

## Support

### Documentation
- [Complete Documentation](./docs/)
- [Troubleshooting Guide](./docs/troubleshooting.md)
- [FAQ](./docs/faq.md)

### Community
- [GitHub Discussions](https://github.com/your-repo/k83/discussions)
- [Issue Tracker](https://github.com/your-repo/k83/issues)
- [AgentOS Community](https://buildermethods.com/agent-os)

### Commercial Support
For enterprise support and custom implementations, contact us at support@k83framework.com

## License

K83 is released under the [MIT License](./LICENSE). See LICENSE file for details.

## Acknowledgments

- Built on [buildermethods/agent-os](https://buildermethods.com/agent-os) methodology
- Powered by Claude Code and MCP (Model Context Protocol)
- Inspired by the agentic AI development community

---

**Ready to revolutionize your development workflow?**

```bash
curl -sSL https://raw.githubusercontent.com/your-repo/k83/main/install-k83.sh | bash
```

*K83 Framework - Where AgentOS meets Agentic AI Development*