# Ralex V2 Daily Usage Guide

**Practical examples for cost-optimized AI coding with AgentOS.**

## 🚀 **Basic Usage**

### **Command Line (Quick Tasks)**
```bash
# Simple fixes (cheap models ~$0.001)
./ralex-agentos-v2.sh "fix this typo in the function name"
./ralex-agentos-v2.sh "add error handling to this function"
./ralex-agentos-v2.sh "format this code to PEP 8 standards"

# Complex tasks (smart analysis + cheap execution ~$0.015 + $0.003)
./ralex-agentos-v2.sh "refactor the user authentication system"
./ralex-agentos-v2.sh "implement a REST API for user management"
./ralex-agentos-v2.sh "optimize database queries for performance"
```

### **Interactive Mode (Recommended for Development)**
```bash
# Start interactive mode
./ralex-agentos-v2.sh

# Add files to context
> /add myfile.py
> /add tests/test_myfile.py

# Use AgentOS commands
> /help                           # Show all available commands
> /breakdown "refactor auth"      # Preview task breakdown and cost
> /review myfile.py               # Code review with AgentOS standards
> /standards                      # Show current coding standards

# Natural language requests (with AgentOS optimization)
> refactor the authentication system to use JWT tokens
> create comprehensive unit tests for the user model
> optimize the database connection handling
```

---

## 💡 **Smart Cost Optimization Examples**

### **How AgentOS Optimizes Your Costs**

#### **Simple Task Example:**
```bash
./ralex-agentos-v2.sh "fix the typo in line 23"

# AgentOS Output:
# 🧠 Analysis: Complexity: low, Cost: $0.001
# Strategy: Direct execution (cheap model)
# ✅ Fixed immediately with Gemini Flash
```

#### **Complex Task Example:**
```bash
./ralex-agentos-v2.sh "refactor authentication system for JWT tokens"

# AgentOS Output:
# 🧠 Analysis: Complexity: high, Cost: $0.015 + $0.006
# Strategy: Analysis first (smart model), then execution (cheap models)
# 
# Phase 1: Analysis (Claude Sonnet - $0.015)
# ✅ Identified 4 specific tasks:
#    1. Create JWT token service
#    2. Update user model for token storage
#    3. Modify login endpoint
#    4. Add token validation middleware
#
# Phase 2: Execution (Gemini Flash - $0.001-0.002 each)
# Type 'next' to execute each task with cheap models
```

---

## 🎯 **Daily Workflow Patterns**

### **Morning Development Session**
```bash
# 1. Start interactive mode
./ralex-agentos-v2.sh

# 2. Add today's work files
> /add src/user_model.py
> /add src/auth_service.py
> /add tests/test_auth.py

# 3. Review yesterday's work
> /review src/auth_service.py

# 4. Plan today's features  
> /breakdown "implement password reset functionality"

# 5. Execute planned work
> implement secure password reset with email verification
> next  # Execute first task
> next  # Execute second task (continue until done)
```

### **Bug Fixing Workflow**
```bash
# Quick fixes (use cheap models)
./ralex-agentos-v2.sh "fix the NoneType error in user login"
./ralex-agentos-v2.sh "handle edge case when email is empty"

# Complex debugging (smart analysis)
./ralex-agentos-v2.sh "analyze and fix performance issues in user search"
# → AgentOS: Analysis finds 3 optimization areas
# → Execute each optimization with cheap models
```

### **Feature Development Workflow**
```bash
# Complex feature (smart breakdown)
./ralex-agentos-v2.sh "build complete user profile management system"

# AgentOS breaks it down:
# 1. Design database schema for profiles
# 2. Create profile model and API endpoints  
# 3. Implement profile update forms
# 4. Add profile image upload
# 5. Create profile permissions system
# 6. Write comprehensive tests

# Execute each task for $0.001-0.002 each instead of $0.15 for everything
```

---

## 🔧 **AgentOS Slash Commands Reference**

### **Essential Commands**
| Command | Usage | Purpose |
|---------|-------|---------|
| `/help` | `/help` | Show all available commands |
| `/add` | `/add file.py` | Add file to context |
| `/review` | `/review file.py` | Code review with standards |
| `/breakdown` | `/breakdown "task"` | Preview cost optimization |
| `/standards` | `/standards` | Show AgentOS coding standards |

