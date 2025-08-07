# Contributing to K83 Framework

Thank you for your interest in contributing to the K83 Framework! This project aims to revolutionize AI-assisted development by combining AgentOS methodology, intelligent MCP orchestration, and agentic workflows.

## Quick Start for Contributors

1. **Fork and clone the repository**
2. **Install K83 in development mode:**
   ```bash
   git clone <your-fork>
   cd k83-framework
   ./install-k83.sh
   ```
3. **Test your changes** with real Claude Code integration
4. **Submit a pull request** with clear description

## Project Architecture

### Core Components
- **AgentOS Integration** - Structured development methodology
- **MCP Orchestration** - 25+ premium MCP servers with intelligent routing
- **Agentic Workflows** - Autonomous `/yolo` and `/orchestrate` modes
- **Context Management** - Session preservation across tools/models
- **Claude Code Integration** - Universal slash command interface

### Key Files
```
k83-framework/
├── install-k83.sh              # Main installer with all MCP servers
├── .agent-os/                  # AgentOS integration structure
├── ralex-integration-package/   # Core Python modules
└── examples/                   # Usage examples and templates
```

## Development Guidelines

### Code Standards
- **Python**: Follow PEP 8, include type hints
- **Shell Scripts**: Use `set -e`, proper error handling
- **Documentation**: Update README.md for any new features
- **Testing**: Include examples for new slash commands

### MCP Server Integration
When adding new MCP servers:
1. **Verify server exists** and is publicly available
2. **Test installation** in clean environment
3. **Add to orchestration logic** in K83MCPServer
4. **Update documentation** with new capabilities

### Agentic Workflow Design
New autonomous workflows should:
- Use AgentOS three-phase methodology (Plan → Implement → Review)
- Include error handling and recovery
- Integrate with context preservation system
- Provide clear success/failure indicators

## Types of Contributions

### 🐛 Bug Reports
- Use GitHub Issues with bug report template
- Include steps to reproduce
- Mention your OS and Claude Code version

### ✨ Feature Requests
- Describe the use case and value
- Consider how it fits with AgentOS methodology
- Propose integration approach

### 🔧 Code Contributions
- Start with small, focused changes
- Include tests and documentation updates
- Follow existing code patterns

### 📚 Documentation
- Fix typos, improve clarity
- Add usage examples
- Update command references

## MCP Server Contribution Guidelines

### Adding New MCP Servers
1. **Research**: Verify the MCP server is stable and well-maintained
2. **Test**: Ensure it works with Claude Code/Desktop
3. **Integration**: Add to `install-k83.sh` with proper error handling
4. **Orchestration**: Add intelligence routing logic to `K83MCPServer`
5. **Documentation**: Update command reference and examples

### MCP Server Categories
- **Core Framework**: Essential for basic functionality
- **Development Tools**: Code analysis, IDE integration
- **Enterprise Features**: DevOps, security, monitoring
- **Specialized**: AI/ML, data processing, automation

## Testing Your Contributions

### Manual Testing
```bash
# Test installation from scratch
rm -rf .k83 .claude
./install-k83.sh

# Test core slash commands in Claude Code
/yolo "simple test task"
/mcp-status
/orchestrate "basic workflow"
```

### Integration Testing
- Test AgentOS workflow integration
- Verify MCP orchestration logic
- Check context preservation across sessions
- Validate error handling and recovery

## Pull Request Process

1. **Create focused commits** with clear messages
2. **Update documentation** for any changes
3. **Test thoroughly** in real environment
4. **Describe changes** clearly in PR description
5. **Link to related issues** if applicable

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Documentation update
- [ ] MCP server addition

## Testing
- [ ] Tested installation process
- [ ] Verified slash commands work
- [ ] Checked AgentOS integration
- [ ] Validated MCP orchestration

## Checklist
- [ ] Code follows project standards
- [ ] Documentation is updated
- [ ] Changes are backwards compatible
- [ ] No breaking changes to existing workflows
```

## Community Guidelines

### Be Respectful
- Welcome newcomers and different perspectives
- Provide constructive feedback
- Focus on the code, not the person

### Be Collaborative  
- Share knowledge and help others learn
- Explain complex concepts clearly
- Credit others' contributions

### Be Professional
- Use clear, professional language
- Respect maintainer decisions
- Follow the Code of Conduct

## Getting Help

### Documentation
- Read the full [README.md](README.md)
- Check [AgentOS integration guide](.agent-os/README.md)
- Review [examples](examples/) directory

### Community Support
- GitHub Issues for bugs and feature requests
- GitHub Discussions for general questions
- Discord community (link in README)

### Maintainer Contact
- Create GitHub issues for specific problems
- Tag `@maintainers` for urgent issues
- Email for security concerns only

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special recognition for major features

## License

By contributing to K83 Framework, you agree that your contributions will be licensed under the same license as the project.

---

**Ready to contribute?** Start with a small documentation fix or bug report to get familiar with the process, then work your way up to larger features!

The K83 Framework is built by the community, for the community. Every contribution makes AI-assisted development better for everyone. 🚀