# Resume Project Workflow - Khamel83 Edition

## Overview
Efficiently resume work on an existing project with cost optimization and progress tracking.

## Quick Resume Checklist (5 minutes)

### Immediate Context Recovery
- [ ] **Last commit message** reviewed: `git log -1 --pretty=format:"%h %s"`
- [ ] **Current branch** confirmed: `git branch --show-current`
- [ ] **Uncommitted changes** checked: `git status`
- [ ] **Development server** status verified
- [ ] **Recent Agent OS activity** reviewed (if applicable)

### Task Status Check
- [ ] **Active spec folder** identified: `ls -la .agent-os/specs/ | head -5`
- [ ] **Current tasks.md** located and reviewed
- [ ] **Next uncompleted task** identified
- [ ] **Cost tracking** status reviewed

## Step 1: Context Reconstruction

### Project State Analysis
**Run these commands to understand current state:**
```bash
# Git context
git log --oneline -5
git status
git branch -a

# Agent OS context
ls -la .agent-os/specs/ 2>/dev/null | tail -5
find .agent-os -name "tasks.md" -exec ls -la {} \; 2>/dev/null

# Development context  
ls -la package.json Gemfile requirements.txt 2>/dev/null
ps aux | grep -E "(rails|node|python|npm|yarn)" | grep -v grep
```

### Last Session Recovery
**Check for session artifacts:**
- [ ] **IDE/Editor** with open files and tabs
- [ ] **Terminal history** for recent commands
- [ ] **Browser tabs** with relevant documentation/resources
- [ ] **Notes files** or scratch pads with context

### Pattern Cache Review
**Check recent patterns used:**
```bash
ls -la .khamel83/pattern-cache/ 2>/dev/null
cat .khamel83/recent-patterns.log 2>/dev/null | tail -10
```

## Step 2: Active Spec & Task Identification

### Find Current Spec
**Automatically identify the most recent spec:**
```bash
# Find most recent spec directory
RECENT_SPEC=$(ls -1t .agent-os/specs/ 2>/dev/null | head -1)
echo "Most recent spec: $RECENT_SPEC"

# Review spec status
if [ -d ".agent-os/specs/$RECENT_SPEC" ]; then
  echo "=== Spec Overview ==="
  head -20 ".agent-os/specs/$RECENT_SPEC/spec.md" 2>/dev/null
  echo "=== Current Tasks ==="
  cat ".agent-os/specs/$RECENT_SPEC/tasks.md" 2>/dev/null
fi
```

### Task Status Assessment
**Create task status summary:**

#### Current Spec: [SPEC_NAME]
**Date**: [SPEC_DATE]
**Status**: [In Progress/Review/Blocked]

#### Task Progress Summary
- **Total Tasks**: [COUNT]
- **Completed**: [COUNT] ✅
- **In Progress**: [COUNT] 🔄  
- **Pending**: [COUNT] ⏳
- **Blocked**: [COUNT] ❌

#### Next Task Identified
**Task**: [TASK_NUMBER] - [TASK_DESCRIPTION]
**Subtasks**:
- [ ] [SUBTASK_1]
- [ ] [SUBTASK_2] ← **RESUME HERE**
- [ ] [SUBTASK_3]

## Step 3: Environment Verification

### Development Environment Check
- [ ] **Dependencies** up to date (package.json, Gemfile, etc.)
- [ ] **Database** running and accessible
- [ ] **Environment variables** loaded
- [ ] **Development server** can start
- [ ] **Tests** can run (at least smoke test)

### Cost Optimization Tools Check
- [ ] **LiteLLM config** present and valid
- [ ] **Cost tracking** file accessible
- [ ] **Pattern cache** readable
- [ ] **Ralex integration** working (if used)

### Quick Environment Test
```bash
# Test basic project functionality
npm test --passWithNoTests 2>/dev/null || echo "No npm tests"
bundle exec rails test 2>/dev/null || echo "No Rails tests"
python -m pytest --version 2>/dev/null || echo "No Python tests"

# Test development server
timeout 10s npm start 2>/dev/null && echo "npm start works" || echo "npm start issues"
```

## Step 4: Progress Since Last Session

### Git History Analysis
**Understand what's been done:**
```bash
# Show commits since last week
git log --since="1 week ago" --oneline --author="$(git config user.name)"

# Show file changes since last session
git diff HEAD~3..HEAD --name-only | sort | uniq
```

### Cost Tracking Review
**Check cost optimization progress:**
```json
// Review .khamel83/cost-tracking.json
{
  "session_date": "[LAST_SESSION_DATE]",
  "tasks_completed_last_session": [COUNT],
  "cost_last_session": "$[AMOUNT]", 
  "savings_last_session": "[PERCENTAGE]%",
  "running_totals": {
    "total_cost": "$[AMOUNT]",
    "total_savings": "$[AMOUNT]",
    "savings_rate": "[PERCENTAGE]%"
  }
}
```

### Pattern Usage Review
**Check what patterns were used:**
- [ ] **Recent patterns** applied successfully
- [ ] **New patterns** discovered in last session
- [ ] **Pattern effectiveness** from last session
- [ ] **Patterns to reuse** in upcoming work

## Step 5: Immediate Next Steps Planning

### Task Resumption Strategy
**Based on current task analysis:**