### **Advanced Commands**
| Command | Usage | Purpose |
|---------|-------|---------|
| `/instructions` | `/instructions` | Show project instructions |
| `/reload` | `/reload` | Reload AgentOS data from disk |
| `/exit` | `/exit` | Exit interactive mode |

### **Command Examples**
```bash
# Interactive mode commands
> /breakdown "implement user authentication"
## Task Breakdown Preview
**Task**: implement user authentication
**Complexity**: high (confidence: 0.95)
**Strategy**: Analysis first (smart model), then execution (cheap models)
**Process**:
1. 💰 Analysis Phase (smart model): Break down requirements
2. 💸 Execution Phase (cheap models): Execute each specific task
**Expected Tasks**: 3-7 specific implementation tasks

> /review src/auth.py  
## Code Review Results
**Standards Compliance**: ✅ PEP 8, ❌ Missing type hints
**Issues Found**: 2 functions need docstrings
**Recommendations**: Add type hints, improve error handling
```

---

## 📊 **Cost Management**

### **Daily Budget Tracking**
```bash
# Check remaining budget anytime
python3 health_check.py

# Sample output:
# 💰 Budget Status: $3.24 remaining of $5.00 daily limit
# 📊 Today's usage: 15 requests, avg $0.12 per request
# 🕐 Budget resets at: midnight UTC
```

### **Cost-Conscious Usage Tips**

#### **Maximize Savings:**
1. **Use descriptive language** - helps AgentOS route correctly
   ```bash
   # Good: "fix authentication bug" → cheap model
   # Good: "refactor entire auth system" → smart analysis
   ```

2. **Batch simple tasks** together
   ```bash
   ./ralex-agentos-v2.sh "fix typos in auth.py and add missing comments"
   ```

3. **Use /breakdown** before expensive tasks
   ```bash
   > /breakdown "redesign user interface"
   # See cost estimate before committing
   ```

#### **When to Use Each Mode:**
- **Direct command**: Quick, single-file changes
- **Interactive mode**: Multi-file development sessions  
- **/breakdown**: Preview costs for expensive features

---

## 🎯 **Best Practices**

### **File Context Management**
```bash
# Interactive mode - add relevant files only
> /add src/main.py          # Core file being modified
> /add tests/test_main.py    # Related tests
> /add requirements.txt     # If adding dependencies

# Avoid adding too many files (increases cost)
# Remove files when done: restart interactive mode
```

### **Effective Prompting**
```bash
# ✅ Good prompts (clear intent)
"refactor authentication to use JWT tokens with proper error handling"
"fix the database connection timeout issue in user service"
"implement user registration with email verification"

# ❌ Avoid vague prompts
"make this better"
"fix everything"
"improve performance"
```

### **Standards Integration**
Your AgentOS standards are automatically applied:
- **Python standards**: Type hints, PEP 8, docstrings, f-strings
- **Git workflow**: Atomic commits, descriptive messages
- **Testing**: pytest, >80% coverage, descriptive test names

Customize standards by editing:
- `agent_os/standards/python.md`
- `agent_os/standards/git-workflow.md`
- `agent_os/instructions/testing.md`

---

## 🚨 **Troubleshooting Common Issues**

### **High Costs**
```bash
# Check if using complex prompts unnecessarily
> /breakdown "your expensive task"

# Use simpler language for simple tasks
# "fix typo" vs "comprehensively analyze and rectify typographical errors"
```

### **Wrong Model Selection**
```bash
# Check complexity analysis
> /breakdown "your task"

# Be more specific about task complexity
# "simple fix" vs "complex refactoring"
```

### **Budget Exceeded**
```bash
# Check daily usage
python3 health_check.py

# Budget resets daily at midnight UTC
# Or increase limit in config/settings.json
```

---

## ⚡ **Quick Reference**

### **Daily Commands**
```bash
# Most common usage patterns
./ralex-agentos-v2.sh "fix this bug"                    # Simple
./ralex-agentos-v2.sh "refactor user authentication"    # Complex
./ralex-agentos-v2.sh                                   # Interactive

# In interactive mode
> /add file.py && your request
> /breakdown "task" && confirm
> /review file.py && implement fixes
```

### **Cost Estimates**
- **Simple fixes**: $0.001-0.002
- **Medium features**: $0.015 analysis + $0.003-0.006 execution  
- **Complex features**: $0.015 analysis + $0.008-0.015 execution
- **Daily budget**: $5.00 (typically use $0.50-1.50/day)

**Ready to optimize your AI coding workflow! 🚀**