#### If Task is Partially Complete:
1. **Review what was done**: Check git commits, code changes
2. **Identify completion point**: Where exactly did work stop?
3. **Estimate remaining work**: How much is left?
4. **Plan cost optimization**: Can remaining work use cheaper models?

#### If Starting New Task:
1. **Apply task breakdown**: Use `@templates/.khamel83/cost-optimization/task-breakdown.md`
2. **Check pattern cache**: Look for similar work done before
3. **Plan three-phase approach**: Planning → Implementation → Review
4. **Set cost targets**: Based on task complexity

### Immediate Action Plan
**Next 30 minutes:**
1. **[ACTION_1]**: [SPECIFIC_TASK]
2. **[ACTION_2]**: [SPECIFIC_TASK]  
3. **[ACTION_3]**: [SPECIFIC_TASK]

**Next 2 hours:**
- [ ] Complete current subtask
- [ ] Update task status in tasks.md
- [ ] Log cost tracking data
- [ ] Identify next logical stopping point

## Step 6: Productivity Optimization

### Focus Session Setup
- [ ] **Distractions minimized** (notifications off, etc.)
- [ ] **Timer set** for focused work session (25-50 minutes)
- [ ] **Clear stopping point** identified
- [ ] **Success criteria** defined for session

### Cost Optimization Reminder
**For current task:**
- **Planning phase needed?** ✅/❌
- **Implementation can use cheap model?** ✅/❌
- **Review/testing needed?** ✅/❌
- **Pattern matching opportunities?** ✅/❌

### Context Preservation for Next Session
**Before ending work:**
- [ ] **Commit progress** with descriptive message
- [ ] **Update tasks.md** with current status
- [ ] **Log cost data** in tracking file
- [ ] **Note stopping point** and next steps
- [ ] **Save IDE state** (tabs, layout, etc.)

## Step 7: Quick Quality Check

### Code Quality Maintenance
- [ ] **Tests still passing** (run relevant test subset)
- [ ] **No obvious regressions** introduced
- [ ] **Code style consistent** with project standards
- [ ] **Documentation updated** if needed

### Cost Efficiency Check
- [ ] **Staying within phase budgets** (planning/implementation/review)
- [ ] **Using appropriate models** for task complexity
- [ ] **Pattern reuse** maximized where possible
- [ ] **Batch opportunities** identified for similar upcoming tasks

## Resume Workflow Templates

### Daily Resume (5-10 minutes)
```bash
# Quick daily resume script
#!/bin/bash
echo "=== Daily Project Resume ==="
echo "Date: $(date)"
echo "Branch: $(git branch --show-current)"
echo "Last commit: $(git log -1 --pretty=format:'%h %s')"
echo "Uncommitted changes: $(git status --porcelain | wc -l) files"
echo ""
echo "=== Current Spec Tasks ==="
find .agent-os/specs -name "tasks.md" -exec tail -20 {} \; 2>/dev/null | grep -E "\[ \]|\[x\]" | tail -10
echo ""
echo "=== Cost Summary ==="
tail -5 .khamel83/cost-tracking.json 2>/dev/null || echo "No cost tracking data"
```

### Weekly Resume (15-20 minutes)
- [ ] **Review week's progress** against goals
- [ ] **Analyze cost optimization** effectiveness
- [ ] **Update pattern library** with new discoveries
- [ ] **Plan next week's priorities** based on Agent OS roadmap
- [ ] **Stakeholder communication** if needed

### Post-Break Resume (After >3 days away)
- [ ] **Full context reconstruction** (30+ minutes)
- [ ] **Environment update** (dependencies, tools)
- [ ] **Stakeholder check-in** for any changes/priorities
- [ ] **Code review** of any changes made by others
- [ ] **Goal realignment** with current project priorities

## Troubleshooting Common Resume Issues

### Can't Find Current Task
1. Check `.agent-os/specs/` for recent folders
2. Look for `tasks.md` files: `find . -name "tasks.md" -type f`
3. Review git history for clues: `git log --grep="task\|implement" --oneline -10`
4. Check browser history for Agent OS or project documentation

### Development Environment Issues
1. **Dependencies out of date**: Run update commands for your package manager
2. **Database issues**: Check if database service is running
3. **Environment variables**: Verify .env files are loaded
4. **Port conflicts**: Check if other services are using same ports

### Lost Context/Motivation
1. **Review project mission**: Read `.agent-os/product/mission-lite.md`
2. **Check progress made**: Review git history and completed tasks
3. **Celebrate wins**: Review cost savings and features completed
4. **Reconnect with purpose**: Why is this project important?

## Completion Checklist

### Environment Ready ✅
- [ ] Development environment verified and working
- [ ] Current task identified and understood
- [ ] Cost optimization tools configured
- [ ] Next steps clearly defined

### Context Restored ✅
- [ ] Recent progress reviewed and understood
- [ ] Blocking issues identified (if any)
- [ ] Pattern opportunities assessed
- [ ] Team communication up to date (if needed)

### Ready to Code ✅
- [ ] Clear task to work on next
- [ ] Cost optimization strategy planned
- [ ] Success criteria defined
- [ ] Stopping point identified for session

---

**Session Started**: [DATE] [TIME]
**Next Task**: [TASK_DESCRIPTION]
**Cost Target**: $[AMOUNT]
**Session Goal**: [SPECIFIC_DELIVERABLE]

---

*This workflow is part of the Khamel83 Agent OS enhancement suite. Adapt the process based on your project complexity and personal productivity preferences.*